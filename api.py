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
    
    query = session.query(Complain)
    if _type != "all":
        query = query.filter(Complain.type == _type)
    if category != "all":
        query = query.filter(Complain.category_id == category)
    
    coms = query.all()
    cc = []
    for com in coms:
        ca = "-"
        if com.category is not None:
            ca = com.category.name
        
        C = {
            "id" : com.id,
            "type" : com.type,
            "category" : ca,
            "date" : com.created_time.strftime("%Y-%m-%d  %H:%M:%S")
        }
        cc.append(C)
    print(cc)
    return jsonify(cc)