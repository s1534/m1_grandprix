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


df = pd.read_csv(r"server_side/train_model/train_data.csv")

df["action_label"] = df["action_label"].replace("0", 0)
df["action_label"] = df["action_label"].replace("20", 1)
df["action_label"] = df["action_label"].replace("40", 2)
df["action_label"] = df["action_label"].replace("60", 3)
df["action_label"] = df["action_label"].replace("80", 4)
df["action_label"] = df["action_label"].replace("100", 5)

train_x = df.drop(['action_label'], axis=1)
train_y = df['action_label']


# 識別モデルの構築
random_forest = RandomForestClassifier(
    max_depth=10, n_estimators=30, random_state=42)
random_forest.fit(train_x, train_y)

file = 'trained_model.pkl'
pickle.dump(random_forest, open(file, 'wb'))

# clf = pickle.load(open('trained_model.pkl', 'rb'))


# モデルを作成する段階でのモデルの識別精度
# trainaccuracy_random_forest = random_forest.score(train_x, train_y)
# print('TrainAccuracy: {}'.format(trainaccuracy_random_forest))


# # 予測値算出
# y_pred = random_forest.predict(test_x)

# # 作成したモデルに学習に使用していない評価用のデータセットを入力し精度を確認
# accuracy_random_forest = accuracy_score(test_y, y_pred)
# print('Accuracy: {}'.format(accuracy_random_forest))

