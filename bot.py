import telebot
import buttons as bt
import database as db
# создаем объект бота
bot = telebot.TeleBot(token="7349504840:AAH9LF1Y0EqTsqR0S6zz6T54KRKiwbp0JAo")

db.add_product(pr_name="Бургер", pr_desc="лучший", pr_price=50000, pr_quantity=10, pr_photo="https://vkusnotochkamenu.ru/image/cache/catalog/photo/799220868-skandinavskij-burger-600x600.png")
db.add_product(pr_name="Чизбургер", pr_desc="лучший чизбургер", pr_price=60000, pr_quantity=10, pr_photo="https://vkusnotochkamenu.ru/image/cache/catalog/photo/348457690-chizburger-600x600.jpg")
db.add_product(pr_name="Чизбургер2", pr_desc="лучший чизбургер2", pr_price=60000, pr_quantity=0, pr_photo="https://vkusnotochkamenu.ru/image/cache/catalog/photo/348457690-chizburger-600x600.jpg")
# обработка команды /start
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    checker = db.check_user(user_id)
    if checker == True:
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.main_menu_kb())
    elif checker == False:
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
                                  f"Локация: {location}\n"
                                  f"Выберите действие", reply_markup=bt.main_menu_kb())
        db.add_user(user_id, name, number)
    else:
        bot.send_message(user_id, "Отправьте свою локацию через кнопку",
                         reply_markup=bt.location_bt())
        bot.register_next_step_handler(message, get_location, name, number)
@bot.message_handler(content_types=["text"])
def main_menu(message):
    user_id = message.from_user.id
    text = message.text
    if text == "🍴Меню":
        all_products = db.get_pr_id_name()
        bot.send_message(user_id, "Выберите продукт", reply_markup=bt.products_in(all_products))
    elif text == "🛒Корзина":
        bot.send_message(user_id, "Ваша корзина")
    elif text == "✒️Оставить отзыв":
        bot.send_message(user_id, "Напишите текст вашего отзыва")


bot.infinity_polling()