import telebot 
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
bot = telebot.TeleBot('7262258841:AAHduA6AaHXE2kehIMatUQ81VL2IMYaixts') 
m_list = ["Шарф", "Футболка"]
w_list = ["Шарф/Платок", "Футболка","Джинсы/Брюки","Юбка","Платье","Блузка/Рубашка"]
w_list_weights = [25,25,15,15,10,10]
channel_id = '-1001522214922'
def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Подписаться на канал","https://t.me/+N6xL0AutGzo4YjAy"))
    return markup

def gen_markup_for_adress():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Яндекс Карты","https://yandex.ru/maps/-/CDWXvIif"),InlineKeyboardButton("2ГИС","https://go.2gis.com/87jts") )
    return markup

def gen_markup_for_gender():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Мужчина👱🏻‍♂️",callback_data="Мужчина"),InlineKeyboardButton("Женщина👩🏼",callback_data="Женщина") )
    return markup

def already_get(call):
    bot.edit_message_text(message_id=pickgender(chat_id = call.message.chat.id, user_id = call.from_user.id).message_id, chat_id = call.message.chat.id, text = "Вы уже получили приз!", reply_markup=None)

def get_user_id(call):
    try:
        f = open('users.txt', 'r')
        check = str.split(f.read(),',')
        f.close()
        if(not (str(call.from_user.id) in check)):
            f = open('users.txt', 'a')
            f.write(str(call.from_user.id) + ',')
            f.close()
        else:
            already_get(call=call)
            return True
    except FileNotFoundError as e:
        print(e)

@bot.callback_query_handler(func = lambda call: call.data in ['Мужчина'])
def genpriceman(call):
    flag = get_user_id(call = call)
    if call.data == 'Мужчина' and flag != True:
        random_index = random.randint(0, len(m_list) - 1)
        message = "Поздравляею! Вы выиграли " + m_list[random_index] + "\nЗабрать можно по адресу: <b>Будапештская 39</b>"
        bot.edit_message_text(message_id = call.message.id, parse_mode='HTML', chat_id = call.message.chat.id, text = message,reply_markup=gen_markup_for_adress())
    elif call.data == 'Женщина' and flag != True:
        message = "Поздравляею! Вы выиграли " + str((random.choices(w_list, w_list_weights))[0]) + "\nЗабрать можно по адресу: <b>Будапештская 39</b>"
        bot.edit_message_text(message_id = call.message.id, parse_mode='HTML', chat_id = call.message.chat.id, text = message, reply_markup = gen_markup_for_adress())

@bot.callback_query_handler(func = lambda call: call.data in ['Женщина'])
def genpricewoman(call):
    flag = get_user_id(call = call)
    if flag != True:
        message = "Поздравляею! Вы выиграли " + str((random.choices(w_list, w_list_weights))[0]) + "\nЗабрать можно по адресу: <b>Будапештская 39</b>"
        bot.edit_message_text(message_id = call.message.id, parse_mode='HTML', chat_id = call.message.chat.id, text = message,reply_markup=gen_markup_for_adress())

def check_channel_subscribe_message(user_id):
    return bot.send_message(user_id, "Не подписаны на канал!",reply_markup=gen_markup())

def pickgender(user_id, chat_id, user_name):
    return bot.edit_message_text(chat_id = chat_id, message_id = check_channel_subscribe_message(user_id).message_id, text = " " + user_name + ", выбери пол👇", reply_markup = gen_markup_for_gender())

@bot.message_handler(commands = ['start'])
def start(message): 
    user_id = message.from_user.id
    if(message.from_user.first_name):
        user_name = message.from_user.first_name
    else:
        user_name = message.from_user.username
    try:
        f = open('users.txt', 'r')
        check = str.split(f.read(),',')
        f.close()
        if(not (str(user_id) in check)):
            chat_member = bot.get_chat_member(channel_id, user_id)
            if (chat_member.status in ['left','kicked']): 
                check_channel_subscribe_message(user_id=user_id)
                while(chat_member.status in ['left','kicked','creator']):
                    if(bot.get_chat_member(channel_id, user_id).status in ['member','creator']):
                        pickgender(user_id = user_id,user_name=user_name, chat_id = message.chat.id)
                        break
            elif(chat_member.status in ['creator']):
                pickgender(user_id = user_id, user_name=user_name, chat_id = message.chat.id)
        else:
            bot.send_message(chat_id = message.chat.id, parse_mode='HTML', text = "<strong>Вы уже получили приз!</strong>")  
    except Exception as e: 
        bot.send_message(user_id, e) 
        
bot.polling()
