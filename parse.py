from models import *
import pandas as pd
from pandas.core.frame import DataFrame
import json

# data = pd.read_excel(r'C:\Projects\refrigerator_py\assets\tash_ref.xlsx', usecols='B:O', header=5, nrows=22)
data = pd.read_excel("info.xls", 'TDAU', header=4)
completed_json = []
jsonf = {}
data = data.fillna("Yo`q")
# with open("data.json", "r", encoding='utf-8') as file:
#     datafromjson = json.load(file)
for index, row_data in data.iterrows():
    jsonf['kafedra'] = row_data[0]
    jsonf['name'] = row_data[3]
    completed_json.append(jsonf)
    # datafromjson.append(jsonf)
    jsonf = {}
    # print(row_data)
with open('padrabnee.json', 'w', encoding='utf-8') as outfile:
    outfile.write(json.dumps(completed_json, ensure_ascii=False, indent=4))
    outfile.close()

