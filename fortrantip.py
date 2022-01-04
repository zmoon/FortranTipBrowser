"""
Use the data file and Fortran source files
to construct MyST Markdown pages for Sphinx.
"""
import subprocess
from pathlib import Path

import yaml

HERE = Path(__file__).parent

DST = HERE / "docs" / "_gen"
SRC = HERE / "src"


with open("data.yaml", "r") as f:
    data = yaml.load(f, Loader=yaml.Loader)


def fortran_to_myst(fn: str) -> str:
    comment_lines = []
    code_lines = []
    out_blocks = []
    with open(SRC / fn, "r") as f:
        for line in f:
            in_code = not line.startswith("!")

            if in_code:
                if comment_lines:
                    out_blocks.append("```{margin}\n" + "\n".join(comment_lines) + "\n```")
                    comment_lines = []

                # TODO: strip eol comments to comment block
                try:
                    code, eol_comment = line.split("!")
                except ValueError:
                    code = line.rstrip()
                    code_lines.append(code)
                else:
                    code_lines.append(code)
                    out_blocks.append("```fortran\n" + "\n".join(code_lines) + "\n```")
                    code_lines = []
                    out_blocks.append("```{margin}\n" + eol_comment.strip() + "\n```")
                

            else:
                if code_lines:
                    out_blocks.append("```fortran\n" + "\n".join(code_lines) + "\n```")
                    code_lines = []

                comment_lines.append(line.lstrip("!").strip())

    # TODO: DRY
    if comment_lines:
        out_blocks.append("```{margin}\n" + "\n".join(comment_lines) + "\n```")
        comment_lines = []

    if code_lines:
        out_blocks.append("```fortran\n" + "\n".join(code_lines) + "\n```")
        code_lines = []

    return "\n\n".join(out_blocks)


def run_fortran(fn: str):
    # Compile
    cp1 = subprocess.run(["gfortran", (SRC / fn).as_posix()], check=True, capture_output=True)

    # Run
    cp2 = subprocess.run(["./a.out"], capture_output=True)

    return {"gfortran": cp2.stdout.decode()}



DST.mkdir(exist_ok=True)

for i, d in enumerate(data["tips"], start=1):
    fn = f"{i:03d}.md"

    title = d["title"]
    tweet_url = d["url"]
    intro = d["intro"]
    fortran = d["file"]

    s = f"# {title}\n\n"

    if intro is not None:
        s += intro

    s += f"""\
Tweet: {tweet_url}

"""

    if fortran is not None:
        s += fortran_to_myst(fortran)

        s += "\n\n" f"""\
Ouput:
```
{run_fortran(fortran)["gfortran"]}
```
"""

    with open(DST / fn, "w") as f:
        f.write(s)
