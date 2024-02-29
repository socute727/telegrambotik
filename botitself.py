#тута мы импортируем бота
import telebot
#для работы калькулятора
from telebot import types
#тута что бы бот мог угарать с файлами
import requests
#для казика
import random
#токен (нада свой)

TOKEN = "6463417924:AAEyaWB5ihc2EvtYJLf_PbAXuDbDtdENkTM"

bot = telebot.TeleBot(TOKEN)

#бот стартовое хуярит сообщение
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        with open('/home/nya/bot.txt', 'r', encoding='utf-8') as file:
            message_content = file.read()
        bot.send_message(message.chat.id, message_content)
    except Exception as e:
        bot.reply_to(message, f"бля ну не работает")

#бот расказывает че умеет
@bot.message_handler(commands=['commandlist'])
def send_list(message):
    try:
        with open('/home/nya/commandlist.txt', 'r', encoding='utf-8') as file:
            message_content = file.read()
        bot.send_message(message.chat.id, message_content)
    except Exception as e:
        bot.reply_to(message, f"бля ну не работает")

#гайд по взрывам(хуле нет?)
@bot.message_handler(commands=['howtoblowup'])
def send_explosion_info(message):
    bot.reply_to(message, "Привет! Для того чтобы кастовать магию взрыва, тебе понадобится собрать всю свою магическую энергию в одной точке и затем освободить ее сразу, создав огромный взрыв! Но будь осторожен, кастование магии взрыва требует много сил и опыта. Удачи!")

#тута из txt файла текст считывает
@bot.message_handler(commands= ['aboutexplousion'])
def send_message_from_file(message):
    try:
        with open('/home/nya/message.txt', 'r', encoding='utf-8') as file:
            message_content = file.read()
        bot.send_message(message.chat.id, message_content)
    except Exception as e:
        bot.reply_to(message, f"бля ну не работает")

#взрыв
def explosion():
    file_url = 'https://c.tenor.com/xQV0IM5rFjkAAAAd/tenor.gif'
    return file_url
@bot.message_handler(commands=['explode'])
def explode_user(message):
    try:
        user_id = message.text.split()[1]
        bot.reply_to(message, f'Мое имя Мегумин! Величайший гений Клана Алых Магов, кто владеет Взрывной магией! EXPLOUSION!!!')
        #отправка гифки со взрывом
        file_url = explosion()
        bot.send_document(message.chat.id, file_url)
        #отправка информации о том какого юзверя взорвали
        bot.reply_to(message, f'{user_id} был взорван.')
    except IndexError:
        bot.reply_to(message, 'Ты долбаёб? Кого мне взрывать? id укажи.')

#гифки
def get_random_konosuba_gif():
    api_key = "edsyceW8ZKcvsPmJaFoTZRhV39ulOGfc"
    tag = "konosuba"  #тег для поиска гифок
    url = f"https://api.giphy.com/v1/gifs/random?api_key={api_key}&tag={tag}&rating=g"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and 'data' in data:
        gif_url = data['data']['images']['original']['url']
        return gif_url
    else:
        return None

@bot.message_handler(commands=['gif'])
def send_random_gif(message):
    try:
        gif_url = get_random_konosuba_gif()
        if gif_url:
            bot.send_document(message.chat.id, gif_url)
        else:
            bot.reply_to(message, "Не удалось получить гифку. Попробуйте позже.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка при отправке гифки: {e}")

#жопа
def get_random_anime_ass_gif():
    api_key = "edsyceW8ZKcvsPmJaFoTZRhV39ulOGfc"
    tag = "explosion"  #тег для поиска гифок
    url = f"https://api.giphy.com/v1/gifs/random?api_key={api_key}&tag={tag}&rating=g"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and 'data' in data:
        gif_ass = data['data']['images']['original']['url']
        return gif_ass
    else:
        return None

@bot.message_handler(commands=['explosions'])
def send_random_gif(message):
    try:
        gif_ass = get_random_anime_ass_gif()
        if gif_ass:
            bot.send_document(message.chat.id, gif_ass)
        else:
            bot.reply_to(message, "Не удалось получить гифку. Попробуйте позже.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка при отправке гифки: {e}")

#калькулятор
@bot.message_handler(func=lambda message: True)
def calculate_expression(message):
    try:
        text = message.text
        result = eval(text)
        bot.reply_to(message, f"Результат: {result}")
    except Exception as e:
        pass

bot.polling()