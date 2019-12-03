import json
import sys
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import ndimage

if len(sys.argv) is not 2:
    print("usage: python process-messages.py filename")
    exit()

filename = sys.argv[1]

with open(filename) as json_file:
    data = json.load(json_file)
    print("number of messages received:", len(data))


def plot_images(images, labels):
    n = len(images)
    k = math.ceil(math.sqrt(n))
    plt.figure(figsize=(10, 10))
    for i in range(len(images)):
        plt.subplot(k, k, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(images[i], cmap=plt.cm.binary)
        plt.title(labels[i])
    plt.tight_layout()
    plt.show()


def correct(datum):
    if datum["timetoken"] == "15751756761692096":
        datum["entry"]["user_label"] = 3
    return datum


#data = [data[0]]
data = [correct(datum) for datum in data]
data = sorted(data, key=lambda datum: datum["entry"]["user_label"])

images = []
labels = []

rot_inc = 20
angles = range(-40, 40 + rot_inc, rot_inc)
pos_inc = 2

for datum in data:
    entry = datum["entry"]
    original_image = np.array(entry["image_data"]).reshape((28, 28))
    user_label = entry["user_label"]

    for angle in angles:
        image_data = ndimage.rotate(original_image, angle, reshape=False)
        images.append(image_data)
        labels.append(user_label)

        rows, cols = np.where(image_data)
        miny = np.min(rows)
        maxy = np.max(rows)
        minx = np.min(cols)
        maxx = np.max(cols)

        for x in range(-minx, 28 - maxx, pos_inc):
            for y in range(-miny, 28 - maxy, pos_inc):
                images.append(np.roll(image_data, (x, y), (1, 0)))
                labels.append(user_label)

print("number of tweaked training data:", len(images))

#plot_images(images, labels)

np.save(filename + ".npy", {"images": images, "labels": labels})
