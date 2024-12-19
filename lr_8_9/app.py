import speech_recognition as sr
import asyncio
import edge_tts
from transformers import pipeline
from gtts import gTTS

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говорите что-то на французском...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="fr-FR")
        print(f"Распознанный текст: {text}")
        return text
    except Exception as e:
        print(f"Ошибка распознавания: {e}")
        return None



async def text_to_speech1(text, output_file="voice1.mp3"):
    try:
        tts = edge_tts.Communicate(text, voice="en-US-JennyNeural")  # Голос на французском
        await tts.save(output_file)  # Сохраняем аудио
        print(f"Аудио сохранено в файл {output_file}")
    except Exception as e:
        print(f"Произошла ошибка при сохранении файла: {e}")

async def text_to_speech2(text, output_file="voice2.mp3"):
    try:
        tts = edge_tts.Communicate(text, voice="fr-FR-EloiseNeural")  # Голос на французском
        await tts.save(output_file)  # Сохраняем аудио
        print(f"Аудио сохранено в файл {output_file}")
    except Exception as e:
        print(f"Произошла ошибка при сохранении файла: {e}")

async def text_to_speech3(text, output_file="voice3.mp3"):
    try:
        tts = edge_tts.Communicate(text, voice="fr-FR-HenriNeural")  # Голос на французском
        await tts.save(output_file)  # Сохраняем аудио
        print(f"Аудио сохранено в файл {output_file}")
    except Exception as e:
        print(f"Произошла ошибка при сохранении файла: {e}")

def text_to_speech4(text, output_file="voice4.mp3"):
    tts = gTTS(text, lang='fr')
    tts.save(output_file)
    print(f"Аудио сохранено в файл {output_file}")



def main():
    k = -1
    while(True):
        
        print("Приложение для работы с французской речью")
        print("1 - распознавание речи")
        print("2 - генерация речи")
        print("0 - выход")
        k = int(input())
        
        if (k == 1):
            print(k)
            text = recognize_speech()
        elif (k == 2):
            test_text = input("Введите текст на французском: ")
            
            asyncio.run(text_to_speech1(test_text))
            # asyncio.run(text_to_speech2(test_text))
            # asyncio.run(text_to_speech3(test_text))
            # text_to_speech4(test_text)
        elif (k == 0):
            break


main()