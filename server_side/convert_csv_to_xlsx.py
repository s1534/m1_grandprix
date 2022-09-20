import openpyxl
import csv
import pandas as pd

csv_path = 'dataset.csv'
excel_path = 'sample.xlsx'

wb = openpyxl.Workbook()
ws = wb.active

with open(csv_path) as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        ws.append(row)

wb.save(excel_path)
