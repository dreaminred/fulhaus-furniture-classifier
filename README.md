# fulhaus-furniture-classifier

A model that uses the MobileNet v2 architecture for classifying the Fulhaus furniture dataset.

Written in Python using `Keras` +  `Tensorflow`, Served by `FastAPI` in `Docker`, CI/CD in `Github Actions`

Validation Accuracy = 94.3% + 2.1% (33 samples, n=20)

## Workflow
0. unzip dataset
1. prepare-data.py (reorgnizes the original dataset for train-model.py) 
2. train-model.py (feed the reorganized data directory into this script)

### Accessing the model

The API file is located inside app/model/model.py

It takes a python list for its input where the first item in the list is a flattened (`np.flatten`) RGB image, and the second item in the list is the shape of the image (`np.shape`). A string label is returned for the prediction.

```
im = cv2.imread('myCat.jpg') 
input = [im.flatten().tolist(), im.shape]
output = model.predict_pipeline(input)
```

## Commands 
### Python
+ python prepare-dataset.py input output_dir
+ python train-model.py training_data
### Docker
+ docker build -t furniture-detection-app .
+ docker run -p 80:80 furniture-detection-app


