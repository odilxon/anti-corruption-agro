import telebot

from models import *
TOKEN = "2042929004:AAEgJShr8Ju6mTr-1ekczXkqP5qcVwaSNxA"
bot = telebot.TeleBot(TOKEN, parse_mode=None)
STATIC_PATH = 'static/bot/'
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
user_data = { }


type_keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

type_warning = telebot.types.InlineKeyboardButton("Этироз",callback_data = "warning")
type_success = telebot.types.InlineKeyboardButton(
    "Таклиф", callback_data="success")
type_danger = telebot.types.InlineKeyboardButton(
    "Шикоят", callback_data="danger")
type_keyboard.add(type_warning,type_success,type_danger)

LAST = telebot.types.ReplyKeyboardMarkup(True,one_time_keyboard=True)
itembtn1 = telebot.types.KeyboardButton('Юбориш')

LAST.add(itembtn1)


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
    print(call.data)
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

    if "kafedra_" in call.data:
        kafedra_id = call.data.split("_")[1]
        items = session.query(Kafedra).all()
        if call.message.chat.id not in user_data:
            user_data[call.message.chat.id] = []
        for i in items:
            if kafedra_id == str(i.id):
                kafedra_name = i.name
                bot.edit_message_text(
                        "Kafedra: " + kafedra_name, call.message.chat.id, call.message.id, reply_markup = None)
                bot.send_message(
                call.message.chat.id, "Илтимос устозни танланг", reply_markup =  gen_model_markup(Teacher,True,kafedra_id))
                ss.step = ""
            user_data[call.message.chat.id].append({
                "type" : "kafedra_id",
                "value": kafedra_id,
                "datetime": datetime.now()
            })
            session.commit()
            break 
    
    elif call.data in ["warning", "success", "danger"]:
        #t = session.query(Teacher).get(t_id).name
        bot.edit_message_text(
            "Мурожат тури" + call.data, call.message.chat.id, call.message.id, reply_markup=None)
        
        bot.send_message(call.message.chat.id,
        "Мурожаатларингизни матн, видео, овозли файл ёки документ куринишида жунатинг: ",
        reply_markup=LAST)
        
        ss.type = call.data
        ss.step = "listening"
        session.add(ss)
        session.commit()
        if call.message.chat.id not in user_data:
            user_data[call.message.chat.id] = []
        print(ss.step)

'''
user_data[message.chat.id].append({
    "type" : "text",
    "value": message.text
    "datetime": datetime.now()
})

'''

@bot.message_handler(content_types='text')
def message_reply(message):
    ss = session.query(Session).filter(Session.chat_id == message.chat.id).first()
    
    if ss.step == "listening":
        if message.text == "Юбориш":
            com = Complain(
                category_id=int(ss.category),
                type = ss.type,
                first_name = ss.first_name,
                username = ss.username,
                chat_id= ss.chat_id
                
            )
            session.add(com)
            session.commit()
            for item in user_data[message.chat.id]:
                com_d = Complain_Data(
                    complain_id = com.id,
                    key = item['key'],
                    value = item['value']
                )
                session.add(com_d)
                session.commit()
            
            ss.step = "test"
            session.add(ss)
            session.commit()
        
        text = message.text
        user_data[message.chat.id].append({
            "key" : "text",
            "value" : text,
            "time" : datetime.now()
        })
        
@bot.message_handler(content_types='audio')
def audio_handler(message):
    ss = session.query(Session).filter(Session.chat_id == message.chat.id).first()
    print(ss.step)
    if ss.step == "listening":
        audio_file = message.audio.file_id
        file_info = bot.get_file(audio_file)
        print(file_info)
        ext = file_info.file_path.split(".")[1]
        filename = file_info.file_unique_id + "." + ext
        path = STATIC_PATH + "audio/" + filename
        user_data[message.chat.id].append({
            "key" : "audio",
            "value" : path,
            "time" : datetime.now()
        })
        downloaded_file = bot.download_file(file_info.file_path)
        with open(path, 'wb') as new_file:
            new_file.write(downloaded_file)
        

@bot.message_handler(content_types='voice')
def voice_handler(message):
    ss = session.query(Session).filter(Session.chat_id == message.chat.id).first()
    print(ss.step)
    if ss.step == "listening":
        voice_file = message.voice.file_id
        file_info = bot.get_file(voice_file)
        print(file_info)
        ext = "ogg"# file_info.file_path.split(".")[1]
        downloaded_file = bot.download_file(file_info.file_path)
        filename = file_info.file_unique_id + "." + ext
        path = STATIC_PATH + "voice/" + filename
        with open(path, 'wb') as new_file:
            new_file.write(downloaded_file)
        user_data[message.chat.id].append({
            "key" : "voice",
            "value" : path,
            "time" : datetime.now()
        })
        print(user_data[message.chat.id])


@bot.message_handler(content_types='document')
def document_handler(message):
    ss = session.query(Session).filter(Session.chat_id == message.chat.id).first()
    print(ss.step)
    if ss.step == "listening":
        doc_file = message.document.file_id
        file_info = bot.get_file(doc_file)
        print(file_info)
        ext = file_info.file_path.split(".")[1]
        downloaded_file = bot.download_file(file_info.file_path)
        filename = file_info.file_unique_id + "." + ext
        path = STATIC_PATH + "document/" + filename
        with open(path, 'wb') as new_file:
            new_file.write(downloaded_file)
        user_data[message.chat.id].append({
            "key" : "document",
            "value" : path,
            "time" : datetime.now()
        })
        print(user_data[message.chat.id])


@bot.message_handler(content_types='photo')
def photo_handler(message):
    ss = session.query(Session).filter(Session.chat_id == message.chat.id).first()
    print(ss.step)
    if ss.step == "listening":
        photo_file = message.photo[-1].file_id
        photo_info = bot.get_file(photo_file)
        
        ext = photo_info.file_path.split(".")[1]
        downloaded_file = bot.download_file(photo_info.file_path)
        filename = photo_info.file_unique_id + "." + ext
        path = STATIC_PATH + "photo/" + filename
        
        with open(path, 'wb') as new_file:
            new_file.write(downloaded_file)
        user_data[message.chat.id].append({
            "key" : "photo",
            "value" : path,
            "time" : datetime.now()
        })
        print(user_data[message.chat.id])


'''
@bot.message_handler(content_types='photo')
def voice_handler(message):
    ss = session.query(Session).filter(Session.chat_id == message.chat.id).first()
    print(ss.step)
    if ss.step == "listening":
        doc_file = message.document.file_id
        file_info = bot.get_file(doc_file)
        print(file_info)
        ext = file_info.file_path.split(".")[1]
        downloaded_file = bot.download_file(file_info.file_path)
        filename = file_info.file_unique_id + "." + ext
        path = STATIC_PATH + "photo/" + filename
        with open(path, 'wb') as new_file:
            new_file.write(downloaded_file)
        user_data[message.chat.id].append({
            "key" : "document",
            "value" : path,
            "time" : datetime.now()
        })
        print(user_data[message.chat.id])

'''
# @bot.message_handler(content_types=['voice'])
# def voice_processing(message):
#     file_info = bot.get_file(message.voice.file_id)
#     downloaded_file = bot.download_file(file_info.file_path)
#     with open('new_file.ogg', 'wb') as new_file:
#         new_file.write(downloaded_file)
       
        
#warning danger success listening

bot.polling(none_stop=True)
session.close()