# markmap-anywidget

A simple [anywidget](https://github.com/manzt/anywidget) implementation of [markmap](https://markmap.js.org/) for Jupyter and marimo notebooks.

## Installation

**PyPI:**
```bash
pip install markmap-anywidget
```

**Nix:**
```nix
# your flake.nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    markmap-anywidget.url = "github:daniel-fahey/markmap-anywidget";
  };

  outputs = { nixpkgs, markmap-anywidget, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = [
          (pkgs.python3.withPackages (ps: [
            markmap-anywidget.packages.${system}.default
          ]))
        ];
      };
    };
}
```

## Usage

See the [`marimo` documentation](https://docs.marimo.io/api/inputs/anywidget/) for more information.

```python
import marimo as mo
from markmap_anywidget import MarkmapWidget

widget = mo.ui.anywidget(
    MarkmapWidget(
        markdown_content="""---
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

# markmap

## Links
- [Website](https://markmap.js.org/)
- [GitHub](https://github.com/gera2ld/markmap)

## Features
- `inline code`
- **strong** and *italic*
- Katex: $x = {-b \pm \sqrt{b^2-4ac} \over 2a}$
"""
    )
)

widget
```

## Development

```bash
git clone git@github.com:daniel-fahey/markmap-anywidget.git
cd markmap-anywidget

nix develop -c marimo run examples/marimo.py
```

Tests run automatically in the Nix build (`nix build` or `nix flake check`).

## Releasing

1. Update `version` in `pyproject.toml`
2. Update the npm dependency hash in `default.nix` if needed
3. Commit, tag, and push: `git add -A && git commit -m "v0.3.0" && git tag v0.3.0 && git push --tags`
4. Create a release on GitHub (publishes to PyPI automatically)
