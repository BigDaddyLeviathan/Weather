Польззователь заходит на сайт, вводит название города и видит погоду на ближайшие 12 часов в этом городе. Внизу страницы есть история поиска с кликабельными городами для повторного поиска этого города. История поиска сохраняется в cookie, поэтому при повторном посещении сайта снова покажет историю пользователя.

Для перевода названий городов в координаты я использовал API opencagedata. А для погоды API open-meteo, как в задании.
Также сделано автодополнение при вводе города, но работают оно немного странно. Города можно искать как на русском, так и на английском.

Для работы проекта необходимо заменить "APIKEY" в файлах views.py и templates/weather.html на ваш API ключ от https://opencagedata.com. Ну или я дам свой, я просто не знаю сколько пользователей увидит этот проект тут. 
Для запуска надо зайти в папку проекта Weather/weather, где есть файл manage.py, через консоль и ввести команду "python manage.py runserver". После запуска сервера зайти на предложенный в консоли локалхост.
