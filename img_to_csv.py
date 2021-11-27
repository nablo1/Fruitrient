import json
import numpy as np
import re

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

    value = np.asarray(img_grey.getdata(), dtype=np.int32)
    return value.flatten()


# USAGE
# python img_to_csv.py path/to/images/dir output/outfile.csv

source_dir, output = list(os.sys.argv)[1:3]
pics = pics(source_dir)
sort_override = {"type": ["Apple Braeburn", "Banana", "Orange"]}

labels = {}

re_groups = "^(?P<quality>rotten|fresh)?(?P<type>.*)"


def lbls(path): return re.search(
    re_groups, os.path.basename(path)).groupdict()


for root, _ in pics:
    base = os.path.basename(root)
    for k, v in lbls(root).items():
        if v is None:
            continue
        if not k in labels:
            labels[k] = {v: None}
        else:
            labels[k][v] = None


for k, v in labels.items():
    st = sorted(list(v.keys()))
    for i, vi in enumerate(sort_override.get(k, [])):
        swi = st.index(vi)
        st[i], st[swi] = st[swi], st[i]

    for i, vi in enumerate(st):
        labels[k][vi] = i


def lbls2(path):
    ret = []
    for k, v in re.search(
            re_groups, os.path.basename(path)).groupdict().items():
        if v is None:
            continue
        ret.append((k, labels[k][v]))
    ret.sort(key=lambda x: x[0])
    return ret


ba = [(os.path.join(root, name), lbls2(root)) for root, name in pics]
# final image res
width = 28
height = 28

with open(output, 'w') as f:
    writer = csv.writer(f)

    csv_labels = [f"pixel{i+1}" for i in range(width * height)]
    for k in labels.keys():
        csv_labels.insert(0, k)

    writer.writerow(csv_labels)

    for path, labelings in ba:
        print(path, labelings)
        value = list(process_file(path, (width, height)))

        for k, v in labelings:
            value.insert(0, v)

        writer.writerow(value)

print(json.dumps(labels, indent=4))
