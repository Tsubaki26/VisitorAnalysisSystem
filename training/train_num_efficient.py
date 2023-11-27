import tensorflow as tf
from keras.datasets import mnist
import numpy as np
import matplotlib.pyplot as plt
# from keras.applications import EfficientNetB0
from keras.applications.efficientnet_v2 import EfficientNetV2B0
from keras.applications.vgg16 import preprocess_input

(x_train, y_train), (x_test, y_test) = mnist.load_data()    #約55MB

def mnist_preprocessing(X):
    import cv2
    X_list = []
    for x_i in X:
        resize_X = cv2.resize(x_i, (32, 32))
        img = cv2.cvtColor(resize_X, cv2.COLOR_GRAY2BGR)
        X_list.append(img)
    X_list = np.array(X_list)

    return X_list

x_train = mnist_preprocessing(x_train)
x_test = mnist_preprocessing(x_test)

x_train = preprocess_input(x_train)
x_test = preprocess_input(x_test)
# x_train = np.expand_dims(x_train, axis=-1)
# x_test = np.expand_dims(x_test, axis=-1)
print(x_train.shape)
x_train_size = x_train.shape[0]
y_train_size = y_train.shape[0]
x_test_size = x_test.shape[0]
y_test_size = y_test.shape[0]

"""
#白が０
#黒が255
#となっているから、cv2の白黒とは逆
"""
print("x_train: ", x_train_size)
print("y_train: ", y_train_size)
print("x_test: ", x_test_size)
print("y_test: ", y_test_size)

batch_size = 64 #32 128 512 1024 2048
epochs = 10
val_ratio = 0.2
img_width = 32
img_height = 32

#plt.imshow(x_train[2], cmap='gray')
#plt.show()

x_val_split = x_train[-int(x_train.shape[0] * val_ratio):]
y_val_split = y_train[-int(y_train.shape[0] * val_ratio):]
x_train_split = x_train[:-int(x_train.shape[0] * val_ratio)]
y_train_split = y_train[:-int(y_train.shape[0] * val_ratio)]

#*モデルの定義
num_classes = 10

base_model = EfficientNetV2B0(input_shape=(img_width,img_height,3), weights='imagenet', include_top=False)
x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
output = tf.keras.layers.Dense(num_classes, activation='softmax')(x)
model = tf.keras.models.Model(inputs=[base_model.input], outputs=[output])

model.compile(
    optimizer='adam',
    loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

history = model.fit(
        x_train_split,
        y_train_split,
        batch_size=batch_size,
        epochs=epochs,
        validation_data=(x_val_split, y_val_split)
    )

model.save('../myModels/num_model(e)1')


train_loss, train_acc = model.evaluate(x_test,y_test)
print(f"test_loss: {train_loss}, test_acc: {train_acc}")

plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.xlabel('epoch')
plt.subplot(1,2,2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.xlabel('epoch')

plt.savefig('./num_hist_b{}_e{}.jpg'.format(batch_size, epochs))