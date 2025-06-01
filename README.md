AIRWAY — система онлайн-бронирования авиабилетов
Описание
AIRWAY — это веб-приложение для поиска, бронирования авиабилетов, управления пользователями и администрирования авиарейсов.

Основные возможности
Поиск и бронирование авиабилетов онлайн

Регистрация и вход пользователей

Личный кабинет с историей и управлением бронированиями

Админ-панель для управления рейсами, пользователями, аэропортами и самолетами

Онлайн-табло вылетов

Установка и запуск
1. Клонируйте проект
git clone https://github.com/yourname/airport-project.git
cd airport-project
2. Установите зависимости для backend (Flask)
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
# или
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
3. Инициализируйте базу данных
Создайте SQLite-базу данных с помощью миграций или скриптов.

Пример:
flask db upgrade
4. Запустите сервер backend
flask run
5. Установите зависимости и запустите frontend (Vue + Vite)
cd ../frontend/airport-project
npm install
npm run dev
6. Откройте приложение
Перейдите в браузере по адресу http://localhost:5173/

Структура проекта
backend/ — серверная часть на Flask

frontend/airport-project/ — клиентская часть на Vue 3 + Vuetify + Vite

Контакты
Для вопросов и поддержки: your.email@example.com
