with import <nixpkgs>{};

{filename}:
let
  inherit (import ./default.nix) gwyddion-pygwy gwyddion-converter;
  path = /rpool/lab/data/lt-afm/nanonis + "/${filename}";
in
stdenv.mkDerivation {
  name = "convert-${baseNameOf filename}";

  buildInputs = [ gwyddion-pygwy  ];
  propagatedBuildInputs = [
    gwyddion-pygwy
    xvfb_run
  ];

  unpackPhase = "true";
  shellHook = '' export PYTHONPATH=${gwyddion-pygwy}/lib/python2.7/site-packages/:$PYTHONPATH '';
  installPhase = ''
    mkdir -p $out
    cd $out
    xvfb-run -a ${gwyddion-converter}/bin/to-gwy ${path}
    xvfb-run -a ${gwyddion-converter}/bin/inspect-gwy data.gwy
    # cp data.gwy $out/
    # cp -r channel $out/
  '';
}
