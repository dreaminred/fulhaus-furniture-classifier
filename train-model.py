import tensorflow as tf
import numpy as np
import os
from pathlib import Path
import re
import sys

BATCH_SIZE = 20
N_CLASSES = 3
TOTAL_EPOCHS = 100

def main(input_dir):

    training_dir = input_dir + "/train"
    testing_dir = input_dir + "/test"


    #Generators
    train_generator = tf.keras.preprocessing.image.ImageDataGenerator(
        data_format='channels_last',
        rescale=1. / 255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )

    train_batches = train_generator.flow_from_directory(
        batch_size=BATCH_SIZE,
        directory=training_dir,
        target_size=[224, 224],
        class_mode='categorical'
    )

    val_batches = train_generator.flow_from_directory(
        batch_size=BATCH_SIZE,
        directory=testing_dir,
        target_size=[224, 224],
        class_mode='categorical'
    )

    kernel_initializer = tf.keras.initializers.glorot_uniform(seed=1337)
    trained_model = tf.keras.applications.mobilenet_v2.MobileNetV2(
        include_top=False,
        weights='imagenet',
        alpha=0.5,
        input_shape=[224, 224, 3],
        pooling='max')
    output = tf.keras.layers.Dense(N_CLASSES, activation='softmax', kernel_initializer=kernel_initializer)(trained_model.output)
    model = tf.keras.Model(inputs=trained_model.input, outputs=output)

    # Callback to save weights, based on val_acc
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        './checkpoints/{epoch:02d}_{val_accuracy:.4f}.h5',
        save_weights_only=False,
        verbose=1,
        monitor='val_accuracy',
        save_best_only=True,
        mode='max'
    )

    # Callbackto plot data on TensorBoard
    tensorboard_callback = tf.keras.callbacks.TensorBoard(
        log_dir='./logs/furniture_classifier',
        histogram_freq=0,
        batch_size=BATCH_SIZE
    )

    reduce_lr_callback = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_accuracy',
        factor=0.5,
        patience=4,
        min_lr=1e-6
    )

    early_stopping_callback = tf.keras.callbacks.EarlyStopping(
        monitor='val_accuracy',
        patience=20,
        mode='max',
    )

    TRAIN_DATASET_SIZE = len(train_batches)
    VAL_DATASET_SIZE   = len(val_batches)

    # Weighted losses for class equilibrium
    unique, counts = np.unique(train_batches.classes, return_counts=True)
    class_weigths = dict(zip(unique, np.true_divide(counts.sum(), N_CLASSES*counts)))

    if Path('./checkpoints/').exists():
        epoch_number_array = []
        val_accuracy_array = []
        file_name_array = []
        for file in os.listdir('./checkpoints/'):
            epoch, val_acc = re.search(r'(\d\d)_(\d\.\d{4})\.h5', file).group(1,2)
            epoch_number_array.append(int(epoch))
            val_accuracy_array.append(float(val_acc))
            file_name_array.append(file)

        if len(val_accuracy_array) == 0:
            INITIAL_EPOCH = 0
        else:
            highest_acc = val_accuracy_array.index(max(val_accuracy_array))
            INITIAL_EPOCH = epoch_number_array[highest_acc]
            model_checkpoint_callback.best = val_accuracy_array[highest_acc]
            model.load_weights('./checkpoints/'+file_name_array[highest_acc])
    else:
        os.makedirs('./checkpoints/')
        INITIAL_EPOCH = 0

    # Prepare model to run
    model.compile(optimizer = tf.keras.optimizers.Adam(),
                  loss = 'categorical_crossentropy',
                  metrics = ['accuracy']
                  )

    # Starts training the model
    model.fit(train_batches,
              epochs=TOTAL_EPOCHS,
              verbose=2,
              steps_per_epoch=TRAIN_DATASET_SIZE,
              validation_data=val_batches,
              validation_steps=VAL_DATASET_SIZE,
              initial_epoch=INITIAL_EPOCH,
              class_weight=class_weigths,
              callbacks=[model_checkpoint_callback, tensorboard_callback, reduce_lr_callback, early_stopping_callback]
              )


if __name__=='__main__':
    input_dir = sys.argv[1]
    main(input_dir)