import telebot
import buttons as bt
import database as db
# создаем объект бота
bot = telebot.TeleBot(token="7349504840:AAH9LF1Y0EqTsqR0S6zz6T54KRKiwbp0JAo")
users = {}
# db.add_product(pr_name="Бургер Биг", pr_desc="лучший", pr_price=50000, pr_quantity=10, pr_photo="https://vkusnotochkamenu.ru/image/cache/catalog/photo/799220868-skandinavskij-burger-600x600.png")
# db.add_product(pr_name="Чизбургер Биг", pr_desc="лучший чизбургер", pr_price=60000, pr_quantity=10, pr_photo="https://vkusnotochkamenu.ru/image/cache/catalog/photo/348457690-chizburger-600x600.jpg")
# db.add_product(pr_name="Чизбургер2", pr_desc="лучший чизбургер2", pr_price=60000, pr_quantity=0, pr_photo="https://vkusnotochkamenu.ru/image/cache/catalog/photo/348457690-chizburger-600x600.jpg")

print(db.get_all_product())
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
@bot.callback_query_handler(lambda call: call.data in ["main_menu", "cart", "minus", "plus", "none",
                                                       "back", "to_cart", "clear_cart",
                                                       "order"])

def all_calls(call):
    user_id = call.message.chat.id
    if call.data == "main_menu":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.main_menu_kb())
    elif call.data == "cart":
        bot.delete_message(user_id, call.message.message_id)
        cart = db.get_cart_id_name(user_id)
        user_cart = db.get_user_cart(user_id)
        full_text = f"Ваша корзина: \n\n"
        total_amount = 0
        print(user_cart)
        for i in user_cart:
            full_text += f"{i[0]} x{i[1]} = {i[2]}\n"
            total_amount += i[2]
        full_text += f"\n\nИтоговая сумма: {total_amount}"
        bot.send_message(user_id, text=full_text, reply_markup=bt.get_cart_kb(cart))
    elif call.data == "plus":
        current_amount = users[user_id]["pr_count"]
        users[user_id]["pr_count"] += 1
        bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id,
                                      reply_markup=bt.exact_product(current_amount=current_amount,
                                                                    plus_or_minus="plus"))

    elif call.data == "minus":
        current_amount = users[user_id]["pr_count"]
        if current_amount > 1:
            users[user_id]["pr_count"] -= 1
            bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id,
                                          reply_markup=bt.exact_product(current_amount=current_amount,
                                                                        plus_or_minus="minus"))
        else:
            pass
    elif call.data == "none":
        pass
    elif call.data == "back":
        bot.delete_message(user_id, call.message.message_id)
        all_products = db.get_pr_id_name()
        bot.send_message(user_id, "Выберите продукт", reply_markup=bt.products_in(all_products))
    elif call.data == "to_cart":
        db.add_to_cart(user_id, users[user_id]["pr_id"], users[user_id]["pr_name"],
                       users[user_id]["pr_count"], users[user_id]["pr_price"])
        users.pop(user_id)
        bot.delete_message(user_id, call.message.message_id)
        all_products = db.get_pr_id_name()
        bot.send_message(user_id, "Продукт добавлен в корзину. Выберите продукт",
                         reply_markup=bt.products_in(all_products))
    elif call.data == "clear_cart":
        db.delete_user_cart(user_id)
        bot.send_message(user_id, "Ваша корзина очищена")
        all_products = db.get_pr_id_name()
        bot.send_message(user_id, "Выберите продукт",
                         reply_markup=bt.products_in(all_products))
    elif call.data == "order":
        bot.delete_message(user_id, call.message.message_id)
        user_cart = db.get_user_cart(user_id)
        full_text = f"Новый заказ от юзера {user_id} :  \n\n"
        total_amount = 0
        for i in user_cart:
            full_text += f"{i[0]} x{i[1]} = {i[2]}\n"
            total_amount += i[2]
        full_text += f"\n\nИтоговая сумма: {total_amount}"
        db.delete_user_cart(user_id)
        bot.send_message(user_id, "Ваш заказ принят. Ожидайте")
        bot.send_message(chat_id=-4281830388, text=full_text)






@bot.callback_query_handler(lambda call: "prod_" in call.data)
def product_call(call):
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)
    product_id = int(call.data.replace("prod_", ""))
    product_info = db.get_exact_product(product_id)
    users[user_id] = {"pr_id": product_id, "pr_name": product_info[0], "pr_count": 1, "pr_price": product_info[1]}
    bot.send_photo(user_id, photo=product_info[3], caption=f"{product_info[0]}\n\n"
                                                           f"Описание: {product_info[2]}\n"
                                                           f"Цена: {product_info[1]} сум",
                   reply_markup=bt.exact_product())


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