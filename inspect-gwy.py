#! /usr/bin/env python2
import sys
import os
import gwy
import json
import pickle
import requests

path = sys.argv[1]

# Helpers
def download_file(url):
    print("Downloading %s" % url)
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

# Main program
## Create output folder
output_folder = "."
try:
    os.makedirs("%s/" % (output_folder))
except OSError as exc:
    pass

## Download file
raw_file=download_file("http://localhost:8080%s" % path)

# Load gwy file
print("Gwyddion loading '%s'" % raw_file)
container = gwy.gwy_file_load(raw_file, gwy.RUN_NONINTERACTIVE)

# Add to data browser to inspect
gwy.gwy_app_data_browser_add(container)

# List all images
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
    #data = data_field.get_data()
    #file = open("%s/channel/%02d/image.p" % (output_folder,i), "w" )
    #pickle.dump(data,file)
    #file.close()

    # Save metadata
    file = open("%s/channel/%02d/image.json" % (output_folder,i), "w" )
    json.dump(ch_meta,file)
    file.close()

gwy.gwy_app_data_browser_remove(container)

print("%s" % (output_folder))
sys.exit()
