import telebot #тута мы импортируем бота
from telebot import types #для работы калькулятора
import requests #тута что бы бот мог угарать с файлами
import random #тута что бы бот мог угарать с файлами
import datetime #ограничение по времени
import json #для хранения токена
#токен 
def load_config(filename):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config

config = load_config('config.json')
TOKEN = config['token']

bot = telebot.TeleBot(TOKEN)

def lmao_megumin():
    meg_url = 'https://c.tenor.com/z6DsdmHQaxoAAAAd/tenor.gif'
    return meg_url

#бот стартовое хуярит сообщение
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        with open('bot.txt', 'r', encoding='utf-8') as file:
            message_content = file.read()
        meg_url = lmao_megumin()
        bot.send_document(message.chat.id, meg_url, caption=message_content)
    except Exception as e:
        bot.reply_to(message, f"бля ну не работает")

#бот расказывает че умеет
@bot.message_handler(commands=['commandlist'])
def send_list(message):
    try:
        with open('commandlist.txt', 'r', encoding='utf-8') as file:
            message_content = file.read()
        bot.send_message(message.chat.id, message_content)
    except Exception as e:
        bot.reply_to(message, f"бля ну не работает")

#faq
@bot.message_handler(commands=['faq'])
def send_faq(message):
    try:
        with open('faq.txt', 'r', encoding='utf-8') as file:
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
        with open('message.txt', 'r', encoding='utf-8') as file:
            message_content = file.read()
        bot.send_message(message.chat.id, message_content)
    except Exception as e:
        bot.reply_to(message, f"бля ну не работает")

#взрыв
def explosion():
    file_url = 'https://c.tenor.com/xQV0IM5rFjkAAAAd/tenor.gif'
    return file_url

#херовина для хранения инфы о том когда ласт тайм была заюзана магия взрыва
last_explode_time = {}

#картинка с грусной Мегумин
def sad_megumin():
    img_url = 'https://media1.tenor.com/m/1qjlHimJe2UAAAAC/megumin-crying-megumin.gif'
    return img_url

def send_sad_megumin(message):
    img_url = sad_megumin()
    bot.send_document(message.chat.id, img_url, caption="К сожалению, взрувную магию можно использовать лишь раз в день, из-за непомерного расхода маны при использовании.")

#для проверки, можно ли пользователю использовать команду /explode снова
def can_explode(user_id):
    if user_id in last_explode_time:
        today = datetime.date.today() #чекаем юзал ли юзер(масло масленное) сегодня взрыв
        return last_explode_time[user_id] != today
    else:
        return True #если не юзал, разрешаем ему

#функшн для обновления времени последнего использования команды /explode
def update_explode_time(user_id):
    last_explode_time[user_id] = datetime.date.today()

@bot.message_handler(commands=['explode'])
def explode_user(message):
    try:
        user_id = message.text.split()[1]
        if not can_explode(user_id):
            send_sad_megumin(message)
            return
        update_explode_time(user_id)
        bot.reply_to(message, f'Мое имя Мегумин! Величайший гений Клана Алых Магов, кто владеет Взрывной магией! EXPLOUSION!!!')
        file_url = explosion()
        bot.send_document(message.chat.id, file_url)
        #информация о том, кого взорвали
        bot.reply_to(message, f'{user_id} был взорван.')
        explosions_count[user_id] = explosions_count.get(user_id, 0) + 1
    except IndexError:
        bot.reply_to(message, 'Кого мне взрывать? Id укажи.')

explosions_count = {}

@bot.message_handler(commands=['expcount'])
def explosion_count(message):
    try:
        user_id = message.text.split()[1]
        if user_id not in explosions_count:
            bot.reply_to(message, f'{user_id} еще не кастовал взрывную магию.')
        else:
            count = explosions_count[user_id]
            bot.reply_to(message, f'{user_id} настоящий алый маг, он использовал взрывную магию уже {count} раз.')
    except IndexError:
        bot.reply_to(message, 'A где ID пользователя?')

#рандомные гифки
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

#получает гиф
def lain():
    lain_url = 'https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdmNoM3N0MHFhajluaTVtMGoxbjlwOWh4eTdtN2U2b2k5ajJxOWxvZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/vP5gXvSXJ2olG/giphy.gif'
    return lain_url
#отправляет гиф
@bot.message_handler(commands=['lain'])
def hui_vstal(message):
    lain_url = lain()
    if lain_url:
        bot.send_document(message.chat.id, lain_url)
    else:
        bot.reply_to(message, "Не удалось получить гифку. Попробуйте позже.")

@bot.message_handler(commands=['konosubagif'])
def send_random_gif(message):
    try:
        gif_url = get_random_konosuba_gif()
        if gif_url:
            bot.send_document(message.chat.id, gif_url)
        else:
            bot.reply_to(message, "Не удалось получить гифку :(")
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
            bot.reply_to(message, "Не удалось получить гифку :(")
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
#i use arch btw