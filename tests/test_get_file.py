import pytest

from reunion import pdf_to_mp3


@pytest.mark.parametrize("file_input, file_output", [
    ('stin.pdf', 'stin.mp3'),
    ('Reao.pdf', 'Reao.mp3')
])
def test_pdf_or_not(file_input, file_output):
    assert pdf_to_mp3(file_path=file_input) == file_output\



@pytest.mark.parametrize("file_input, error_file", [
    ('sad.pdf', FileNotFoundError),
])
def test_pdf_error(file_input, error_file):
    assert pdf_to_mp3(file_path=file_input) == error_file