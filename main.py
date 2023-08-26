import telebot
import sqlite3
import datetime
import requests
import random
import string
import pyperclip
from telebot import types
from config import *
user_id = None  # Глобальная переменная для хранения user_id
is_registered = False

bot = telebot.TeleBot('6642921305:AAEL6ZdNP7o7nzHeaQz4haojqnpkWNsbKDE')

# Функция для создания базы данных
def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS пользователи
                      (user_id text PRIMARY KEY,
                       username text,
                       email text,
                       phone text,
                       full_name text,
                       secret_password text,
                       registration_date text,
                       ip_address text, 
                       course_name text,
                       course_price real,
                       discounted_price real,
                       contest_participation_date text,
                       product text,
                       price real,
                       pass_adm text)''')
    conn.commit()
    conn.close()

create_database()

# Функция получения IP пользователя
def get_user_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        data = response.json()
        ip_address = data['origin']
    except:
        ip_address = 'Unknown'
    return ip_address

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, text=start, parse_mode='Markdown')
    bot.send_message(message.chat.id, text=start2, parse_mode='Markdown')
    msg = bot.send_message(message.chat.id, login, parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_username_step)

# Следующий шаг, получение логина пользователя
def process_username_step(message):
    if message.text.startswith('/start') or message.text.startswith('/menu') \
            or message.text.startswith('Маркет') or message.text.startswith('Личный кабинет')\
            or message.text.startswith('Наши проекты') or message.text.startswith('Образование'):
        bot.reply_to(message, "*Сначала полностью начните регистрацию используя команду* /start", parse_mode='Markdown')
        return

    username = message.text

    global user_id  # Используйте глобальную переменную user_id
    # Ваш код для вставки данных в БД
    user_id = message.chat.id

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO пользователи (user_id, username) VALUES (?, ?)", (user_id, username))
    cursor.execute("UPDATE пользователи SET username = ? WHERE user_id = ?", (username, user_id))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, text=email1, parse_mode='Markdown')
    msg = bot.send_message(message.chat.id, email2, parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_email_step)

# Следующий шаг, получение email пользователя
def process_email_step(message):
    if message.text.startswith('/start') or message.text.startswith('/menu') \
            or message.text.startswith('Маркет') or message.text.startswith('Личный кабинет') \
            or message.text.startswith('Наши проекты') or message.text.startswith('Образование'):
        bot.reply_to(message, "Нужно вводить данные для регистарции, перезагрузите бота нажав /start")
        return
    email = message.text

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE пользователи SET email = ? WHERE user_id = ?", (email, message.chat.id))
    conn.commit()
    conn.close()

    msg = bot.send_message(message.chat.id, text=phone, parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_phone_step)

# Следующий шаг, получение телефона пользователя
def process_phone_step(message):
    if message.text.startswith('/start') or message.text.startswith('/menu') \
            or message.text.startswith('Маркет') or message.text.startswith('Личный кабинет') \
            or message.text.startswith('Наши проекты') or message.text.startswith('Образование'):
        bot.reply_to(message, "Нужно вводить данные для регистарции, перезагрузите бота нажав /start")
        return
    phone = message.text

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE пользователи SET phone = ? WHERE user_id = ?", (phone, message.chat.id))
    conn.commit()
    conn.close()

    msg = bot.send_message(message.chat.id, text=name, parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_full_name_step)

# Следующий шаг, получение полного имени пользователя
def process_full_name_step(message):
    if message.text.startswith('/start') or message.text.startswith('/menu') \
            or message.text.startswith('Маркет') or message.text.startswith('Личный кабинет') \
            or message.text.startswith('Наши проекты') or message.text.startswith('Образование'):
        bot.reply_to(message, "Нужно вводить данные для регистарции, перезагрузите бота нажав /start")
        return
    full_name = message.text

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE пользователи SET full_name = ? WHERE user_id = ?", (full_name, message.chat.id))
    conn.commit()
    conn.close()

    generate_password_button = telebot.types.InlineKeyboardButton("Сгенерировать", callback_data="generate_password")
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(generate_password_button)

    msg = bot.send_message(message.chat.id, text=password, reply_markup=keyboard, parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_secret_password_step)

# функция которая генерирует рандомный пароль
def generate_random_password():
    length = 8
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

passwords = {}  # Словарь для хранения паролей по идентификатору пользователя

# Следующий шаг, получение пароля который ввел пользователь пользователя

secret_passworddd = None
def process_secret_password_step(message):
    if message.text.startswith('/start') or message.text.startswith('/menu') \
            or message.text.startswith('Маркет') or message.text.startswith('Личный кабинет') \
            or message.text.startswith('Наши проекты') or message.text.startswith('Образование'):
        bot.reply_to(message, "Нужно вводить данные для регистарции, перезагрузите бота нажав /start")
        return
    global user_id
    markup = telebot.types.InlineKeyboardMarkup()
    konkye = telebot.types.InlineKeyboardButton('Да', callback_data="yes")
    konkno = telebot.types.InlineKeyboardButton('Нет', callback_data="no")
    markup.row(konkye, konkno)

    secret_password = message.text
    passwords[user_id] = secret_password

    if secret_password == "/generate":
        secret_password = generate_random_password()

    registration_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_address = get_user_ip()

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE пользователи SET secret_password = ? WHERE user_id = ?", (secret_password, user_id))
    cursor.execute("UPDATE пользователи SET registration_date = ? WHERE user_id = ?", (registration_date, user_id))
    cursor.execute("UPDATE пользователи SET ip_address = ? WHERE user_id = ?", (ip_address, user_id))
    conn.commit()
    conn.close()

    # Регистрация завершена, можно выполнить необходимые действия
    bot.send_message(message.chat.id, text=reg, parse_mode='Markdown')
    keyboard = telebot.types.InlineKeyboardMarkup()
    copy_button = telebot.types.InlineKeyboardButton("Скопировать", callback_data="copy_password")
    keyboard.add(copy_button)
    bot.send_message(message.chat.id, text=sekpas + secret_password, reply_markup=keyboard, parse_mode='Markdown')

    # Отправка сообщения с кнопкой "Принять участие в конкурсе"
    bot.send_message(user_id, text=kon, reply_markup=markup, parse_mode='Markdown')
    global is_registered
    is_registered = True

# Если пользователь нажал "Сгенерировать"
@bot.callback_query_handler(func=lambda call: call.data == "generate_password")
def generate_password_callback(call):
    global user_id
    keyboard = types.InlineKeyboardMarkup()
    copy_button = types.InlineKeyboardButton("Скопировать", callback_data="copy_password")
    keyboard.add(copy_button)

    markup = types.InlineKeyboardMarkup()
    konkye2 = types.InlineKeyboardButton('Да', callback_data="yes")
    konkno2 = types.InlineKeyboardButton('Нет', callback_data="no")
    markup.row(konkye2,konkno2)

    secret_password = generate_random_password()
    registration_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_address = get_user_ip()
    # Сохраняем пароль в словаре по идентификатору пользователя
    passwords[user_id] = secret_password

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE пользователи SET secret_password = ? WHERE user_id = ?", (secret_password, user_id))
    cursor.execute("UPDATE пользователи SET registration_date = ? WHERE user_id = ?", (registration_date, user_id))
    cursor.execute("UPDATE пользователи SET ip_address = ? WHERE user_id = ?", (ip_address, user_id))
    conn.commit()
    conn.close()

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=sekpas2 + secret_password, parse_mode='Markdown')


    bot.send_message(user_id, text=sekpas + secret_password, reply_markup=keyboard, parse_mode='Markdown')
    bot.send_message(user_id, text=reg, parse_mode='Markdown')

    # Отправка сообщения с кнопкой "Принять участие в конкурсе"
    bot.send_message(user_id, text=kon, reply_markup=markup, parse_mode='Markdown')
    global is_registered
    is_registered = True

# Обработка Inline-кнопки "Скопировать"
@bot.callback_query_handler(func=lambda call: call.data == "copy_password")
def copy_password_callback(call):
    user_id = call.message.chat.id

    if user_id in passwords:
        generated_password = passwords[user_id]
        pyperclip.copy(generated_password)
        bot.answer_callback_query(call.id, text="Пароль скопирован!")
    else:
        bot.answer_callback_query(call.id, text="Пароль не найден.")

# Обработка Inline-кнопки "Нет" при участии в конкурсе
@bot.callback_query_handler(func=lambda call: call.data == "no")
def no_callback(call):
    bot.send_message(call.message.chat.id,text=otkaz1, parse_mode="Markdown")
    bot.send_message(call.message.chat.id,text=otkaz2, parse_mode="Markdown")
    bot.delete_message(call.message.chat.id, call.message.message_id)

    global index
    index = 1
    markup = types.InlineKeyboardMarkup()
    btn_prev = types.InlineKeyboardButton('⬅️', callback_data='prev_button')
    btn_next = types.InlineKeyboardButton('➡️', callback_data='next_button')
    buy_button = types.InlineKeyboardButton('Купить', callback_data='buy_product')
    btn_index = types.InlineKeyboardButton(f'{index}/{total_images}', callback_data='current_index')
    markup.row(btn_prev, btn_index, btn_next)
    markup.row(buy_button)

    file = open('./image1.png', 'rb')
    bot.send_photo(call.message.chat.id, file, caption="*Название*: _Digital education_\n*Описание*: _Описание продукта Digital education_", reply_markup=markup,  parse_mode="Markdown")
    file.close()


# Обработка Inline-кнопки "Да" при участии в конкурсе
@bot.callback_query_handler(func=lambda call: call.data == "yes")
def yes_callback(call):
    user_id = call.from_user.id

    send_product_info(user_id)
    bot.delete_message(call.message.chat.id, call.message.message_id)

product_name1 = None
index1 =None
# Предоставление продукта который выйграл пользователь

def send_product_info(user_id):
    random.shuffle(products)  # Перемешиваем список продуктов перед выбором случайного продукта
    product = random.choice(products)
    discount = random.choice(discounts)

    photo_path = product['фото']
    product_name = product["название"]
    product_description = product["описание"]
    product_price = product["стоимость"]
    discounted_price = product_price - (product_price * discount / 100)


    global product_name1
    global index1
    if product_name == "Digital education":
        index1 = 1
    if product_name == "Флюиды осознанности":
        index1 = 2
    else:
        index1 =3

    product_name1 = product_name

    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("UPDATE пользователи SET course_name = ?, course_price = ?, discounted_price = ? WHERE user_id = ?",
    #                (product_name, product_price, discounted_price, user_id))
    # conn.commit()
    # conn.close()

    message = f"*Название*: _{product_name}_\n\n" \
              f"*Описание*: _{product_description}_\n\n" \
              f"*Стоимость*: _{product_price} руб._\n" \
              f"*Скидка*: _{discount}%_\n\n" \
              f"*Цена со скидкой*: _{discounted_price} руб._"

    markup = types.InlineKeyboardMarkup()
    about_button = types.InlineKeyboardButton('Подробнее', callback_data='about_product')
    buy_button = types.InlineKeyboardButton('Приобрести', callback_data=f'buy_product2:{product_name}:{discounted_price}')
    markup.row(about_button, buy_button)

    with open(photo_path, 'rb') as photo:
        bot.send_message(user_id, text=f"*Поздравляем!*", parse_mode="Markdown")
        bot.send_message(user_id, text=f"*Ваш приз*:\n_Скидка: {discount}% на образоватльный продукт_ - *{product_name}*\n", parse_mode="Markdown")
        bot.send_photo(user_id, photo, caption=message, parse_mode="Markdown", reply_markup=markup)

import webbrowser

@bot.callback_query_handler(func=lambda call: call.data.startswith('about_product'))
def about_product(call):
    global product_name1
    global index1
    if product_name1 == "Digital education" or index1 == 1:
        url = "https://digitaled.info"
    elif product_name1 == "Флюиды осознанности" or index1 == 2:
        url = "http://likas.digitaled.info"
    else:
        url = "http://ivanskornyakov.digitaled.info/"

    webbrowser.open(url)

global_product_name = None
global_discounted_price = None

# Нажатие на кнопку "Приобрести" при показе продукта со скидкой
@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_product2'))
def buy_product_handler(call):
    callback_data = call.data
    product_name, discounted_price = callback_data.split(':')[1:]
    confirm_purchase(call.message, product_name, discounted_price)

# Подтверждение платежа продукта со скидкой
def confirm_purchase(message, product_name, discounted_price):
    markup = types.InlineKeyboardMarkup()
    agree_button = types.InlineKeyboardButton('Согласен', callback_data='agree_purchase')
    decline_button = types.InlineKeyboardButton('Отказаться', callback_data='decline_purchase')
    markup.row(agree_button, decline_button)

    global global_product_name
    global global_discounted_price
    global_product_name = product_name
    global_discounted_price = discounted_price


    bot.send_message(message.chat.id,
                     f"*Вы совершаете покупку:*\n\n*Название:* {product_name}\n*Цена:* {discounted_price} руб.",
                     parse_mode="Markdown")
    bot.send_message(message.chat.id, "Совершая покупку, вы соглашаетесь с [договором оферты](http://digitaled.info/files/dogovor.docx) и [политикой конфиденциальности](http://digitaled.info/files/policy.docx).", reply_markup=markup, parse_mode="Markdown")
# Сообщение с сообщением какой товар покупаешь

@bot.callback_query_handler(func=lambda call: call.data == 'agree_purchase')
def agree_purchase(call):
    global global_product_name
    global global_discounted_price

    product_name3 = global_product_name
    discounted_price3 = global_discounted_price
    send_invoice(call.message, product_name3, discounted_price3)  # Передача объекта message в качестве аргумента


    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE пользователи SET course_name = ?, discounted_price = ? WHERE user_id = ?",
                   (product_name3, discounted_price3, user_id))
    conn.commit()
    conn.close()



# Кнопка где можно купить продукт со скидкой
def send_invoice(message, product_name, discounted_price):
    global user_id
    bot.send_invoice(message.chat.id, "Покупка курса", f"{product_name}", "invoice",
                     "284685063:TEST:MjAxYWYxZGQyNWE5", "USD",
                     [types.LabeledPrice(f'{product_name}', int(float(discounted_price) * 100))])

# Сообщение если ты отказался от покупки
@bot.callback_query_handler(func=lambda call: call.data == 'decline_purchase')
def decline_purchase_handler(call):
    markup = types.InlineKeyboardMarkup()
    men = types.InlineKeyboardButton('Главное меню', callback_data='men')
    markup.row(men)
    bot.send_message(call.message.chat.id, "*❌Вы отказались от покупки.*", parse_mode="Markdown", reply_markup=markup)



def men(message):
    global is_registered

    if not is_registered:
        keyboard = types.InlineKeyboardMarkup()
        start_button = types.InlineKeyboardButton("Начать регистрацию заново", callback_data= "restart_registration")
        keyboard.add(start_button)
        #bot.reply_to(message, "Сначала зарегистрируйтесь")
        bot.send_message(message.chat.id, text="*Сначала полностью зарегистрируйтесь* нажав /start", parse_mode='Markdown')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    education_button = types.KeyboardButton('Образование')
    market = types.KeyboardButton('Маркет')
    our_projects_button = types.KeyboardButton('Наши проекты')
    personal_cabinet_button = types.KeyboardButton('Личный кабинет')
    markup.add(education_button, market, our_projects_button, personal_cabinet_button)

    bot.send_message(message.chat.id, '👋🏻*Добро пожаловать в главное меню!*', reply_markup=markup, parse_mode='Markdown')

# Обработка команды /start
@bot.message_handler(commands=['menu'])
def create_main_menu_markup(message):
    global is_registered

    if not is_registered:
        keyboard = types.InlineKeyboardMarkup()
        start_button = types.InlineKeyboardButton("Начать регистрацию заново", callback_data= "restart_registration")
        keyboard.add(start_button)
        #bot.reply_to(message, "Сначала зарегистрируйтесь")
        bot.send_message(message.chat.id, text="*Сначала полностью зарегистрируйтесь* нажав /start", parse_mode='Markdown')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    education_button = types.KeyboardButton('Образование')
    market = types.KeyboardButton('Маркет')
    our_projects_button = types.KeyboardButton('Наши проекты')
    personal_cabinet_button = types.KeyboardButton('Личный кабинет')
    markup.add(education_button, market, our_projects_button, personal_cabinet_button)

    bot.send_message(message.chat.id, '👋🏻*Добро пожаловать в главное меню!*', reply_markup=markup,  parse_mode='Markdown')


#переменные для слайдера
index1 = 1
total_images = 3

# Обработка нажатия на кнопку Маркет
@bot.message_handler(func=lambda message: message.text == 'Маркет')
def market(message):
    global index1
    index1 = 1
    markup = types.InlineKeyboardMarkup()
    btn_prev = types.InlineKeyboardButton('⬅️', callback_data='prev_button1')
    btn_next = types.InlineKeyboardButton('➡️', callback_data='next_button1')
    buy_button = types.InlineKeyboardButton('Приобрести', callback_data='buy_product')
    about_button = types.InlineKeyboardButton('Подробнее', callback_data='about_product')
    btn_index = types.InlineKeyboardButton(f'{index1}/{total_images}', callback_data='current_index')
    markup.row(btn_prev, btn_index, btn_next)
    markup.row(about_button, buy_button)

    file = open('./image1.png', 'rb')
    bot.send_photo(message.chat.id, file, caption="*Название*: _Digital education_\n*Описание*: _Описание продукта Digital education_\n*Стоимость*: 100", reply_markup=markup, parse_mode="Markdown")
    file.close()

#отслеживание индексов предыдущей кнопки
def prev_button1(message):
    global index1
    index1 -= 1
    if index1 < 1:
        index1 = total_images
    change_image1(message, index1)

#отслеживание индексов следующей кнопки
def next_button1(message):
    global index1
    index1 += 1
    if index1 > total_images:
        index1 = 1
    change_image1(message, index1)

#слайдер с товарами
def change_image1(message, index1):
    markup = types.InlineKeyboardMarkup()
    btn_prev = types.InlineKeyboardButton('⬅️', callback_data='prev_button1')
    btn_next = types.InlineKeyboardButton('➡️', callback_data='next_button1')
    buy_button = types.InlineKeyboardButton('Приобрести', callback_data='buy_product')
    about_button = types.InlineKeyboardButton('Подробнее', callback_data='about_product')
    btn_index = types.InlineKeyboardButton(f'{index1}/{total_images}', callback_data='current_index')
    markup.row(btn_prev, btn_index, btn_next)
    markup.row(about_button, buy_button)

    caption1 = image_captions2[index1]

    if index1 == 1:
        with open('image1.png', 'rb') as file:
            bot.edit_message_media(
                chat_id=message.chat.id, message_id=message.id, media=types.InputMediaPhoto(file), reply_markup=markup
            )
            bot.edit_message_caption(chat_id=message.chat.id, message_id=message.id, caption=caption1,
                                     reply_markup=markup, parse_mode="Markdown")
    elif index1 == 2:
        with open('image2.png', 'rb') as file:
            bot.edit_message_media(
                chat_id=message.chat.id, message_id=message.id, media=types.InputMediaPhoto(file), reply_markup=markup
            )
            bot.edit_message_caption(chat_id=message.chat.id, message_id=message.id, caption=caption1,
                                     reply_markup=markup, parse_mode="Markdown")
    elif index1 == 3:
        with open('image3.png', 'rb') as file:
            bot.edit_message_media(
                chat_id=message.chat.id, message_id=message.id, media=types.InputMediaPhoto(file), reply_markup=markup
            )
            bot.edit_message_caption(chat_id=message.chat.id, message_id=message.id, caption=caption1,
                                     reply_markup=markup, parse_mode="Markdown")


# Нажатие на кнопку "Приобрести" при показе продукта без скидки
def buy_product(message):
    global user_id

    keyboard = types.InlineKeyboardMarkup()
    agree_button = types.InlineKeyboardButton("Согласен", callback_data="agree")
    disagree_button = types.InlineKeyboardButton("Отказаться", callback_data="disagree")
    keyboard.add(agree_button, disagree_button)
    bot.send_message(message.chat.id, "Совершая покупку, вы соглашаетесь с [договором оферты](http://digitaled.info/files/dogovor.docx) и [политикой конфиденциальности](http://digitaled.info/files/policy.docx).", reply_markup=keyboard, parse_mode="Markdown")
def agree(message):
    if index1 == 1:
        product = "Digital education"
    if index1 == 2:
        product = "Флюиды осознанности"
    if index1 == 3:
        product = "Иван Скорняков"
    price = image_prices[index1]
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot.send_invoice(message.chat.id, "Покупка курса", f"{product}", "invoice",
                     "284685063:TEST:MjAxYWYxZGQyNWE5", "USD", [types.LabeledPrice(f'{product}', price * 100)])
    insert_purchase(product, price, user_id, date)  # Передача user_id в функцию insert_purchase

def disagree(message):
    markup = types.InlineKeyboardMarkup()
    men = types.InlineKeyboardButton('Главное меню', callback_data='men')
    markup.row(men)
    bot.send_message(message.chat.id, "*❌Вы отказались от покупки.*", parse_mode="Markdown", reply_markup=markup)
# Добавление в бд купленного товара без скидки----------------------------------------------------------------------------------------------------------------------------------
def insert_purchase(product, price, user_id, date):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Получение текущих значений столбцов product и price для пользователя
    cursor.execute("SELECT product, price, contest_participation_date  FROM пользователи WHERE user_id = ?", (user_id,))
    result = cursor.fetchone() # возвращает кортеж (product, price) или None
    if result is not None:
        current_product, current_price, current_date = result
    else:
        current_product, current_price, current_date = '', '', ''

    # Добавление новых значений к текущим
    new_product = current_product + ', ' + product if current_product else product
    new_price = str(current_price) + ', ' + str(price) if current_price else str(price)
    new_date = str(current_date) + ', ' + str(date) if current_date else str(date)
    # Обновление значений столбцов product и price для пользователя
    cursor.execute("UPDATE пользователи SET product = ?, price = ?, contest_participation_date = ? WHERE user_id = ?",
                   (new_product, new_price, new_date, user_id))
    conn.commit()
    conn.close()


#кал беки
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'prev_button1':
        prev_button1(callback.message)
    if callback.data == 'next_button1':
        next_button1(callback.message)
    if callback.data == 'prev_button':
        prev_button(callback.message)
    if callback.data == 'next_button':
        next_button(callback.message)
    if callback.data == 'buy_product':
        buy_product(callback.message)
    if callback.data == 'agree':
        agree(callback.message)
    if callback.data == 'disagree':
        disagree(callback.message)
    if callback.data == 'men':
        men(callback.message)
    if callback.data == 'contacts':
        contacts(callback.message)
    if callback.data == 'subscriptions':
        subscriptions(callback.message)
    if callback.data == 'psw':
        psw(callback.message)
    if callback.data == 'prev_button4':
        prev_button4(callback.message)
    if callback.data == 'next_button4':
        next_button4(callback.message)
    if callback.data == 'info':
        info(callback.message)
    if callback.data == 'key':
        key(callback.message)
    if callback.data == 'fin':
        fin(callback.message)
    if callback.data == 'per':
        per(callback.message)
    if callback.data == 'pod':
        pod(callback.message)
    if callback.data == 'prev_bu':
        prev_bu(callback.message)
    if callback.data == 'next_bu':
        next_bu(callback.message)

@bot.message_handler(func=lambda message: message.text == 'Личный кабинет')
def handle_personal_cabinet(message):
    user_id = message.chat.id

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Получаем данные пользователя из базы данных
    cursor.execute("SELECT * FROM пользователи WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()

    if user_data is None:
        bot.send_message(message.chat.id, "Вы еще не зарегистрированы.")
        return

    # Разбираем данные пользователя
    username = user_data[1]
    email = user_data[2]
    phone = user_data[3]
    full_name = user_data[4]
    registration = user_data[6]


    # Формируем информацию о пользователе
    personal_info = f'*Личный кабинет*:\n\n' \
                    f'*Логин*: _{username}_\n' \
                    f'*Имя*: _{full_name}_\n' \
                    f'*Email*: _{email}_\n' \
                    f'*Дата регистрации*: _{registration}_\n'\
                    f'*Контактный телефон*: _{phone}_\n'




    markup = types.InlineKeyboardMarkup()
    subscriptions = types.InlineKeyboardButton('Подписки', callback_data='subscriptions')
    contacts = types.InlineKeyboardButton('Контакты', callback_data='contacts')
    psw = types.InlineKeyboardButton('Пароль', callback_data='psw')

    markup.row(subscriptions, contacts)
    markup.row(psw)

    bot.send_message(message.chat.id, personal_info, reply_markup=markup, parse_mode="Markdown")

    conn.close()


def contacts(message):
    bot.send_message(message.chat.id, "*Email*: hello@digitaled.info\n*Support*: support@digitaled.info\n*Site*: Digitaled.info", parse_mode="Markdown")


def subscriptions(message):
    user_id = message.chat.id

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Получаем данные пользователя из базы данных
    cursor.execute("SELECT * FROM пользователи WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()

    if user_data is None:
        bot.send_message(message.chat.id, "У вас нету подписок")
        return

    # Разбираем данные пользователя
    data = user_data[11]
    sub = user_data[12]
    price = user_data[13]

    # Формируем информацию о пользователе
    personal_info = f'*Ваши подписки*:\n\n'\
                    f'*Название*: _{sub}_\n'\
                    f'*Дата оформления*: _{data}_\n\n' \
                    f'*Мои оплаты*: _{price}_\n\n' \
                    f'*Дата платежа*: _{data}_\n'

    bot.send_message(message.chat.id, personal_info, parse_mode="Markdown")

    conn.close()








passwords2 = {}  # Словарь для хранения паролей по идентификатору пользователяpasswords = {}  # Словарь для хранени
def psw(message):
    user_id = message.chat.id

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Получаем данные пользователя из базы данных
    cursor.execute("SELECT * FROM пользователи WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()

    if user_data is None:
        bot.send_message(message.chat.id, "Вы еще не зарегистрированы.")
        return

    psw_value = user_data[5]
    pyperclip.copy(psw_value)
    keyboard = telebot.types.InlineKeyboardMarkup()
    copy_button = telebot.types.InlineKeyboardButton("Скопировать", callback_data="copy_passw")
    keyboard.add(copy_button)
    bot.send_message(message.chat.id, text=sekpas + " " + psw_value, reply_markup=keyboard, parse_mode='Markdown')
    passwords2[user_id] = psw_value




# Обработка нажатия на кнопку Образование
@bot.message_handler(func=lambda message: message.text == 'Образование')
def handle_education(message):
    markup = types.InlineKeyboardMarkup()
    channel_button = types.InlineKeyboardButton('Канал', url='https://t.me/+I2GA5vUkLmc2MTNi')
    chat_button = types.InlineKeyboardButton('Чат', url='https://t.me/+zIYKF6WCdekzY2My')

    bot.send_message(message.chat.id, '*Образование:*', parse_mode="Markdown")

    global index
    index = 1
    btn_prev = types.InlineKeyboardButton('⬅️', callback_data='prev_button')
    btn_next = types.InlineKeyboardButton('➡️', callback_data='next_button')
    btn_index = types.InlineKeyboardButton(f'{index}/{total_images}', callback_data='current_index')
    markup.row(btn_prev, btn_index, btn_next)
    markup.row(channel_button, chat_button)

    file = open('./image1.png', 'rb')
    bot.send_photo(message.chat.id, file, caption="*Название*: _Digital education_\n*Описание*: _Описание продукта Digital education_", reply_markup=markup, parse_mode="Markdown")
    file.close()

#отслеживание индексов предыдущей кнопки
def prev_button(message):
    global index
    index -= 1
    if index < 1:
        index = total_images
    change_image(message, index)

#отслеживание индексов следующей кнопки
def next_button(message):
    global index
    index += 1
    if index > total_images:
        index = 1
    change_image(message, index)

#слайдер с товарами
def change_image(message, index):
    markup = types.InlineKeyboardMarkup()
    btn_prev = types.InlineKeyboardButton('⬅️', callback_data='prev_button')
    btn_next = types.InlineKeyboardButton('➡️', callback_data='next_button')
    channel_button = types.InlineKeyboardButton('Канал', url='https://t.me/+I2GA5vUkLmc2MTNi')
    chat_button = types.InlineKeyboardButton('Чат', url='https://t.me/+zIYKF6WCdekzY2My')
    btn_index = types.InlineKeyboardButton(f'{index}/{total_images}', callback_data='current_index')
    markup.row(btn_prev, btn_index, btn_next)
    markup.row(channel_button, chat_button)

    caption = image_captions[index]

    if index == 1:
        with open('image1.png', 'rb') as file:
            bot.edit_message_media(
                chat_id=message.chat.id, message_id=message.id, media=types.InputMediaPhoto(file), reply_markup=markup
            )
            bot.edit_message_caption(chat_id=message.chat.id, message_id=message.id, caption=caption,
                                     reply_markup=markup, parse_mode="Markdown")
    elif index == 2:
        with open('image2.png', 'rb') as file:
            bot.edit_message_media(
                chat_id=message.chat.id, message_id=message.id, media=types.InputMediaPhoto(file), reply_markup=markup
            )
            bot.edit_message_caption(chat_id=message.chat.id, message_id=message.id, caption=caption,
                                     reply_markup=markup, parse_mode="Markdown")
    elif index == 3:
        with open('image3.png', 'rb') as file:
            bot.edit_message_media(
                chat_id=message.chat.id, message_id=message.id, media=types.InputMediaPhoto(file), reply_markup=markup
            )
            bot.edit_message_caption(chat_id=message.chat.id, message_id=message.id, caption=caption,
                                     reply_markup=markup, parse_mode="Markdown")


# Нажатие на кнопку "Приобрести" при показе продукта без скидки


# Обработка нажатия на кнопку Наши проекты
@bot.message_handler(func=lambda message: message.text == 'Наши проекты')
def handle_our_projects(message):
    markup = types.InlineKeyboardMarkup()
    video = types.InlineKeyboardButton('Видео студия', url='https://instagram.com/fresh.ms?igshid=NTc4MTIwNjQ2YQ==')
    brain = types.InlineKeyboardButton('Brain University ', url='https://Brainuniversity.ru')

    markup.row(video)
    markup.row(brain)

    bot.send_message(message.chat.id, '*Наши проекты*:', reply_markup=markup, parse_mode='Markdown')




# Обработка нажатия кнопки "Назад"
@bot.callback_query_handler(func=lambda call: call.data == 'back')
def handle_back(callback_query):
    markup = create_main_menu_markup()
    bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
text='Добро пожаловать в главное меню!', reply_markup=markup)



#Админка---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------

@bot.message_handler(commands=['adminka'])
def admin_start(message):
    bot.send_message(message.chat.id, '*Привет админ*:',
                     parse_mode='Markdown')
    bot.send_message(message.chat.id, '*Добро пожаловать в бот администратора Digital Education*:', parse_mode='Markdown')
    bot.send_message(message.chat.id, '*Введите ваш пароль*:',
                     parse_mode='Markdown')
    bot.register_next_step_handler(message, pass_adm)  # Передаем объект message, а не строку

def pass_adm(message):
    pass_adm = message.text
    user_id = message.from_user.id  # Добавляем получение user_id из message

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE пользователи SET pass_adm = ? WHERE user_id = ?", (pass_adm, user_id))
    conn.commit()
    conn.close()
    print(pass_adm)
    bot.send_message(message.chat.id, 'Поздравляем, вы успешно авторизовались в системе!', parse_mode='Markdown')
    bot.send_message(message.chat.id, 'Меню админа /adminmenu', parse_mode='Markdown')

@bot.message_handler(commands=['adminmenu'])
def adminmen(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    prog = types.KeyboardButton('Проекты')
    Stat = types.KeyboardButton('Статистика')
    cab = types.KeyboardButton('Личный кабинет')
    markup.add(prog, Stat, cab)

    bot.send_message(message.chat.id, '👋🏻*Добро пожаловать в главное меню админа!*', reply_markup=markup, parse_mode='Markdown')


@bot.message_handler(func=lambda message: message.text == 'Проекты')
def progect4(message):
    markup1 = types.InlineKeyboardMarkup()


    info = types.InlineKeyboardButton('Обобщенная информация', callback_data='info')
    key = types.InlineKeyboardButton('Ключевая по ученикам', callback_data='key')
    fin = types.InlineKeyboardButton('Финансы', callback_data='fin')
    per = types.InlineKeyboardButton('Переходы', callback_data='per')
    pod = types.InlineKeyboardButton('Подписки', callback_data='pod')

    markup1.row(info)
    markup1.row(key)
    markup1.row(fin, per, pod)

    bot.send_message(message.chat.id, '*_*', parse_mode="Markdown", reply_markup=markup1)

def key(message):
    bot.send_message(message.chat.id, ke, parse_mode="Markdown")

def fin(message):
    bot.send_message(message.chat.id, fi, parse_mode="Markdown")

def per(message):
    bot.send_message(message.chat.id, pe, parse_mode="Markdown")

indexsub = 1
total_indexsub = 5
captionsub = " "
def pod(message):
    global indexsub
    global captionsub

    if indexsub == 1:
        captionsub = "1 день"
    elif indexsub == 2:
        captionsub = "7 дней"
    elif indexsub == 3:
        captionsub = "1 месяц"
    elif indexsub == 4:
        captionsub = "1 год"
    elif indexsub == 5:
        captionsub = "Все время"

    markup = types.InlineKeyboardMarkup()
    btn_pr = types.InlineKeyboardButton('⬅️', callback_data='prev_bu')
    btn_ne = types.InlineKeyboardButton('➡️', callback_data='next_bu')
    btn_in = types.InlineKeyboardButton(f'{captionsub}', callback_data='btn_in')
    markup.row(btn_pr, btn_in, btn_ne)

    bot.send_message(message.chat.id, po, reply_markup=markup, parse_mode="Markdown")

def prev_bu(message):
    global indexsub
    global total_indexsub
    indexsub -= 1
    if indexsub < 1:
        indexsub = total_indexsub
    change_text(message, indexsub)

def next_bu(message):
    global indexsub
    global total_indexsub
    indexsub += 1
    if indexsub > total_indexsub:
        indexsub = 1
    change_text(message, indexsub)

def change_text(message, indexsub):
    global captionsub

    if indexsub == 1:
        captionsub = "1 день"
    elif indexsub == 2:
        captionsub = "7 дней"
    elif indexsub == 3:
        captionsub = "1 месяц"
    elif indexsub == 4:
        captionsub = "1 год"
    elif indexsub == 5:
        captionsub = "Все время"

    markup = types.InlineKeyboardMarkup()
    btn_pr = types.InlineKeyboardButton('⬅️', callback_data='prev_bu')
    btn_ne = types.InlineKeyboardButton('➡️', callback_data='next_bu')
    btn_in = types.InlineKeyboardButton(f'{captionsub}', callback_data='btn_in')
    markup.row(btn_pr, btn_in, btn_ne)

    if indexsub == 1:
            bot.edit_message_caption(chat_id=message.chat.id, message_id=message.id, caption=po,
                                     reply_markup=markup, parse_mode="Markdown")
    elif indexsub == 2:
            bot.edit_message_caption(chat_id=message.chat.id, message_id=message.id, caption=po,
                                     reply_markup=markup, parse_mode="Markdown")
    elif indexsub == 3:
            bot.edit_message_caption(chat_id=message.chat.id, message_id=message.id, caption=po,
                                     reply_markup=markup, parse_mode="Markdown")
    elif indexsub == 4:
            bot.edit_message_caption(chat_id=message.chat.id, message_id=message.id, caption=po,
                                     reply_markup=markup, parse_mode="Markdown")
    elif indexsub == 5:
            bot.edit_message_caption(chat_id=message.chat.id, message_id=message.id, caption=po,
                                     reply_markup=markup, parse_mode="Markdown")





index4 = 1
total_images4 = 3

def info(message):
    bot.send_message(message.chat.id, '*Проекты*', parse_mode="Markdown")
    global index4
    index4 = 1
    markup = types.InlineKeyboardMarkup()
    btn_prev4 = types.InlineKeyboardButton('⬅️', callback_data='prev_button4')
    btn_next4 = types.InlineKeyboardButton('➡️', callback_data='next_button4')
    btn_index4 = types.InlineKeyboardButton(f'{index4}/{total_images4}', callback_data='current_index4')
    markup.row(btn_prev4, btn_index4, btn_next4)

    file = open('./image1.png', 'rb')
    bot.send_photo(message.chat.id, file,
                   caption="*Название*: _Digital education_\n*Описание*: _Описание продукта Digital education_\n*Стоимость*: 100",
                   reply_markup=markup, parse_mode="Markdown")
    file.close()


def prev_button4(message):
    global index4
    index4 -= 1
    if index4 < 1:
        index4 = total_images4
    change_image4(message, index4)

def next_button4(message):
    global index4
    index4 += 1
    if index4 > total_images4:
        index4 = 1
    change_image4(message, index4)

def change_image4(message, index4):
    markup = types.InlineKeyboardMarkup()
    btn_prev4 = types.InlineKeyboardButton('⬅️', callback_data='prev_button4')
    btn_next4 = types.InlineKeyboardButton('➡️', callback_data='next_button4')
    btn_index4 = types.InlineKeyboardButton(f'{index4}/{total_images4}', callback_data='current_index4')
    markup.row(btn_prev4, btn_index4, btn_next4)

    caption4 = image_captions2[index4]

    if index4 == 1:
        with open('image1.png', 'rb') as file:
            bot.edit_message_media(
                chat_id=message.chat.id, message_id=message.id, media=types.InputMediaPhoto(file), reply_markup=markup
            )
            bot.edit_message_caption(chat_id=message.chat.id, message_id=message.id, caption=caption4,
                                     reply_markup=markup, parse_mode="Markdown")
    elif index4 == 2:
        with open('image2.png', 'rb') as file:
            bot.edit_message_media(
                chat_id=message.chat.id, message_id=message.id, media=types.InputMediaPhoto(file), reply_markup=markup
            )
            bot.edit_message_caption(chat_id=message.chat.id, message_id=message.id, caption=caption4,
                                     reply_markup=markup, parse_mode="Markdown")
    elif index4 == 3:
        with open('image3.png', 'rb') as file:
            bot.edit_message_media(
                chat_id=message.chat.id, message_id=message.id, media=types.InputMediaPhoto(file), reply_markup=markup
            )
            bot.edit_message_caption(chat_id=message.chat.id, message_id=message.id, caption=caption4,
                                     reply_markup=markup, parse_mode="Markdown")


@bot.message_handler(func=lambda message: message.text == 'Статистика')
def statist(message):
    pass






# Запуск бота
bot.polling(none_stop=True)

