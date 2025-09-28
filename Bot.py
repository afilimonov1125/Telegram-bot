import schedule
import random
import telebot
import time
import threading

# Замени 'TOKEN' на токен твоего бота
# Этот токен ты получаешь от BotFather, чтобы бот мог работать
bot = telebot.TeleBot("")

def beep(chat_id) -> None:
    """Send the beep message."""
    bot.send_message(chat_id, text='Beep!')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши что-нибудь! Команды:\n/hello\n/bye\n/generate_password\n/dice")

@bot.message_handler(commands=['generate_password'])
def password(message):
    elements = "+-/*!&$#?=@<>123456789"
    password = ""
    for i in range(10):
        password += random.choice(elements)
    bot.reply_to(message, 'Пароль: ' + str(password))
    print('Someone generated a password.')

@bot.message_handler(commands=['set'])
def set_timer(message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        sec = int(args[1])
        schedule.every(sec).seconds.do(beep, message.chat.id).tag(message.chat.id)
    else:
        bot.reply_to(message, 'Использование: /set <секунды>')

@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)



    
@bot.message_handler(commands=['wait'])
def wait(message):
    if int(message.text.split()[1]):
        time.sleep(int(message.text.split()[1]))
        bot.reply_to(message, 'Будильник сработал!!!!!!11!!!11!!11!!11!!1')
    else:
        print('Используйте /wait (количество секунд)')

@bot.message_handler(commands=['dice'])
def random_number(message):
    bot.reply_to(message, 'На кубике выпало число ' + str(random.randint(1, 6)))
    print('Someone rolled the dice.')

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)
