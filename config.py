import settings
# Конфигурационный файл Flask приложения


class Config(object):
    # Определяет, включен ли режим отладки
    # В случае если включен, flask будет показывать
    # подробную отладочную информацию. Если выключен -
    # - 500 ошибку без какой либо дополнительной информации.
    DEBUG = False
    # Включение защиты против "Cross-site Request Forgery (CSRF)"
    CSRF_ENABLED = True
    # Случайный ключ, которые будет исползоваться для подписи
    # данных, например cookies.
    SECRET_KEY = 'YOUR_RANDOM_SECRET_KEY'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Папка для сохранения загруженных файлов (изображений)
    UPLOAD_FOLDER = 'app/uploads/'


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    # URI используемая для подключения к базе данных
    SQLALCHEMY_DATABASE_URI = settings.DATABASE_URL


CONFIGS = {
    "production": ProductionConfig(),
    "development": DevelopmentConfig(),
}
