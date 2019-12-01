import json
import sys
import matplotlib.pyplot as plt
import numpy as np
import math

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
    plt.figure(figsize=(k*1.5, k*1.5))
    for i in range(len(images)):
        plt.subplot(k, k, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(images[i], cmap=plt.cm.binary)
        plt.title(labels[i])
    plt.show()


images = []
labels = []
for datum in data:
    entry = datum["entry"]
    image_data = np.array(entry["image_data"]).reshape((28, 28))
    images.append(image_data)
    labels.append(entry["user_label"])

# manual corrections
labels[2] = 3

plot_images(images, labels)
