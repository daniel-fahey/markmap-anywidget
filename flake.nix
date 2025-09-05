{
  description = "markmap-anywidget: interactive mindmaps from Markdown";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      # Function to apply a function to all supported systems
      forAllSystems = function:
        nixpkgs.lib.genAttrs [
          "x86_64-linux"
          "aarch64-linux"
          "x86_64-darwin"
          "aarch64-darwin"
        ] (system: function nixpkgs.legacyPackages.${system});

      # Shared configuration
      supportedPythonVersions = [ "310" "311" "312" "313" ];
      latestPythonVersion = "313";

      # Function to create a dev shell for a specific Python version
      mkPythonDevShell = pkgs: pyVersion:
        let
          python = pkgs."python${pyVersion}";
        in
        pkgs.mkShell {
          name = "markmap-anywidget-py${pyVersion}";
          buildInputs = with pkgs; [
            python
            uv
            nodejs-slim
            pnpm
            git
            gh
            sd
            gawk
          ];
          shellHook = ''
            export UV_PYTHON="${python}/bin/python"
            export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH"
            echo "🚀 markmap-anywidget development environment (Python ${pyVersion})"
            echo "Python: $(${python}/bin/python --version)"
            echo "Node.js: $(node --version)"
            echo "uv: $(uv --version)"
            echo "pnpm: $(pnpm --version)"
            echo ""
            echo "Ready to build markmap-anywidget!"
          '';
        };

      # Function to generate Python shells for a given package set
      mkPythonShells = pkgs:
        builtins.listToAttrs (map (v: {
          name = "py${v}";
          value = mkPythonDevShell pkgs v;
        }) supportedPythonVersions);

    in {
      # Development shells
      devShells = forAllSystems (pkgs:
        let
          pythonDevShells = mkPythonShells pkgs;
        in
        pythonDevShells // {
          default = pythonDevShells."py${latestPythonVersion}";
        }
      );
    };
}