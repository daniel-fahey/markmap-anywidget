{
  lib,
  python3Packages,
  esbuild,
  fetchNpmDeps,
  nodejs_latest,
  npmHooks,
}:

let
  pyproject = lib.importTOML ./pyproject.toml;
  src = ./.;
in

python3Packages.buildPythonPackage (finalAttrs: {
  inherit src;
  pname = pyproject.project.name;
  version = pyproject.project.version;

  pyproject = true;

  build-system = with python3Packages; [ hatchling ];

  nativeBuildInputs = [
    esbuild
    nodejs_latest
    npmHooks.npmConfigHook
  ];

  npmDeps = fetchNpmDeps {
    inherit (finalAttrs) src;
    hash = "sha256-KpBDqntdfYfwo83a0UUJw7c24Z8GLmKhmOmgiY+cEOc=";
  };

  preBuild = ''
    npm ci --offline
    esbuild widget.ts --minify --format=esm --bundle --outdir=src/markmap_anywidget/static
  '';

  dependencies = with python3Packages; [ anywidget ];

  nativeCheckInputs = with python3Packages; [ pytestCheckHook ];
})
