project = "FortranTip"
author = "Beliavsky and FortranTip contributors"
copyright = "2021"

extensions = [
    "myst_parser",
    "sphinx_design",
]

html_title = "FortranTip"
html_theme = "sphinx_book_theme"
html_theme_options = {
    "use_repository_button": True,
    "repository_url": "https://github.com/zmoon/FortranTip-site",
    "repository_branch": "main",
}

myst_enable_extensions = [
    "tasklist",
]
