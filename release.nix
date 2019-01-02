with import <nixpkgs>{};
let
  inherit (import ./default.nix) gwyddion-pygwy gwyddion-converter;
in
stdenv.mkDerivation {
  name = "convert";

  buildInputs = [ gwyddion-pygwy  ];
  propagatedBuildInputs = [
    gwyddion-pygwy
    xvfb_run
  ];

  unpackPhase = "true";
  buildPhase = ''
  cd /nix/store/h2rbfsjxvw9vg87v3lpgfpzdqps9aaz4-2015-10-06-fcc16s1/raw
  xvfb-run -a ${gwyddion-converter}/bin/to-gwy ${file}
  xvfb-run -a ${gwyddion-converter}/bin/inspect-gwy data.gwy
  '';
  shellHook = '' export PYTHONPATH=${gwyddion-pygwy}/lib/python2.7/site-packages/:$PYTHONPATH '';
  installPhase = ''
    mkdir -p $out
    cp data.gwy $out/
    cp -r channel $out/
  '';
}
