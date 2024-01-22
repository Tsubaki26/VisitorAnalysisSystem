import tensorflow as tf

model = tf.keras.models.load_model("./myModels/area_model(e)1", compile=False)

tf.keras.utils.plot_model(model, show_shapes=True, expand_nested=True, to_file='model2.png')