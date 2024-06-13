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

def products_in(all_products):
    kb = types.InlineKeyboardMarkup(row_width=2)
    # создание постоянных кнопок
    main_menu = types.InlineKeyboardButton(text="Главное меню", callback_data="main_menu")
    cart = types.InlineKeyboardButton(text="Корзина", callback_data="cart")
    # создание динамичных кнопок
    all_buttons = [types.InlineKeyboardButton(text=product[1], callback_data=f"prod_{product[0]}")
                   for product in all_products]
    # добавление всех кнопок в пространство
    kb.add(*all_buttons)
    kb.row(cart)
    kb.row(main_menu)
    return kb


