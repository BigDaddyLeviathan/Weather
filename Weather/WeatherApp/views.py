from django.shortcuts import render
from .forms import CityForm
import requests
import json
import datetime

def format_time(time_str):
    dt = datetime.datetime.fromisoformat(time_str)
    return dt.strftime("%d.%m.%Y %H:%M")

# Обработчик запроса для получения данных о погоде
def get_weather(request):
    weather_data = None  # Переменная для хранения данных о погоде
    search_history = json.loads(request.COOKIES.get('search_history', '[]'))  # Получение истории поиска из cookies

    # Проверка наличия города в GET-запросе или в POST-запросе
    city = request.GET.get('city') if 'city' in request.GET else None

    if request.method == 'POST':
        form = CityForm(request.POST)  # Создание формы с данными из POST-запроса
        if form.is_valid():
            city = form.cleaned_data['city']  # Извлечение города из формы
    else:
        form = CityForm(initial={'city': city})  # Создание формы с начальными данными из GET-запроса

    if city:
        # Запрос на получение геокодированных данных (широта и долгота) по названию города
        geocode_url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key=APIKEY"
        geocode_response = requests.get(geocode_url).json()

        if geocode_response['results']:
            location = geocode_response['results'][0]['geometry']  # Извлечение геометрических данных
            latitude = location['lat']
            longitude = location['lng']

            # Запрос на получение данных о погоде по координатам
            weather_url = (f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m"
                           f"&current_weather=true"
                           f"&forecast_hours=12")
            weather_response = requests.get(weather_url).json()

            if 'hourly' in weather_response:
                # Обработка данных о погоде (время и температура)
                weather_data = list(
                    zip([format_time(time_str) for time_str in weather_response['hourly']['time']],
                         weather_response['hourly']['temperature_2m']))
            else:
                weather_data = 'Нет прогноза для вашего города'

            # Обновление истории поиска и сохранение ее в cookies
            if city not in search_history:
                search_history.append(city)
                search_history = search_history[-5:]  # Ограничение истории до последних 5 записей
            response = render(request, 'weather.html',
                              {'form': form, 'weather_data': weather_data, 'search_history': search_history})
            response.set_cookie('search_history', json.dumps(search_history))  # Сохранение истории в cookies
            return response
        else:
            weather_data = 'Ваш город не найден'
    else:
        form = CityForm()

    return render(request, 'weather.html',
                              {'form': form, 'weather_data': weather_data, 'search_history': search_history})