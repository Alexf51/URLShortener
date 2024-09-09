Приложение для сокращения URL, разработанное на Django, позволяет пользователям создавать короткие ссылки, которые перенаправляют на оригинальные URL. База данных создана на PostgreSQL.

Для работы приложения нужно:
1) Установить Django: pip install django psycopg2-binary (django — основной фреймворк, psycopg2-binary — драйвер для работы с PostgreSQL)
2) Настройте базу данных PostgreSQL.
- Создайте базу данных: CREATE DATABASE url; 
- Cоздайте пользователя, например, с именем admin и паролем admin: CREATE USER admin WITH PASSWORD 'admin';
- Затем предоставьте этому пользователю права на созданную базу данных: GRANT ALL PRIVILEGES ON DATABASE url TO admin;
- Убедитесь, что в вашем файле settings.py указаны правильные параметры подключения к базе данных: settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'url',  # Имя вашей базы данных
        'USER': 'admin',  # Имя пользователя
        'PASSWORD': 'admin',  # Пароль пользователя
        'HOST': 'localhost',  # Хост (обычно localhost)
        'PORT': '5432',  # Порт (обычно 5432)
    }
}
- После настройки базы данных выполните миграции, чтобы создать необходимые таблицы: python manage.py migrate
- Теперь вы можете запустить сервер разработки одной командой: python manage.py runserver


Ниже представлено краткое описание основных файлов и их функциональности.
admin.py
Этот файл отвечает за регистрацию модели URL в административной панели Django.
URLAdmin - класс настраивает отображение модели в админ панеле. Он определяет, какие поля будут видны в списке, какие фильтры будут доступны, и как будет производиться поиск.
Модель URL регистрируется с помощью admin.site.register(URL, URLAdmin), что позволяет управлять записями URL через интерфейс администратора.

forms.py
Файл содержит формы для создания URL и регистрации пользователей.
URLForm - Форма для создания нового короткого URL.
UserRegisterForm - Форма для регистрации нового пользователя, включающая поля для имени пользователя, электронной почты и паролей.

models.py
Здесь определена модель URL, которая представляет собой структуру базы данных для хранения информации о сокращенных ссылках.
Поля:
- original_url: Хранит оригинальный URL.
- short_url: Хранит сокращенный URL (уникальный).
- clicks: Счетчик переходов по сокращенной ссылке.
- created_at: Дата и время создания записи.
- user: Связь с моделью пользователя, указывающая, кто создал ссылку.

tests.py
Файл содержит тесты для проверки функциональности приложения.
URLModelTest: Тестирование создания объекта URL и его строкового представления.
URLViewTest: Проверка перенаправления на оригинальный URL и успешного создания нового URL через представление.
UserRegistrationTest: Тестирование процесса регистрации нового пользователя.
UserDetailViewTest: Проверка отображения информации о пользователе.
(Для запуска тестов необходимо настроить settings.py -> DATABASES -> заменить |'USER': 'admin','PASSWORD': 'admin'| на |'USER': 'testuser' 'PASSWORD': 'password'|)

urls.py
Файл определяет маршруты для приложения.
Маршруты: Включает маршруты для главной страницы, списка URL, создания нового URL, регистрации пользователей и административной панели. Каждому маршруту присвоено имя для удобства использования в шаблонах.

views.py
Файл содержит представления, которые обрабатывают запросы и возвращают ответы.
Вот основные:
create_url: Обрабатывает создание нового сокращенного URL. Генерирует короткий URL и сохраняет его в базе данных.
redirect_to_original_url: Перенаправляет пользователя на оригинальный URL по сокращенной ссылке и увеличивает счетчик переходов.
user_list и user_detail: Отображают список пользователей и детали конкретного пользователя соответственно.
url_list и url_detail: Отображают список URL и детали конкретного URL соответственно.

settings.py
Конфигурационный файл проекта Django, включающий настройки базы данных, установленные приложения, middleware и другие параметры.

templates:
Шаблоны страниц со всеми нужными перенаправлениями. В шаблонах также использовал Bootstrap для более практичной и красивой визуализации.
