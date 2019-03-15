with import <nixpkgs>{};

{path ? "", url ? "", sha256 ? ""}:
let
  inherit (import ./default.nix) gwyddion-pygwy gwyddion-converter;

  filepath =
    if (path != "") then
      /. + path
    else if (url != "" && sha256 != "") then
      fetchurl {
        name = sha256;
        url = url;
        sha256 = sha256;
      }
    else throw ''
      Cannot retrieve file. Either provide a path to the file to convert as argument `path`
      or a URL and sha256 signature of it as arguments `url` and `sha256`
    '';
in
stdenv.mkDerivation {
  # name = "convert-${baseNameOf filepath}";
  name = "gwy_converter";

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
