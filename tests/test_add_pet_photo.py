from api import PetFriends
import os
import pytest


pf = PetFriends()


class TestAddPetPhoto:
    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.parametrize("pet_photo", ['images/dog.jpg', 'images/cat2.png'], ids=['Jpeg photo', 'Png photo'])
    @pytest.mark.parametrize("accept", ['application/json', 'application/xml'], ids=['json', 'xml'])
    def test_add_pet_photo_jpg(self, get_key, pet_photo, accept):
        """Проверяем возможность добавления фото в формате jpg и png для питомца без фото"""

        # Добавляем нового питомца без фото
        _, my_pet, _ = pf.add_new_pet_without_photo(get_key, "Собакен", "собака", "6", "application/json")

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Пробуем добавить фото для питомца:
        status, result, content_type = pf.add_pet_photo(get_key, my_pet['id'], pet_photo, accept)

        # Проверяем что статус ответа = 200 и поле фото питомца не пустое
        assert status == 200
        assert content_type == 'application/json'
        assert result['pet_photo'] != ''

        # Удаляем созданного питомца
        _ = pf.delete_pet(get_key, result['id'])

    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.parametrize("pet_photo", ['images/cat1.jpg', 'images/cat2.png'], ids=['Jpeg photo', 'Png photo'])
    @pytest.mark.parametrize("accept", ['application/json', 'application/xml'], ids=['json', 'xml'])
    def test_update_pet_photo_jpg(self, get_key, pet_photo, accept):
        """Проверяем возможность обновления фото в формате jpg и png для питомца с фото"""

        # Добавляем нового питомца с фото
        _, my_pet, _ = pf.add_new_pet(get_key, "Барсик", "кот", "4", "images/cat.jpg", "application/json")

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Пробуем добавить фото для питомца:
        status, result, content_type = pf.add_pet_photo(get_key, my_pet['id'], pet_photo, accept)

        # Проверяем что статус ответа = 200 и поле фото питомца не пустое
        assert status == 200
        assert content_type == 'application/json'
        assert result['pet_photo'] != ''

        # Удаляем созданного питомца
        _ = pf.delete_pet(get_key, result['id'])

    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.parametrize("pet_photo", ['images/newcat.ico', 'images/cat3.gif'], ids=['Ico photo', 'Gif photo'])
    @pytest.mark.parametrize("accept", ['application/json', 'application/xml'], ids=['json', 'xml'])
    def test_add_pet_photo_negative(self, get_key, pet_photo, accept):
        """Проверяем что невозможно добавить фото в формате gif для питомца без фото"""

        # Добавляем нового питомца без фото
        _, my_pet, _ = pf.add_new_pet_without_photo(get_key, "Вася", "кот", "3", "application/json")

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Пробуем добавить фото для питомца:
        status, result, content_type = pf.add_pet_photo(get_key, my_pet['id'], pet_photo, accept)

        # Запрашиваем список своих питомцев
        _, my_pets, _ = pf.get_list_of_pets(get_key, "my_pets", accept)

        # Проверяем что статус ответа = 500 и поле фото питомца пустое
        assert status == 500
        assert my_pets['pets'][0]['pet_photo'] == ''

        # Удаляем созданного питомца
        _ = pf.delete_pet(get_key, my_pet['id'])
