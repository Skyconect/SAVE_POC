# -*- coding: utf-8 -*-
"""model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18idE0ipVZgCWVKo0ySOTuGAJNxLKQvWz
"""

# Commented out IPython magic to ensure Python compatibility.
import os
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2 as cv
from numpy.random import seed
seed(45)
import pickle
import pandas as pd
import re,json

from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from skimage import io
from glob import glob 
import datetime
# %matplotlib inline
# %load_ext tensorboard

# Commented out IPython magic to ensure Python compatibility.
# %cd /Users/barakasoka/Desktop

CUSTOM_MODEL_NAME = 'FinalModel_1'

paths = {
    'WORKSPACE_PATH': os.path.join('SAVE', 'workspace'),
    'SCRIPTS_PATH': os.path.join('SAVE','scripts'),
    'METADATA_PATH': os.path.join('SAVE','metadata'),
    'DATASET_PATH': os.path.join('SAVE','Datasets'),
    'NONCERVIX_PATH': os.path.join('SAVE','non_cervix'),
    'IMAGE_PATH': os.path.join('SAVE', 'workspace','images'),
    'TRAIN_PATH': os.path.join('SAVE', 'workspace','images','train'),
    'VALID_PATH': os.path.join('SAVE','workspace','images','valid' ),
    'TRAINPOS_PATH': os.path.join('SAVE','workspace','images','train','positive'),
    'TRAINNEG_PATH': os.path.join('SAVE','workspace','images','train','negative'),
    'VALIDPOS_PATH': os.path.join('SAVE','workspace','images','valid','positive'),
    'VALIDNEG_PATH': os.path.join('SAVE','workspace','images','valid','negative'),
    'SORTED_PATH': os.path.join('SAVE', 'workspace','images','sorted'),
    'MODEL_PATH': os.path.join('SAVE', 'workspace','models'),
    'OUTPUT_PATH': os.path.join('SAVE', 'workspace','models',CUSTOM_MODEL_NAME), 
 }

for path in paths.values():
    if not os.path.exists(path):
        if os.name == 'posix':
            !mkdir -p {path}
        if os.name == 'nt':
            !mkdir {path}

"""#### modeling"""

from keras.preprocessing.image import ImageDataGenerator
BATCHSIZE=16
SIZE=256
EPOCH=60
TRAIN=192
train_gen=ImageDataGenerator(rescale=1./255)
val_gen=ImageDataGenerator(rescale=1./255)
train_dir=paths['TRAIN_PATH']
val_dir=paths['VALID_PATH']

train_data=train_gen.flow_from_directory(train_dir, target_size=(SIZE,SIZE), class_mode="categorical",
                                        batch_size=BATCHSIZE)
val_data=val_gen.flow_from_directory(val_dir, target_size=(SIZE,SIZE), class_mode="categorical",
                                    batch_size=BATCHSIZE)
for data_batch, labels_batch in train_data:
    print('data batch shape:', data_batch.shape)
    print('label batch shape:', labels_batch.shape)
    break

"""#### tranfer learning"""

base_model = tf.keras.applications.vgg19.VGG19(input_shape=(256,256,3),
                                         include_top=False,
                                         weights='imagenet')
base_model.trainable = False

def create_model():
    model = Sequential([
        base_model,
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(16, activation='relu'),
        Dropout(0.25),
        BatchNormalization(),
        Dense(2, activation='softmax')])
    METRICS = [ 
        tf.keras.metrics.BinaryAccuracy(name='accuracy'),
        tf.keras.metrics.Precision(name='precision'),
        tf.keras.metrics.Recall(name='recall'),
        tf.keras.metrics.AUC(name='auc'),]
    model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(0.001),
                  metrics= METRICS)
    return model
model= create_model()
model.summary()

log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

"""#### training 1"""

history = model.fit(train_data,
                    steps_per_epoch = TRAIN/BATCHSIZE,
                    epochs = EPOCH,
                    validation_data= val_data,
                   callbacks=[tensorboard_callback])

"""#### tensorboard"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorboard --logdir logs/fit

model.save('cancer_detection_model_v1.h5')

pickle.dump(history.history, open(f'cancer_detection_history_v1.pkl', 'wb'))

"""#### checking metrics"""

METRICS = ['accuracy', 'loss', 'precision', 'recall', 'auc']

for i in METRICS:
  metric = history.history[i]
  val_metric = history.history['val_'+i]

  epochs = range(1, len(metric) + 1)

  plt.figure(figsize=(8.0, 8.0))
  plt.plot(epochs, metric, 'r', label='Training '+i)
  plt.plot(epochs, val_metric, 'b', label = 'validation '+i)
  plt.xlabel('Epoch')
  plt.ylabel(i)
  plt.title('training and validation '+i)
  plt.legend()
  plt.show()