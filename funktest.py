import telebot

import datetime

TOKEN = "6463417924:AAEyaWB5ihc2EvtYJLf_PbAXuDbDtdENkTM"

bot = telebot.TeleBot(TOKEN)

#бот стартовое хуярит сообщение
@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(message, f"динаху")

# Словарь для хранения времени последнего использования команды /explode для каждого пользователя
last_explode_time = {}

# Функция для проверки, можно ли пользователю использовать команду /explode снова
def can_explode(user_id):
    if user_id in last_explode_time:
        # Проверяем, была ли последняя команда /explode использована сегодня
        today = datetime.date.today()
        return last_explode_time[user_id] != today
    else:
        # Если пользователь еще не использовал команду, разрешаем ему
        return True

# Функция для обновления времени последнего использования команды /explode
def update_explode_time(user_id):
    last_explode_time[user_id] = datetime.date.today()

@bot.message_handler(commands=['explode'])
def explode_user(message):
    try:
        user_id = message.from_user.id
        if not can_explode(user_id):
            # Если пользователь уже использовал команду сегодня, сообщаем ему об этом
            bot.reply_to(message, "Взрувную магию можно использовать лишь раз в день, из-за непомерного расхода маны при использовании.")
            return
        # Обновляем время последнего использования команды /explode для данного пользователя
        update_explode_time(user_id)
        bot.reply_to(message, f'Мое имя Мегумин! Величайший гений Клана Алых Магов, кто владеет Взрывной магией! EXPLOUSION!!!')
        # Отправляем гифку со взрывом
        file_url = explosion()
        bot.send_document(message.chat.id, file_url)
        # Отправляем информацию о том, кого взорвали
        bot.reply_to(message, f'{user_id} был взорван.')
    except IndexError:
        bot.reply_to(message, 'Ты долбаёб? Кого мне взрывать? id укажи.')

bot.polling()