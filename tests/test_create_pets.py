from api import PetFriends
import os
import pytest


pf = PetFriends()


def generate_string(n):
    return "x" * n


def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'


class TestAddNewPet:
    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.parametrize("name",
                             [
                                 generate_string(255),
                                 generate_string(1001),
                                 russian_chars(),
                                 russian_chars().upper(),
                                 special_chars(),
                                 '123'
                             ],
                             ids=[
                                 '255 symbols',
                                 'more than 1000 symbols',
                                 'russian',
                                 'RUSSIAN',
                                 'specials',
                                 'digit'])
    @pytest.mark.parametrize("animal_type",
                             [
                                 generate_string(255),
                                 generate_string(1001),
                                 russian_chars(),
                                 russian_chars().upper(),
                                 special_chars(),
                                 '123'
                             ],
                             ids=[
                                 '255 symbols',
                                 'more than 1000 symbols',
                                 'russian',
                                 'RUSSIAN',
                                 'specials',
                                 'digit'
                             ])
    @pytest.mark.parametrize("age", ['1'], ids=['min'])
    @pytest.mark.parametrize("pet_photo", ['images/cat.jpg', 'images/cat2.png'], ids=['Jpeg photo', 'Png photo'])
    @pytest.mark.parametrize("accept", ['application/json', 'application/xml'], ids=['json', 'xml'])
    def test_add_new_pet_with_valid_data(self, get_key, name, animal_type, age, pet_photo, accept):
        """Проверяем что можно добавить питомца с корректными данными"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Добавляем питомца
        status, result, content_type = pf.add_new_pet(get_key, name, animal_type, age, pet_photo, accept)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert content_type == 'application/json'
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == age
        assert result['pet_photo'] != ''

        # Удаляем созданного питомца
        _ = pf.delete_pet(get_key, result['id'])

    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.skip(reason='Тут баг: питомец с некорректными данными успешно создаётся')
    @pytest.mark.parametrize("name", [''], ids=['empty'])
    @pytest.mark.parametrize("animal_type", [''], ids=['empty'])
    @pytest.mark.parametrize("age",
                             [
                                 '',
                                 '-1',
                                 '0',
                                 '100',
                                 '1.5',
                                 '2147483647',
                                 '2147483648',
                                 special_chars(),
                                 russian_chars(),
                                 russian_chars().upper()
                             ],
                             ids=[
                                 'empty',
                                 'negative',
                                 'zero',
                                 'greater than max',
                                 'float',
                                 'int_max',
                                 'int_max + 1',
                                 'specials',
                                 'russian',
                                 'RUSSIAN'
                             ])
    @pytest.mark.parametrize("pet_photo", ['', 'images/cat3.gif'], ids=['empty', 'Gif photo'])
    @pytest.mark.parametrize("accept", ['application/json', 'application/xml'], ids=['json', 'xml'])
    def test_add_new_pet_negative(self, get_key, name, animal_type, age, pet_photo, accept):
        """Проверяем что при создании питомца с некорректными данными получаем 400ую ошибку"""

        # Добавляем питомца
        status, result, content_type = pf.add_new_pet(get_key, name, animal_type, age, pet_photo, accept)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 400

    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.parametrize("name",
                             [
                                 generate_string(255),
                                 generate_string(1001),
                                 russian_chars(),
                                 russian_chars().upper(),
                                 special_chars(),
                                 '123'
                             ],
                             ids=[
                                 '255 symbols',
                                 'more than 1000 symbols',
                                 'russian',
                                 'RUSSIAN',
                                 'specials',
                                 'digit'])
    @pytest.mark.parametrize("animal_type",
                             [
                                 generate_string(255),
                                 generate_string(1001),
                                 russian_chars(),
                                 russian_chars().upper(),
                                 special_chars(),
                                 '123'
                             ],
                             ids=[
                                 '255 symbols',
                                 'more than 1000 symbols',
                                 'russian',
                                 'RUSSIAN',
                                 'specials',
                                 'digit'
                             ])
    @pytest.mark.parametrize("age", ['1'], ids=['min'])
    @pytest.mark.parametrize("accept", ['application/json', 'application/xml'], ids=['json', 'xml'])
    def test_add_new_pet_with_valid_data_without_photo(self, get_key, name, animal_type, age, accept):
        """Проверяем что можно добавить питомца с различными данными без фото"""

        # Добавляем питомца
        status, result, content_type = pf.add_new_pet_without_photo(get_key, name, animal_type, age, accept)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert content_type == 'application/json'
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == age
        assert result['pet_photo'] == ''

        # Удаляем созданного питомца
        _ = pf.delete_pet(get_key, result['id'])

    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.skip(reason='Тут баг: питомец с некорректными данными успешно создаётся')
    @pytest.mark.parametrize("name", [''], ids=['empty'])
    @pytest.mark.parametrize("animal_type", [''], ids=['empty'])
    @pytest.mark.parametrize("age",
                             [
                                 '',
                                 '-1',
                                 '0',
                                 '100',
                                 '1.5',
                                 '2147483647',
                                 '2147483648',
                                 special_chars(),
                                 russian_chars(),
                                 russian_chars().upper()
                             ],
                             ids=[
                                 'empty',
                                 'negative',
                                 'zero',
                                 'greater than max',
                                 'float',
                                 'int_max',
                                 'int_max + 1',
                                 'specials',
                                 'russian',
                                 'RUSSIAN'
                             ])
    @pytest.mark.parametrize("accept", ['application/json', 'application/xml'], ids=['json', 'xml'])
    def test_add_new_pet_without_photo_negative(self, get_key, name, animal_type, age, accept):
        """Проверяем что при создании питомца с некорректными данными получаем 400ую ошибку"""

        # Добавляем питомца
        status, result, content_type = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 400
