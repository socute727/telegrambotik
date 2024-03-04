import telebot # Импортируем библиотеку для работы с телеграм ботами
import requests # Импортируем библиотеку для работы с запросами
import datetime # Импортируем библиотеку для работы с временными промежутками
import json # Импортируем библиотеку для работы с конфигами формата json

# Загрузка конфига
def load_config(filename):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config

config = load_config('config.json')
TOKEN = config['token']

bot = telebot.TeleBot(TOKEN)

# Стартовое сообщение
def send_megumin_image(message):
    meg_url = 'https://c.tenor.com/z6DsdmHQaxoAAAAd/tenor.gif'
    try:
        with open('bot.txt', 'r', encoding='utf-8') as file:
            message_content = file.read()
        bot.send_document(message.chat.id, meg_url, caption=message_content)
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    send_megumin_image(message)

# Обработчик команды /commandlist
@bot.message_handler(commands=['commandlist'])
def send_list(message):
    try:
        with open('commandlist.txt', 'r', encoding='utf-8') as file:
            message_content = file.read()
        bot.send_message(message.chat.id, message_content)
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

# Обработчик команды /faq
@bot.message_handler(commands=['faq'])
def send_faq(message):
    try:
        with open('faq.txt', 'r', encoding='utf-8') as file:
            message_content = file.read()
        bot.send_message(message.chat.id, message_content)
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

# Функция для отправки грустной Мегумин
def send_sad_megumin(message):
    img_url = 'https://media1.tenor.com/m/1qjlHimJe2UAAAAC/megumin-crying-megumin.gif'
    bot.send_document(message.chat.id, img_url, caption="К сожалению, взрывную магию можно использовать лишь раз в день, из-за непомерного расхода маны при использовании.")

# Для хранения информации о времени последнего использования команды /explode
last_explode_time = {}

# Функция для проверки возможности использования взрыва
def can_explode(user_id):
    if user_id in last_explode_time:
        today = datetime.date.today()
        return last_explode_time[user_id] != today
    else:
        return True

# Функция для обновления времени последнего использования взрыва
def update_explode_time(user_id):
    last_explode_time[user_id] = datetime.date.today()

# Обработчик взрыва
@bot.message_handler(commands=['explode'])
def explode_user(message):
    try:
        user_id = message.text.split()[1]
        if not can_explode(user_id):
            send_sad_megumin(message)
            return
        update_explode_time(user_id)
        bot.reply_to(message, f'Мое имя Мегумин! Величайший гений Клана Алых Магов, кто владеет Взрывной магией! EXPLOUSION!!!')
        file_url = 'https://c.tenor.com/xQV0IM5rFjkAAAAd/tenor.gif'
        bot.send_document(message.chat.id, file_url)
        bot.reply_to(message, f'{user_id} был взорван.')
        explosions_count[user_id] = explosions_count.get(user_id, 0) + 1
    except Exception as e:
        bot.reply_to(message, f'Произошла ошибка: {e}')
         
# Для хранения информации о количестве взрывов для каждого пользователя
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

# Функция для получения случайной гифки 
def get_random_konosuba_gif():
    api_key = "edsyceW8ZKcvsPmJaFoTZRhV39ulOGfc"
    tag = "konosuba"
    url = f"https://api.giphy.com/v1/gifs/random?api_key={api_key}&tag={tag}&rating=g"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and 'data' in data:
        gif_url = data['data']['images']['original']['url']
        return gif_url
    else:
        return None

# Обработчик команды /konosubagif
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

# Функция для получения случайной гифки со взрывом
def get_random_anime_gif():
    api_key = "edsyceW8ZKcvsPmJaFoTZRhV39ulOGfc"
    tag = "explosion"
    url = f"https://api.giphy.com/v1/gifs/random?api_key={api_key}&tag={tag}&rating=g"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and 'data' in data:
        gif_url = data['data']['images']['original']['url']
        return gif_url
    else:
        return None

# Обработчик команды /explosions
@bot.message_handler(commands=['explosions'])
def send_random_gif(message):
    try:
        gif_url = get_random_anime_gif()
        if gif_url:
            bot.send_document(message.chat.id, gif_url)
        else:
            bot.reply_to(message, "Не удалось получить гифку :(")
    except Exception as e:
        bot.reply_to(message, f"Ошибка при отправке гифки: {e}")

# Обработчик всех текстовых сообщений для калькулятора
@bot.message_handler(func=lambda message: True)
def calculate_expression(message):
    try:
        text = message.text
        result = eval(text)
        bot.reply_to(message, f"Результат: {result}")
    except Exception as e:
        pass

bot.polling()