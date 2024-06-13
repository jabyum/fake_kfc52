from telebot import types

def phone_number_bt():
    # создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # создаем кнопку "поделиться контактом"
    button = types.KeyboardButton("Поделиться контактом",
                                  request_contact=True)
    # добавляю кнопку в пространство
    kb.add(button)
    return kb
def location_bt():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Поделиться локацией",
                                  request_location=True)
    kb.add(button)
    return kb
def main_menu_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    products = types.KeyboardButton(text="🍴Меню")
    cart = types.KeyboardButton(text="🛒Корзина")
    feedback = types.KeyboardButton(text="✒️Оставить отзыв")
    kb.add(products, cart, feedback)
    return kb

