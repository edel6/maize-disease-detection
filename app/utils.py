from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

model_paths = {
    'mdm': 'app/models/healthyVSmdm.h5',
    'sclb': 'app/models/healthyVSsclb.h5',
    'nclb': 'app/models/healthyVSnclb.h5'
}

models = {key: load_model(path) for key, path in model_paths.items()}

def classify_image(filepath, disease):
    img = image.load_img(filepath, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    model = models[disease]
    prediction = model.predict(img_array)

    # Invert the prediction for SCLB and NCLB
    if disease in ['sclb', 'nclb']:
        if prediction[0][0] > 0.5:
            return f'{disease.upper()} Disease'
        else:
            return 'Healthy'
    else:
        if prediction[0][0] > 0.5:
            return 'Healthy'
        else:
            return f'{disease.upper()} Disease'
