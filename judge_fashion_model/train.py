import tensorflow as tf
import numpy as np
import argparse
import random
import matplotlib.pyplot as plt

a = argparse.ArgumentParser()
a.add_argument("--path", help="path of db")
args = a.parse_args()


IMG_SHAPE = (160, 160) + (3,)
epochs=10
base_learning_rate = 0.0001
LABELS = 3
batch_size=50



seed = int(random.random() * 100)
directory = args.path
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    directory, labels="inferred", label_mode='categorical',
    color_mode='rgb', batch_size=batch_size, image_size=IMG_SHAPE, shuffle=True, seed=seed,
    validation_split=0.1, subset="training", interpolation='bilinear', follow_links=False
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    directory, labels="inferred", label_mode='binary',
    color_mode='rgb',image_size=IMG_SHAPE, seed=seed,
    validation_split=0.1, subset="validation"
)


AUTOTUNE = tf.data.AUTOTUNE
train_dataset = train_ds.prefetch(buffer_size=AUTOTUNE)
validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)
test_dataset = val_ds.prefetch(buffer_size=AUTOTUNE)

preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input
rescale = tf.keras.layers.experimental.preprocessing.Rescaling(1./127.5, offset= -1)

# data agumentation
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.experimental.preprocessing.RandomFlip('horizontal'),
    tf.keras.layers.experimental.preprocessing.RandomRotation(0.2),
])

base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE, include_top=False, weights='imagenet')
base_model.trainable = False

image_batch, label_batch = next(iter(train_dataset))
feature_batch = base_model(image_batch)
print(feature_batch.shape)

global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
feature_batch_average = global_average_layer(feature_batch)

print(feature_batch_average.shape)

prediction_layer = tf.keras.layers.Dense(LABELS, activation='sigmoid')

inputs = tf.keras.Input(shape=(160, 160, 3))
x = data_augmentation(inputs)
x = preprocess_input(x)
x = base_model(x, training=False)
x = global_average_layer(x)
x = tf.keras.layers.Dropout(0.2)(x)
outputs = prediction_layer(x)
model = tf.keras.Model(inputs, outputs)


model.compile(optimizer=tf.keras.optimizers.Adam(lr=base_learning_rate),
              loss=tf.keras.losses.categorical_crossentropy(),
              metrics=['accuracy'])

print(model.summary())
history = model.fit(train_ds,
                    epochs=epochs,
                    validation_data=val_ds)


converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()
with open('./trained_modelv1.tflite', 'wb') as f:
  f.write(tflite_model)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.ylabel('Accuracy')
plt.ylim([min(plt.ylim()),1])
plt.title('Training and Validation Accuracy')

plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.ylabel('Cross Entropy')
plt.ylim([0,1.0])
plt.title('Training and Validation Loss')
plt.xlabel('epoch')
plt.show()