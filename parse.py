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
    if kafa[0] == " ":
        kafa = kafa[1::]
    # if kafa not in completed_json:
    #     completed_json.append(kafa)
    if not session.query(Kafedra).filter_by(name=kafa).first():
        kaf = Kafedra(name=kafa)
        session.add(kaf)
def parse_kaf_teach():
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
        if kafa[0] == " ":
            kafa = kafa[1::]
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

def write_kategory():
    cats = ['Ошхона', 'Ўқитувчи', 'TTJ (Ётоқхона)', 'Ҳожатхона']
    for cat in cats:
        f = Category(
            name=cat
        )
        session.add(f)
        session.commit()
    

# parse_kaf_teach()
# write_kategory()
session.close()
with open('kafedra.json', 'w', encoding='utf-8') as outfile:
    outfile.write(json.dumps(completed_json, ensure_ascii=False, indent=4))
    outfile.close()

# with open('padrabnee.json', 'w', encoding='utf-8') as outfile:
#     outfile.write(json.dumps(completed_json, ensure_ascii=False, indent=4))
#     outfile.close()

