from pandas.plotting import scatter_matrix
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
import seaborn as sns
from sklearn.metrics import classification_report

import pandas as pd  # pandasのインポート
import datetime  # 元データの日付処理のためにインポート
from sklearn.model_selection import train_test_split  # データ分割用
from sklearn.ensemble import RandomForestClassifier  # ランダムフォレスト
from sklearn.metrics import f1_score
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import japanize_matplotlib
import pickle


df = pd.read_csv(r"dataset.csv")
# df = pd.read_csv(r"micro_train_data/walking/write_test.csv")

# print(df.shape)
# print(df.head())

# df['deadline'] = pd.to_datetime(df["deadline"])
# df["launched"] = pd.to_datetime(df["launched"])
# df["days"] = (df["deadline"] - df["launched"]).dt.days
# df = df[(df["state"] == "successful") | (df["state"] == "failed")]

df["action_label"] = df["action_label"].replace("walking", 0)
df["action_label"] = df["action_label"].replace("standing", 1)
df["action_label"] = df["action_label"].replace("sitting", 2)
df["action_label"] = df["action_label"].replace("holding_smartphone", 3)
df["action_label"] = df["action_label"].replace("using_smartphone", 4)

# print(df.head())

df_walking = df.loc[df["action_label"] == 0]
df_standing = df.loc[df["action_label"] == 1]
df_sitting = df.loc[df["action_label"] == 2]
df_holding_smartphone = df.loc[df["action_label"] == 3]
df_using_smartphone = df.loc[df["action_label"] == 4]


train_x = df.drop(['action_label'], axis=1)
train_y = df['action_label']
(train_x, test_x, train_y, test_y) = train_test_split(
    train_x, train_y, test_size=0.3, random_state=42, shuffle=False)

print('=============最初=======================')
print(train_x.head())
print(train_y.head())

# 機械学習のモデルを作成するトレーニング用と評価用の2種類に分割する
train_x_walking = df_walking.drop(['action_label'], axis=1)  # 説明変数のみにする
train_y_walking = df_walking['action_label']  # 正解クラス
(train_x_walking, test_x_walking, train_y_walking, test_y_walking) = train_test_split(
    train_x_walking, train_y_walking, test_size=0.3, random_state=42, shuffle=False)

train_x_standing = df_standing.drop(['action_label'], axis=1)  # 説明変数のみにする
train_y_standing = df_standing['action_label']  # 正解クラス
(train_x_standing, test_x_standing, train_y_standing, test_y_standing) = train_test_split(
    train_x_standing, train_y_standing, test_size=0.3, random_state=42, shuffle=False)

train_x_sitting = df_sitting.drop(['action_label'], axis=1)  # 説明変数のみにする
train_y_sitting = df_sitting['action_label']  # 正解クラス
(train_x_sitting, test_x_sitting, train_y_sitting, test_y_sitting) = train_test_split(
    train_x_sitting, train_y_sitting, test_size=0.3, random_state=42, shuffle=False)

train_x_holding_smartphone = df_holding_smartphone.drop(
    ['action_label'], axis=1)  # 説明変数のみにする
train_y_holding_smartphone = df_holding_smartphone['action_label']  # 正解クラス
(train_x_holding_smartphone, test_x_holding_smartphone, train_y_holding_smartphone, test_y_holding_smartphone) = train_test_split(
    train_x_holding_smartphone, train_y_holding_smartphone, test_size=0.3, random_state=42, shuffle=False)

train_x_using_smartphone = df_using_smartphone.drop(
    ['action_label'], axis=1)  # 説明変数のみにする
train_y_using_smartphone = df_using_smartphone['action_label']  # 正解クラス
(train_x_using_smartphone, test_x_using_smartphone, train_y_using_smartphone, test_y_using_smartphone) = train_test_split(
    train_x_using_smartphone, train_y_using_smartphone, test_size=0.3, random_state=42, shuffle=False)
# 訓練用の説明変数と正解クラス、評価用の説明変数と正解クラスに分割

train_x = pd.concat([train_x_holding_smartphone, train_x_sitting,
                    train_x_standing, train_x_using_smartphone, train_x_walking])
train_y = pd.concat([train_y_holding_smartphone, train_y_sitting,
                    train_y_standing, train_y_using_smartphone, train_y_walking])
test_x = pd.concat([test_x_holding_smartphone, test_x_sitting,
                    test_x_standing, test_x_using_smartphone, test_x_walking])
test_y = pd.concat([test_y_holding_smartphone, test_y_sitting,
                    test_y_standing, test_y_using_smartphone, test_y_walking])

print('==============最後=======================')
# print(train_x.head())
# print(train_y.head())

# 識別モデルの構築
random_forest = RandomForestClassifier(
    max_depth=10, n_estimators=30, random_state=42)
random_forest.fit(train_x, train_y)

file = 'trained_model.pkl'
pickle.dump(random_forest, open(file, 'wb'))

# clf = pickle.load(open('trained_model.pkl', 'rb'))


# モデルを作成する段階でのモデルの識別精度
trainaccuracy_random_forest = random_forest.score(train_x, train_y)
print('TrainAccuracy: {}'.format(trainaccuracy_random_forest))


# 予測値算出
y_pred = random_forest.predict(test_x)

# 作成したモデルに学習に使用していない評価用のデータセットを入力し精度を確認
accuracy_random_forest = accuracy_score(test_y, y_pred)
print('Accuracy: {}'.format(accuracy_random_forest))


mat = confusion_matrix(test_y, y_pred)
print(mat)
# df_tmp = pd.DataFrame(data=mat)
df_tmp = pd.DataFrame(data=mat, index=['walk', 'stand', 'sit', 'take out', 'use'], columns=[
                      'walk', 'stand', 'sit', 'take out', 'use'])
sns.set(font_scale=1)
sns.heatmap(df_tmp, square=True, annot=True, cbar=True,
            fmt='d', cmap='Blues')
plt.xlabel("Prediction")
plt.ylabel("Ground Truth")
# plt.show()
# plt.savefig('seaborn_heatmap_dataframe.png')
print(classification_report(test_y, y_pred))
