"""
Use the data file and Fortran source files
to construct MyST Markdown pages for Sphinx.
"""
import subprocess
from pathlib import Path

import yaml

HERE = Path(__file__).parent

DST = HERE / "docs" / "tips"
SRC = HERE / "src"


with open("data.yaml", "r") as f:
    data = yaml.load(f, Loader=yaml.Loader)


def fortran_to_myst(fn: str) -> str:
    return f"""\
```{{literalinclude}} ../../src/{fn}
:language: fortran
:linenos:
:caption: {fn} <a href="https://github.com/zmoon/FortranTip-site/blob/main/src/{fn}" target="_blank"><i class="fab fa-github"></i></a>
```
"""


def run_fortran(fn: str):
    # Compile
    cp1 = subprocess.run(["gfortran", (SRC / fn).as_posix()], check=True, capture_output=True)

    # Run
    cp2 = subprocess.run(["./a.out"], capture_output=True)

    return {"gfortran": cp2.stdout.decode()}


DST.mkdir(exist_ok=True)


# Generate tip pages

# TODO: cache last Fortran run, MD generation time, yaml DATA, so can regen only things that need it

for i, d in enumerate(data["tips"], start=1):
    fn = f"{i:03d}.md"

    # Required keys
    title = d["title"]
    # tweet_url = d["url"]
    intro = d["intro"]
    fortran = d["file"]

    # Optional keys
    concl = d.get("concl")
    tweet_html = d.get("embed")

    s = f"# {i:03d}. {title}\n\n"

#     s += f"""\
# Tweet: <{tweet_url}>

# """

    # Intro MD
    if intro is not None:
        s += intro + "\n"

    # Fortran source file and output
    if fortran is not None:
        s += fortran_to_myst(fortran)

        s += "\n" f"""\
```{{code-block}} text
:caption: Output

{run_fortran(fortran)["gfortran"]}
```
"""
    # TODO: footnote with `gfortran --version` first line?

    # TODO: Conclu MD
    if concl is not None:
        s += f"\n{concl}"

    # TODO: List of refs for futher info

    # Tweet embed
    if tweet_html is not None:
        s += "\n---\n\n" f"{tweet_html}"

    # Write tip MD
    with open(DST / fn, "w") as f:
        f.write(s)


# Generate tips index file

nums = "\n".join(f"{n:03d}" for n in range(1, i+1))

s = f"""\
---
sd_hide_title: true
...

# Tips index

```{{toctree}}
:hidden:

{nums}
```
"""

with open(DST / "index.md", "w") as f:
    f.write(s)
