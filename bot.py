import telebot
import buttons as bt
# создаем объект бота
bot = telebot.TeleBot(token="7349504840:AAH9LF1Y0EqTsqR0S6zz6T54KRKiwbp0JAo")

# обработка команды /start
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Здравствуйте! Это бот доставки.\n"
                              "Пожалуйста, напишите своё имя")
    # указываю следующий этап после старта (функция,
    # которая должна сработать после обработки /start)
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    user_id = message.from_user.id
    # сохраняем имя
    name = message.text
    bot.send_message(user_id, "Отправьте свой номер", reply_markup=bt.phone_number_bt())
    # отправляю пользователя в функцию получение номера и отправляю name в следующий этап
    bot.register_next_step_handler(message, get_number,  name)

def get_number(message, name):
    user_id = message.from_user.id
    # проверяю как отправил пользователь свой номер
    if message.contact:
        # сохраняем номер
        number = message.contact.phone_number
        bot.send_message(user_id, "Отправьте свою локацию",
                         reply_markup=bt.location_bt())
        bot.register_next_step_handler(message, get_location, name, number)
    else:
        # если пользователь неправильно отправил свой номер, возвращаем его в эту функцию
        bot.send_message(user_id, 'Отправьте свой номер через кнопку',
                         reply_markup=bt.phone_number_bt())
        bot.register_next_step_handler(message, get_number, name)

def get_location(message, name, number):
    user_id = message.from_user.id
    if message.location:
        location = message.location
        bot.send_message(user_id, f"Вы успешно прошли регистрацию. Ваши данные:\n"
                                  f"Имя: {name}\n"
                                  f"Номер: {number}\n"
                                  f"Локация: {location}")
    else:
        bot.send_message(user_id, "Отправьте свою локацию через кнопку",
                         reply_markup=bt.location_bt())
        bot.register_next_step_handler(message, get_location, name, number)


bot.infinity_polling()