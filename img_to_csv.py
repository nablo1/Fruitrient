import numpy as np

from PIL import Image

import os
import os.path
import csv


def pics(myDir, format='.jpg', limit=5):
    ret = []
    for root, _, files in os.walk(myDir, topdown=False):
        for i, name in enumerate((files)):
            if i > limit:
                break
            if name.endswith(format):
                ret.append((root, name))
    return ret


def process_file(file, res):
    img_file = Image.open(file)
    img_grey = img_file.resize(res).convert('L')

    value = np.asarray(img_grey.getdata(), dtype=np.int)
    return value.flatten()


# USAGE
# python img_to_csv.py path/to/images/dir output/outfile.csv

source_dir, output = list(os.sys.argv)[1:3]
pics = pics(source_dir)

# Hacky way of having somewhat stable indices
directories = {}
for root, _ in pics:
    directories[os.path.basename(root)] = None
directories2 = list(directories.keys())

# final image res
width = 28
height = 28

with open(output, 'w') as f:
    writer = csv.writer(f)

    labels = [f"pixel{i+1}" for i in range(width * height)]
    labels.insert(0, "type")

    writer.writerow(labels)

    for i, dir in enumerate(directories2):
        directories[dir] = i

    for root, name in pics:
        value = list(process_file(os.path.join(root, name), (width, height)))

        print(name)
        value.insert(0, directories[os.path.basename(root)])
        writer.writerow(value)
