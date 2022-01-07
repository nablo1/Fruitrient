import json
import numpy as np
import re

from PIL import Image

import os
import os.path
import csv
import sqlite3
import io

def pics(myDir, limit=100):
    ret_train = []
    ret_test = []
    for root, _, files in os.walk(myDir, topdown=False):
        this = []
        for name in files:
            if name.endswith(".jpg") or name.endswith(".png"):
                this.append((root, name))
        if len(this) == 0:
            continue

        tr = int(len(this) * 0.7)
        te = len(this) - tr
        train = this[:tr]
        test = this[-te:]

        ret_train.extend(train)
        ret_test.extend(test)

    return ret_train, ret_test


def process_file(file, res):
    img_file = Image.open(file)
    img_grey = img_file.resize(res)

    value = np.asarray(img_grey.getdata(), dtype=np.int32)
    return value.flatten()


# USAGE
# python img_to_csv.py path/to/images/dir output/outfile.db

source_dir, output = list(os.sys.argv)[1:3]
pics_train, pics_test = pics(source_dir)
sort_override = {"type": []}

labels = {}

re_groups = "^(?P<type>.*)"


def lbls(path): return re.search(
    re_groups, os.path.basename(path)).groupdict()


for root, _ in pics_train:
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


def fgor(arr): return [(os.path.join(root, name), lbls2(root))
                       for root, name in arr]

width = 100
height = 100

def write_data(cursor, table, data):
    for path, labelings in data:
        # print(path, labelings)
        image = Image.open(path).resize((width, height))
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='png')
        image_bytes.seek(0)

        _, label_value = next(iter(labelings))
        cursor.execute(f'''
            insert into {table}
            (label, image) values (?, ?)
        ''', (label_value, image_bytes.read()))



ba_train = fgor(pics_train)
ba_test = fgor(pics_test)

try:
    os.remove(output)
except:
    pass

conn = sqlite3.connect(output)
cursor = conn.cursor()

cursor.execute(f'''
        create table {"data_df"}
        (label integer, image blob)
''')

write_data(cursor, "data_df", ba_train)
write_data(cursor, "data_df", ba_test)

print("total entries: ", len(ba_test) + len(ba_train))

conn.commit()

print(json.dumps(labels, indent=4))
