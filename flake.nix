{
  description = "Markmap Anywidget - Interactive mind maps from markdown";

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
    in {
      # Development shells
      devShells = forAllSystems (pkgs:
        let
          # List of supported Python versions
          supportedPythonVersions = [ "312" "313" ];
          latestPythonVersion = "313";

          # Function to create a dev shell for a specific Python version
          mkPythonDevShell = pyVersion:
            let
              python = pkgs."python${pyVersion}";
            in
            pkgs.mkShell {
              name = "markmap-anywidget-py${pyVersion}";
              buildInputs = with pkgs; [
                python
                uv
                nodejs_20
                pnpm
                ruff
                mypy
                git
                gh
                esbuild
              ];
              shellHook = ''
                export UV_PYTHON="${python}/bin/python"
                export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH"
                echo "🚀 Markmap Anywidget Development Environment (Python ${pyVersion})"
                echo "Python: $(${python}/bin/python --version)"
                echo "Node.js: $(node --version)"
                echo "uv: $(uv --version)"
                echo "pnpm: $(pnpm --version)"
                echo ""
                echo "Ready to build markmap-anywidget!"
              '';
            };

          # Generate devShells for each Python version
          pythonDevShells = builtins.listToAttrs (map (v: {
            name = "py${v}";
            value = mkPythonDevShell v;
          }) supportedPythonVersions);

        in
        pythonDevShells // {
          default = pythonDevShells."py${latestPythonVersion}";
        }
      );

      # Generate checks for each devShell
      checks = forAllSystems (pkgs:
        let
          supportedPythonVersions = [ "312" "313" ];
          mkPythonDevShell = pyVersion:
            let
              python = pkgs."python${pyVersion}";
            in
            pkgs.mkShell {
              name = "markmap-anywidget-py${pyVersion}";
              buildInputs = with pkgs; [
                python
                uv
                nodejs_20
                pnpm
                ruff
                mypy
                git
                gh
                esbuild
              ];
              shellHook = ''
                export UV_PYTHON="${python}/bin/python"
                export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH"
                echo "🚀 Markmap Anywidget Development Environment (Python ${pyVersion})"
                echo "Python: $(${python}/bin/python --version)"
                echo "Node.js: $(node --version)"
                echo "uv: $(uv --version)"
                echo "pnpm: $(pnpm --version)"
                echo ""
                echo "Ready to build markmap-anywidget!"
              '';
            };
        in
        builtins.listToAttrs (map (v: {
          name = "devShell-py${v}";
          value = mkPythonDevShell v;
        }) supportedPythonVersions)
      );
    };
}
