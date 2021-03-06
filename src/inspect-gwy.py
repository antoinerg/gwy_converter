#! /usr/bin/env python2
import sys
import os
import gwy
import json
import pickle
import requests

path = sys.argv[1]

# Main program
## Create output folder
output_folder = "."
try:
    os.makedirs("%s/" % (output_folder))
except OSError as exc:
    pass

## Download file
raw_file = path

# Load gwy file
print("Gwyddion loading '%s'" % raw_file)
container = gwy.gwy_file_load(raw_file, gwy.RUN_NONINTERACTIVE)

# Add to data browser to inspect
gwy.gwy_app_data_browser_add(container)

# Save metadata to image.json
image_folder = output_folder
image_meta = {}
image_meta["type"] = "inspect-gwy"
meta = container["/0/meta"]
for entry in meta.keys_by_name():
    image_meta[entry] = meta[entry]
    #print('%s:%s' % (entry,meta[entry]))
file = open("%s/image.json" % (image_folder), "w" )
json.dump(image_meta,file)
file.close()

# List all channels
ids = gwy.gwy_app_data_browser_get_data_ids(container)

for i in ids:
    channel_folder = "%s/channel/%02d/" % (output_folder,i)
    os.makedirs(channel_folder)
    print("Created folder '%s'" % channel_folder)
    # Channel metadata
    ch_meta = {}

    # Get channel title
    title = container["/%d/data/title" % i]
    ch_meta["title"] = title
    ch_meta["index"] = i

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

    data = data_field.get_data()

    # from array import array
    # output_file = open("%s/channel/%02d/binary" % (output_folder,i), 'wb')
    # float_array = array('d', data)
    # float_array.tofile(output_file)
    # output_file.close()

    # Save into JSON
    ch_meta["data"] = data

    # Save pickle
    #file = open("%s/channel/%02d/image.p" % (output_folder,i), "w" )
    #pickle.dump(data,file)
    #file.close()

    # Save binary data
    #data = data_field.get_data()

    # Save PNG thumbnail
    gwy.gwy_file_save(container, "%s/channel/%02d/image.png" % (output_folder,i), gwy.RUN_NONINTERACTIVE)

    # Save metadata
    file = open("%s/channel/%02d/channel.json" % (output_folder,i), "w" )
    json.dump(ch_meta,file)
    file.close()

gwy.gwy_app_data_browser_remove(container)

print("%s" % (output_folder))
sys.exit()
