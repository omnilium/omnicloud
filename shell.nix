{pkgs ? import <nixpkgs> {}}:
with pkgs.python3Packages; let
  manager = buildPythonPackage {
    name = "manager";
    src = ./.;
    propagatedBuildInputs = [
      ruamel-yaml
      click
    ];
  };
in
  with pkgs;
    mkShell {
      packages = [
        wget
        yq
        jq

        kubectl
        kubernetes-helm
        cilium-cli
        fluxcd

        (python3.withPackages (python-pkgs:
          with python-pkgs; [
            black
            isort
            flake8
            mypy
            setuptools
            ruamel-yaml
            click
          ]))

        manager
      ];
    }
