import telebot # Тута мы импортируем бота
from telebot import types # Для работы калькулятора
import requests # Тута что бы бот мог угарать с файлами
import random # Тута что бы бот мог угарать с файлами
import datetime # Ограничение по времени
import json # Для хранения токена
# Токен 
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

# Бот стартовое хуярит сообщение
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        with open('bot.txt', 'r', encoding='utf-8') as file:
            message_content = file.read()
        meg_url = lmao_megumin()
        bot.send_document(message.chat.id, meg_url, caption=message_content)
    except Exception as e:
        bot.reply_to(message, f"бля ну не работает")

# Бот расказывает че умеет
@bot.message_handler(commands=['commandlist'])
def send_list(message):
    try:
        with open('commandlist.txt', 'r', encoding='utf-8') as file:
            message_content = file.read()
        bot.send_message(message.chat.id, message_content)
    except Exception as e:
        bot.reply_to(message, f"бля ну не работает")

# Взрыв
def explosion():
    file_url = 'https://c.tenor.com/xQV0IM5rFjkAAAAd/tenor.gif'
    return file_url

# Херовина для хранения инфы о том когда ласт тайм была заюзана магия взрыва
last_explode_time = {}

# Картинка с грусной Мегумин
def sad_megumin():
    img_url = 'https://media1.tenor.com/m/1qjlHimJe2UAAAAC/megumin-crying-megumin.gif'
    return img_url

def send_sad_megumin(message):
    img_url = sad_megumin()
    bot.send_document(message.chat.id, img_url, caption="К сожалению, взрувную магию можно использовать лишь раз в день, из-за непомерного расхода маны при использовании.")

# Для проверки, можно ли пользователю использовать команду /explode снова
def can_explode(user_id):
    if user_id in last_explode_time:
        today = datetime.date.today() # Чекаем юзал ли юзер(масло масленное) сегодня взрыв
        return last_explode_time[user_id] != today
    else:
        return True # Если не юзал, разрешаем ему

# Функшн для обновления времени последнего использования команды /explode
def update_explode_time(user_id):
    last_explode_time[user_id] = datetime.date.today()

# Обработчик команды /explode
@bot.message_handler(commands=['explode'])
def explode_user(message):
    try:
        user_id = message.text.split()[1]
        user_who_crimson_magic = message.from_user.username
        if not can_explode(user_id):
            send_sad_megumin(message)
            return
        update_explode_time(user_id)
        bot.reply_to(message, f'Мое имя Мегумин! Величайший гений Клана Алых Магов, кто владеет Взрывной магией! EXPLOUSION!!!')
        file_url = explosion()
        bot.send_document(message.chat.id, file_url)
        # Информация о том, кого взорвали
        bot.reply_to(message, f'{user_id} был взорван.')
        explosions_count[user_who_crimson_magic] = explosions_count.get(user_who_crimson_magic, 0) + 1
    except IndexError:
        bot.reply_to(message, 'Кого мне взрывать? Id укажи.')

explosions_count = {}

# Обработчик команды /expcount
@bot.message_handler(commands=['expcount'])
def explosion_count(message):
    try:
        user_id = message.from_user.username
        if user_id not in explosions_count:
            bot.reply_to(message, f'@{user_id} еще не кастовал взрывную магию.')
        else:
            count = explosions_count[user_id]
            bot.reply_to(message, f'@{user_id} настоящий алый маг, он использовал взрывную магию уже {count} раз.')
    except Exception as e:
        bot.reply_to(message, f'Произошла ошибка: {e}')

# Рандомные гифки
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

# Получает гиф
def lain():
    lain_url = 'https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdmNoM3N0MHFhajluaTVtMGoxbjlwOWh4eTdtN2U2b2k5ajJxOWxvZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/vP5gXvSXJ2olG/giphy.gif'
    return lain_url
# Отправляет гиф
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