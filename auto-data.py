"""
Get tip info from the FortranTip readme
"""
import base64
import os
import re
from dataclasses import asdict, dataclass
from collections import Counter
from pathlib import Path

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
    r"(<br>)?$"
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


# Get list of files in the FT GH repo and compare to the readme

r = requests.get(
    "https://api.github.com/repos/Beliavsky/FortranTip/git/trees/HEAD?recursive=1"
)
r.raise_for_status()
ghtree = r.json()["tree"]

gh_fns = {d["path"] for d in ghtree} - {"README.md",}

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

if not os.environ.get("GITHUB_ACTIONS"):
    p = HERE / ".env"
    assert p.is_file(), ".env needed"
    load_dotenv(p)

BT = os.environ.get("TWITTER_BT")

for d in track(tips, description="Getting data from Twitter"):
    tweet_id = d["tweet_id"]

    # Get Tweet text
    r = requests.get(
        f"https://api.twitter.com/2/tweets/{tweet_id}?tweet.fields=text,created_at",
        headers={"Authorization": f"Bearer {BT}"}
    )
    r.raise_for_status()
    data = r.json()["data"]
    d["tweet_text"] = data["text"]  # by default just has `text` and `id`
    d["tweet_created_at"] = data["created_at"]

    # Get embed HTML
    r = requests.get(
        "https://publish.twitter.com/oembed?"
        f"url=https://twitter.com/fortrantip/status/{tweet_id}"
    )
    r.raise_for_status()
    d["tweet_embed"] = r.json()["html"].strip()


# Save data

with open("data0.yaml", "w") as f:
    f.write(f"# !! This file is autogenerated by {Path(__file__).name} !!\n")
    f.write(yaml.dump(tips))
