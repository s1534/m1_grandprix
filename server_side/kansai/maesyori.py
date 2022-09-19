from csv import writer
from nbformat import write
from pyparsing import NoMatch
import pathlib
from cv2 import norm
import pandas as pd

path_dir = r"micro_activity_dataset_kai/sitting"
ext_file = r"*.xlsx"
list_path = list(pathlib.Path(path_dir).glob(ext_file))

kakunin = []
refer_list = []


for input_file_name in list_path:
    # print(i)

    # input file name
    # input_file_name = 'micro_activity_dataset/walking/walking_3.xlsx'
    # input_file_name = 'micro_activity_dataset/walking/walking_3.xlsx'
    df = pd.read_excel(input_file_name, index_col=0)
    # print(df)

    l_2d = df.values.tolist()
    normalize = []
    for i in l_2d:
        # print(i)
        torso_cordinate = i[7:10]
        cordinates = i[1:]
        for j in range(len(cordinates)):
            cordinates[j] -= torso_cordinate[j % 3]

        normalize.append(cordinates)
    # print(syorigo)

    # print(len(normalize))

    normalize = normalize[:34]
    print(len(normalize))

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
    write_rows = write_row+['walking']+distance_diff+positions_avg

    # Pre-requisite - The CSV file should be manually closed before running this code.

    # First, open the old CSV file in append mode, hence mentioned as 'a'
    # Then, for the CSV file, create a file object
    with open('dataset.csv', 'a', newline='') as f_object:
        # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(write_rows)
        # Close the file object
        f_object.close()
    print(len(normalize))
