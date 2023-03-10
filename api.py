import json

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from pathlib import Path
from decorators import write_log


class PetFriends:
    """апи библиотека к веб приложению Pet Friends"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    @write_log
    def get_api_key(self, email: str, passwd: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключём пользователя, найденного по указанным email и паролем"""

        headers = {
            'email': email,
            'password': passwd
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    @write_log
    def get_list_of_pets(self, auth_key: json, filter: str, accept: str):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        со списком найденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
        либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
        собственных питомцев"""

        headers = {'auth_key': auth_key['key'], 'accept': accept}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        content_type = res.headers.get('content-type')
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result, content_type

    @write_log
    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str, accept: str):
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type, 'accept': accept}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        content_type = res.headers.get('content-type')
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result, content_type

    @write_log
    def delete_pet(self, auth_key: json, pet_id: str):
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления об успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    @write_log
    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int, accept: str):
        """Метод отправляет запрос на сервер об обновлении данных питомца по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлёнными данными питомца"""

        headers = {'auth_key': auth_key['key'], 'accept': accept}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        content_type = res.headers.get('content-type')
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result, content_type

    @write_log
    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str, accept: str):
        """Метод отправляет (постит) на сервер данные о добавляемом питомце (без фото) и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type, 'accept': accept}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        content_type = res.headers.get('content-type')
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result, content_type

    @write_log
    def add_pet_photo(self, auth_key: json, pet_id: str, pet_photo: str, accept: str):
        """Метод отправляет (постит) на сервер фото питомца и возвращает статус запроса на сервер
        и результат в формате JSON с обновлёнными данными питомца"""

        if Path(pet_photo).suffix == '.png':
            type = 'image/png'
        else:
            type = 'image/jpeg'
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), type)
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type, 'accept': accept}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        content_type = res.headers.get('content-type')
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result, content_type
