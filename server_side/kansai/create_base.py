import csv
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

# for i in label:
#     for j in label_positions_var:
#         label_label.append(i+'_'+j)

print(label_label)
with open('dataset4.csv', 'w', newline="") as write_file:
    writer = csv.writer(write_file)
    writer.writerow(label_label)
