import os.path
import numpy as np

import pdfplumber
from gtts import gTTS
from pathlib import Path
from PIL import Image
from pdf2image import convert_from_path
from pdf2docx import Converter


def pdf_to_mp3(file_path='test.pdf', language='ru'):
    """ Конвертировать PDF-файл в mp3-файл"""
    if os.path.exists(file_path) and Path(file_path).suffix == '.pdf':

        # открытие файла с использованием pdfplumber для
        # получения подробных сведений о каждом текстовом символе
        # extract - собирает все символьные объекты страницы в одну строку

        with pdfplumber.PDF(open(file=file_path, mode='rb')) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
        text = ''.join(pages)
        text = text.replace('\n', '')

        # преобразования текста в речь Google Translate

        my_audio = gTTS(text=text, lang=language, slow=False)
        file_name = Path(file_path).stem
        my_audio.save(fr'mp_files\{file_name}.mp3')
        return f'{file_name}.mp3'
    else:
        return FileNotFoundError


def pdf_to_image(file_path='test.pdf', directory='received_file'):
    """ Конвертирует PDF-файл в фотографии, постранично """
    output_folder = r'jpeg_files/'
    file_name = Path(file_path).stem
    images = convert_from_path(f'{directory}/{file_name}.pdf',
                               poppler_path=r'/usr/bin/',
                               output_folder=output_folder, fmt='jpeg',
                               output_file=f'{file_name}')
    return f'[+] {file_name}.jpg saved success!'


def pdf_to_word(file_path='test.pdf', docx_file='test.docx'):
    """ Конвертировать PDF-файл в word-файл """
    file = Converter(file_path)
    file.convert(docx_file)
    file.close()
    return file


def filesfolder(file_path1=r'mp_files'):
    """ Количество файлов в определённой папке """
    for root, dirs, files in os.walk(file_path1):
        return len(files)


def delete_file():
    """Очистка файлов из списка папок"""
    try:
        for i in ['received_file', 'mp_files', 'docx_files',
                  'jpeg_files', 'bw_photo', 'resize_photo', 'square_photo']:
            for root, dirs, files in os.walk(fr'{i}'):
                for filename in files:
                    os.remove(fr'{i}\{filename}')
    except Exception as ex:
        return ex


def create_folder(file_name='testfile'):
    """Создание папки в директории, для файлов \
        полученных тг-ботом, если папки не существует"""
    try:
        new_path = Path(file_name)
        if Path.is_dir(new_path):
            return 'No folder'
        return Path.mkdir(new_path)
    except Exception as ex:
        return ex


def photo_noir_convert(file_path='test.jpg', file_name='test1.jpeg'):
    """ Конвертировать изображение из цветного в чёрно-белое"""
    a = np.asarray(Image.open(fp=file_path, mode='r'), dtype='uint8')
    b = np.array([[[0.2989, 0.587, 0.114]]])
    sums = np.round(np.sum(a * b, axis=2)).astype(np.uint8)
    k = np.repeat(sums, 3).reshape(a.shape)
    Image.fromarray(k).save(fr'bw_photo\{file_name}')


def resize_image(file_name='test.jpeg', resize_x=0, resize_y=0):
    """ Изменение размера изображение в 2 раза """
    resize_in_percent = 50
    resize_x = resize_x
    resize_y = resize_y

    if resize_y or resize_x != 0:
        resize_in_percent = False

    sent_img = Image.open(fr'received_file\\{file_name}')
    (width, height) = sent_img.size
    print(width, height)

    if resize_in_percent:
        percent = 100 / resize_in_percent
        width_size = int(float(sent_img.size[0]) / percent)
        height_size = int(float(sent_img.size[1]) / percent)
    else:
        if resize_x:
            delta = resize_x / float(sent_img.size[0])
            width_size = int(float(sent_img.size[0]) * delta)
            height_size = int(float(sent_img.size[1]) * delta)
        else:
            delta = resize_y / float(sent_img.size[1])
            width_size = int(float(sent_img.size[0]) * delta)
            height_size = int(float(sent_img.size[1]) * delta)
    sent_img = sent_img.resize((width_size, height_size))
    sent_img.save(f'resize_photo\\{file_name}')


def square_image(file_name='test.jpeg') -> Image:
    """Функция для обрезки изображения по центру"""
    image = Image.open(fr'received_file\{file_name}')
    img_width, img_height = image.size
    image = image.crop(((img_width - min(image.size)) // 2,
                        (img_height - min(image.size)) // 2,
                        (img_width + min(image.size)) // 2,
                        (img_height + min(image.size)) // 2))
    image.save(f'square_photo\\{file_name}', quality=95)
