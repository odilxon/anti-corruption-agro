import telebot

from models import *
TOKEN = "1258084373:AAFnxvjZ67Gx4iMROrCtyk21h981G-4xJWE"
bot = telebot.TeleBot(TOKEN, parse_mode=None)




def gen_kafedra_inline():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 1
    kfds = session.query(Kafedra).all()
    kfds = sorted(kfds, key=lambda kaf: kaf.name)
    f = []
    for kf in kfds:
        f.append(telebot.types.InlineKeyboardButton(kf.name, callback_data="k_" + str(kf.id)))
    f.append(telebot.types.InlineKeyboardButton("❎ Ортга қайтиш", callback_data="k_0"))
    markup.add(*f)
    return markup

def gen_teacher_inline(k_id):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 1
    teachers = session.query(Teacher).filter(Teacher.kafedra_id==k_id).all()
    teachers = sorted(teachers, key=lambda teacher: teacher.name)
    ins = []
    for teach in teachers:
        ins.append(telebot.types.InlineKeyboardButton(teach.name, callback_data="t_" + str(teach.id)))
    ins.append(telebot.types.InlineKeyboardButton("❎ Ортга қайтиш", callback_data="t_0"))
    markup.add(*ins)
    return markup

def gen_type_complain():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(telebot.types.InlineKeyboardButton("Таклиф", callback_data="type_positive"),
    telebot.types.InlineKeyboardButton("Шикоят", callback_data="type_negative"))
    return markup
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    ss = session.query(Session).filter(Session.chat_id==chat_id).first()
    if "type_" in call.data:
        _type = call.data
        _type = _type.replace("type_", "")
        ss.type = _type
        if _type == "positive":
            t = "Таклиф"
        else:
            t = "Шикоят"
        bot.edit_message_text("Мурожат тури: " + t, call.message.chat.id,call.message.id,reply_markup=None)
        if _type == "negative":
            bot.send_message(call.message.chat.id, "Кафедрани танланг:", reply_markup=gen_kafedra_inline())
        else:
            bot.send_message(call.message.chat.id, "Таклиф матнини киритинг")
            ss.step = "text"
        session.commit()
        
    if "k_" in call.data:
        k_id = int(call.data.replace("k_", ""))
        if k_id == 0:
            bot.send_message(call.message.chat.id, "Ассалому алайкум. Таклиф ва шикоятларингизни аноним холда қолдиришингиз мумкин:", reply_markup=gen_type_complain())
            bot.delete_message(call.message.chat.id,call.message.id)
        else:
            k = session.query(Kafedra).get(k_id).name
            bot.edit_message_text("Кафедра: " + k, call.message.chat.id,call.message.id,reply_markup=None)
            bot.send_message(call.message.chat.id, "Ўқитувчини танланг:", reply_markup=gen_teacher_inline(k_id))
            ss.step = "teacher"
            ss.kafedra_id = k_id
            session.commit()
        
    if "t_" in call.data:
        t_id = int(call.data.replace("t_", ""))
        if t_id == 0:
            bot.send_message(call.message.chat.id, "Кафедрани танланг:", reply_markup=gen_kafedra_inline())
            bot.delete_message(call.message.chat.id,call.message.id)
        else:
            t = session.query(Teacher).get(t_id).name
            bot.edit_message_text("Ўқитувчи: " + t, call.message.chat.id,call.message.id,reply_markup=None)
            bot.send_message(call.message.chat.id, "Шикоят матнини киритинг")
            ss.step = "text"
            ss.teacher_id = t_id
            session.commit()
            
    
    #bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=None)



@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    session.query(Session).filter(Session.chat_id == chat_id).delete()
    session.commit()
    s = Session(
        chat_id = chat_id,
        first_name = first_name,
        username = username,
        step="kafedra"
    )
    session.add(s)
    session.commit()

    bot.reply_to(message, "Ассалому алайкум. Таклиф ва шикоятларингизни аноним холда қолдиришингиз мумкин:", reply_markup=gen_type_complain())
@bot.message_handler(func=lambda message: True)
def get_msg(message):
    chat_id = message.chat.id
    ss = session.query(Session).filter(Session.chat_id==chat_id).first()
    if ss.step == "text":
        text = message.text
        co = Complain(
            message=text,
            teacher_id=ss.teacher_id,
            first_name = ss.first_name,
            username = ss.username,
            type = ss.type,
            chat_id = chat_id
        )
        session.add(co)
        session.commit()
        bot.send_message(chat_id,"Сизнинг мурожатингиз қабул қилинди, сизнинг шахсингиз махфийлигича қолади")
    else:
        bot.send_message(chat_id, "Шикоят юбориш учун /start")

    


if __name__ == "__main__":
    bot.infinity_polling()
    session.close()