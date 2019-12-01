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


# manual corrections
data[2]["entry"]["user_label"] = 3

data = sorted(data, key=lambda datum: datum["entry"]["user_label"])

images = []
labels = []
for datum in data:
    entry = datum["entry"]
    image_data = np.array(entry["image_data"]).reshape((28, 28))
    images.append(image_data)
    labels.append(entry["user_label"])

plot_images(images, labels)
