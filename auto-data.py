"""
Get tip info from the FortranTip readme
"""
import datetime
import re
from dataclasses import dataclass

import requests
#import yaml
from dateutil.parser import parse


re_readme_line = re.compile(
    r"\[(?P<title>.+)\]\(https://twitter.com/fortrantip/status/(?P<tweet_id>[0-9]+)\)"
    r" (?P<time>[0-9]{1,2}:[0-9]{2} [A|P]M)"
    r" \u00B7 (?P<date>[A-Z][a-z]{2} [0-9]{1,2}, [0-9]{4})"
    r"(?P<file_links> *\[.*\]\(.+\))*"
    r"(<br>)?$"
)

re_link = re.compile(r"\[(?P<text>.*)\]\((?P<target>.+)\)")


@dataclass(frozen=True)
class link:
    text: str
    target: str

    def as_md(self) -> str:
        return f"[{self.text}]({self.target})"

    def check(self):
        raise NotImplementedError


r = requests.get(
    "https://raw.githubusercontent.com/Beliavsky/FortranTip/main/README.md"
)
r.raise_for_status()
readme = r.text

lines = readme.splitlines()
ihead = 3
assert lines[ihead].startswith("### Index")

mentioned_files = []

for line in lines[ihead+1:]:
    if not line.strip():
        continue

    m = re_readme_line.match(line)
    if m is None:
        print(f"doesn't match the format:\n  {line}")

    else:
        d = m.groupdict()
        title = d["title"]
        dt = parse(f"{d['time']} {d['date']}")
        s_file_links = d["file_links"]
        if s_file_links is not None:
            file_links = [link(a, b) for a, b in re_link.findall(s_file_links)]
        else:
            file_links = []

        mentioned_files.extend(l.target for l in file_links if not l.target.startswith("http"))

        # Validate finding of file links
        if not file_links:
              s_ = line[m.span(2)[1]:]
              assert s_.count(".f90") == s_.count(".txt") == 0, line


r = requests.get(
    "https://api.github.com/repos/Beliavsky/FortranTip/git/trees/HEAD?recursive=1"
)
r.raise_for_status()
ghtree = r.json()["tree"]

gh_fns = {d["path"] for d in ghtree} - {"README.md",}

assert len(set(mentioned_files)) == len(mentioned_files), "files should be unique to tip"

fns = {fn.lstrip("./") for fn in mentioned_files}

print("Not mentioned in the readme:")
for fn in sorted(gh_fns - fns):
    print(f"- `{fn}`")
print()
print("Mentioned in the readme but not present in the repo:")
for fn in sorted(fns - gh_fns):
    print(f"- `{fn}`")

