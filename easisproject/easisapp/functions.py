from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from collections import Counter
import re
import asyncio


model_name = "spolivin/lang-recogn-model"

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)


async def neural_predict_language(text):
    # Tokenize the input text with padding and truncation
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding=True).to(device)

    with torch.no_grad():
        try:
            outputs = model(**inputs)
        except RuntimeError as e:
            print(f"RuntimeError: {e}")
            raise

    logits = outputs.logits
    predicted_language = torch.argmax(logits, dim=1).item()

    # Map the predicted class to a language
    if predicted_language == 3:
        return 'English'
    if predicted_language == 12:
        return 'Russian'
    else:
        return 'None'


# Частотные слова для русского и английского языков
async def detect_language_by_frequency(text):
    english_words = {'the', 'of', 'and', 'to', 'a',
                     'in', 'that', 'is', 'was', 'he',
                     'it', 'with', 'for', 'on', 'you',
                     'as', 'at', 'by', 'this', 'an'
    }

    russian_words = {'и', 'в', 'на', 'с', 'по', 'что',
                     'это', 'он', 'она', 'я', 'для',
                     'от', 'не', 'бы', 'так', 'да',
                     'как', 'мы', 'вы', 'они'
    }

    # Приводим текст к нижнему регистру и удаляем все символы кроме букв и пробелов
    words = re.findall(r'\b\w+\b', text.lower())

    # Подсчитываем частоту встречаемых слов в тексте
    word_count = Counter(words)

    english_count = sum(word_count[word] for word in words if word in english_words)
    russian_count = sum(word_count[word] for word in words if word in russian_words)

    # Определяем язык
    if english_count > russian_count:
        return 'English'
    elif russian_count > english_count:
        return 'Russian'
    else:
        return 'Undetermined'


async def detect_language_by_short_words(text):
    # Короткие слова для английского и русского языков
    english_short_words = {'a', 'the', 'of', 'and', 'in', 'to', 'is', 'it', 'on', 'for', 'with', 'as', 'at'}
    russian_short_words = {'и', 'в', 'на', 'с', 'по', 'что', 'для', 'от', 'не', 'так', 'да'}

    # Приводим текст к нижнему регистру и разбиваем на слова
    words = re.findall(r'\b\w+\b', text.lower())

    # Считаем количество коротких слов для каждого языка
    english_short_count = sum(1 for word in words if word in english_short_words)
    russian_short_count = sum(1 for word in words if word in russian_short_words)

    # Определяем язык
    if english_short_count > russian_short_count:
        return 'English'
    elif russian_short_count > english_short_count:
        return 'Russian'
    else:
        return 'Undetermined'


async def detect_language(text):
    result = dict()

    result['neural'] = await neural_predict_language(text)
    result['short_words'] = await detect_language_by_short_words(text)
    result['freq'] = await detect_language_by_frequency(text)

    return result


def det_language(text):
    a = asyncio.run(detect_language(text))
    return a
