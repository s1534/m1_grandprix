from csv import writer
from nbformat import write
from pyparsing import NoMatch
import pathlib
from cv2 import norm
import pandas as pd
import openpyxl
import csv

def main():
    # create_base()
    # convert_csv_to_xlsx()
    # prepro()
    prepro2()
    print('学習モデル作成済み')

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

    with open('server_side/train_model/train_data.csv', 'w', newline="") as write_file:
        writer = csv.writer(write_file)
        writer.writerow(label_label)

# データセットをcsv→xlsxに変換
def convert_csv_to_xlsx():
    csv_path = 'server_side/data_set/dataset.csv'
    excel_path = 'server_side/data_set/dataset.xlsx'

    wb = openpyxl.Workbook()
    ws = wb.active

    with open(csv_path) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            ws.append(row)

    wb.save(excel_path)

def prepro2():
    path_dir = r"server_side/skelton_csv_100"
    ext_file = r"*.csv"
    list_path = list(pathlib.Path(path_dir).glob(ext_file))
    print(list_path)

    MAX_HEIGHT = 34

    for input_file_name in list_path:
        print(input_file_name)
        df = pd.read_csv(input_file_name)
        l_2d = df.values.tolist()
        normalize = []

        for i in l_2d:
            torso_cordinate = i[8:11]
            cordinates = i[2:]
            print(len(cordinates))
            for j in range(len(cordinates)):
                cordinates[j] -= torso_cordinate[j % 3]

            normalize.append(cordinates)

        print(len(normalize))
        # print(normalize[0])
        # return 0
        min_num = 0
        for k in range(int(len(l_2d)/MAX_HEIGHT)-1):
            normalize_dash = normalize[min_num:min_num+MAX_HEIGHT]
            min_num += MAX_HEIGHT

            print(len(normalize_dash))

            positions_avg = [sum(column)/len(normalize_dash)
                             for column in zip(*normalize_dash)]
            positions_var_max = [max(column) for column in zip(*normalize_dash)]
            positions_var_min = [min(column)
                                 for column in zip(*normalize_dash)]

            # print(positions_var_max - positions_var_min)
            positions_var = []
            for i in range(len(positions_var_min)):
                positions_var.append(positions_var_max[i] - positions_var_min[i])

            diff_x = 0
            diff_y = 0
            diff_z = 0

            distance_diff = [0]*60
            cordinate_sum = [0]*60
            cordinate_avg = [0]*60

            ans = 0

            for i in range(len(normalize_dash)-1):
                for j in range(0, len(normalize_dash[i]), 3):
                    cordinate_sum[j] += normalize_dash[i][j]
                    cordinate_sum[j+1] += normalize_dash[i][j+1]
                    cordinate_sum[j+2] += normalize_dash[i][j+2]

                    distance_diff[j] += abs(normalize_dash[i][j] - normalize_dash[i+1][j])
                    distance_diff[j+1] += abs(normalize_dash[i]
                                            [j+1] - normalize_dash[i+1][j+1])
                    distance_diff[j+2] += abs(normalize_dash[i]
                                              [j+2] - normalize_dash[i+1][j+2])

            for i in range(len(cordinate_sum)):
                cordinate_avg[i] = cordinate_sum[i]/len(normalize_dash)
            write_row = []
            write_rows = write_row+['100']+distance_diff+positions_avg

            # Pre-requisite - The CSV file should be manually closed before running this code.

            # First, open the old CSV file in append mode, hence mentioned as 'a'
            # Then, for the CSV file, create a file object
            with open('server_side/train_model/train_data.csv', 'a', newline='') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(write_rows)
                f_object.close()

    # データセットの前処理を行う
def prepro():
    path_dir = r"server_side/skelton_csv_100"
    ext_file = r"*.xlsx"
    list_path = list(pathlib.Path(path_dir).glob(ext_file))

    kakunin = []
    refer_list = []

    for input_file_name in list_path:


        df = pd.read_excel(input_file_name, index_col=0)

        l_2d = df.values.tolist()
        print(l_2d)
        normalize = []
        for i in l_2d:
            # print(i)
            torso_cordinate = i[7:10]
            cordinates = i[1:]
            for j in range(len(cordinates)):
                cordinates[j] -= torso_cordinate[j % 3]

            normalize.append(cordinates)


        normalize = normalize[:150]
        print(len(normalize))

        positions_avg = [sum(column)/len(normalize) for column in zip(*normalize)]
        positions_var_max = [max(column) for column in zip(*normalize)]
        positions_var_min = [min(column) for column in zip(*normalize)]

        # print(positions_var_max - positions_var_min)
        positions_var = []
        for i in range(len(positions_var_min)):
            positions_var.append(positions_var_max[i] - positions_var_min[i])
        print(len(normalize[0]))
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
        write_rows = write_row+['100']+distance_diff+positions_avg

        # Pre-requisite - The CSV file should be manually closed before running this code.

        # First, open the old CSV file in append mode, hence mentioned as 'a'
        # Then, for the CSV file, create a file object
        with open('server_side/train_model/train_data.csv', 'w', newline='') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(write_rows)
            f_object.close()

if __name__ == "__main__":
    main()
