# gwyddion on NixOS

In order to compile Gwyddion with pygwy module under NixOS,
we need to patch the configure script as [shown here](https://github.com/NixOS/nixpkgs/tree/master/pkgs/development/python-modules/pygtksourceview).

## TODO

Build python package the Nix way.

## Running

```bash
PYTHONPATH=result/lib/python2.7/site-packages/:PYTHONPATH xvfb-run ./test.py /mnt/data/nanonis/2015-03-inas_capped/raw/28-03-2015.inas_capped.001.sxm
```
