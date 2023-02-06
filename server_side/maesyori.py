from csv import writer
from nbformat import write
from pyparsing import NoMatch
import pathlib
from cv2 import norm
import pandas as pd
import openpyxl
import csv

def main():
    create_base()
    prepro()
    print('テストデータ作成完了')

def create_base():
    label = ['head',
            'neck',
            'torso',
            'waist',
            'left_collar',
            'left_shoulder',
            'left_elbow',
            'left_wrist',
            'left_hand',
            'right_collar',
            'right_shoulder',
            'right_elbow',
            'right_wrist',
            'right_hand',
            'left_hip',
            'left_knee',
            'left_ankle',
            'right_hip',
            'right_knee',
            'right_ankle']

    label_positions = [
        'x', 'y', 'z'
    ]
    label_positions_diff = ['diff_x', 'diff_y', 'diff_z']
    label_positions_var = ['var_x', 'var_y', 'var_z']
    label_label = ['action_label']

    for i in label:
        for j in label_positions:
            label_label.append(i+'_'+j)
    for i in label:
        for j in label_positions_diff:
            label_label.append(i+'_'+j)

    with open('server_side/test_data/sample.csv', 'w', newline="") as write_file:
        writer = csv.writer(write_file)
        writer.writerow(label_label)

# データセットの前処理を行う
def prepro():

    path_dir = r"server_side/skelton_csv"
    ext_file = r"*.xlsx"
    list_path = list(pathlib.Path(path_dir).glob(ext_file))

    kakunin = []
    refer_list = []


    for input_file_name in list_path:

        df = pd.read_excel(input_file_name, index_col=0)

        l_2d = df.values.tolist()
        normalize = []
        for i in l_2d:
            # print(i)
            torso_cordinate = i[7:10]
            cordinates = i[1:]
            for j in range(len(cordinates)):
                cordinates[j] -= torso_cordinate[j % 3]

            normalize.append(cordinates)

        # print(len(normalize))

        positions_avg = [sum(column)/len(normalize) for column in zip(*normalize)]
        positions_var_max = [max(column) for column in zip(*normalize)]
        positions_var_min = [min(column) for column in zip(*normalize)]

        # print(positions_var_max - positions_var_min)
        positions_var = []
        for i in range(len(positions_var_min)):
            positions_var.append(positions_var_max[i] - positions_var_min[i])
        # print(positions_var)

        diff_x = 0
        diff_y = 0
        diff_z = 0

        distance_diff = [0]*60
        cordinate_sum = [0]*60
        cordinate_avg = [0]*60

        ans = 0

        kakunin.append(len(normalize))

        for i in range(len(normalize)-1):
            for j in range(0, len(normalize[i]), 3):
                cordinate_sum[j] += normalize[i][j]
                cordinate_sum[j+1] += normalize[i][j+1]
                cordinate_sum[j+2] += normalize[i][j+2]

                distance_diff[j] += abs(normalize[i][j] - normalize[i+1][j])
                distance_diff[j+1] += abs(normalize[i][j+1] - normalize[i+1][j+1])
                distance_diff[j+2] += abs(normalize[i][j+2] - normalize[i+1][j+2])

        for i in range(len(cordinate_sum)):
            cordinate_avg[i] = cordinate_sum[i]/len(normalize)
        write_row = []
        write_rows = write_row+['test_data']+distance_diff+positions_avg

        # Pre-requisite - The CSV file should be manually closed before running this code.

        # First, open the old CSV file in append mode, hence mentioned as 'a'
        # Then, for the CSV file, create a file object
        with open('server_side/test_data/sample.csv', 'a', newline='') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(write_rows)
            f_object.close()

if __name__ == "__main__":
    main()
