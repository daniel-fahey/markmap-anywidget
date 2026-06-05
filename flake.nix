{
  description = "markmap-anywidget: interactive mindmaps from markdown";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
    flake-parts.inputs.nixpkgs-lib.follows = "nixpkgs";
  };

  outputs =
    inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } (
      { lib, ... }:
      {
        systems = [
          "x86_64-linux"
          "aarch64-linux"
          "x86_64-darwin"
          "aarch64-darwin"
        ];

        perSystem =
          { config, pkgs, ... }:
          {
            packages.default = pkgs.callPackage ./default.nix { };

            checks.default = config.packages.default;

            devShells.default = pkgs.mkShell {
              packages = with pkgs; [
                (python3.withPackages (ps: with ps; [
                  config.packages.default
                  marimo
                ]))
              ];
            };
          };
      }
    );
}
