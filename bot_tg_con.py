from random import randint

import telebot
from telebot import types

from reunion import pdf_to_mp3, photo_noir_convert, pdf_to_image, pdf_to_word, filesFolder, \
    delete_file, create_folder, resize_image, square_image

bot = telebot.TeleBot(r'5780381393:AAHsbrC8uV8mib125ZucgCs6WxtNbZWPavE', parse_mode=None)


@bot.message_handler(commands=['start'])
def start(message):
    delete_file()
    name = f'Hello, {message.from_user.first_name} {message.from_user.last_name}\nОтправьте свой файл: '
    bot.send_message(message.chat.id, name, parse_mode='html')


# получение файла ботом и дальнейшие пути обработки
@bot.message_handler(content_types=['document'])
def converter(message):
    # сохранение полученного файла и определение типа
    delete_file()
    file_info = bot.get_file(message.document.file_id)
    print(file_info)
    create_folder(file_name='received_file')
    src = r'received_file/' + message.document.file_name
    file_download = bot.download_file(file_info.file_path)
    with open(src, 'wb') as new_file:
        new_file.write(file_download)

    markup_inline = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton(text='2mp3', callback_data=f'2mp3,name={message.document.file_name}')
    btn2 = types.InlineKeyboardButton(text='2word', callback_data=f'2word,name={message.document.file_name}')
    btn3 = types.InlineKeyboardButton(text='2jpeg', callback_data=f'2jpeg,name={message.document.file_name}')

    markup_inline.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Выберите процедуру', reply_markup=markup_inline)


@bot.message_handler(content_types=['photo'])
def converter(message):
    delete_file()
    file_info = bot.get_file(message.photo[-1].file_id)
    file_downloaded = bot.download_file(file_info.file_path)
    file_namee = str(randint(1, 1000))
    create_folder(file_name='received_file')
    src = fr'received_file\{file_namee}.jpeg'
    with open(src, 'wb') as new_file:
        new_file.write(file_downloaded)

    markup_inline = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton(text='blackout', callback_data=f'blackout,name={file_namee}.jpeg')
    btn2 = types.InlineKeyboardButton(text='square', callback_data=f'square,name={file_namee}.jpeg')
    btn3 = types.InlineKeyboardButton(text='resize', callback_data=f'resize,name={file_namee}.jpeg')

    markup_inline.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Выберите процедуру', reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    """ В зависимости от выбранной кнопки, возвращает данные и вызывает необходимую функцию для обработки файла"""
    try:
        if call.message:
            method = call.data.split(',name=')[0]
            file_name = call.data.split(',name=')[1]

            if method == '2mp3':

                bot.send_message(call.message.chat.id, 'Обрабатываю...подождите пожалуйста')
                create_folder(file_name='mp_files')
                pdf_to_mp3(file_path=r'received_file/' + file_name, language='ru')
                file = open(fr'mp_files\{file_name[:-4]}.mp3', 'rb')

                bot.send_document(call.message.chat.id, file)
                file.close()

            elif method == '2jpeg':
                create_folder(file_name='jpeg_files')
                pdf_to_image(file_path=r'received_file/' + file_name)
                if filesFolder(r'jpeg_files') == 1:
                    file = open(fr'jpeg_files\{file_name[:-4]}0001-1.jpg', 'rb')
                    bot.send_document(call.message.chat.id, file)
                    file.close()
                else:
                    for page in range(filesFolder(r'jpeg_files')):
                        file = open(fr'jpeg_files\{file_name[:-4]}0001-{page + 1}.jpg', 'rb')
                        bot.send_document(call.message.chat.id, file)
                        file.close()

            elif method == '2word':
                create_folder(file_name='docx_files')
                pdf_to_word(file_path=r'received_file/' + file_name,
                            docx_file=fr'docx_files\{file_name[:-4]}.docx')
                file = open(fr'docx_files\{file_name[:-4]}.docx', 'rb')
                bot.send_document(call.message.chat.id, file)
                file.close()

            elif method == 'blackout':
                create_folder(file_name='bw_photo')
                photo_noir_convert(file_path=fr'received_file/{file_name}', file_name=file_name)
                file = open(fr'bw_photo\{file_name}', 'rb')
                bot.send_document(call.message.chat.id, file)
                file.close()

            elif method == 'square':
                create_folder(file_name='square_photo')
                square_image(file_name)
                file = open(fr'square_photo\\{file_name}', 'rb')
                bot.send_document(call.message.chat.id, file)
                file.close()

            elif method == 'resize':
                create_folder(file_name='resize_photo')
                resize_image(file_name)
                file = open(f'resize_photo\\{file_name}', 'rb')
                bot.send_document(call.message.chat.id, file)
                file.close()

            else:
                bot.send_message(call.message.chat.id, 'oh, no, pls')

    except Exception as ex:
        bot.send_message(call.message.chat.id, 'Error, что то пошло не так...')
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
