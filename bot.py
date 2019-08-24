import uuid
import telebot
import os
import crm
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GoToCRM.settings")
import django
django.setup()

from crm.models import Student, Comments

telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}

# TODO: указать token
token = "809058421:AAGBrnzEmFU1AgqK5fb3wUjtZu6YomOenHQ"
bot = telebot.TeleBot(token=token)

data = {}
data2 = {}
gett2 = True
sett = False
gett4 = True
sett2 = False
gett6 = True
s = True
@bot.message_handler(content_types=['text'])
def search(message):
    global gett2, sett, gett4, sett2, s, gett6
    text = message.text
    user = message.chat.id
    gett = ['Пришли']
    gett3 = ['Оставь коммент', 'Напиши коммент', 'Оставь комментарий' 'Напиши комментарий']
    gett5 = ['Поставь']
    for i in gett:
        if i in text:
            gett2 = False
            bot.send_message(user, "Пришлите имя и фамилию")
            return
    for i in gett3:
        if i in text:
            gett4 = False
            s = False
            bot.send_message(user, "Пришлите имя и фамилию")
            return
    for i in gett5:
        if i in text:
            gett6 = False
            s = True
            bot.send_message(user, "Пришлите имя и фамилию")
            return
    if gett6 == False and s == True:
        try:
            name, surname = text.split(' ')
        except:
            bot.send_message(user, "Пришлите имя и фамилию")
            return
        student = Student.objects.filter(name=name, surname=surname).first()
        if student:
            data[user] = student
            print(data)
            bot.send_message(user, "Присылайте фото...")
            sett = True
            gett6 = False
        else:
            bot.send_message(user, "Я не нашел...")
    if gett2 == False and s == True:
        try:
            name, surname = text.split(' ')
        except:
            bot.send_message(user, "Пришлите имя и фамилию")
            return
        student = Student.objects.filter(name=name, surname=surname).first()
        if student:
            bot.send_message(user, "Присылаю фото...")
            bot.send_photo(user, student.photo)
            bot.send_message(user, "ok")
            gett2 = True
            return
        else:
            bot.send_message(user, "Я не нашел...")
    if gett4 == False and gett2 == True:
        try:
            name, surname = text.split(' ')
        except:
            bot.send_message(user, "Пришлите имя и фамилию")
            return

        student = Student.objects.filter(name=name, surname=surname).first()
        if student:
            bot.send_message(user, "Присылайте комментарий...")
            data2[user] = student
            sett2 = True
            return
        else:
            bot.send_message(user, "Я не нашел...")
    if sett2 == True:
        if user not in data2 or sett2 == False:
            bot.send_message(user, "Сначала пришлите имя")
            return
        comment = Comments()
        comment.student = data2[user]
        comment.text = text
        comment.save()
        s = True
        sett2 = False
        gett4 = True
        bot.send_message(user, "ok")

@bot.message_handler(content_types=['photo'])
def photo(message):
    user = message.chat.id

    if user not in data or sett == False:
        bot.send_message(user, "Сначала пришлите имя")
        return

    # скачивание файла
    file_id = message.photo[-1].file_id
    path = bot.get_file(file_id)
    downloaded_file = bot.download_file(path.file_path)

    # узнаем расширение и случайное придумываем имя
    extn = '.' + str(path.file_path).split('.')[-1]
    name = 'avatars/' + str(uuid.uuid4()) + extn

    # создаем файл и записываем туда данные
    with open(name, 'wb') as new_file:
        new_file.write(downloaded_file)

    student = data[user]

    student.photo = name
    student.save()
    bot.send_message(message.chat.id, 'ok')

bot.polling(none_stop=True)