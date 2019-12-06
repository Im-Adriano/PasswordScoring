# CSEC-659-Group-Project


## What is it?
* Project5.py
  * Used to train the network
* CheckPassword.py
  * Used to run the interactive session with the model. Where the user inputs their password and the model scores it.
  * Model must be adjusted within the code to match the model weights you are trying to load onto it.

## Trained Models
* model_weights_1.hdf5
  * Trained without a dropout layer on 10 million passwords
  * Remove dropout layer from model in CheckPassword.py before running.
* model_weights_2.hdf5
  * Trained on 100 million password with dropout layer.
  * Just rename to model_weights.hdf5 to use with current CheckPassword.py

## Requirements
* rockyou.txt
* tensorflow
* numpy
