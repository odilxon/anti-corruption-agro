from sqlalchemy.sql.type_api import INDEXABLE
from models import *
from flask import *
import jwt, requests
from functools import wraps
from datetime import datetime, time, timedelta
app = Flask(__name__)
app.config['SECRET_KEY'] = 'internship'

Session = sessionmaker(bind=engine)
session = Session()

@app.after_request
def after_request(response):
    header = response.headers
    header.add('Access-Control-Allow-Origin', '*')
    header.add('Access-Control-Allow-Headers', '*')
    header.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            print(token)
            
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            print(data)
            current_user = session.query(User)\
                .filter_by(id = data['public_id'])\
                .first()
        except Exception as E:
            return jsonify({
                'message' : str(E)
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated


@app.route("/api/login",methods=['POST'])
def login_a():
    
    username = request.form.get('username')
    password = request.form.get('password')
    print(request.form)
    try:
        session.rollback()
        user = session.query(User).filter(User.username==username).first()
    except:
        session.rollback()
        session.commit()
    if user:
        ch = user.check_password(password)
        if ch:
            token = jwt.encode({
                'public_id': user.id,
                'exp' : datetime.utcnow() + timedelta(days = 100)
                    }, app.config['SECRET_KEY'],algorithm="HS256")
            print(token)
            return jsonify({"token" : token,"msg": "ok"}),200
        return jsonify({"msg": "incorrect"}), 401
    return jsonify({"msg": "not found"}), 404
import hashlib
@app.route("/api/main", methods=['POST'])
@token_required
def api_main(c):
    
    form = request.form
    print(request.form)
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
            "first_name" : com.first_name,
            "username" : com.username,
            "date" : com.created_time.strftime("%Y-%m-%d  %H:%M:%S"),
            "avatar": hashlib.sha256(com.first_name.encode("utf-8")).hexdigest()
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
@app.route("/api/category", methods=['GET'])
@token_required
def api_cats(c):
    cts = session.query(Category).all()
    d = [x.format() for x in cts]
    return jsonify(d)

@app.route("/api/teachers", methods=['POST'])
def get_teacher():
    kaf_id = request.form.get("kaf_id")
    tchs = session.query(Teacher.id, Teacher.name)
    if kaf_id !='all':
            tchs = tchs.filter(Teacher.kafedra_id == int(kaf_id))
    tchs = tchs.order_by(Teacher.name.asc()).all()
    
    return jsonify([ [x, y] for x, y in tchs])
    
@app.route("/api/complain/<int:c_id>", methods=['GET'])
@token_required
def c_api(c,c_id):
    try:
        c = session.query(Complain).get(c_id)
    except:
        session.rollback()
        return jsonify({"msg": "not found"}), 404
    if c is None:
        session.rollback()
        return jsonify({"msg": "not found"}), 404
    com = c.format()
    complain_data = session.query(Complain_Data).filter(Complain_Data.complain_id==c_id).all()
    if c is None:
        abort(404)
    kafedra_name = ""
    teacher_name = ""
    for comp in complain_data:
        if comp.key == 'kafedra_id':
            kaf = session.query(Kafedra).filter(Kafedra.id==comp.value).first()
            kafedra_name = "" if kaf is None else kaf.name
        if comp.key == 'teacher_id':
            teach = session.query(Teacher).filter(Teacher.id==comp.value).first()
            teacher_name = "" if teach is None else teach.name
    c.created_time = datetime.strftime(c.created_time, "%Y-%m-%d")
    data = {}
    data['complain'] = com
    data['teacher_name'] = teacher_name
    data['kafedra_name'] = kafedra_name
    
    print(data)
    return jsonify(data)

@app.route("/api/related/<int:chat_id>", methods=['GET'])
@token_required
def api_related(c,chat_id):
    coms = session.query(Complain).filter(Complain.chat_id==chat_id).order_by(Complain.created_time.desc()).all()
    cc = []
    for com in coms:
        ca = "-"
        if com.category is not None:
            ca = com.category.name
        
        print([(x.key, x.value) for x in com.complain_data])
        C = {   
            "id" : com.id,
            "type" : com.type,
            "category" : ca,
            "first_name" : com.first_name,
            "username" : com.username,
            "date" : com.created_time.strftime("%Y-%m-%d  %H:%M:%S"),
            "avatar": hashlib.sha256(com.first_name.encode("utf-8")).hexdigest()
        }
        cc.append(C)
    return jsonify(cc)