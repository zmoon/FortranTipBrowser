project = "FortranTip"
author = "Beliavsky and FortranTip contributors"
copyright = f"2021\u20132022, {author} (website by zmoon)"

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
]

html_title = "FortranTip Browser"
html_theme = "sphinx_book_theme"
html_theme_options = {
    "use_repository_button": True,
    "repository_url": "https://github.com/zmoon/FortranTipBrowser",
    "repository_branch": "main",
}

myst_enable_extensions = [
    "dollarmath",
    "substitution",
    "tasklist",
]

linkcheck_ignore = [
    "https://github\.com/.+/.+#.+",  # anchor link in a Markdown file on GH
]
