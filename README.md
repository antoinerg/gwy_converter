# gwy_converter

Uses Gwyddion to convert SPM (scanning probe microscopy) files into well-supported data-interchange format.

Uses Nix to produce artefacts in a completely reproducible fashion.

## Usage

```bash
$ git clone https://github.com/antoinerg/gwy_converter
$ cd gwy_converter
$ nix-build convert.nix --argstr path "/path/afm_file.sxm"
$ tree result
result
├── channel
│   ├── 00
│   │   ├── channel.json
│   │   └── image.png
│   ├── 01
│   │   ├── channel.json
│   │   └── image.png
... snip ... snip ...
│   ├── 20
│   │   ├── channel.json
│   │   └── image.png
│   └── 21
│       ├── channel.json
│       └── image.png
├── data.gwy
└── image.json

23 directories, 46 files
```

### About gwyddion on NixOS

In order to compile Gwyddion with pygwy module under NixOS,
we need to patch the configure script as [shown here](https://github.com/NixOS/nixpkgs/tree/master/pkgs/development/python-modules/pygtksourceview).

### Running

```bash
PYTHONPATH=result/lib/python2.7/site-packages/:PYTHONPATH xvfb-run ./test.py /mnt/data/nanonis/2015-03-inas_capped/raw/28-03-2015.inas_capped.001.sxm
```
