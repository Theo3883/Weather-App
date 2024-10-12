from django.shortcuts import render
import requests
import datetime
api_key = '733b193adb4e8a2e9e7434d95e330aeb'

def index(request):
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&exclude={}&appid={}'

    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        # Fetch weather and forecast for city1
        weather_data1= fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url)

        # Fetch weather and forecast for city2, if provided
        if city2:
            weather_data2 = fetch_weather_and_forecast(city2, api_key, current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        # Context to pass to the template
        context = {
            'weather_data1': weather_data1,
            'weather_data2': weather_data2,
        }

        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    # Format the current weather URL with the city and API key
    current_weather_url = current_weather_url.format(city, api_key)

    response = requests.get(current_weather_url.format(city, api_key))
    if response.status_code != 200:
        return None
    
    response_data = response.json()
    
    '''# Extract latitude and longitude from the current weather response
    lat, lon = response_data['coord']['lat'], response_data['coord']['lon']

    # Format the forecast URL with latitude, longitude, and API key
    part = 'minutely'
    forecast_url = forecast_url.format(lat,lon,part,api_key)

    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()'''


    weather_data = {
        'city': city,
        'temperature': round(response_data['main']['temp'] - 273.15, 2),  
        'description': response_data['weather'][0]['description'],
        'icon': response_data['weather'][0]['icon'],
    }

    '''# Structure the daily forecasts 
    daily_forecasts = []
    for daily_data in forecast_data['daily'][:5]:
        daily_forecasts.append({
            'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
            'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
            #'description': daily_data['weather'][0]['description'],
            #'icon': daily_data['weather'][0]['icon'],
        })
    '''
    return weather_data
