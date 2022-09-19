from flask import Flask
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

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World'


@app.route('/model')
def tmp():
    clf = pickle.load(open('server_side/trained_model.pkl', 'rb'))
    
    return 'aaaaa'


if __name__ == "__main__":
    app.run(debug=True)
