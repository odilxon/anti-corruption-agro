from models import *

u = User(
    username = "sber",
    password= "sber",
    token = "sber"
)
session.add(u)
session.commit()