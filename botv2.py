import telebot

from models import *
TOKEN = "2042929004:AAEXRHWYKZ2LvbRsTUReAT9gNp6h7CQL4Rk"
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

категории динамично с базы
если там учителей выбрали
для учителей есть база
там кафедры в табле есть потом по ID кафедры есть училтеля таблица


с отдельными таблицами?

для сохранение одна таблица пройдика в models
'''

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
    
        
    bot.reply_to(message, "Ассалому алайкум. Таклиф ва шикоятларингизни аноним холда қолдиришингиз мумкин, категорияни танланг:",
        reply_markup=gen_model_markup(Category))



bot.polling(none_stop=True)
session.close()