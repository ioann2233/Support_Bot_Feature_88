# Телеграм-бот для отчетов о дорожных происшествиях 🚗

Телеграм-бот для сбора и обработки информации о дорожных происшествиях. Бот поддерживает как текстовые, так и голосовые сообщения на русском языке.

## 🚀 Возможности

- ✅ Обработка текстовых сообщений о происшествиях
- 🎤 Распознавание и обработка голосовых сообщений
- 📍 Автоматическое определение местоположения из сообщений
- 🔍 Классификация типов происшествий
- 💾 Сохранение всех отчетов в базе данных SQLite

## 🎯 Поддерживаемые типы происшествий

Бот автоматически определяет следующие типы происшествий:
- 🚨 ДТП (аварии, столкновения)
- 🚦 ЗАТОР (пробки, заторы на дороге)
- 🚧 ДОРОЖНЫЕ РАБОТЫ (ремонт, строительство)
- ❓ ДРУГОЕ (прочие происшествия)

## 📱 Как пользоваться

1. **Запуск бота:**
   - Найдите бота в Telegram
   - Отправьте команду `/start`

2. **Отправка сообщения:**
На улице [название улицы] произошла [тип происшествия]
Пример: "На улице Ленина произошла авария, образовался затор"

4. **Голосовые сообщения:**
- Нажмите кнопку записи голоса
- Опишите ситуацию
- Бот автоматически распознает текст и определит тип происшествия

## 🛠️ Установка и запуск

1. **Клонируйте репозиторий:**
```bash
git clone [URL репозитория]

2. Установите зависимости:
pip install -r requirements.txt

3. Настройте переменные окружения:

Создайте файл .env
Добавьте токен бота:

TELEGRAM_TOKEN=ваш_токен

4. Запустите бота: 
python bot.py

py
📦 Зависимости
Основные:

🤖 pyTelegramBotAPI
🗃️ sqlite3
🌐 requests
🎤 speech_recognition
🔊 pydub
📦 python-dotenv
Системные:

ffmpeg (для работы с аудио)
🔧 Системные требования
Python 3.8+
ffmpeg
Доступ к интернету
Токен Telegram бота
📝 Примечания
Бот работает только с русскоязычными сообщениями
Для корректной работы с голосовыми сообщениями требуется установленный ffmpeg
База данных автоматически создается при первом запуске
🔒 Безопасность
Не публикуйте токен бота в публичном доступе
Храните чувствительные данные в файле .env
Регулярно делайте резервные копии базы данных
📨 Поддержка
По всем вопросам обращайтесь:

📧 [kramivan20@gmail.com]
💬 [@ioan2233]
