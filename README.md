# django-simbirsoft
## Тестовый проект для практикума

Инструкция по деплою приложения на вашей машине:
1. Убедитесь, что запущен Docker.
2. Клонируйте в любое удобное место этот репозиторий:
    git clone https://github.com/StanislavGaranzha/django-simbirsoft
3. Перейдите в папку с клонированным репозиторием и сделайте следующее:
- docker-compose up --build - собрать приложение и сделать его первоначальный запуск
- docker-compose down - остановить работу приложения
- docker-compose run web python manage.py migrate - сделать необходимые миграции
- docker-compose up - окончательно запустить приложение.
