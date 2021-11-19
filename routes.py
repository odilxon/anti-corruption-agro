from datetime import datetime
from api import *
import functools



def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)

    return secure_function

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    return render_template('pages/login.html')

@app.route('/', methods=['GET'])
def index_page():
    return redirect(url_for('main_app'))
    filter_type = request.args.getlist('type')
    filter_keyword = request.args.get('keyword')
    filter_kaf = request.args.getlist('kafedra')
    filter_start_date = request.args.get('start_date')
    filter_end_date = request.args.get('end_date')
    kafedra_list = [(i.name, i.id) for i in session.query(Kafedra).all()]
    type_list = [('negative', "Shikoyat"), ('warning', 'Etiroz'), ('positive', "Taklif")]
    selected_list = filter_type
    kaf_selected_list = filter_kaf
    print(kaf_selected_list)
    data = session.query(Complain, Teacher, Kafedra)\
        .outerjoin(Teacher, Complain.teacher_id==Teacher.id)\
        .outerjoin(Kafedra, Kafedra.id==Teacher.kafedra_id)\
        .order_by(Complain.id.desc())
    if filter_type and 'all' not in filter_type:
        data = data.filter(Complain.type.in_(filter_type))
    if filter_keyword:
        data = data.filter(or_(Complain.first_name.ilike('%' + str(filter_keyword.lower()) + '%'), Complain.username.ilike('%' + str(filter_keyword.lower()) + '%')))
    if filter_kaf and 'all' not in filter_kaf:
        data = data.filter(Kafedra.id.in_(filter_kaf))
    if filter_start_date and filter_end_date:
        filter_start_date = datetime.strptime(filter_start_date, "%Y-%m-%d")
        filter_end_date = datetime.strptime(filter_end_date, "%Y-%m-%d")
        data = data.filter(Complain.created_time.between(filter_start_date,filter_end_date))
    data = data.all()
    # data = sorted(data, key=lambda kafedra: kafedra.name)
    return render_template('pages/index.html', \
    data=data, type_list=type_list, \
    selected_list=selected_list, kafedra_list=kafedra_list, \
    kaf_selected_lis=kaf_selected_list, \
    filter_keyword=filter_keyword, \
    )


    

@app.route("/main", methods=['GET', "POST"])
def main_app():
    categories = session.query(Category).all() 
    kafedra = session.query(Kafedra).all()
    kafedra = sorted(kafedra, key=lambda kaf: kaf.name)
    data = {
        "cats" : categories,
        "kafedra" : kafedra
    }
    return render_template("pages/list.html", data=data)

@app.route("/complain/<int:c_id>")
def comp_i(c_id):
    c = session.query(Complain).get(c_id)
    complain_data = session.query(Complain_Data).filter(Complain_Data.complain_id==c_id).all()
    if c is None:
        abort(404)
    for comp in complain_data:
        if comp.key == 'kafedra_id':
            comp.value = Kafedra.query.filter_by(id=comp.value).first()
        if comp.key == 'teacher_id':
            comp.value = Teacher.query.filter_by(id=comp.value).first()

    data = {}
    data['complain'] = c
    data['complain_data'] = complain_data # there array
    print([(x.key, x.value) for x in complain_data])
    return render_template("pages/complain.html", data=data)
session.close()