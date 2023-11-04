import tensorflow as tf
from keras.datasets import mnist
import matplotlib.pyplot as plt
import numpy as np
import csv

(x_train, y_train), (x_test, y_test) = mnist.load_data()    #約55MB

x_train = np.expand_dims(x_train, axis=-1)
x_test = np.expand_dims(x_test, axis=-1)

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

batch_size = 128 #32 128 512 1024 2048
epochs = 50
val_ratio = 0.2

#plt.imshow(x_train[2], cmap='gray')
#plt.show()


#*モデルの定義
num_classes = 10

# model = tf.keras.Sequential([
#     tf.keras.layers.Rescaling(1./255),          #標準化
#     tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same'),
#     tf.keras.layers.MaxPooling2D(),
#     tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same'),
#     tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same'),
#     tf.keras.layers.MaxPooling2D(strides=(2,2)),
#     tf.keras.layers.Conv2D(128, 3, activation='relu', padding='same'),
#     tf.keras.layers.Conv2D(128, 3, activation='relu', padding='same'),
#     tf.keras.layers.MaxPooling2D(strides=(2,2)),
#     tf.keras.layers.Flatten(),                  #１次元に
#     tf.keras.layers.Dense(128, activation='relu'),
#     tf.keras.layers.Dropout(0.5),
#     tf.keras.layers.Dense(num_classes, activation='softmax')
# ])

#モデル2
model = tf.keras.Sequential([
    tf.keras.layers.Rescaling(1./255),          #標準化
    tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same'),
    tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same'),
    tf.keras.layers.MaxPooling2D(strides=(2,2)),
    tf.keras.layers.Flatten(),                  #１次元に
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

learning_logs = []

train_accuracies = []
val_accuracies = []
train_losses = []
val_losses = []

ratios = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

#*学習

for ratio in ratios:
    #学習データの分割
    x_train_split = x_train[:int(x_train_size*ratio)]
    y_train_split = y_train[:int(y_train_size*ratio)]

    x_val_split = x_train_split[-int(x_train_split.shape[0] * val_ratio):]
    y_val_split = y_train_split[-int(y_train_split.shape[0] * val_ratio):]
    x_train_split = x_train_split[:-int(x_train_split.shape[0] * val_ratio)]
    y_train_split = y_train_split[:-int(y_train_split.shape[0] * val_ratio)]

    #学習
    history = model.fit(
        x_train_split,
        y_train_split,
        batch_size=batch_size,
        epochs=epochs,
        validation_data=(x_val_split, y_val_split)
    )
    #モデルの評価
    train_loss, train_acc = model.evaluate(x_train_split, y_train_split)
    val_loss, val_acc = model.evaluate(x_val_split, y_val_split)

    #精度，損失を配列に格納
    learning_logs.append([train_acc,val_acc,train_loss,val_loss])
    train_accuracies.append(train_acc)
    val_accuracies.append(val_acc)
    train_losses.append(train_loss)
    val_losses.append(val_loss)

    text_file = open('./training/history_log.txt', 'a')
    text_file.write("{}\n".format(history))
text_file.write("\n")
#csvファイルに保存
with open('./training/trainLog4.csv', 'a', newline="") as f:
    writer = csv.writer(f)
    writer.writerows(learning_logs)


#学習
"""
ratio = 1.0
x_train_split = x_train[:int(x_train_size*ratio)]
y_train_split = y_train[:int(y_train_size*ratio)]

x_val_split = x_train_split[-int(x_train_split.shape[0] * val_ratio):]
y_val_split = y_train_split[-int(y_train_split.shape[0] * val_ratio):]
x_train_split = x_train_split[:-int(x_train_split.shape[0] * val_ratio)]
y_train_split = y_train_split[:-int(y_train_split.shape[0] * val_ratio)]

history = model.fit(
    x_train_split,
    y_train_split,
    batch_size=batch_size,
    epochs=epochs,
    validation_data=(x_val_split, y_val_split)
)
#モデルの評価
print(model.evaluate(x_train_split, y_train_split))
print(model.evaluate(x_val_split, y_val_split))
print(history.history['accuracy'])
print(history.history['val_accuracy'])
print(history.history['loss'])
print(history.history['val_loss'])
model.save("./myModels/num_model5")
"""
# x_train_sizes = []
# for ratio in ratios:
#     x_train_sizes.append(int(x_train_size * ratio))
# plt.plot(x_train_sizes,train_accuracies)
# plt.plot(x_train_sizes,val_accuracies)
# plt.grid()
# plt.xlabel('number of training samples')
# plt.ylabel('accuracy')
# plt.ylim([0.85, 1.01])
# #plt.xlim([0, x_train_size])

# plt.savefig('./training/fig_sample_curve.jpg')

# test_loss, test_acc = model.evaluate(x_test, y_test)

# file = open('./training/train_log.txt', 'a')

# file.write("\nbatchsize: {}, epoch: {}\n".format(batch_size, epochs))
# file.write("======================\n")
# file.write("TEST loss: {}\n".format(train_loss))
# file.write("TEST acc: {}\n".format(train_acc))
# file.write("======================\n")
# file.write("TEST loss: {}\n".format(test_loss))
# file.write("TEST acc: {}\n".format(test_acc))
# file.write("======================\n")

# csvFile = open('./training/trainLog.csv', 'a')
# writer = csv.writer(csvFile)
# writer.writerow(history.history['accuracy'])
# writer.writerow(history.history['val_accuracy'])
# writer.writerow(history.history['loss'])
# writer.writerow(history.history['val_loss'])

# plt.figure(figsize=(10,5))
# plt.subplot(1,2,1)
# plt.plot(history.history['accuracy'])
# plt.plot(history.history['val_accuracy'])
# plt.title('Model accuracy')
# plt.xlabel('epoch')
# plt.subplot(1,2,2)
# plt.plot(history.history['loss'])
# plt.plot(history.history['val_loss'])
# plt.title('Model loss')
# plt.xlabel('epoch')

# #plt.show()
# plt.savefig('./training/fig_b{}_e{}.jpg'.format(batch_size, epochs))

# model.save("./myModels/num_model4")