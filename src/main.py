from src.utils.parsing import request_streets, fetch_street_data, extract_street_names
from src.utils.database import update_db, create_connection
from src.config import host, user, password, db_name, port
from src.utils.cookies_headers import cookies_streets, cookies_buildings, headers_buildings, headers_streets
import time
import concurrent.futures

streets = request_streets(cookies_streets, headers_streets)

if streets is not None:

    street_names = extract_street_names(streets)

    def main():
        start_time = time.time()

        update_db()

        try:
            connection = create_connection(host, port, user, password, db_name)
            connection.autocommit = True

            # Создаем пул потоков с использованием ThreadPoolExecutor
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                # Запускаем задачи для каждой улицы в отдельном потоке
                futures = [executor.submit(fetch_street_data, street_name, connection, cookies_buildings, headers_buildings) for street_name in street_names]

                # Ожидаем завершения всех задач
                concurrent.futures.wait(futures)

            end_time = time.time()
            full_time = end_time - start_time
            print(f'Время выполнения: {full_time} секунд')

        except Exception as ex:
            print("[INFO] Error", ex)

        finally:
            if connection:
                connection.close()

if __name__ == "__main__":
    main()