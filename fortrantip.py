"""
Use the data file and Fortran source files
to construct MyST Markdown pages for Sphinx.
"""
from __future__ import annotations

# import multiprocessing
import os
import subprocess
from sys import stderr
import urllib.parse
from functools import lru_cache
from pathlib import Path
from typing import Optional

import joblib
import yaml
# from rich.progress import Progress


HERE = Path(__file__).parent.absolute()

DOC = HERE / "docs"
DST = DOC / "tips"
SRC = HERE / "src"

GH_LINK_FMT = (
    '<a href="https://github.com/zmoon/FortranTipBrowser/blob/main/src/{fn}" '
    'target="_blank" title="See this source on GitHub">'
    '<i class="fab fa-github"></i></a>'
)
GH0_LINK_FMT = (
    '<a href="https://github.com/Beliavsky/FortranTip/blob/main/{fn}" '
    'target="_blank" title="See the original source on Beliavsky/FortranTip GitHub">'
    '<i class="fab fa-github"></i><sub>0</sub></a>'
)
GB_URL_FMT = (
    "https://godbolt.org/#g:!((g:!((g:!((g:!((h:codeEditor,i:(filename:'1',"
    "fontScale:14,fontUsePx:'0',j:1,lang:fortran,selection:(endColumn:1,endLineNumber:{nl},"
    "positionColumn:1,positionLineNumber:{nl},selectionStartColumn:1,selectionStartLineNumber:{nl},"
    "startColumn:1,startLineNumber:{nl}),source:'{source:s}'),l:'5',n:'0',"
    "o:'Fortran+source+%231',t:'0')),""k:50,l:'4',n:'0',o:'',s:0,t:'0'),"
    "(g:!((h:compiler,i:(compiler:gfortran112,filters:(b:'0',binary:'1',commentOnly:'0',"
    "demangle:'0',directives:'0',execute:'0',intel:'0',libraryCode:'0',trim:'1'),"
    "flagsViewOpen:'1',fontScale:14,fontUsePx:'0',j:1,lang:fortran,libs:!(),options:'',"
    "selection:(endColumn:1,endLineNumber:1,positionColumn:1,positionLineNumber:1,"
    "selectionStartColumn:1,selectionStartLineNumber:1,startColumn:1,startLineNumber:1),"
    "source:1,tree:'1'),l:'5',n:'0',"
    "o:'x86-64+gfortran+11.2+(Fortran,+Editor+%231,+Compiler+%231)',t:'0')),"
    "k:50,l:'4',n:'0',o:'',s:0,t:'0')),l:'2',m:62.300683371298405,n:'0',o:'',t:'0'),"
    "(g:!((h:output,i:(compiler:1,editor:1,fontScale:14,fontUsePx:'0',tree:'1',wrap:'1'),"
    "l:'5',n:'0',o:'Output+of+x86-64+gfortran+11.2+(Compiler+%231)',t:'0')),"
    "header:(),l:'4',m:37.699316628701595,n:'0',o:'',s:0,t:'0')),l:'3',n:'0',o:'',t:'0')),version:4"
)
GB_LINK_FMT = (
    '<a href="{url}" target="_blank" title="Open in Godbolt Compiler Explorer">'
    '<img src="https://raw.githubusercontent.com/compiler-explorer/compiler-explorer/main/views/resources/site-logo.svg"'
    ' alt="Godbolt Compiler Explorer logo" width="55.11" height="16.7" class="align-text-bottom" />'
    "</a>"
)


def fortran_to_myst(fn: str, *, fn0: Optional[str] = None) -> str:
    gh = GH_LINK_FMT.format(fn=fn)

    with open(SRC / fn) as f:
        s = f.read()
    nl = len(s.splitlines())
    source = urllib.parse.quote_plus(s, safe=",:!*()/'")
    source = source.replace("!", "!!")  # this is how GodBolt escapes `!`
    source = source.replace("'", "!'")  # " "                         `'`
    gb_url = GB_URL_FMT.format(nl=nl, source=source)
    # TODO: use GB short links (only create new if needed)

    gb = GB_LINK_FMT.format(url=gb_url)

    if fn0 is not None:
        gh0 = GH0_LINK_FMT.format(fn=fn0)
        caption = f"{fn} | {gh} | {gh0} | {gb}"
    else:
        caption = f"{fn} | {gh} | {gb}"

    return f"""\
```{{literalinclude}} ../../src/{fn}
:language: fortran
:caption: {caption}
```
"""


def get_gfortran_version_info() -> str:
    cp = subprocess.run(["gfortran", "--version"], check=True, capture_output=True)
    return cp.stdout.decode().splitlines()[0]


GFORTRAN_VERSION_INFO = get_gfortran_version_info()


def _run_fortran_inputs(fp: str, inputs: list[str]) -> str:
    "Give inputs and capture outputs, then kill and return."
    # p = subprocess.Popen(
    #     [fp],
    #     shell=False,
    #     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # outs = []
    # for input_ in inputs:
    #     print(input_)
    #     # oe, _ = p.communicate(input_.encode(), timeout=1)
    #     # p.kill()
    #     p.stdin.write((input_ + "\n").encode())
    #     print(p.stdout.read())
    #     oe = p.stdout.read()
    #     outs.append(oe.decode())
    #     print(input_, oe)

    # print(p)

    # p.kill()

    cp = subprocess.run(
        [fp],
        input="\n".join(inputs),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    res = cp.stdout
    
    return res


def run_fortran(fn: str, *, inputs: list[Optional[str]] = None) -> str:
    import tempfile

    xname = "a.x"

    cwd = os.getcwd()
    td = tempfile.mkdtemp(prefix="fortrantip")
    os.chdir(td)

    # Compile
    try:
        subprocess.run(
            ["gfortran", (SRC / fn).as_posix(), "-o", xname],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        import textwrap

        w = lambda s: textwrap.indent(s, "... ")

        print("compilation error!")
        print(f"return code: {e.returncode}")
        print(f"stdout:\n{w(e.stdout.decode())}")
        print(f"stderr:\n{w(e.stderr.decode())}")
        raise

    # Run
    fp = f"{td}/{xname}"
    if inputs is None:
        cp = subprocess.run([fp], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = cp.stdout
    else:
        out = _run_fortran_inputs(fp, inputs)
    
    os.chdir(cwd)

    return out


def write_tip_md(i: int, d: dict) -> None:
    fn = f"{i:03d}.md"

    # Required keys (but all except title can be null (parsed to None))
    title = d["title"]
    # tweet_url = d["url"]
    intro = d["intro"]
    fortran = d["file"]
    inputs = d.get("inputs")
    ft_topic_id = d["ft_topic_id"]

    # Optional keys
    concl = d.get("concl")
    tweet_html = d.get("embed")

    # File in original FortranTip repo
    fortran0 = d.get("file0")
    if fortran0 == "same":
        fortran0 = fortran
    elif fortran0 == "missing":
        fortran0 = None
    assert fortran0 is None or fortran0.endswith(".f90")

    s = (
        f"# {i:03d}. {title}\n\n"
        f"<span style='font-size: small;' class='text-muted'>topic: {{ref}}`{ft_topic_id}`</span>\n\n"
    )

    # Intro MD
    if intro is not None:
        s += intro + "\n"

    # Fortran
    if fortran is not None:
        # Source
        s += fortran_to_myst(fn=fortran, fn0=fortran0)

        # Input
        if inputs is not None:
            s_inputs = "\n".join(inputs)
            s += "\n" f"""\
```{{code-block}} text
:caption: Input

{s_inputs}
```
"""
        # Output
        s += "\n" f"""\
```{{code-block}} text
:caption: Output[^gfortran-version]

{run_fortran(fortran, inputs=inputs)}
```

[^gfortran-version]: Compiled using `{GFORTRAN_VERSION_INFO}` with no flags
"""

    # TODO: Conclu MD
    if concl is not None:
        s += f"\n{concl}"

    # TODO: List of refs for further info

    # Tweet embed
    if tweet_html is not None:
        s += "\n---\n\n" f"{tweet_html}"  # TODO: wrap with ```{raw} html

    # Write tip MD
    with open(DST / fn, "w") as f:
        f.write(s)

    return None


def write_tips_index(tips: list[dict], ft_topics: dict[str, str]) -> None:
    from collections import defaultdict

    ntips = len(tips)
    nums = "\n".join(f"{i:03d}" for i in range(1, ntips+1))

    # Topics
    tips_by_topic = defaultdict(list)
    for i, d in enumerate(tips, start=1):
        tips_by_topic[d["ft_topic_id"]].append((i, d["title"]))

    lines = []
    for id_, title in ft_topics.items():
        lines.extend([f"({id_})=", f"### {title}", ""])
        lines.extend([f"- [{i:03d}.](./{i:03d}.md) {title}" for i, title in tips_by_topic[id_]])
        lines.extend([""])

    topics = "\n".join(lines)

    s = f"""\
---
sd_hide_title: true
...

# Tips index

```{{toctree}}
:hidden:

{nums}
```

## By topic

*According to [the FortranTip topics page](https://github.com/Beliavsky/FortranTip/blob/main/topics.md).*

{topics}
"""

    with open(DST / "index.md", "w") as f:
        f.write(s)


def write_random_tip_button_snippet(ntips: int) -> None:
    btn_snippet = f"""\
```{{raw}} html
<script>
function randoTip() {{
i = Math.floor(1 + Math.random() * {ntips});
tip = String(i).padStart(3, '0');
tip_page = `tips/${{tip}}.html`;
// alert(tip_page);
window.open(tip_page, "_self")
}}

</script>

<button class="sd-sphinx-override sd-btn sd-btn-primary sd-shadow-sm", onclick="randoTip()">
Go to random tip
</button>
```
"""

    with open(DOC / "_random-tip-btn_snippet.myst", "w") as f:
        f.write(btn_snippet)


def main(tip: str) -> int:
    with open("data.yaml", "r") as f:
        data = yaml.load(f, Loader=yaml.Loader)

    with open("data0.yaml", "r") as f:
        data0 = yaml.load(f, Loader=yaml.Loader)

    ft_topic_titles = data0["ft_topic_titles"]

    # Add FT topic ID to tip dicts
    tips0_by_id = {d["tweet_id"]: d for d in data0["tips"]}
    for d in data["tips"]:
        tweet_id = d["url"][len("https://twitter.com/fortrantip/status/"):]
        d["ft_topic_id"] = tips0_by_id[tweet_id]["ft_topic_id"]

    ntips = len(data["tips"])

    # Generate tip pages
    # TODO: cache last Fortran run, MD generation time, yaml DATA, so can regen only things that need it
    DST.mkdir(exist_ok=True)
    if tip in {"a", "all"}:
        # TODO: figure out how to fix...?:
        # RuntimeError:
        #   An attempt has been made to start a new process before the
        #   current process has finished its bootstrapping phase.
        # with Progress() as progress:
        #     task_id = progress.add_task("Generating MD pages...", total=ntips)
        #     with multiprocessing.Pool(3) as pool:
        #         for _ in pool.map(write_tip_md, enumerate(data["tips"][:3], start=1)):
        #             progress.advance(task_id)

        joblib.Parallel(n_jobs=-1, verbose=5)(
            joblib.delayed(write_tip_md)(i, d)
            for i, d in enumerate(data["tips"], start=1)
        )
        write_tips_index(data["tips"], ft_topics=ft_topic_titles)
        write_random_tip_button_snippet(ntips)
    elif tip in {"i", "index"}:
        write_tips_index(data["tips"], ft_topics=ft_topic_titles)
        write_random_tip_button_snippet(ntips)
    else:  # single tip
        try:
            i = int(tip)
        except ValueError:
            print(f"invalid tip input {tip!r} (not int-able)")
            return 1

        if not 1 <= i <= ntips:
            print(f"invalid tip input {tip!r} (not in [1, {ntips}])")
            return 1

        d = data["tips"][i - 1]
        write_tip_md(i, d)

    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "tip",
        help=(
            "tip (e.g. '42' or '042') to generate MD for. 'a'/'all' to generate all. "
            "'i'/'index' to generate the tips index"
        ),
    )

    args = parser.parse_args()

    raise SystemExit(main(args.tip))
