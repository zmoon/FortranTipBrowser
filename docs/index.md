---
sd_hide_title: true
myst:
  substitutions:
    gb_logo: |
      <img src="https://raw.githubusercontent.com/compiler-explorer/compiler-explorer/main/views/resources/site-logo.svg"
      alt="Godbolt Compiler Explorer logo" width="55.11" height="16.7" class="align-text-bottom" />
    fpg_logo: |
      <img src="https://raw.githubusercontent.com/fortran-lang/playground/main/frontend/src/fortran-logo.png"
      alt="Fortran logo" height="15.5" class="align-text-bottom" />
...

# FortranTip

[FortranTip](https://twitter.com/fortrantip) tips in one Sphinx site.


```{include} _random-tip-btn_snippet.myst
```

## Tips for browsing this site

* Use the {{ gb_logo }} buttons above code samples to open them in the
  [Godbolt Compiler Explorer](https://godbolt.org/)
  and test different compilers
* Use the {{ fpg_logo }} buttons above code samples to open them in
  [Fortran Playground](https://play.fortran-lang.org/)
* Use the {kbd}`Left` and {kbd}`Right` arrow keys to switch between sequential tips
* The embedded Tweets seem to load much faster in Chrome than Firefox
* The tips [are in](./tips/index.md) chronological Tweet order, but you can also
  {ref}`browse by topic <by-topic>`


```{toctree}
:maxdepth: 2
:hidden:

Tips <tips/index>

@FortranTip <https://twitter.com/fortrantip>

```
