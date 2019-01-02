with import <nixpkgs>{};
let
  inherit (import ./default.nix) gwyddion-pygwy gwyddion-converter;
  filename = /rpool/lab/data/lt-afm/nanonis/2015-10-06-fcc16s1/raw/23-10-2015.fcc16s1.028.sxm;
  name = "23-10-2015.fcc16s1.028.sxm";
in
stdenv.mkDerivation {
  name = "convert-${name}";

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
    xvfb-run -a ${gwyddion-converter}/bin/to-gwy ${filename}
    xvfb-run -a ${gwyddion-converter}/bin/inspect-gwy data.gwy
    # cp data.gwy $out/
    # cp -r channel $out/
  '';
}
