import requests
from bs4 import BeautifulSoup


def request_streets(cookies_streets, headers_streets):
    try:
        response = requests.get('https://dom.mingkh.ru/novosibirskaya-oblast/novosibirsk/streets/', cookies=cookies_streets, headers=headers_streets)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def extract_street_names(streets_text):
    try:
        soup = BeautifulSoup(streets_text.text, 'html.parser')

        street_names = []
        # Находим все блоки <ul> с классом "list-unstyled list-columns"
        ul_blocks = soup.find_all('ul', class_='list-unstyled list-columns')
        for ul_block in ul_blocks:
            links = ul_block.find_all('a')
            for link in links:
                href = link.get('href')  # Извлекаем значение атрибута "href" (ссылки)
                text = link.text  # Извлекаем текст ссылки
                # Добавьте условие для фильтрации ненужных ссылок
                if not href.startswith('#'):
                    # Извлекаем название улицы (последний элемент после последнего слеша)
                    parts = href.split('/')
                    if len(parts) > 3:
                        street_name = parts[-1]
                        street_names.append(street_name)

        return street_names
    except Exception as e:
        print("Error while extracting street names:", e)
        return []

def fetch_street_data(street_name, connection, cookies_buildings, headers_buildings):
    try:
        response = requests.get(
            'https://dom.mingkh.ru/api/map/house/street/novosibirskaya-oblast/novosibirsk/' + street_name,
            cookies=cookies_buildings,
            headers=headers_buildings,
        )

        if response.status_code == 200:
            data = response.json()
            with connection.cursor() as cursor:
                for feature in data["features"]:
                    year_of_construction = feature["properties"].get(
                        "year")
                    coordinates = None
                    if year_of_construction:
                        coordinates = feature["geometry"]["coordinates"]
                        latitude = coordinates[0]
                        longitude = coordinates[1]
                        insert_query = "INSERT INTO buildings (year_of_construction, latitude, longitude) VALUES (%s, %s, %s)"
                        data_to_insert = (year_of_construction, latitude, longitude)
                        cursor.execute(insert_query, data_to_insert)
                        print("successful")
                    else:
                        print(f"Year of construction not found for {coordinates}")
    except Exception as e:
        print(f"Error while fetching data for street {street_name}:", e)