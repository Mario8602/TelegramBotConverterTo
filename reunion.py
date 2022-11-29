from gtts import gTTS
import pdfplumber
import os.path
from pathlib import Path

import numpy as np
from PIL import Image

from pdf2image import convert_from_path
from pdf2docx import Converter


def pdf_to_mp3(file_path='test.pdf', language='ru'):
    """ Конвертировать PDF-файл в mp3-файл"""
    if os.path.exists(file_path) and Path(file_path).suffix == '.pdf':

        # открытие файла с использованием pdfplumber для получения подробных сведений о каждом текстовом символе
        # extract - cобирает все символьные объекты страницы в одну строку

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


# def main():
#     file_path = input("\nУкажите путь до файла: ")
#     language = input("\nУкажите язык: ")
#     print(pdf_to_mp3(file_path=file_path, language=language))
#
#
# if __name__ == "__main__":
#     main()


def pdf_to_image(file_path='test.pdf'):

    output_folder = r'jpeg_files/'
    file_name = Path(file_path).stem
    images = convert_from_path(fr'jpeg_files\{file_name}.pdf',
                               poppler_path=r'M:\poppler-22.04.0\Library\bin',
                               output_folder=output_folder, fmt='jpeg',
                               output_file=f'{file_name}')
    return f'[+] {file_name}.jpg saved succes!'


# def main():
#     print(pdf_to_image(r'M:\PythonProjects\neiron\pdf_files\Reao.pdf'))
#
#
# if __name__ == "__main__":
#     main()


def pdf_to_word(file_path='test.pdf', docx_file='test.docx'):
    """ Конвертировать PDF-файл в word-файл"""
    file = Converter(file_path)
    file.convert(docx_file)
    file.close()
    return file


# def main():
#     print(pdf_to_word(r'M:\PythonProjects\neiron\pdf_files\Reao.pdf'))
#
#
# if __name__ == "__main__":
#     main()


def filesFolder(file_path1=r"mp_files"):
    for root, dirs, files in os.walk(file_path1):
        return len(files)


def delete_file():
    """Очистка файлов из списка папок"""
    try:
        for i in ['received_file', 'mp_files', 'docx_files', 'jpeg_files', 'bw_photo', '']:
            for root, dirs, files in os.walk(fr"{i}"):
                for filename in files:
                    os.remove(fr'{i}\{filename}')
    except Exception as ex:
        return ex


def create_folder(file_name='testfile'):
    """Создание папки в директории, для файлов полученных тг-ботом, если папки не существует"""
    try:
        new_path = Path(file_name)
        if Path.is_dir(new_path):
            return 'No folder'
        return Path.mkdir(new_path)
    except Exception as ex:
        return ex


def photo_noir_convert(file_path='test.jpg', file_name='test1.jpeg'):
    """ Конвертировать изображение из цветного в чёрнобелое"""
    a = np.asarray(Image.open(fp=file_path, mode='r'), dtype='uint8')
    b = np.array([[[0.2989, 0.587, 0.114]]])
    sums = np.round(np.sum(a * b, axis=2)).astype(np.uint8)
    k = np.repeat(sums, 3).reshape(a.shape)
    Image.fromarray(k).save(fr"bw_photo\{file_name}")


# def main():
#     print(photo_noir_convert(file_path=r"M:\PythonProjects\tg_bot_convert\received_file\9d0ecc90b315444a927f50b6eeaa91e6.jpeg"))
#
#
# if __name__ == "__main__":
#     main()


def photo_oua():
    pass


def mourin(n):
    """ Список простых чисел до n """
    c = 0
    result = []
    for i in range(1, n+1):
        a = 0
        for j in range(1, i+1):
            if i % j == 0:
                a += 1
                c = j
            if a == 2:
                if c not in result:
                    result.append(c)
    return result


def check_number(number=11):
    return [f'Yes, {number} is simple number' if len([i for i in range(1, number + 1) if number % i == 0]) == 2 else 'Not s1mple']\


def compress():
    pass