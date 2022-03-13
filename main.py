
import dp as dp
import telebot
import mysql.connector
from pprint import pprint
from telebot import types

bot = telebot.TeleBot("5294575459:AAEka_AvMS8OiHDX8BoDvvDHrJdKDRVfWiw")
group_id = "1704651548"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="abc",
    database="tour"
)

cursor = db.cursor()

user_date = {}


class User:
    def __init__(self, first_name):
        self.first_name = first_name
        self.last_name = ''
        self.end_name = ''
        self.phone = ''
        self.photo_id1 = 0
        self.photo_id2 = 0
        self.photo_id3 = 0


# если /help, /start
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('/about')
    itembtn2 = types.KeyboardButton('/registratsiya')
    itembtn3 = types.KeyboardButton('/регистрация')
    markup.add(itembtn1, itembtn2, itembtn3)

    bot.send_message(message.chat.id, "Здравствуйте "
                     + message.from_user.first_name
                     + ", я бот, который найдет вам гида, а также жилье.",
                     reply_markup=markup)
    bot.send_message(message.chat.id, "Salom "
                     + message.from_user.first_name
                     + "hi, I am a bot\nI will find you the guide and house ",
                     reply_markup=markup)


# /about
@bot.message_handler(commands=['about'])
def send_about(message):
    bot.send_message(message.chat.id,
                     "the owner of this project: AR")
    bot.send_message(message.chat.id,
                     " More info:\nt.me/ar1234567890")


# /registratsiya
@bot.message_handler(commands=["registration"])
def user_start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, "Your name:")
    bot.register_next_step_handler(msg, first_name_step)


def first_name_step(message):
    try:
        users_id = message.from_user.id
        user = user_date[users_id] = User(message.text)
        msg = bot.send_message(message.chat.id, "Your surname:")
        bot.register_next_step_handler(msg, last_name_step)
    except Exception as e:
        bot.reply_to(message, 'if bot is not working,\nWrite:\n@Asad_2209')


def last_name_step(message):
    try:
        users_id = message.from_user.id
        user = user_date[users_id]
        user.last_name = message.text
        msg = bot.send_message(message.chat.id, "Father's name")
        bot.register_next_step_handler(msg, end_name_step)
    except Exception as e:
        bot.reply_to(message, 'if bot is not working,\nWrite:\n@Asad_2209')


def end_name_step(message):
    try:
        users_id = message.from_user.id
        user = user_date[users_id]
        user.end_name = message.text
        msg = bot.send_message(message.chat.id, "Your phone number")
        bot.register_next_step_handler(msg, phone_step)
    except Exception as e:
        bot.reply_to(message, 'if bot is not working,\nWrite:\n@Asad_2209')


def phone_step(message):
    try:
        users_id = message.from_user.id
        user = user_date[users_id]
        user.phone = message.text
        msg = bot.send_message(message.chat.id, "your birthday")
        bot.register_next_step_handler(msg, photo1_step)
    except Exception as e:
        bot.reply_to(message, 'if bot is not working,\nWrite:\n@Asad_2209')


def photo1_step(message):
    try:
        if message.content_type == 'photo':
            users_id = message.from_user.id
            user = user_date[users_id]
            user.photo_id1 = message.photo[-1].file_id
            msg = bot.send_message(message.chat.id, "Please, send photo 3.5*4.5")
            bot.register_next_step_handler(msg, photo2_step)
        else:
            bot.reply_to(message, 'please send IMAGE!!!')
            bot.register_next_step_handler(message, photo1_step)
    except Exception as e:
        bot.reply_to(message, 'if bot is not working,\nWrite:\n@Asad_2209')


def photo2_step(message):
    try:
        if message.content_type == 'photo':
            users_id = message.from_user.id
            user = user_date[users_id]
            user.photo_id2 = message.photo[-1].file_id
            msg = bot.send_message(message.chat.id, "Passport, please")
            bot.register_next_step_handler(msg, photo3_step)
        else:
            bot.reply_to(message, 'please, send IMAGE!!!')
            bot.register_next_step_handler(message, photo2_step)
    except Exception as e:
        bot.reply_to(message, 'if bot is not working,\nWrite:\n@Asad_2209')


def photo3_step(message):
    try:
        users_id = message.from_user.id
        user = user_date[users_id]
        user.photo_id3 = message.photo[-1].file_id

        sql = "INSERT INTO users_uzb (first_name, last_name, end_name, phone) values (%s, %s, %s, %s)"
        val = (user.first_name, user.last_name, user.end_name, user.phone)
        cursor.execute(sql, val)

        db.commit()

        bot.send_message(message.chat.id, "You have registered fully.")
        bot.send_message(group_id,
                         '\nName: ' + user.first_name + '\nSurname: ' + user.last_name + '\nFathers name: ' + user.end_name + '\nPhone number: ' + user.phone)
        bot.send_photo(group_id, user.photo_id1)
        bot.send_photo(group_id, user.photo_id2)
        bot.send_photo(group_id, user.photo_id3)

    except Exception as e:
        bot.reply_to(message, 'if bot is not working,\nWrite:\n@Asad_2209')


# /регистрация
@bot.message_handler(commands=["регистрация"])
def user_start1(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, "Ваше имя")
    bot.register_next_step_handler(msg, first_name_step_rus)


def first_name_step_rus(message):
    try:
        users_id = message.from_user.id
        user = user_date[users_id] = User(message.text)
        msg = bot.send_message(message.chat.id, "Вашa фамилия")
        bot.register_next_step_handler(msg, last_name_step_rus)
    except Exception as e:
        bot.reply_to(message, 'бот не работает, пожалуйста, свяжитесь с @Asad_2209')


def last_name_step_rus(message):
    try:
        users_id = message.from_user.id
        user = user_date[users_id]
        user.last_name = message.text
        msg = bot.send_message(message.chat.id, "Имя вашего отца")
        bot.register_next_step_handler(msg, end_name_step_rus)
    except Exception as e:
        bot.reply_to(message, 'бот не работает, пожалуйста, свяжитесь с @Asad_2209')


def end_name_step_rus(message):
    try:
        users_id = message.from_user.id
        user = user_date[users_id]
        user.end_name = message.text
        msg = bot.send_message(message.chat.id, "Ваш номер телефона (рабочий)")
        bot.register_next_step_handler(msg, phone_step_rus)
    except Exception as e:
        bot.reply_to(message, 'бот не работает, пожалуйста, свяжитесь с @Asad_2209')


def phone_step_rus(message):
    try:
        users_id = message.from_user.id
        user = user_date[users_id]
        user.phone = message.text
        msg = bot.send_message(message.chat.id, "SPRAVKA")
        bot.register_next_step_handler(msg, photo1_step_rus)
    except Exception as e:
        bot.reply_to(message, 'бот не работает, пожалуйста, свяжитесь с @Asad_2209')


def photo1_step_rus(message):
    try:
        if message.content_type == 'photo':
            users_id = message.from_user.id
            user = user_date[users_id]
            user.photo_id1 = message.photo[-1].file_id
            msg = bot.send_message(message.chat.id, "Фото размером 3,5х4,5")
            bot.register_next_step_handler(msg, photo2_step_rus)
        else:
            bot.reply_to(message, 'пожалуйста, пришлите фото!!!')
    except Exception as e:
        bot.reply_to(message, 'бот не работает, пожалуйста, свяжитесь с @Asad_2209')


def photo2_step_rus(message):
    try:
        if message.content_type == 'photo':
            users_id = message.from_user.id
            user = user_date[users_id]
            user.photo_id2 = message.photo[-1].file_id
            msg = bot.send_message(message.chat.id, "Копия свидетельства о рождении или паспорта.")
            bot.register_next_step_handler(msg, photo3_step_rus)
        else:
            bot.reply_to(message, 'пожалуйста, пришлите фото!!!')
    except Exception as e:
        bot.reply_to(message, 'бот не работает, пожалуйста, свяжитесь с @Asad_2209')


def photo3_step_rus(message):
    try:
        users_id = message.from_user.id
        user = user_date[users_id]
        user.photo_id3 = message.photo[-1].file_id

        sql = "INSERT INTO users_rus (first_name, last_name, end_name, phone) values (%s, %s, %s, %s)"
        val = (user.first_name, user.last_name, user.end_name, user.phone)
        cursor.execute(sql, val)

        db.commit()

        bot.send_message(message.chat.id, "Вы зарегистрированы")
        bot.send_message(group_id,
                         '\nИмя: ' + user.first_name + '\nФамилия: ' + user.last_name + '\nИмя отца: ' + user.end_name + '\nНомер: ' + user.phone)
        bot.send_photo(group_id, user.photo_id1)
        bot.send_photo(group_id, user.photo_id2)
        bot.send_photo(group_id, user.photo_id3)

    except Exception as e:
        bot.reply_to(message, 'бот не работает, пожалуйста, свяжитесь с @Asad_2209')


bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()




@dp.message_handler(commands="target")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["guider", "tourist"]
    keyboard.add(*buttons)
    await message.answer("Who are you?", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "guider")
async def guider(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Tashkent", "Samarkand", "Bukhara"]
    keyboard.add(*buttons)
    await message.reply("Perfect! Please, send the location")

@dp.message_handler(lambda message: message.text == "tourist")
async def tourist(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Tashkent ", "Samarkand ", "Bukhara "]
    keyboard.add(*buttons)
    await message.reply("Perfect! Please, send the location, where you want to be")


@dp.message_handler(lambda message: message.text == "Tashkent")
async def guider(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["0", "50 000 - 150 000", "150 000 - 300 000"]
    keyboard.add(*buttons)
    await message.reply("Perfect! Select the price, you want to get:")


@dp.message_handler(lambda message: message.text == "Samarkand")
async def tourist(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["0 ", "50 000-150 000", "150 000-300 000"]
    keyboard.add(*buttons)
    await message.reply("Perfect! Select the price, you want to get:")



@dp.message_handler(lambda message: message.text == "Bukhara")
async def guider(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [" 0", "50000 - 150000", "150000 - 300000"]
    keyboard.add(*buttons)
    await message.reply("Perfect! Select the price, you want to get:")


@dp.message_handler(lambda message: message.text == "Tashkent ")
async def tourist(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["0 $", "5$-15$", "15$-30$"]
    keyboard.add(*buttons)
    await message.reply("Perfect! Select the price, you want to give:")



@dp.message_handler(lambda message: message.text == "Samarkand ")
async def tourist(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["0 $ ", "5$ - 15$", "15$ - 30$"]
    keyboard.add(*buttons)
    await message.reply("Perfect! Select the price, you want to give:")



@dp.message_handler(lambda message: message.text == "Bukhara ")
async def tourist(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["0$", "5$-15$ ", "15$-30$ "]
    keyboard.add(*buttons)
    await message.reply("Perfect! Select the price, you want to give:")



# date

@dp.message_handler(lambda message: message.text == "0")
async def guider(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Monday, 13.03.2022 - Tuesday, 14.03.2022", "Tuesday, 14.03.2022 - Wednesday, 15.03.2022", "Wednesday, 15.03.2022 - Thursday, 16.03.2022"]
    keyboard.add(*buttons)
    await message.reply("Perfect! Select the day, you want to give:")

@dp.message_handler(lambda message: message.text == "0 $")
async def tourist(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Monday, 13.03.2022 - Tuesday, 14.03.2022 ", "Tuesday, 14.03.2022 - Wednesday, 15.03.2022 ", "Wednesday, 15.03.2022 - Thursday, 16.03.2022 "]
    keyboard.add(*buttons)
    await message.reply("Perfect! Select the day:")



# total


@dp.message_handler(lambda message: message.text == "Monday, 13.03.2022 - Tuesday, 14.03.2022")
async def guider(message: types.Message):
    await message.reply("Perfect! Name: Asad Kayumov, city: Tashkent, price: 0")


@dp.message_handler(lambda message: message.text == "Monday, 13.03.2022 - Tuesday, 14.03.2022 ")
async def guider(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["  Yes  ", "No"]
    keyboard.add(*buttons)
    await message.reply("Perfect! We have a suggestion:\nName: Asad Kayumov\nnumber: +998970022036\ncity: Tashkent\nprice: 0\nAre you agree with this variant?")

# if yeeees

@dp.message_handler(lambda message: message.text == "  Yes  ")
async def guider(message: types.Message):

    await message.reply("Perfect! You can arrive to Tashkent and call to number:\n +998970022036")




@dp.message_handler()
async def process_start_command(message: types.Message):
    global dictionary_users  # empty dictionary of users
    print("# User Name:", message.from_user.first_name)
    print("# Last Name:", message.from_user.last_name)
    print("id:", message.from_user.id)
    print("Username:", message.from_user.username)

    print("Text:", message.text)




if __name__ == '__main__':
    bot.polling(none_stop=True)
