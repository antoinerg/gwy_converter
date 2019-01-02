with import <nixpkgs>{};

{filename ? "23-10-2015.fcc16s1.028.sxm"}:
let
  inherit (import ./default.nix) gwyddion-pygwy gwyddion-converter;
  path = /rpool/lab/data/lt-afm/nanonis/2015-10-06-fcc16s1/raw + "/${filename}";
in
stdenv.mkDerivation {
  name = "convert-${filename}";

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