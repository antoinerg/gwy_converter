#! /usr/bin/env python2
import sys
import os
import gwy
import json
import pickle

# Load gwy file
path = sys.argv[1]
print("Loading '%s'" % path)
container = gwy.gwy_file_load(path, gwy.RUN_NONINTERACTIVE)

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

# Add to data browser to inspect
gwy.gwy_app_data_browser_add(container)

# List all images
ids = gwy.gwy_app_data_browser_get_data_ids(container)
for i in ids:
    os.makedirs("%s/channel/%02d/" % (output_folder,i))
    # Channel metadata
    ch_meta = {}

    # Get channel title
    title = container["/%d/data/title" % i]
    ch_meta["title"] = title

    # Get channel metadata
    meta = container["/%d/meta" % i]

    for entry in meta.keys_by_name():
        ch_meta[entry] = meta[entry]
        #print('%s:%s' % (entry,meta[entry]))

    # Select the channel
    gwy.gwy_app_data_browser_select_data_field(container, i)

    # Run some functions
    #gwy.gwy_process_func_run('align_rows', container, gwy.RUN_NONINTERACTIVE)
    #gwy.gwy_process_func_run('flatten_base', container, gwy.RUN_NONINTERACTIVE)

    key = gwy.gwy_app_get_data_key_for_id(i)
    data_field = container[key]

    # Extract simple statistics and print them.
    avg, ra, rms, skew, kurtosis = data_field.get_stats()
    #print '%s:%s\t%g\t%g\t%g\t%g' % (path, i, ra, rms, skew, kurtosis)

    # Save PNG thumbnail
    gwy.gwy_file_save(container, "%s/channel/%02d/image.png" % (output_folder,i), gwy.RUN_NONINTERACTIVE)

    # Save pickle
    data = data_field.get_data()
    file = open("%s/channel/%02d/image.p" % (output_folder,i), "w" )
    pickle.dump(data,file)
    file.close()
    # Save metadata
    file = open("%s/channel/%02d/image.json" % (output_folder,i), "w" )
    json.dump(ch_meta,file)
    file.close()

gwy.gwy_app_data_browser_remove(container)

print("%s" % (output_folder))
sys.exit()
