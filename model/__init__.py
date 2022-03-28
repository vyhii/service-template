import tensorflow as tf

# load model

try:
    model = tf.keras.models.load_model("model/EfficientNetB0/")
    print("Model loaded")
except:
    print("Model not found")

