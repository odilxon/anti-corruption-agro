from models import *
from flask import *
app = Flask(__name__)
app.config['SECRET_KEY'] = 'internship'
import functools

Session = sessionmaker(bind=engine)
session = Session()

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
    filter_type = request.args.getlist('type')
    filter_keyword = request.args.get('keyword')
    filter_kaf = request.args.getlist('kafedra')
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
    data = data.all()
    # data = sorted(data, key=lambda kafedra: kafedra.name)
    return render_template('pages/index.html', data=data, type_list=type_list, selected_list=selected_list, kafedra_list=kafedra_list, kaf_selected_lis=kaf_selected_list)


session.close()