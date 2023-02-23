import tensorflow as tf
from skimage import transform
import numpy as np
from pathlib import Path

__version__ = "0.1.0"

BASE_DIR = Path(__file__).resolve(strict=True).parent
with open(f"{BASE_DIR}/59_0.9683.h5", "rb") as f:
    model = tf.keras.models.load_model(f.name)

labels = ['Bed', 'Chair', 'Sofa']

def predict_pipeline(image):
    im = np.reshape(image[0], image[1]).astype(np.uint8)
    prediction = labels[np.argmax(model.predict(tf.expand_dims(transform.resize(im,(224,224)),axis=0), verbose=0))]
    return prediction