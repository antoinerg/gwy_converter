with import <nixpkgs>{};

{path}:
let
  inherit (import ./default.nix) gwyddion-pygwy gwyddion-converter;
  filepath = /. + path;
in
stdenv.mkDerivation {
  name = "convert-${baseNameOf filepath}";

  buildInputs = [
    gwyddion-pygwy
    xvfb_run
  ];

  unpackPhase = "true";
  shellHook = '' export PYTHONPATH=${gwyddion-pygwy}/lib/python2.7/site-packages/:$PYTHONPATH '';
  installPhase = ''
    mkdir -p $out
    cd $out
    xvfb-run -a ${gwyddion-converter}/bin/to-gwy ${filepath}
    xvfb-run -a ${gwyddion-converter}/bin/inspect-gwy data.gwy
  '';
}
