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
