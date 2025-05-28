import os

class Config:
    # Путь к базе данных SQLite относительно папки backend
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///airport.db')

    # Отключаем отслеживание изменений SQLAlchemy (рекомендуется)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Секретный ключ для сессий и JWT
    SECRET_KEY = os.getenv('SECRET_KEY', '63f4945d921d599f27ae4fdf5bada3f1')

    # Опционально: настройки JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)

    # Другие возможные настройки, например:
    # DEBUG = True
