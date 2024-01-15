import telebot
from telebot import types
import pandas as pd
import random

from text_emotions import text_emotions

bot = telebot.TeleBot('6385211036:AAE1MR1y5W0PqaGNM-x3w-VPsD4kh2BQIOI')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("Счастливое 😊")
    btn2 = types.KeyboardButton('Грустное 😔')
    btn3 = types.KeyboardButton('Энергичное 😈')
    btn4 = types.KeyboardButton('Спокойное 😑')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.from_user.id, "Выберите ваше настроение или напишите текст чтоб определить ваше настроение, а я подберу для вас песни", reply_markup=markup)


# Обработчик нажатия на кнопку
@bot.message_handler(func=lambda message: True)
def handle_button_click(message):
    if message.text == 'Счастливое 😊':
        bot.send_message(message.chat.id, 'Вот список песен под ваше счастливое настроение:')
        randomTracksHappyMood(message)
    elif message.text == 'Грустное 😔':
        bot.send_message(message.chat.id, 'Вот список песен под ваше грустное настроение:')
        randomTracksSadMood(message)
    elif message.text == 'Энергичное 😈':
        bot.send_message(message.chat.id, 'Вот список песен под ваше энергичное настроение:')
        randomTracksEnergeticMood(message)
    elif message.text == 'Спокойное 😑':
        bot.send_message(message.chat.id, 'Вот список песен под ваше спокойное настроение:')
        randomTracksCalmMood(message)
    else:
        emotions = ['empty', 'sadness', 'enthusiasm', 'neutral', 'worry', 'surprise',
             'love', 'fun', 'hate', 'happiness', 'boredom', 'relief', 'anger']

        emotion = text_emotions(message.text)
        if emotion == emotions[0]:
            bot.send_message(message.chat.id, 'Вот список песен под ваше опустошённое настроение:')
            randomTracksSadMood(message)
        elif emotion == emotions[1]:
            bot.send_message(message.chat.id, 'Вот список песен под ваше грустное настроение:')
            randomTracksSadMood(message)
        elif emotion == emotions[2]:
            bot.send_message(message.chat.id, 'Вот список песен под ваш энтузиазм:')
            randomTracksEnergeticMood(message)
        elif emotion == emotions[3]:
            bot.send_message(message.chat.id, 'Вот список песен под ваше нейтральное настроение:')
            randomTracksCalmMood(message)
        elif emotion == emotions[4]:
            bot.send_message(message.chat.id, 'Вот список песен для вашего волнения:')
            randomTracksCalmMood(message)
        elif emotion == emotions[5]:
            bot.send_message(message.chat.id, 'Вот список песен под вашего удивления:')
            randomTracksHappyMood(message)
        elif emotion == emotions[6]:
            bot.send_message(message.chat.id, 'Вот список песен для вашей любви:')
            randomTracksHappyMood(message)
        elif emotion == emotions[7]:
            bot.send_message(message.chat.id, 'Вот список песен под ваше веселье:')
            randomTracksHappyMood(message)
        elif emotion == emotions[8]:
            bot.send_message(message.chat.id, 'Вот список песен для ненависти:')
            randomTracksEnergeticMood(message)
        elif emotion == emotions[9]:
            bot.send_message(message.chat.id, 'Вот список песен для счастья:')
            randomTracksHappyMood(message)
        elif emotion == emotions[10]:
            bot.send_message(message.chat.id, 'Вот список песен для скуки:')
            randomTracksCalmMood(message)
        elif emotion == emotions[11]:
            bot.send_message(message.chat.id, 'Вот список песен под ваше облегчение:')
            randomTracksCalmMood(message)
        elif emotion == emotions[12]:
            bot.send_message(message.chat.id, 'Вот список песен для злости:')
            randomTracksEnergeticMood(message)




def getTracksSorted():
    tracks = pd.read_csv("tracks_with_moods.csv")
    tracks_sorted = tracks.sort_values(by='popularity', ascending=False)

    selected_features = ["artist", "name", "duration_ms", "mood"]
    tracks_sorted = tracks_sorted[selected_features]
    return tracks_sorted


def randomTracksHappyMood(message):
    tracks = getTracksSorted()
    tracks = tracks[tracks['mood'] == "Happy"].tail(1000)
    selectedTracks = tracks.sample(n=10)
    print(selectedTracks)
    data_list = selectedTracks.values.tolist()
    print(len(data_list))
    for track in data_list:
        bot.send_message(message.chat.id, f'🎵 Название: {track[1]} | Артист : {track[0]} | Длительность: '
                                          f'{track[2] // 1000 // 60}:{track[2] // 1000 % 60 // 10}{track[2] // 1000 % 60 % 10}')


def randomTracksSadMood(message):
    tracks = getTracksSorted()
    tracks = tracks[tracks['mood'] == "Sad"].tail(1000)
    selectedTracks = tracks.sample(n=10)
    print(selectedTracks)
    data_list = selectedTracks.values.tolist()
    print(len(data_list))
    for track in data_list:
        bot.send_message(message.chat.id, f'🎵 Название: {track[1]} | Артист : {track[0]} | Длительность: '
                                          f'{track[2] // 1000 // 60}:{track[2] // 1000 % 60 // 10}{track[2] // 1000 % 60 % 10}')


def randomTracksEnergeticMood(message):
    tracks = getTracksSorted()
    tracks = tracks[tracks['mood'] == "Energetic"].tail(1000)
    selectedTracks = tracks.sample(n=10)
    print(selectedTracks)
    data_list = selectedTracks.values.tolist()
    print(len(data_list))
    for track in data_list:
        bot.send_message(message.chat.id, f'🎵 Название: {track[1]} | Артист : {track[0]} | Длительность: '
                                          f'{track[2] // 1000 // 60}:{track[2] // 1000 % 60 // 10}{track[2] // 1000 % 60 % 10}')


def randomTracksCalmMood(message):
    tracks = getTracksSorted()
    tracks = tracks[tracks['mood'] == "Calm"]
    print(tracks)
    selectedTracks = tracks.sample(n=10)
    print(selectedTracks)
    data_list = selectedTracks.values.tolist()
    print(len(data_list))
    for track in data_list:
        bot.send_message(message.chat.id, f'🎵 Название: {track[1]} | Артист : {track[0]} | Длительность: '
                                          f'{track[2] // 1000 // 60}:{track[2] // 1000 % 60 // 10}{track[2] // 1000 % 60 % 10}')


bot.polling(none_stop=True, interval=0)
