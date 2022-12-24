import os
from dotenv import load_dotenv

# Данный пакет предназначен для экспортирования
# из файла .env в переменные окружения и
# их последующей загрузки

load_dotenv()

# Данный параметр определяет в каком режиме
# будет осуществлятся запуск приложения
# 'development' - в режиме разработчика
# 'production' - в рабочем режиме
APP_SETTINGS = os.environ.get('APP_SETTINGS')
# указываем путь к базе данных
# например postgresql://<имя пользователя>:<пароль>@<хост>/<имя базы данных>
DATABASE_URL = os.environ.get('DATABASE_URL')
