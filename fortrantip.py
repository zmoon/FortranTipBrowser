"""
Use the data file and Fortran source files
to construct MyST Markdown pages for Sphinx.
"""
# import multiprocessing
import os
import subprocess
import urllib.parse
from pathlib import Path
from typing import Optional

import joblib
import yaml
# from rich.progress import Progress

HERE = Path(__file__).parent.absolute()

DOC = HERE / "docs"
DST = DOC / "tips"
SRC = HERE / "src"


with open("data.yaml", "r") as f:
    data = yaml.load(f, Loader=yaml.Loader)

ntips = len(data["tips"])


gb_url_fmt = "https://godbolt.org/#g:!((g:!((g:!((g:!((h:codeEditor,i:(filename:'1',fontScale:14,fontUsePx:'0',j:1,lang:fortran,selection:(endColumn:1,endLineNumber:{nl},positionColumn:1,positionLineNumber:{nl},selectionStartColumn:1,selectionStartLineNumber:{nl},startColumn:1,startLineNumber:{nl}),source:'{source:s}'),l:'5',n:'0',o:'Fortran+source+%231',t:'0')),k:50,l:'4',n:'0',o:'',s:0,t:'0'),(g:!((h:compiler,i:(compiler:gfortran112,filters:(b:'0',binary:'1',commentOnly:'0',demangle:'0',directives:'0',execute:'0',intel:'0',libraryCode:'0',trim:'1'),flagsViewOpen:'1',fontScale:14,fontUsePx:'0',j:1,lang:fortran,libs:!(),options:'',selection:(endColumn:1,endLineNumber:1,positionColumn:1,positionLineNumber:1,selectionStartColumn:1,selectionStartLineNumber:1,startColumn:1,startLineNumber:1),source:1,tree:'1'),l:'5',n:'0',o:'x86-64+gfortran+11.2+(Fortran,+Editor+%231,+Compiler+%231)',t:'0')),k:50,l:'4',n:'0',o:'',s:0,t:'0')),l:'2',m:62.300683371298405,n:'0',o:'',t:'0'),(g:!((h:output,i:(compiler:1,editor:1,fontScale:14,fontUsePx:'0',tree:'1',wrap:'1'),l:'5',n:'0',o:'Output+of+x86-64+gfortran+11.2+(Compiler+%231)',t:'0')),header:(),l:'4',m:37.699316628701595,n:'0',o:'',s:0,t:'0')),l:'3',n:'0',o:'',t:'0')),version:4"
gh_link_fmt = (
    '<a href="https://github.com/zmoon/FortranTipBrowser/blob/main/src/{fn}" '
    'target="_blank" title="See this source on GitHub">'
    '<i class="fab fa-github"></i></a>'
)
gh0_link_fmt = (
    '<a href="https://github.com/Beliavsky/FortranTip/blob/main/{fn}" '
    'target="_blank" title="See the original source on Beliavsky/FortranTip GitHub">'
    '<i class="fab fa-github"></i><sub>0</sub></a>'
)
gb_link_fmt = (
    '<a href="{url}" target="_blank" title="Open in Godbolt Compiler Explorer">'
    '<img src="https://raw.githubusercontent.com/compiler-explorer/compiler-explorer/main/views/resources/site-logo.svg" alt="Godbolt Compiler Explorer logo" width="55.11" height="16.7" class="align-text-bottom" />'
    "</a>"
)

def fortran_to_myst(fn: str, *, fn0: Optional[str] = None) -> str:
    gh = gh_link_fmt.format(fn=fn)

    with open(SRC / fn) as f:
        s = f.read()
    nl = len(s.splitlines())
    source = urllib.parse.quote_plus(s, safe=",:!*()/'")
    source = source.replace("!", "!!")  # this is how GodBolt escapes `!`
    source = source.replace("'", "!'")  # " "                         `'`
    gb_url = gb_url_fmt.format(nl=nl, source=source)
    # TODO: use GB short links (only create new if needed)

    gb = gb_link_fmt.format(url=gb_url)

    if fn0 is not None:
        gh0 = gh0_link_fmt.format(fn=fn0)
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


def run_fortran(fn: str):
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
    try:
        cp = subprocess.run([f"{td}/{xname}"], capture_output=True)
    except:
        print(td, os.listdir(td))
        raise
    finally:
        os.chdir(cwd)

    return {"gfortran": cp.stdout.decode()}


DST.mkdir(exist_ok=True)

gfortran_version_info = get_gfortran_version_info()


# Generate tip pages

# TODO: cache last Fortran run, MD generation time, yaml DATA, so can regen only things that need it

def write_tip_md(i, d):

    fn = f"{i:03d}.md"

    # Required keys (but all except title can be null (parsed to None))
    title = d["title"]
    # tweet_url = d["url"]
    intro = d["intro"]
    fortran = d["file"]

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

    s = f"# {i:03d}. {title}\n\n"

#     s += f"""\
# Tweet: <{tweet_url}>

# """

    # Intro MD
    if intro is not None:
        s += intro + "\n"

    # Fortran source file and output
    if fortran is not None:
        s += fortran_to_myst(fn=fortran, fn0=fortran0)

        s += "\n" f"""\
```{{code-block}} text
:caption: Output[^gfortran-version]

{run_fortran(fortran)["gfortran"]}
```

[^gfortran-version]: Compiled using `{gfortran_version_info}` with no flags
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


# Generate tips index file

nums = "\n".join(f"{i:03d}" for i in range(1, ntips+1))

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


# Generate random tip button snippet

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