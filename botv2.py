import telebot

from models import *
TOKEN = "2042929004:AAEgJShr8Ju6mTr-1ekczXkqP5qcVwaSNxA"
bot = telebot.TeleBot(TOKEN, parse_mode=None)

'''
|------------------------------------------------------|
|           this is steps ----                         |
|                            |                         |
|                            |                         |
|                           \ /                        |
|                            ^                         |
|   start -> category -> if(cat == 'oqituvchi') |      |
|   |>  kafedra -> oqituvchi <| ->                     |
|   -> type -> while(stop) -> accepting data from user |
|------------------------------------------------------|

We have to write code below 
We will use only inline buttons group

What? D
Смотри здесь я написал этапы

по рисунку будем правую часть делать
c_
категории динамично с базы
если там учителей выбрали
для учителей есть база
там кафедры в табле есть потом по ID кафедры есть училтеля таблица


с отдельными таблицами?
!!!!!!!!!!!!!!!!!!!!!!!!!11
этироз warning таклиф success шикоят danger
для сохранение одна таблица пройдика в models
'''
user_data = {
    "chat_id":{
        "text": "",
        "img": "",
        "video": "",
        "audio": ""
        }
}


type_keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

type_warning = telebot.types.InlineKeyboardButton("Этироз",callback_data = "warning")
type_success = telebot.types.InlineKeyboardButton(
    "Таклиф", callback_data="success")
type_danger = telebot.types.InlineKeyboardButton(
    "Шикоят", callback_data="danger")
type_keyboard.add(type_warning,type_success,type_danger)


def gen_model_markup(Item, is_teachers=False, kaf_id=0) -> list[telebot.types.InlineKeyboardButton]:
    """[Generates Markup Inline keyboards by given Model]

    Args:
        Item ([DB Model]): ORM Model
        is_teachers (bool, optional): If is_teachers given, you should give kaf_id to load teachers by kafedra id. Defaults to False.
        kaf_id (int, optional): if give kaf_id, it filter teachers by kafedra_id. Defaults to 0.

    Returns:
        list[Inline Keyboards]: Returns Inline Keyboards in array by given Model
    """    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 1
    items = session.query(Item)
    if is_teachers:
        items = items.filter(Item.kafedra_id==kaf_id)
    items = sorted(items.all(), key=lambda item: item.name)
    cb_pref = str(Item.__tablename__)+"_"
    ins = [telebot.types.InlineKeyboardButton(item.name, callback_data=cb_pref + str(item.id)) for item in items]
    if Item.__tablename__ != "category":
        ins.append(telebot.types.InlineKeyboardButton("❎ Ортга қайтиш", callback_data=cb_pref + "0"))
    markup.add(*ins)
    return markup

def Set_Session(user_id,next_step) -> bool:
    s = session.query(Session).filter()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    s = session.query(Session).filter_by(chat_id=message.chat.id).delete()
    session.commit()
    s = Session(
        chat_id = message.chat.id,
        first_name = message.from_user.first_name,
        step = "category",
        username = message.from_user.username
    )
    bot.reply_to(message, "Ассалому алайкум. Таклиф ва шикоятларингизни аноним холда қолдиришингиз мумкин, категорияни танланг:",
        reply_markup=gen_model_markup(Category))
    
    session.add(s)
    session.commit()
    

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    
    chat_id = call.message.chat.id
    ss = session.query(Session).filter(Session.chat_id == chat_id).first()
    
    if "category_" in call.data:
        category_id = call.data.replace("category_","")
        items = session.query(Category).all()
        for i in items:
            if category_id == str(i.id):
                if category_id == "2":
                    category = i.name
                    bot.edit_message_text(
                        "Мурожат мавзуси: " + category, call.message.chat.id, call.message.id, reply_markup=None)
                    bot.send_message(
                        call.message.chat.id, "Илтимос кафедрани танланг", reply_markup = gen_model_markup(Kafedra))
                    ss.step = "kafedra"
                else:
                    category = i.name
                    bot.edit_message_text(
                        "Мурожат мавзуси: " + category, call.message.chat.id, call.message.id, reply_markup = None)
                    bot.send_message(call.message.chat.id,"Мурожат турини танланг:",reply_markup=type_keyboard)
                    ss.step = "type"
                ss.category = category_id
                session.commit()
                break        
    
    elif call.data == "warning":
        #t = session.query(Teacher).get(t_id).name
        bot.edit_message_text(
            "Этирозни матнини йозб колдиринг, видео жонатинг, аудио жонатинг, фото жонатинг, файл жонатинг: ", call.message.chat.id, call.message.id, reply_markup=None)
        ss.step = "listening"
        session.add(ss)
        session.commit()
        print(ss.step)


@bot.message_handler(content_types='text')
def message_reply(message):
    ss = session.query(Session).filter(Session.chat_id == message.chat.id).first()
    print(ss.step)
    if ss.step == "listening":
        text = message.text
        bot.send_message(
            message.chat.id, "Этироз матни кабул килинди, файл, видео, аудио, расм ташен")

        
#warning danger success listening

bot.polling(none_stop=True)
session.close()