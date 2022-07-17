"""
Get tip info from the FortranTip readme
"""
import base64
import datetime
import os
import re
from dataclasses import asdict, dataclass
from collections import Counter
from pathlib import Path
from typing import NamedTuple

import requests
import yaml
from dateutil.parser import parse
from dotenv import load_dotenv
from rich.progress import track


HERE = Path(__file__).parent

re_readme_line = re.compile(
    r"\[(?P<title>.+)\]\(https://twitter.com/fortrantip/status/(?P<tweet_id>[0-9]+)\)"
    r" (?P<time>[0-9]{1,2}:[0-9]{2} [A|P]M)"
    r" \u00B7 (?P<date>[A-Z][a-z]{2} [0-9]{1,2}, [0-9]{4})"
    r"(?P<file_links> *\[.*\]\(.+\))*"
    r"\s*(<br>)?$"
)

re_link = re.compile(r"\[(?P<text>.*?)\]\((?P<target>.+?)\)")


@dataclass(frozen=True)
class Link:
    text: str
    target: str

    def as_md(self) -> str:
        return f"[{self.text}]({self.target})"

    def check(self):
        raise NotImplementedError


class TipInfo(NamedTuple):
    """FortranTip tip info from readme line."""
    title: str
    tweet_id: str
    datetime: datetime.datetime
    # TODO: file links


# Get the FT readme and parse it

r = requests.get(
    f"https://api.github.com/repos/Beliavsky/FortranTip/contents/README.md"
)
r.raise_for_status()
data = r.json()
file_content = data["content"]
file_content_encoding = data.get("encoding")
if file_content_encoding == "base64":
    file_content = base64.b64decode(file_content).decode()
readme = file_content

# Workaround for non-Twitter link
readme = readme.replace(
    "[When is the -ffast-math option safe?](https://fortran-lang.discourse.group/t/can-one-design-coding-rules-to-follow-so-that-ffast-math-is-safe/2762) 7:14 AM · Apr 29, 2022<br>",
    "[When is the -ffast-math option safe?](https://twitter.com/fortrantip/status/1519998641133563905) 7:14 AM · Apr 29, 2022<br>"
)

lines = readme.splitlines()
ihead = 3
assert lines[ihead].startswith("### Index")

mentioned_files = []

tips = []  # this is what we will save to the YAML file

for line in lines[ihead+1:]:
    if not line.strip():
        continue

    m = re_readme_line.match(line)
    if m is None:
        print(f"doesn't match the format:\n  {line}")

    else:
        d = m.groupdict()
        title = d["title"]
        tweet_id = d["tweet_id"]
        dt = parse(f"{d['time']} {d['date']}")
        s_file_links = d["file_links"]
        if s_file_links is not None:
            file_links = [Link(a, b) for a, b in re_link.findall(s_file_links)]
        else:
            file_links = []

        mentioned_files.extend(l.target for l in file_links if not l.target.startswith("http"))

        # Validate finding of file links
        if not file_links:
              s_ = line[m.span(2)[1]:]
              assert s_.count(".f90") == s_.count(".txt") == 0, line

        # Save tip data
        tips.append(
            {
                "title": title,
                "tweet_id": tweet_id,
                "datetime": dt,
                "file_links": [asdict(l) for l in file_links],
            }
        )


# Get FT list by topic and parse it

r = requests.get(
    f"https://api.github.com/repos/Beliavsky/FortranTip/contents/topics.md"
)
r.raise_for_status()
data = r.json()
file_content = data["content"]
file_content_encoding = data.get("encoding")
if file_content_encoding == "base64":
    file_content = base64.b64decode(file_content).decode()
topics_md = file_content

# Workaround for non-Twitter link
topics_md = topics_md.replace(
    "[When is the -ffast-math option safe?](https://fortran-lang.discourse.group/t/can-one-design-coding-rules-to-follow-so-that-ffast-math-is-safe/2762) 7:14 AM · Apr 29, 2022<br>",
    "[When is the -ffast-math option safe?](https://twitter.com/fortrantip/status/1519998641133563905) 7:14 AM · Apr 29, 2022<br>"
)

lines = topics_md.splitlines()
istart = 3
assert lines[istart].startswith("### ")

# Topic ID overrides
topic_id_overrides = {"interoperability-with-c-and-c++": "interoperability-with-c"}

topic_titles = {}
topic_id = None
tips_w_topic = []
for line in lines[istart:]:
    if not line.strip():
        continue

    if line.startswith("###"):
        # New topic block
        topic_title = line[4:].strip()
        topic_id = topic_title.lower().replace(" ", "-")
        topic_id = topic_id_overrides.get(topic_id, topic_id)
        # TODO: check topic ID is alphanum + hyphen + ...
        topic_titles[topic_id] = topic_title
    else:
        # Tip
        m = re_readme_line.match(line)
        if m is None:
            print(f"doesn't match the format:\n  {line}")

        else:
            d = m.groupdict()

        tips_w_topic.append(
            {
                "title": d["title"],
                "tweet_id": d["tweet_id"],
                "datetime": parse(f"{d['time']} {d['date']}"),
                "ft_topic_id": topic_id,
            }
        )

# Each one from the readme should be here
# and be in one and only one topic

tips_ti = {TipInfo(d["title"], d["tweet_id"], d["datetime"]) for d in tips}
tips_w_topic_ti = {TipInfo(d["title"], d["tweet_id"], d["datetime"]) for d in tips_w_topic}
assert len(tips) == len(tips_ti)
assert len(tips_w_topic) == len(tips_w_topic_ti)

d = tips_ti - tips_w_topic_ti
if d:
    print("Mentioned in readme but not topic list:", d)

d = tips_w_topic_ti - tips_ti
if d:
    print("Mentioned in topic list but not readme:", d)

tips_w_topic_by_title = {tip["title"]: tip for tip in tips_w_topic}

for d in tips:
    try:
        id_ = tips_w_topic_by_title[d["title"]]["ft_topic_id"]
    except KeyError:
        id_ = None
    d.update(ft_topic_id=id_)


# Get list of files in the FT GH repo and compare to the readme

r = requests.get(
    "https://api.github.com/repos/Beliavsky/FortranTip/git/trees/HEAD?recursive=1"
)
r.raise_for_status()
ghtree = r.json()["tree"]

gh_fns = {d["path"] for d in ghtree} - {"README.md", "LICENSE", "topics.md"}

file_mention_allowed_dups = {"./lbound_assumed_shape.f90",}

mentioned_file_counts = Counter(mentioned_files)

if len(mentioned_file_counts) != len(mentioned_files):
    g1 = {
        k: n for k, n in mentioned_file_counts.items()
        if n > 1 and k not in file_mention_allowed_dups
    }
    if g1:
        raise Exception(f"files should be unique to tip but we have {g1}")

fns = {fn.lstrip("./") for fn in mentioned_files}

gh_fns_only = gh_fns - fns
if gh_fns_only:
    print("Not mentioned in the readme:")
    for fn in sorted(gh_fns_only):
        print(f"- `{fn}`")
    print()
fns_only = fns - gh_fns
if fns_only:
    print("Mentioned in the readme but not present in the repo:")
    for fn in sorted(fns_only):
        print(f"- `{fn}`")
    print()


# Get Tweet info and embed HTML

use_prev_tweets = True  # from existing data0
if use_prev_tweets:
    with open("./data0.yaml") as f:
        tips0 = yaml.load(f, yaml.Loader)["tips"]
        tips0d = {d["tweet_id"]: d for d in tips0}

if not os.environ.get("GITHUB_ACTIONS"):
    p = HERE / ".env"
    assert p.is_file(), ".env needed"
    load_dotenv(p)

BT = os.environ.get("TWITTER_BT")

for d in track(tips, description="Getting data from Twitter"):
    tweet_id = d["tweet_id"]

    if tweet_id in tips0d and use_prev_tweets:
        # Use existing data
        d0 = tips0d[tweet_id]
        text = d0["tweet_text"]
        created_at = d0["tweet_created_at"]
        embed = d0["tweet_embed"]
    else:
        # Get Tweet text
        r = requests.get(
            f"https://api.twitter.com/2/tweets/{tweet_id}?tweet.fields=text,created_at",
            headers={"Authorization": f"Bearer {BT}"}
        )
        r.raise_for_status()
        data = r.json()["data"]
        text = data["text"]  # by default just has `text` and `id`
        created_at = data["created_at"]

        # Get embed HTML
        r = requests.get(
            "https://publish.twitter.com/oembed?"
            f"url=https://twitter.com/fortrantip/status/{tweet_id}"
        )
        r.raise_for_status()
        embed = r.json()["html"].strip()

    d["tweet_text"] = text
    d["tweet_created_at"] = created_at
    d["tweet_embed"] = embed

    del text, created_at, embed

# Save data

with open("data0.yaml", "w") as f:
    f.write(f"# !! This file is autogenerated by {Path(__file__).name} !!\n")
    f.write(yaml.dump({"tips": tips, "ft_topic_titles": topic_titles}))
