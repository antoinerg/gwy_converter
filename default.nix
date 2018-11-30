with import <nixpkgs>{};

rec {
  convert = stdenv.mkDerivation rec {
    name = "convert";

    file = fetchurl {
	url = "http://localhost:8080/ipfs/QmVzRoYs87Kh3fky2uXQAjKsRW7whP5e6ftGsJp3GTXbo5/raw/01-10-2015.fcc16s1.003.sxm";
	sha256 = "0iss6ppvw68b7baax57nfmbmnr31wblm2i60na8qdl1xqzafhjn1";
    }; 

    buildInputs = [ gwyddion-pygwy  ];
    propagatedBuildInputs = [
      gwyddion-pygwy
      xvfb_run
    ];

    unpackPhase = "true";
    buildPhase = ''
    xvfb-run -a ${gwyddion-converter}/bin/to-gwy ${file}
    xvfb-run -a ${gwyddion-converter}/bin/inspect-gwy data.gwy
    '';
    shellHook = '' export PYTHONPATH=${gwyddion-pygwy}/lib/python2.7/site-packages/:$PYTHONPATH '';
    installPhase = ''
      mkdir -p $out
      cp data.gwy $out/
      cp -r channel $out/
    '';
  };

  gwyddion-converter = stdenv.mkDerivation rec {
    name = "gwyddion-converter";
    src = ./src;

    buildInputs = [ makeWrapper ];
    propagatedBuildInputs = [
      gwyddion-pygwy
      python
      python2Packages.pygtk
      python2Packages.pygobject2
      python2Packages.requests
    ];

    unpackPhase = "true";
    #shellHook = '' export PYTHONPATH=${gwyddion-pygwy}/lib/python2.7/site-packages/:$PYTHONPATH '';
    installPhase = ''
      echo ${gwyddion-pygwy}
      mkdir -p $out/bin
      cp ${./src/to-gwy.py} $out/bin/to-gwy
      wrapProgram $out/bin/to-gwy --prefix PYTHONPATH : $PYTHONPATH

      cp ${./src/inspect-gwy.py} $out/bin/inspect-gwy
      wrapProgram $out/bin/inspect-gwy --prefix PYTHONPATH : $PYTHONPATH
    '';
  };

  gwyddion-pygwy = stdenv.mkDerivation rec {
    name = "gwyddion-pygwy";
    version = "2.48";
    src = fetchurl {
      url = "http://sourceforge.net/projects/gwyddion/files/gwyddion/2.48/gwyddion-2.48.tar.xz";
      sha256 = "119iw58ac2wn4cas6js8m7r1n4gmmkga6b1y711xzcyjp9hshgwx";
    };

    patches = [ ./codegendir.patch ];

    nativeBuildInputs = [ pkgconfig ];
    buildInputs = [
      python
      python2Packages.pygtk
      python2Packages.pygobject2
      glib gnome2.gtksourceview

      # For openGL
      gnome2.gtkglext
      mesa_glu mesa_glu.dev
      xorg.libXt xorg.libXmu xorg.libXt xorg.libICE xorg.libSM

    ];

    meta = {
      homepage = http://gwyddion.net/;

      description = "Scanning probe microscopy data visualization and analysis";

      longDescription = ''
        A modular program for SPM (scanning probe microscopy) data
        visualization and analysis. Primarily it is intended for the
        analysis of height fields obtained by scanning probe microscopy
        techniques (AFM, MFM, STM, SNOM/NSOM) and it supports a lot of
        SPM data formats. However, it can be used for general height
        field and (greyscale) image processing, for instance for the
        analysis of profilometry data or thickness maps from imaging
        spectrophotometry.
      '';
      license = stdenv.lib.licenses.gpl2;
      platforms = stdenv.lib.platforms.linux;
    };
  };
}
