## Многофункциональный телеграм-бот

`python3.9.14` `aiogram2.18`  `pyowm==3.3.0` `py-currency-converter-1.2.0`

### Описание
```angular2html
Бот реализует API запросы к нескольким сервисам:
    1. Запрос на получение погоды от сервиса OpenWeatherMap с помощью библиотке pyowm==3.3.0;
    2. Запрос на конвертацию валюты в одну или сразу в несколько других с помощью библиотеки py-currency-converter-1.2.0;
    3. Запрос на получение случайного животного с помощью aiohttp.
Механизм работы с ботом:
    1. По команде /start выпадает меню с инлайн кнопками для выбор интересующего сервис, так же сервисы доступы по обычным командам из списка;
    2. /weather - выводит погоду в городе, который вы отправите в запросе;
    3. /currency_conversion - выводит конвератцию валюты и сумму одной или нескольких валют;
    4. /poll - позволяет создать и отправить опрос в группу, которую необходимо указать в файл .env.dist (переименовать в .env)
    5. /random_image - отправляет случайную картинку с животным (собаками).
```

### Как запустить проект:

#### Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/krivse/Bogdanov_bot.git
```

#### Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
# для OS Lunix и MacOS
source venv/bin/activate

# для OS Windows
source venv/Scripts/activate
```

#### Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
#### Запустить проект:
```angular2html
Переименовать файл .env.dist -> .env. В файле обязательные поля для изменения: BOT_TOKEN, GROUP 
python bot.py
```
#### Запуск проекта в докере:
**_Установить на сервере Docker, Docker Compose_**
```
sudo apt install curl                                   - установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      - скачать скрипт для установки
sh get-docker.sh                                        - запуск скрипта
sudo apt-get install docker-compose-plugin              - последняя версия docker compose
**_В корне проекта переименовать .env.dist в .env и по желанию изменить название BOT_CONTAINER_NAME, BOT_IMAGE_NAME, BOT_NAME, GROUPS (не забыть указать id группы куда будут поститься опросы)_**
```
**_Скопировать на сервер файлы docker-compose.yml, .env. Команды выполняются из корня проекта._**
```
scp docker-compose.yml .env username@IP:/home/username/
# username - имя пользователя на сервере
# IP - публичный IP сервера
```
**_Создать и запустить контейнеры Docker_**
```angular2html
sudo docker compose up -d
```
**_Для остановки контейнеров Docker:_**
```
sudo docker compose down -v      - с их удалением
sudo docker compose stop         - без удаления
```

##### Ivan Krasnikov
