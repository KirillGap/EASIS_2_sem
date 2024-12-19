from django.shortcuts import render, redirect
from django.conf import settings
import os
import fitz  # PyMuPDF
from nltk.tokenize import sent_tokenize

from .forms import UploadFileForm
from .functions import det_language
from .methods import classic_document, listDocument
from .machine_translation import TextTranslation
from .synt_frequancy_list import get_word_statistics
from .tree_constructor import build_tree_for_sentence

raw_text = ''
translated_text = ''

current_translator = TextTranslation()


def upload_file(request):
    """
    Функция для загрузки файла и сохранения его на сервере.
    После загрузки файла пользователь будет перенаправлен на страницу с результатами анализа.
    """
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Сохранение файла
            handle_uploaded_file(request.FILES['file'])

            # Перенаправление на страницу анализа
            return redirect('analys', file_name=request.FILES['file'].name)
    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})


def handle_uploaded_file(f):
    """
    Сохраняем загруженный файл на сервере.
    """
    project_root = settings.BASE_DIR
    save_path = os.path.join(project_root, 'uploaded_files', f.name)

    # Сохраняем файл на сервере
    with open(save_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def analyse_file(request, file_name):
    """
    Функция для анализа загруженного файла: извлечение текста и определение языка.
    """
    context = {'name': file_name}

    project_root = settings.BASE_DIR
    file_path = os.path.join(project_root, 'uploaded_files', file_name)

    # Получение текста из файла (PDF или текстовый файл)
    raw_text = get_raw_text(file_path)

    # Определение языка текста (ЛР2)
    language = det_language(raw_text)
    context.update({'language': language})

    # Оформление отчётов (ЛР3)
    list_res = listDocument(raw_text)
    save_list_path = os.path.join(settings.MEDIA_ROOT, 'results', 'listDocument.txt')
    with open(save_list_path, 'w', encoding='utf-8') as file:
        file.write(list_res)
    listFile = f"{settings.MEDIA_URL}results/listDocument.txt"

    classic_res = classic_document(raw_text)
    save_list_path = os.path.join(settings.MEDIA_ROOT, 'results', 'classicDocument.txt')
    with open(save_list_path, 'w', encoding='utf-8') as file:
        file.write(classic_res)
    classicFile = f"{settings.MEDIA_URL}results/classicDocument.txt"

    context.update(
        {
            'classicDocumentFile': classicFile,
            'listDocumentFile': listFile
        }
    )

    # Машинный перевод (ЛР4)
    translated_text = current_translator.translate_text(raw_text)
    context.update({'translatedText': translated_text})

    word_stats = get_word_statistics(raw_text, lang='english')
    word_stats1 = get_word_statistics(translated_text, lang='russian')
    context.update({'word_data': word_stats + word_stats1})

    sentences = sent_tokenize(raw_text, language='english')
    sentences = [(sent, num) for sent, num in zip(sentences, range(len(sentences)))]
    context.update({'sentences': sentences})

    return render(
        request,
        'analys.html',
        context=context,
    )


def get_raw_text(file_path):
    """
    Получаем текст из файла, поддерживаем PDF и обычные текстовые файлы.
    """
    # Проверяем, является ли файл PDF
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)

    # Если файл обычный текстовый, читаем его как текст
    else:
        text = ''
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text


def extract_text_from_pdf(pdf_path):
    """
    Извлекаем текст из PDF-файла с использованием PyMuPDF.
    """
    doc = fitz.open(pdf_path)
    text = ''

    # Извлекаем текст со всех страниц
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()

    return text


def tree_view(request, file_name, sentence):
    build_tree_for_sentence(sentence)

    # Перенаправляем обратно на анализ
    return redirect('analys', file_name=file_name)

