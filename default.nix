{
  pkgs ? import <nixpkgs> { },
}:

pkgs.python3Packages.buildPythonPackage {
  pname = "markmap-anywidget";
  version = builtins.readFile ./VERSION;
  src = pkgs.lib.fileset.toSource {
    root = ./.;
    fileset = pkgs.lib.fileset.unions [
      ./pyproject.toml
      ./VERSION
      ./README.md
      ./src
      ./tests
    ];
  };

  pyproject = true;
  build-system = [ pkgs.python3Packages.setuptools ];
  dependencies = [ pkgs.python3Packages.anywidget ];
  nativeCheckInputs = [ pkgs.python3Packages.pytest ];

  checkPhase = "pytest";
}
