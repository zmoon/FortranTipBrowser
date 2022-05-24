"""
Use the data0.yaml data to draft tips and append to data.yaml
"""
from pathlib import Path
from textwrap import indent

import yaml


def findfirst(seq, pred):
    "Find the first element of `seq` meeting predicate `pred`."
    return next(filter(pred, seq), None)


p_data0 = Path("./data0.yaml")
p_data = Path("./data.yaml")
assert p_data0.is_file() and p_data.is_file()

with open(p_data0) as f:
    tips0 = yaml.load(f, yaml.Loader)["tips"][::-1]

with open(p_data) as f:
    tips = yaml.load(f, yaml.Loader)["tips"]

# Find last ID in data
last_id = tips[-1]["url"][-19:]
istart = [d["tweet_id"] for d in tips0].index(last_id) + 1

fmt = """\
  # TODO
  - title: {title}
    intro: |
{indented_intro}
    file: ~
    file0: {file0}
    url: {url}
    embed: '{embed}'
""".rstrip()

lines = []

last_date = None
for i in range(istart, len(tips0)):
    d = tips0[i]

    if i == istart:
        print(f"writing {len(tips0) - istart} new tips, {d['datetime']} to present")

    title = d["title"]
    if "`" in title:
        title = f"'{title}'"

    tweet_text = d["tweet_text"]
    try:
        iendtext = tweet_text.index("https://t.co/")
    except ValueError:  # substring not found
        iendtext = None
    intro = tweet_text[:iendtext].rstrip()
    if not intro:
        intro = "&nbsp;"  # can't be empty
    indented_intro = indent(intro, " "*6)
    
    file0 = findfirst(
        (l["target"].lstrip("./") for l in d["file_links"]),
        lambda s: s.endswith(".f90")
    )
    if file0 is None:
        file0 = "~"

    url = f"https://twitter.com/fortrantip/status/{d['tweet_id']}"
    embed = d["tweet_embed"].replace("\n", "")

    dt = d["datetime"]
    date = dt.date().strftime(r"%d-%b-%Y")
    if date != last_date:
        lines.append(f"  # {date}")

    lines.append(
        fmt.format(
            title=title,
            indented_intro=indented_intro,
            file0=file0,
            url=url,
            embed=embed
        )
    )

    last_date = date

s = "\n\n".join(lines)

with open("data.yaml", "a") as f:
    f.write("\n")
    f.write(s)
    f.write("\n")
