import telebot
import random
import json
import re
from telebot import types
from settings import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

films = []
hello = []
hello_text = []


def load():
    global films
    with open("films.json", "r", encoding="utf-8") as fh:
        films = json.load(fh)


def load_hello():
    global hello
    global hello_text
    with open("hello.json", "r", encoding="utf-8") as fh:
        hello = json.load(fh)
    with open("hello_text.json", "r", encoding="utf-8") as fh:
        hello_text = json.load(fh)


def is_part_in_list(str_, words):
    for word in words:
        if word in str_:
            return True
    return False


def save():
    with open("films.json", "w", encoding="utf-8") as fh:
        fh.write(json.dumps(films, ensure_ascii=False))
    print("Наша фильмотека была успешно сохранена в файле films.json")


def sort_films():
    global films
    with open("films.json", "r", encoding="utf-8") as fh:
        films = json.load(fh)
    films.sort()
    with open("films.json", "w", encoding="utf-8") as fh:
        fh.write(json.dumps(films, ensure_ascii=False))


@bot.message_handler(commands=['start'])
def start(message):

    load()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Приветики')
    buttonSort = types.KeyboardButton('Сортировка фильмотеки')
    buttonA = types.KeyboardButton('Добавить фильм в список')
    buttonB = types.KeyboardButton('Фильмотека')
    buttonC = types.KeyboardButton('Случайное кино на вечер')
    buttonD = types.KeyboardButton('Удалить фильм из списка')

    markup.row(button)
    markup.row(buttonA, buttonB)
    markup.row(buttonC, buttonD)
    markup.row(buttonSort)
    bot.send_message(message.chat.id, 'Слушаю 🤖', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_me(message):
    bot.send_message(
        message.chat.id, 'Пока что я умею немного. Но я быстро учусь 🤓')
    bot.send_message(
        message.chat.id, 'Все мои умения внизу ⬇️')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    load_hello()
    if is_part_in_list(message.text, hello_text):
        random_photo = random.choice(hello)
        bot.send_photo(
            message.chat.id, photo=f'{random_photo}')
    elif message.text == "Сортировка фильмотеки":
        sort_films()
        bot.send_message(message.chat.id, "Фильмотека отсортирована ❤️")
    elif message.text == "Фильмотека":
        load()
        bot.send_message(message.chat.id, "Вот список фильмов ⬇️")
        bot.send_message(message.chat.id, "🔸 " + "\n🔸 ".join(films))
    elif message.text == "Случайное кино на вечер":
        load()
        random_film = random.choice(films)
        if " " in random_film:
            random_film_cor = re.sub(' ', '+', random_film)
            markup = types.InlineKeyboardMarkup()
            btn_my_site = types.InlineKeyboardButton(
                text='Кинопоиск', url=f"https://www.kinopoisk.ru/index.php?kp_query={random_film_cor}")
            markup.add(btn_my_site)
            bot.send_message(message.chat.id, "😜 " +
                             random_film, reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup()
            btn_my_site = types.InlineKeyboardButton(
                text='Кинопоиск', url=f"https://www.kinopoisk.ru/index.php?kp_query={random_film}")
            markup.add(btn_my_site)
            bot.send_message(message.chat.id, "😜 " +
                             random_film, reply_markup=markup)
    elif message.text == 'Добавить фильм в список':
        bot.send_message(
            message.chat.id, 'Напишите "Добавь <Название фильма>"')
    elif 'Добавь ' in message.text:
        load()
        message.text = re.sub('Добавь ', '', message.text)
        if message.text in films:
            bot.send_message(message.chat.id, '⚠️ Этот фильм уже есть в списке')
        else:
            films.append(message.text)
            save()
            sort_films()
            bot.send_message(
                message.chat.id, f'✅ Фильм "{message.text}" добавлен в список')
            bot.send_message(message.chat.id, "Фильмотека отсортирована ❤️")
    elif message.text == 'Удалить фильм из списка':
        bot.send_message(message.chat.id, 'Напишите мне название фильма')
    elif message.text in films:
        films.remove(message.text)
        save()
        bot.send_message(message.chat.id, f'❌ Фильм "{message.text}" удалён')
    else:
        bot.send_message(message.from_user.id,
                         "Я тебя не понимаю. 😔 Воспользуйся командой /help")


bot.polling()
