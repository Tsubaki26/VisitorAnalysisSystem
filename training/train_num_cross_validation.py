import tensorflow as tf
import pathlib
import matplotlib.pyplot as plt
from keras.applications.efficientnet_v2 import EfficientNetV2B0
from keras.applications.vgg16 import preprocess_input
from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping
from sklearn.model_selection import KFold, train_test_split
from sklearn.metrics import mean_absolute_error
import numpy as np
import pandas as pd

data_dir = pathlib.Path('./../images/num_images/')
print(len(list(data_dir.glob('*/*.png'))))  #学習データ数

img_height = 54
img_width = 32
random_seed = 123
validation_split = 0.2

BATCH_SIZE = 64
EPOCH = 10
b = np.array([0,1,3,4])
for i in b:
    print(i)
print('b', b)
'''画像とラベル取得，訓練・検証・テスト分割'''
#画像読み込み
image_dataset = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    image_size=(img_height,img_width),
    batch_size=BATCH_SIZE,
    shuffle=False
)

#クラス名を取得
class_names = image_dataset.class_names
print(class_names)

#画像データセットを画像(X)とラベル(Y)に各々配列化
img_X = []
img_Y = []
for img_ds_batch in list(image_dataset.as_numpy_iterator()):
    img_X.extend(img_ds_batch[0])
    img_Y.extend(img_ds_batch[1])

img_X = np.asarray(img_X)
img_Y = np.asarray(img_Y)

#画像の標準化
img_X = preprocess_input(img_X)

#データセットを train, test に分割
#train : test = 80 : 20
train_size = 0.8
test_size = 0.2

img_X_train, img_X_test, img_Y_train, img_Y_test = train_test_split(
    img_X, img_Y,
    train_size=train_size,
    random_state=random_seed,
    stratify=img_Y              #正解ラベルの割合を均一化
)
print(img_X_train.shape)



'''モデル構築'''
num_classes = len(class_names)

base_model = EfficientNetV2B0(input_shape=(img_height,img_width,3), weights='imagenet', include_top=False)
x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
output = tf.keras.layers.Dense(num_classes, activation='softmax')(x)
model = tf.keras.models.Model(inputs=[base_model.input], outputs=[output])

model.compile(
    optimizer='adam',
    loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

'''K-FOLD クロスバリデーション'''
FOLD = 5

train_sizes = []
val_loss_mean = []
val_loss_std = []
val_acc_mean = []
val_acc_std = []
train_loss_mean = []
train_loss_std = []
train_acc_mean = []
train_acc_std = []
test_loss_mean = []
test_acc_std = []

kf = KFold(n_splits=FOLD, shuffle=True, random_state=random_seed)
train_sizes = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
for train_size in train_sizes:
    print('train size: ', int(img_X_train.shape[0] * train_size))
    val_loss_scores = []
    val_acc_scores = []
    train_loss_scores = []
    train_acc_scores = []
    # train_score_mae = []
    # val_score_mae = []
    models = []

    img_X_train_split = img_X_train[:int(img_X_train.shape[0] * train_size)]
    img_Y_train_split = img_Y_train[:int(img_Y_train.shape[0] * train_size)]
    print(img_X_train_split.shape)
    print(img_Y_train_split.shape)
    generator = kf.split(img_X_train_split)
    # print(generator)
    # for i in generator:
    #     print(i)
    for fold, (train_indices, val_indices) in enumerate(generator):
        x_train, x_val = img_X_train_split[train_indices.tolist()], img_X_train_split[val_indices.tolist()]
        y_train, y_val = img_Y_train_split[train_indices.tolist()], img_Y_train_split[val_indices.tolist()]
        rlr = ReduceLROnPlateau(monitor='val_loss',
                            factor=0.1,
                            patience=3,
                            verbose=0,
                            min_delta=1e-4,
                            mode='max')
        ckp = ModelCheckpoint(f'model_{fold}.hdf5',
                                monitor='val_loss',
                                verbose=0,
                                save_best_only=True,
                                save_weights_only=True,
                                mode='max')
        es = EarlyStopping(monitor='val_loss',
                            min_delta=1e-4,
                            patience=7,
                            mode='max',
                            baseline=None,
                            restore_best_weights=True,
                            verbose=0)
        print("CCCCCC")
        history = model.fit(
            x_train, y_train,
            batch_size=BATCH_SIZE,
            epochs=EPOCH,
            validation_data=(x_val, y_val),
            callbacks=[rlr,ckp,es],
            verbose=0
        )

        train_loss, train_acc = model.evaluate(x_train, y_train)
        val_loss, val_acc = model.evaluate(x_val, y_val)

        #クロスバリデーション精度の保存
        train_acc_scores.append(train_acc)
        val_acc_scores.append(val_acc)
        #クロスバリデーション損失の保存
        train_acc_scores.append(train_acc)
        val_acc_scores.append(val_acc)

        # #平均絶対誤差
        # y_train_pred = model(x_train)
        # y_val_pred = model(x_val)
        # train_score_mae = mean_absolute_error(y_train, y_train_pred)
        # val_score_mae = mean_absolute_error(y_val, y_val_pred)
        # #MAEの保存
        # train_loss_scores.append(train_score_mae)
        # val_loss_scores.append(val_score_mae)

        models.append(model)

    #テストデータでの精度
    test_accs = []
    for model in models:
        test_loss, test_acc = model.evaluate(img_X_test, img_Y_test)
        test_accs.append(test_acc)

    #各精度・損失の平均と標準偏差を計算
    score_test_acc_mean = np.mean(test_accs)
    score_test_acc_std = np.std(test_accs)
    score_train_loss_mean = np.mean(train_loss_scores)
    score_train_loss_std = np.std(train_loss_scores)
    score_train_acc_mean = np.mean(train_acc_scores)
    score_train_acc_std = np.std(train_acc_scores)
    score_val_loss_mean = np.mean(val_loss_scores)
    score_val_loss_std = np.std(val_loss_scores)
    score_val_acc_mean = np.mean(val_acc_scores)
    score_val_acc_std = np.std(val_acc_scores)

    #学習データサイズ，精度・損失の平均と標準偏差を格納
    train_sizes.append(int(len(img_X_train) * train_size))
    val_loss_mean.append(score_val_loss_mean)
    val_loss_std.append(score_val_loss_std)
    val_acc_mean.append(score_val_acc_mean)
    val_acc_std.append(score_val_acc_std)
    train_loss_mean.append(score_train_loss_mean)
    train_loss_std.append(score_train_loss_std)
    train_acc_mean.append(score_train_acc_mean)
    train_acc_std.append(score_train_acc_std)
    test_loss_mean.append(score_test_acc_mean)
    test_acc_std.append(score_test_acc_std)


'''学習データをCSVファイルに保存'''
# データをDataFrameに変換
data = {
    'train_size': train_sizes,
    'val_loss_mean': val_loss_mean,
    'val_loss_std': val_loss_std,
    'val_acc_mean': val_acc_mean,
    'val_acc_std': val_acc_std,
    'train_loss_mean': train_loss_mean,
    'train_loss_std': train_loss_std,
    'train_acc_mean': train_acc_mean,
    'train_acc_std': train_acc_std,
    'test_loss_mean': test_loss_mean,
    'test_acc_std': test_acc_std,
}
df = pd.DataFrame(data)

# CSVファイルに保存
df.to_csv('./training_data.csv', index=False)


'''学習曲線の作成・保存'''
plt.style.use('seaborn-whitegrid')

# draw the training scores
plt.plot(train_sizes, train_acc_mean, color='orange', marker='o', markersize=5, label='training accuracy')
plt.fill_between(train_sizes, train_acc_mean + train_acc_std, train_acc_mean - train_acc_std, alpha=0.1, color='darkblue')

# draw the validation scores
plt.plot(train_sizes, val_acc_mean, color='darkblue', marker='o', markersize=5,label='validation accuracy')
plt.fill_between(train_sizes, val_acc_mean + val_acc_std,val_acc_mean - val_acc_std, alpha=0.1, color='orange')

plt.xlabel('#training samples')
plt.ylabel('accuracy')
plt.legend(loc='lower right')
plt.ylim([0.7, 1.01])
plt.savefig('./learning_curve_acc.jpg')

#figureをクリア
plt.clf()
#新しいfigureの作成
plt.figure()

plt.style.use('seaborn-whitegrid')

# draw the training scores
plt.plot(train_sizes, train_loss_mean, color='orange', marker='o', markersize=5, label='training accuracy')
plt.fill_between(train_sizes, train_loss_mean + train_loss_std, train_loss_mean - train_loss_std, alpha=0.1, color='darkblue')

# draw the validation scores
plt.plot(train_sizes, val_loss_mean, color='darkblue', marker='o', markersize=5,label='validation accuracy')
plt.fill_between(train_sizes, val_loss_mean + val_loss_std,val_loss_mean - val_loss_std, alpha=0.1, color='orange')

plt.xlabel('#training samples')
plt.ylabel('loss')
plt.legend(loc='lower right')
plt.savefig('./learning_curve_loss.jpg')