from PyNuitrack import py_nuitrack
import PyNuitrack
import sys
import cv2
from itertools import cycle
import numpy as np
import time
from collections import namedtuple
import pyrealsense2 as rs
import math
import tifffile
import csv
from traceback import print_exc
from pdb import set_trace
import datetime
from threading import Event, Thread
import os
import setproctitle
from flask import Flask, render_template, request, make_response, jsonify,g
import maesyori
import pandas as pd
import pickle
from collections import deque
import json

app = Flask(__name__)


# process name
setproctitle.setproctitle("m1_grandprix")
# Setting CSV limit
CSV_ROW_NUM = 150

skeleton_list=[]
skeleton_list_out=[]
event = Event()

eval_json = {
    "evals" :[
        0,20,40,60,80,100
    ]
}
# aiueo = 1111111110


# values = [0,20,40,60,80,100]
values = [0] * 50
evals = deque(values)

file = 'server_side/train_model/trained_model.pkl'
random_forest_model = pickle.load(open(file,'rb'))


def eval_skelton():
    global eval_json
    global evals
    print('ここまでのものを評価します')
    df = pd.read_csv(r"server_side/test_data/sample.csv")
    test_x = df.drop(['action_label'],axis=1)
    predict = random_forest_model.predict(test_x)
    evals.append(predict[0])
    evals.popleft()
    eval_json["evals"] = list(evals)
    # print("更新しました",eval_json)

    with open('server_side/tmp.txt', 'w') as f:
        for d in eval_json["evals"]:
            f.write("%s\n" % d)


def skeleton_save():
    global skeleton_list
    global skeleton_list_out

    while True:
        # ↓内部フラグの値がtrueになるまでブロックする
        event.wait()
        # ↓内部フラグをfalseにする
        event.clear()

        timestamp = datetime.datetime.now()
        # csv_dirname = "server_side/skelton_csv" + timestamp.strftime("%Y%m%d")
        csv_dirname = "server_side/skelton_csv"
        # if not os.path.exists(csv_dirname):
        #     os.makedirs(csv_dirname)
        csv_filename = timestamp.strftime("%Y%m%d_%H%M%S")
        # print("csv export ...", csv_dirname + "/rsdata_" + csv_filename + ".csv")
        # with open("{}/data_set.csv".format(csv_dirname, csv_filename), 'w') as file:
        #     w = csv.writer(file, lineterminator='\n')
        #     w.writerows(skeleton_list_out)
        df = pd.DataFrame(skeleton_list_out)
        # df = df.drop(df.columns[0],axis = 1)
        # df = df.drop(df.index[0],axis = 0)

        df.to_excel('server_side/skelton_csv/dataset.xlsx',index=False, header=False)

        maesyori.main()
        eval_skelton()
        print("aaaaaaaaaaaaa",eval_json)


def run():
    global skeleton_list
    global skeleton_list_out
    try:
        nuitrack = py_nuitrack.Nuitrack()
        nuitrack.init()

        # Change number of userID
        nuitrack.set_config_value("Skeletonization.ActiveUsers", "1")

        devices = nuitrack.get_device_list()
        for i, dev in enumerate(devices):
            print(dev.get_name(), dev.get_serial_number())
            if i == 0:
                dev.activate("") #you can activate device using python api
                print(dev.get_activation())
                nuitrack.set_device(dev)

        nuitrack.create_modules()
        nuitrack.run()

        modes = cycle(["depth", "color"])
        mode = next(modes)
        skeleton_list = []

        while True:
            key = cv2.waitKey(1)
            nuitrack.update()
            data = nuitrack.get_skeleton()
            data_instance = nuitrack.get_instance()
            img_depth = nuitrack.get_depth_data()
            if img_depth.size:
                cv2.normalize(img_depth, img_depth, 0, 255, cv2.NORM_MINMAX)
                img_depth = np.array(cv2.cvtColor(img_depth,cv2.COLOR_GRAY2RGB), dtype=np.uint8)
                img_color = nuitrack.get_color_data()
                point_color = (59, 164, 0)
                timestamp = datetime.datetime.now()

                for skel in data.skeletons:
                    id_ = skel.user_id
                    pre_skeleton_list = []

                    for el in skel[1:]:
                        x = (round(el.projection[0]), round(el.projection[1]))
                        xlabel = el.projection[0]
                        ylabel = el.projection[1]
                        zlabel = el.projection[2]
                        pre_skeleton_list += [xlabel, ylabel, zlabel]
                        cv2.circle(img_depth, x, 8, point_color, -1)

                    skeleton_list.append([timestamp, id_, *pre_skeleton_list])

                if len(skeleton_list) > CSV_ROW_NUM:
                    skeleton_list_out = skeleton_list.copy()
                    skeleton_list = []
                    # ↓内部フラグをtrueにする
                    event.set()
                if key == 32:
                    mode = next(modes)
                if mode == "depth":
                    cv2.imshow('Image', img_depth)
                if mode == "color":
                    if img_color.size:
                        cv2.imshow('Image', img_color)
            if key == 27:
                break
        nuitrack.release()

    except Exception as ex:
        print_exc()


@app.route('/')
def index():
    return 'Hello World'


@app.route('/model')
def tmp():
    with open('server_side/tmp.txt') as f:
        lines = f.readlines()

        lines = [line.rstrip('\n') for line in lines]
    global eval_json
    eval_json["evals"] = lines
    print("flaflaflask",eval_json)


    return make_response(jsonify(eval_json))
    # return json.dumps(eval_json_dash)
    # return jsonify({"language": "python"})



if __name__ == "__main__":
    t1 = Thread(target=run)
    t2 = Thread(target=skeleton_save)

    t1.start()
    t2.start()
    app.run(debug=True)
