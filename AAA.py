# Загрузка библиотек
import requests
from bs4 import BeautifulSoup
import json
import folium

# Получение данных о маршруте
url = 'https://www.google.com/maps/dir/'
params = {
    'api': '1',
    'destination': 'озеро Карачинское',
    'origin': 'Новосибирск'
}
response = requests.get(url, params=params)
soup = BeautifulSoup(response.text, 'html.parser')
script_tag = soup.find('script', {'type': 'application/ld+json'})
print(soup.text)
# data = json.loads(script_tag.string)
#
# # Создание карты и добавление маркера начальной точки
# map_center = data['routes'][0]['legs'][0]['start_location']
# map_center['lat'] += .001
# map_center['lng'] += .001
# map = folium.Map(location=map_center, zoom_start=10)
# folium.Marker(location=map_center).add_to(map)
#
# # Добавление маршрута на карту
# for step in data['routes'][0]['legs'][0]['steps']:
#     location = step['start_location']
#     location['lat'] += .001
#     location['lng'] += .001
#     folium.PolyLine([map_center, location], color='#ff0000').add_to(map)
#
# # Открытие карты в браузере
# map.save('map.html')
