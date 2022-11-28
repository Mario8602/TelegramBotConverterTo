from random import randint

import telebot
from telebot import types

import tempfile
import uuid

from nbconvert import HTMLExporter
from nbformat.v2 import nbformat
from pathlib import Path

from reunion import pdf_to_mp3, photo_noir_convert, pdf_to_image, pdf_to_word, filesFolder, delete_file
import os

bot = telebot.TeleBot("5780381393:AAHsbrC8uV8mib125ZucgCs6WxtNbZWPavE", parse_mode=None)


@bot.message_handler(commands=['start'])
def start(message):
    name = f'Hello, {message.from_user.first_name} {message.from_user.last_name}\nОтправьте свой файл: '
    bot.send_message(message.chat.id, name, parse_mode='html')


# получение файла и дальнейшие пути обработки
@bot.message_handler(content_types=['document'])
def converter(message):
    # сохранение полученного файла и определение типа
    file_info = bot.get_file(message.document.file_id)
    src = r"M:/PythonProjects/tg_bot_convert/received_file/" + message.document.file_name
    file_download = bot.download_file(file_info.file_path)
    with open(src, 'wb') as new_file:
        new_file.write(file_download)
    # filename, file_extension = os.path.splitext(file_info.file_path)
    print(file_info.file_path)

    markup_inline = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton(text='2mp3', callback_data=f'2mp3,name={message.document.file_name}')
    btn2 = types.InlineKeyboardButton(text='2word', callback_data=f'2word,name={message.document.file_name}')
    btn3 = types.InlineKeyboardButton(text='2jpeg', callback_data=f'2jpeg,name={message.document.file_name}')

    markup_inline.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Выберите процедуру', reply_markup=markup_inline)


@bot.message_handler(content_types=['photo'])
def converter(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    print(f'[+] {file_info}')
    file_downloaded = bot.download_file(file_info.file_path)
    file_namee = str(randint(1, 1000))
    src = fr"M:\PythonProjects\tg_bot_convert\received_file\{file_namee}.jpeg"
    with open(src, 'wb') as new_file:
        new_file.write(file_downloaded)

    markup_inline = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton(text='blackout', callback_data=f'blackout,name={file_namee}.jpeg')
    btn2 = types.InlineKeyboardButton(text='compress', callback_data=f'compress,name={file_namee}.jpeg')
    btn3 = types.InlineKeyboardButton(text='2jpeg', callback_data=f'2jpeg,name={file_namee}.jpeg')

    markup_inline.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Выберите процедуру', reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    try:
        if call.message:
            method = call.data.split(',name=')[0]
            file_name = call.data.split(',name=')[1]

            if method == '2mp3':

                bot.send_message(call.message.chat.id, 'Я В ПРОЦЕССЕ..., жди')

                pdf_to_mp3(file_path=r"M:/PythonProjects/tg_bot_convert/received_file/" + file_name, language='ru')
                file = open(fr'M:\PythonProjects\tg_bot_convert\mp_files\{file_name[:-4]}.mp3', 'rb')

                bot.send_document(call.message.chat.id, file)
                bot.send_message(call.message.chat.id, 'GOOD')
                file.close()

            elif method == '2jpeg':
                pdf_to_image(file_path=r"M:/PythonProjects/tg_bot_convert/received_file/" + file_name)
                if filesFolder(r'M:\PythonProjects\tg_bot_convert\jpeg_files') == 1:
                    file = open(fr'M:\PythonProjects\tg_bot_convert\jpeg_files\{file_name[:-4]}0001-1.jpg', 'rb')
                    bot.send_document(call.message.chat.id, file)
                    file.close()
                else:
                    for page in range(filesFolder(r'M:\PythonProjects\tg_bot_convert\jpeg_files')):
                        file = open(fr'M:\PythonProjects\tg_bot_convert\jpeg_files\{file_name[:-4]}0001-{page + 1}.jpg', 'rb')
                        bot.send_document(call.message.chat.id, file)
                        file.close()
                bot.send_message(call.message.chat.id, 'оно?')

            elif method == '2word':
                pdf_to_word(file_path="M:/PythonProjects/tg_bot_convert/received_file/" + file_name,
                            docx_file=fr'M:\PythonProjects\tg_bot_convert\docx_files\{file_name[:-4]}.docx')
                file = open(fr'M:\PythonProjects\tg_bot_convert\docx_files\{file_name[:-4]}.docx', 'rb')
                bot.send_document(call.message.chat.id, file)
                file.close()

            elif method == 'blackout':
                photo_noir_convert(file_path=fr"M:/PythonProjects/tg_bot_convert/received_file/{file_name}", file_name=file_name)
                file = open(fr"M:\PythonProjects\tg_bot_convert\bw_photo\{file_name}", 'rb')
                bot.send_document(call.message.chat.id, file)

            elif method == 'compress':
                photo_noir_convert(file_path=fr"M:/PythonProjects/tg_bot_convert/received_file/{file_name}", file_name=file_name)
                file = open(fr"M:\PythonProjects\tg_bot_convert\bw_photo\{file_name}", 'rb')
                bot.send_document(call.message.chat.id, file)

            else:
                bot.send_message(call.message.chat.id, 'oh, no, pls')

            # delete_file()

    except Exception as ex:
        bot.send_message(call.message.chat.id, 'Я поломаться')
        print(ex)


# try:
#     for i in ['mp_files', 'docx_files', 'pdf_files', 'pdftojpeg']:
#         for root, dirs, files in os.walk(fr"M:\PythonProjects\neiron\{i}"):
#             for filename in files:
#                 os.remove(fr'M:\PythonProjects\neiron\{i}\{filename}')
# except Exception as ex:
#     print(ex)


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == 'да':
        bot.send_message(message.chat.id, 'Дай пять')
    elif message.text.lower() == 'нет':
        bot.send_message(message.chat.id, 'Отстой...')
    elif message.text.lower() == 'удаляй':
        delete_file()
        bot.send_message(message.chat.id, 'I DO IT!!!')
    else:
        bot.send_message(message.chat.id, 'Мне бы твой файл ;)')


bot.infinity_polling()
