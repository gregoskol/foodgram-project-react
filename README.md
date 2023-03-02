[![foodgram_workflow](https://github.com/gregoskol/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/gregoskol/foodgram-project-react/actions/workflows/foodgram_workflow.yml)
# Foodgram 
## _Продуктовый помощник_
## Описание:
На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Подготовка к установке:
Клонировать репозиторий:
```sh
git clone git@github.com:gregoskol/foodgram-project-react.git
```
Подключиться к удаленному серверу:
```sh
ssh <USER>@<HOST>
```
Установить docker и docker-compose:
```sh
sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
Скопировать файлы docker-compose.yaml, nginx.conf и папку docs/ из проекта на сервер в home/<USER>/
```sh
scp ./<FILENAME> <USER>@<HOST>:/home/<USER>/...
```
Добавить в Secrets GitHub Actions переменные окружения (пример в infra/.env.sample), а также:
*DOCKER_USERNAME, DOCKER_PASSWORD  - логин и пароль с DockerHub
*USER, HOST, PASSPHRASE, SSH_KEY - имя пользователя, пароль, ключ SSH и ip удаленного сервера
*TELEGRAM_TO, TELEGRAM_TOKEN - токены чата и бота в Telegram

## Установка:
При пуше в ветку main запустится Workflow:
*Проверка кода на соответствие PEP8
*Сборка и пуш образов на Docker Hub
*Деплой проекта на сервер
*Уведомление в Telegram об успешном завершении Workflow
После завершения Workflow:
Подключиться к удаленному серверу:
```sh
ssh <USER>@<HOST>
```
Выполнить миграции:
```sh
docker-compose exec backend python manage.py migrate --noinput
```
Создать суперпользователя:
```sh
docker-compose exec backend python manage.py createsuperuser
```

## Развернутый проект:
http://158.160.12.177/
login: admin@yandex.ru 
password: 123