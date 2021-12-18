from sqlalchemy.sql.type_api import INDEXABLE
from models import *
from flask import *
app = Flask(__name__)
app.config['SECRET_KEY'] = 'internship'

Session = sessionmaker(bind=engine)
session = Session()


@app.route("/api/main", methods=['POST'])
def api_main():
    
    form = request.form

    _type = form.get("type")
    category = form.get("category")
    s_date = form.get("s_date")
    e_date = form.get("e_date")
    kaf = form.get("kaf")
    teacher = form.get("teacher")
    
    query = session.query(Complain)
    if _type != "all":
        query = query.filter(Complain.type == _type)
    if category != "all":
        query = query.filter(Complain.category_id == category)
    if s_date and e_date:
        filter_start_date = datetime.strptime(s_date, "%Y-%m-%d")
        filter_end_date = datetime.strptime(e_date, "%Y-%m-%d")
        query = query.filter(Complain.created_time.between(filter_start_date,filter_end_date))
    elif s_date and not e_date:
        filter_start_date = datetime.strptime(s_date, "%Y-%m-%d")
        filter_end_date = datetime.now()
        query = query.filter(Complain.created_time.between(filter_start_date,filter_end_date))
    elif not s_date and e_date:
        filter_start_date = datetime.strptime(session.query(Complain).order_by(Complain.id.asc()).first().created_time, "%Y-%m-%d")
        filter_end_date = datetime.strptime(e_date, "%Y-%m-%d")
        query = query.filter(Complain.created_time.between(filter_start_date,filter_end_date))
    coms = query.all()
    
    
    # if kaf != 'all':
    #     kafef = Kafedra.query.filter(Kafedra.id==kaf).first()
    # if teacher != 'all':
    #     teacherf = Complain_Data.query.filter(Complain_Data.key=='teacher_id', Complain_Data.value==teacher).first()
    cc = []
    print(kaf)
    print(teacher)
    for com in coms:
        ca = "-"
        if com.category is not None:
            ca = com.category.name
        
        print([(x.key, x.value) for x in com.complain_data])
        C = {   
            "id" : com.id,
            "type" : com.type,
            "category" : ca,
            "date" : com.created_time.strftime("%Y-%m-%d  %H:%M:%S")
        }
        if category != 'all' and int(category) == 2:
            if teacher != 'all':
                if teacher in [x.value for x in com.complain_data if x.key =='teacher_id']:
                    cc.append(C)
                continue
            elif kaf != 'all':
                if kaf in [x.value for x in com.complain_data if x.key =='kafedra_id']:
                    cc.append(C)
                continue
            else:
                cc.append(C)
                continue
        else:
            cc.append(C)
    return jsonify(cc)

@app.route("/api/teachers", methods=['POST'])
def get_teacher():
    kaf_id = request.form.get("kaf_id")
    tchs = session.query(Teacher.id, Teacher.name)
    if kaf_id !='all':
            tchs = tchs.filter(Teacher.kafedra_id == int(kaf_id))
    tchs = tchs.order_by(Teacher.name.asc()).all()
    
    return jsonify([ [x, y] for x, y in tchs])
    