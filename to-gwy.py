#! /usr/bin/env python2
import sys
import os
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
    os.chdir(output_folder)
except OSError as exc:
    pass

## Download file
rawFile = download_file("http://localhost:8080/%s" % path)

## Gywddion load
print("Gwyddion loading %s" % rawFile)
import gwy
container = gwy.gwy_file_load(rawFile, gwy.RUN_NONINTERACTIVE)

## Save to gwy
gwy.gwy_file_save(container, "%s/data.gwy" % (output_folder) , gwy.RUN_NONINTERACTIVE)

print("%s/" % (output_folder))
sys.exit()
