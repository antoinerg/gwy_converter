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
print("SHA1: {0}".format(file_hash))

import gwy
container = gwy.gwy_file_load(path, gwy.RUN_NONINTERACTIVE)

# Save into gwyddion file format
try:
    os.makedirs("/tmp/gwyconvert/%s/" % file_hash)
except OSError as exc:
    pass

gwy.gwy_file_save(container, "/tmp/gwyconvert/%s/data.gwy" % file_hash , gwy.RUN_NONINTERACTIVE)
gwy.gwy_app_data_browser_add(container)

# List all images
ids = gwy.gwy_app_data_browser_get_data_ids(container)
for i in ids:
    # Select the channel and run some functions.
    gwy.gwy_app_data_browser_select_data_field(container, i)
    gwy.gwy_process_func_run('align_rows', container, gwy.RUN_NONINTERACTIVE)
    gwy.gwy_process_func_run('flatten_base', container, gwy.RUN_NONINTERACTIVE)
    # Extract simple statistics and print them.
    data_field = container[gwy.gwy_app_get_data_key_for_id(i)]
    avg, ra, rms, skew, kurtosis = data_field.get_stats()
    print '%s:%s\t%g\t%g\t%g\t%g' % (path, i, ra, rms, skew, kurtosis)
    gwy.gwy_file_save(container, "/tmp/gwyconvert/%s/%d.png" % (file_hash,i), gwy.RUN_NONINTERACTIVE)

gwy.gwy_app_data_browser_remove(container)

sys.exit()
