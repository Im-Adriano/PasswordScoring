import tensorflow as tf
import numpy as np
import math
import random
import datetime
import sys

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(500, activation='sigmoid', input_dim=70),
    tf.keras.layers.Dense(500, activation='sigmoid'),
    tf.keras.layers.Dense(500, activation='sigmoid'),
    tf.keras.layers.Dense(500, activation='sigmoid'),
    tf.keras.layers.Dense(500, activation='sigmoid'),
    tf.keras.layers.Dense(500, activation='sigmoid'),
    tf.keras.layers.Dense(5, activation='softmax')
])


model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

filepath = "model_weights.hdf5"

try:
    model.load_weights(filepath)
except OSError:
    print('No trained model found')
    sys.exit()


while True:
    password = input('Input the password you would like scored: ')
    passwordAsInt = np.fromiter((ord(c) for c in password), dtype=np.int)
    passwordAsInt = np.pad(passwordAsInt, (0,70-len(passwordAsInt)))
    prediction = model.predict_classes(np.array([passwordAsInt]), verbose=0)
    print(f'Your password score: {prediction[0]}')