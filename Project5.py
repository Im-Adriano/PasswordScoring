import tensorflow as tf
import numpy as np
import math
import random
import datetime
import PasswordGenerator

passGen = PasswordGenerator.PASSWORD_GENERATOR(1000)

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


epochs = 5

filepath = "model_weights.hdf5"
checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')

log_dir="logs\\fit\\" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=0)

model.fit_generator(passGen, steps_per_epoch=500, epochs=20, callbacks=[tensorboard_callback, checkpoint])
model.evaluate_generator(passGen, steps=1000, verbose = 2)



