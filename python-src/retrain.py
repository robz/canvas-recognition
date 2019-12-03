import math
import matplotlib.pyplot as plt
import numpy as np
import sys
import tensorflow as tf
import tensorflowjs as tfjs
from sklearn.utils import shuffle

if len(sys.argv) is not 2:
    print("usage: python read-data.py filename")
    exit()

filename = sys.argv[1]

data = np.load(filename + ".npy", allow_pickle=True)
x_fails = data.item().get("images")
y_fails = np.array(data.item().get("labels"), dtype=np.uint8)

print("loaded", len(x_fails), "failure cases")

x_fails = tf.cast(tf.reshape(x_fails, (len(x_fails), 28 * 28)), dtype=tf.float64)

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

x_train = x_train / 255
x_test = x_test / 255
x_train = tf.reshape(x_train, (len(x_train), 28 * 28))
x_test = tf.reshape(x_test, (len(x_test), 28 * 28))

x_train = tf.concat([x_train, x_fails], 0).numpy()
y_train = tf.concat([y_train, y_fails], 0).numpy()
x_train, y_train = shuffle(x_train, y_train)

x_val = x_train[-10000:]
y_val = y_train[-10000:]
x_train = x_train[:-10000]
y_train = y_train[:-10000]

model = tf.keras.Sequential(
    [
        tf.keras.layers.Dense(64, input_shape=(28 * 28,), activation="relu"),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(10, activation="softmax"),
    ]
)
model.summary()
model.compile(
    optimizer=tf.keras.optimizers.RMSprop(),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
)
model.fit(x_train, y_train, batch_size=64, epochs=20, validation_data=(x_val, y_val))

filename = filename.split('/')[1].split('.')[0]
model.save("model/mnist_model-" + filename + ".h5")
tfjs.converters.save_keras_model(model, "model-retrained")
