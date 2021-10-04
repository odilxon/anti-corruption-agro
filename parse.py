from models import *
import pandas as pd
from pandas.core.frame import DataFrame
import json

data = pd.read_excel("info.xls", 'TDAU', usecols ="A,D")
completed_json = []
jsonf = {}
data = data.fillna("Yo`q")
for index, row_data in data.iterrows():
    if "Yo`q" in list(row_data):
        continue
    kaf = row_data[0]
    for i in kaf:
        if i.isdigit():
            kaf = kaf.replace(i,"")
    kafa = kaf.replace(". ", "")
    kafa = kaf.replace(".", "")
    if not session.query(Kafedra).filter_by(name=kafa).first():
        kaf = Kafedra(name=kafa)
        session.add(kaf)
        session.commit()
        
    teacher = row_data[1]
    for i in teacher:
        if i.isdigit():
            teacher = teacher.replace(i,"")
    teacher = teacher.replace(", ","")
    teach = Teacher(name=teacher, kafedra_id=session.query(Kafedra).filter_by(name=kafa).first().id)
    session.add(teach)
    session.commit()
session.close()
# with open('padrabnee.json', 'w', encoding='utf-8') as outfile:
#     outfile.write(json.dumps(completed_json, ensure_ascii=False, indent=4))
#     outfile.close()

