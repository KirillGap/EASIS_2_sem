import torch
from transformers import pipeline, MarianTokenizer,  AutoModelForSeq2SeqLM
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk import pos_tag

import pymorphy3

class TextTranslation:
    def __init__(self):
        model_name = "Helsinki-NLP/opus-mt-en-ru"
        self.pipe = pipeline("translation_en_to_ru", model=model_name, tokenizer=model_name)

    def translate_text(self, text, max_chunk_length=400):
        # Разделяем текст на части
        chunks = [text[i:i+max_chunk_length] for i in range(0, len(text), max_chunk_length)]
        # Переводим каждую часть и объединяем результаты
        translated_chunks = [self.pipe(chunk)[0]["translation_text"] for chunk in chunks]
        return " ".join(translated_chunks)
