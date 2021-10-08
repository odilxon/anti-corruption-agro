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
    data = session.query(Complain, Teacher, Kafedra)\
        .outerjoin(Teacher, Complain.teacher_id==Teacher.id)\
        .outerjoin(Kafedra, Kafedra.id==Teacher.kafedra_id)\
        .order_by(Complain.id.desc()).all()

    return render_template('pages/index.html', data=data)


session.close()