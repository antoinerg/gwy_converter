#! /usr/bin/env python2
import sys
import os

path = sys.argv[1]
print("Loading '%s'" % path)

# Hash files
import hashlib
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

sha1 = hashlib.sha1()

with open(path, 'r') as f:
    while True:
        data = f.read(BUF_SIZE)
        if not data:
            break
        sha1.update(data)

file_hash = sha1.hexdigest()
output_folder = "."
print("SHA1: {0}".format(file_hash))

# Create output folder
try:
    os.makedirs("%s/" % (output_folder))
except OSError as exc:
    pass

import gwy
container = gwy.gwy_file_load(path, gwy.RUN_NONINTERACTIVE)

# Save to gwy
gwy.gwy_file_save(container, "%s/data.gwy" % (output_folder) , gwy.RUN_NONINTERACTIVE)

print("%s/" % (output_folder))
sys.exit()
