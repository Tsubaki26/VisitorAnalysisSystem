import tensorflow as tf
import pathlib
import matplotlib.pyplot as plt
import sys
# from keras.applications import EfficientNetB0
from keras.applications.efficientnet_v2 import EfficientNetV2B0
from keras.applications.vgg16 import preprocess_input

data_dir = pathlib.Path('./../images/area_images/')
total_samples = len(list(data_dir.glob('*/*.png')))
print(total_samples)  #学習データ数

img_height = 50
img_width = 100
batch_size = 64
epochs = 5

train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height,img_width),
    batch_size=batch_size
)
# print(len(train_ds))
# train_ds = train_ds.take(total_samples//batch_size//2)
# print(len(train_ds))
# sys.exit()


val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height,img_width),
    batch_size=batch_size
)

# 画像データを前処理します。
class_names = train_ds.class_names
print(class_names)

train_ds = train_ds.map(lambda x, y: (preprocess_input(x), y))
val_ds = val_ds.map(lambda x, y: (preprocess_input(x), y))



kana_classes = len(class_names)

base_model = EfficientNetV2B0(input_shape=(img_height,img_width,3), weights='imagenet', include_top=False)
x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
output = tf.keras.layers.Dense(kana_classes, activation='softmax')(x)
model = tf.keras.models.Model(inputs=[base_model.input], outputs=[output])

model.compile(
    optimizer='adam',
    loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)


# xとyを取得します。
# x_train_ds = list(train_ds.map(lambda x, y: x))
# y_train_ds = list(train_ds.map(lambda x, y: y))
# x_val_ds = list(val_ds.map(lambda x, y: x))
# y_val_ds = list(val_ds.map(lambda x, y: y))

# print(x_train_ds)
# history = model.fit(
#     train_ds,
#     validation_data=val_ds,
#     epochs=epochs
# )
history = model.fit(
        train_ds,
        batch_size=batch_size,
        epochs=epochs,
        validation_data=val_ds
    )

model.save('./../myModels/area_model(e)2')
# tf.saved_model.save(model, './myModels/area_model(e)1')


train_loss, train_acc = model.evaluate(train_ds)
print(train_loss, train_acc)
# valn_loss, val_acc = model.evaluate(val_ds)

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

plt.savefig('./area_hist_b{}_e{}2.jpg'.format(batch_size, epochs))
