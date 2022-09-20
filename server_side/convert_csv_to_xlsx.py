import openpyxl
import csv
import pandas as pd

# data = pd.read_csv('using_smartphone/using_sma_1.csv')

# data.to_excel('excel.xlsx', encoding='utf-8')

csv_path = 'using_smartphone/using_sma_1.csv'
excel_path = 'test.xlsx'

wb = openpyxl.Workbook()
ws = wb.active

with open(csv_path) as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        ws.append(row)

wb.save(excel_path)
