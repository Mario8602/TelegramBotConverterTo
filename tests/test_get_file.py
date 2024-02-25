import os
import pytest
from app.handlers import (pdf_to_mp3, pdf_to_image,
                          pdf_to_word, delete_file, create_folder)

TEST_PDF_PATH = os.path.join('tests/data_for_tests', 'test_2.pdf')


@pytest.fixture
def test_dir(tmpdir):
    return str(tmpdir)


def test_pdf_to_mp3(test_dir):
    # Test pdf_to_mp3 function
    pdf_path = os.path.join(test_dir, 'test.pdf')
    mp3_file = pdf_to_mp3(file_path=pdf_path)
    assert os.path.exists(mp3_file)


def test_pdf_to_image(test_dir):
    # Test pdf_to_image function
    pdf_path = os.path.abspath(os.path.join(test_dir, '..', 'data_for_tests', 'test_2.pdf'))
    result = pdf_to_image(file_path=pdf_path, directory=test_dir)
    assert result.startswith('[+]')


def test_pdf_to_word(test_dir):
    # Test pdf_to_word function
    pdf_path = os.path.join(test_dir, 'test.pdf')
    docx_file = os.path.join(test_dir, 'test.docx')
    result = pdf_to_word(file_path=pdf_path, docx_file=docx_file)
    assert os.path.exists(docx_file)


def test_delete_file(test_dir):
    # Test delete_file function
    assert os.path.exists(test_dir)
    delete_file()
    assert not os.path.exists(test_dir)


def test_create_folder(test_dir):
    # Test create_folder function
    folder_name = os.path.join(test_dir, 'test_folder')
    result = create_folder(file_name=folder_name)
    assert os.path.exists(folder_name)
    assert result is None
