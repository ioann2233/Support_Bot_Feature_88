import os
import re
import telebot
import sqlite3
import requests
import subprocess
import speech_recognition as sr
from pydub import AudioSegment
from collections import defaultdict

TELEGRAM_TOKEN = '7621398388:AAEGYUI_JwtfYtfPbDrfb3oh25ATULJR380'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_sessions = defaultdict(dict)

def create_database():
    conn = sqlite3.connect('user_requests.db', check_same_thread=False)  
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        request_text TEXT,
        request_type TEXT,
        location TEXT,
        incident_type TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

def log_request(chat_id, request_text, request_type, location, incident_type):
    conn = sqlite3.connect('user_requests.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''INSERT INTO user_requests (chat_id, request_text, request_type, location, incident_type)
               VALUES (?, ?, ?, ?, ?)''',
            (chat_id, request_text, request_type, location, incident_type)
        )
        conn.commit()
    finally:
        conn.close()

def extract_location(text):
    match = re.search(r'\b(?:улица|ул\.|ул|улице)\s+([А-ЯЁа-яё\s]+)', text, re.IGNORECASE)
    return match.group(0) if match else None

def determine_incident_type(text):
    incident_keywords = {
        'ДТП': ['авария', 'столкновение', 'ДТП'],
        'ЗАТОР': ['пробка', 'затор', 'трафик'],
        'ДОРОЖНЫЕ РАБОТЫ': ['ремонт', 'дорожные работы', 'строительство'],
        'ДРУГОЕ': []
    }
    for incident, keywords in incident_keywords.items():
        if any(keyword.lower() in text.lower() for keyword in keywords):
            return incident
    return 'ДРУГОЕ'

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    user_sessions[chat_id] = {'state': 'waiting_for_input'}
    bot.send_message(
        chat_id,
        "Привет! Пожалуйста, отправьте сообщение в следующем формате:\n"
        "- Местоположение: укажите улицу (например, 'улица Ленина')\n"
        "- Тип инцидента: выберите из следующих вариантов: ДТП, ЗАТОР, ДОРОЖНЫЕ РАБОТЫ, ДРУГОЕ\n\n"
        "Пример: 'На улице Ленина произошла авария, образовался затор.'"
    )

@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def handle_text(message):
    chat_id = message.chat.id
    request_text = message.text.strip()

    location = extract_location(request_text)
    incident_type = determine_incident_type(request_text)

    try:
        if location and incident_type != 'ДРУГОЕ':
            log_request(chat_id, request_text, "text", location, incident_type)
            bot.send_message(chat_id, f"Ваш запрос был записан:\nМестоположение: {location}\nТип инцидента: {incident_type}")
        else:
            bot.send_message(
                chat_id,
                "Не удалось определить местоположение или тип инцидента. Пожалуйста, следуйте следующему формату:\n"
                "- Местоположение: укажите улицу (например, 'улица Ленина')\n"
                "- Тип инцидента: выберите из следующих вариантов: ДТП, ЗАТОР, ДОРОЖНЫЕ РАБОТЫ, ДРУГОЕ\n\n"
                "Пример: 'На улице Ленина произошла авария, образовался затор.'"
            )
    except Exception as e:
        bot.send_message(chat_id, "Произошла ошибка при обработке запроса. Попробуйте позже.")

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    chat_id = message.chat.id
    try:
        file_info = bot.get_file(message.voice.file_id)
        file_path = file_info.file_path
        file_url = f'https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}'

        voice_file = f'voice_{chat_id}.ogg'
        wav_file = f'voice_{chat_id}.wav'

        response = requests.get(file_url)
        if response.status_code == 200:
            with open(voice_file, 'wb') as f:
                f.write(response.content)

            AudioSegment.from_ogg(voice_file).export(wav_file, format='wav')

            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_file) as source:
                audio = recognizer.record(source)
                try:
                    recognized_text = recognizer.recognize_google(audio, language='ru-RU')
                    location = extract_location(recognized_text)
                    incident_type = determine_incident_type(recognized_text)

                    if location and incident_type != 'ДРУГОЕ':
                        log_request(chat_id, recognized_text, "voice", location, incident_type)
                        bot.send_message(chat_id,
                            f"Благодарим Вас. Ваш голосовой запрос был записан:\n"
                            f"Местоположение: {location}\n"
                            f"Тип инцидента: {incident_type}")
                    else:
                        bot.send_message(chat_id,
                            "Не удалось определить местоположение или тип инцидента из голосового сообщения. "
                            "Отправьте текстовое сообщение.")
                except sr.UnknownValueError:
                    bot.send_message(chat_id, "Не удалось распознать голосовое сообщение.")
                except sr.RequestError as e:
                    bot.send_message(chat_id, f"Ошибка распознавания: {e}")

            os.remove(voice_file)
            os.remove(wav_file)
    except Exception as e:
        bot.send_message(chat_id, "Произошла ошибка при обработке голосового сообщения.")

def main():
    create_database()
    print("Бот запущен...")
    bot.polling(none_stop=True, timeout=60, long_polling_timeout=60, interval=0)
if __name__ == "__main__":
    main()