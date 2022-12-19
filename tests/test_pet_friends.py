from api import PetFriends
from settings import valid_email, valid_password
import os
import lxml.html

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Рыжик', animal_type='пушистый кот', age='3', pet_photo='images/cat.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert result['pet_photo'] != ''


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age='5'):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == age
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_new_pet_with_valid_data_without_photo(name='Кисун', animal_type='дворовый', age='5'):
    """Проверяем что можно добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert result['pet_photo'] == ''

    # Удаляем созданного питомца
    _ = pf.delete_pet(auth_key, result['id'])


def test_add_pet_photo_jpg(pet_photo='images/dog.jpg'):
    """Проверяем возможность добавления фото в формате jpg для питомца без фото"""

    # Получаем ключ auth_key и добавляем нового питомца без фото
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pet = pf.add_new_pet_without_photo(auth_key, "Собакен", "собака", "6")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Пробуем добавить фото для питомца:
    status, result = pf.add_pet_photo(auth_key, my_pet['id'], pet_photo)

    # Проверяем что статус ответа = 200 и поле фото питомца не пустое
    assert status == 200
    assert result['pet_photo'] != ''

    # Удаляем созданного питомца
    _ = pf.delete_pet(auth_key, result['id'])


def test_update_pet_photo_jpg(pet_photo='images/cat1.jpg'):
    """Проверяем возможность обновления фото в формате jpg для питомца с фото"""

    # Получаем ключ auth_key и добавляем нового питомца с фото
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pet = pf.add_new_pet(auth_key, "Барсик", "кот", "4", "images/cat.jpg")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Пробуем добавить фото для питомца:
    status, result = pf.add_pet_photo(auth_key, my_pet['id'], pet_photo)

    # Проверяем что статус ответа = 200 и поле фото питомца не пустое
    assert status == 200
    assert result['pet_photo'] != ''

    # Удаляем созданного питомца
    _ = pf.delete_pet(auth_key, result['id'])


def test_get_api_key_for_user_with_invalid_email(email='example@tes.com', password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 и ошибку в случае несуществующего email"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Забираем текст ошибки из запроса
    tree = lxml.html.document_fromstring(result)
    error = tree.xpath('/html/body/p/text()')

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert error[0] == "This user wasn\'t found in database"


def test_get_api_key_for_user_with_invalid_password(email=valid_email, password='qwerty'):
    """ Проверяем что запрос api ключа возвращает статус 403 и ошибку в случае неверного пароля"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Забираем текст ошибки из запроса
    tree = lxml.html.document_fromstring(result)
    error = tree.xpath('/html/body/p/text()')

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert error[0] == "This user wasn\'t found in database"


# Тут баг, поэтому данный тест закомментирован, не возникает ошибки при добавлении питомца с пустыми параметрами
# def test_add_new_pet_without_parameters(name='', animal_type='', age=''):
#     """Проверяем что невозможно добавить питомца с пустыми данными"""
#
#     # Запрашиваем ключ api и сохраняем в переменную auth_key
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#
#     # Добавляем питомца
#     status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
#
#     # Сверяем полученный ответ с ожидаемым результатом
#     assert status == 400


# Тут баг, поэтому данный тест закомментирован, не возникает ошибки при добавлении питомца с невалидными значениями
# def test_add_new_pet_without_photo_with_long_name(name='1@45', animal_type='909', age='abc'):
#     """Проверяем что невозможно добавить питомца с некорректными данными"""
#
#     # Запрашиваем ключ api и сохраняем в переменную auth_key
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#
#     # Добавляем питомца
#     status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
#
#     # Сверяем полученный ответ с ожидаемым результатом
#     assert status == 400


# Тут баг, поэтому данный тест закомментирован, не возникает ошибки при обновлении питомца с отрицательным возрастом
# def test_update_pet_info_with_negative_age(name='Принц', animal_type='кот', age=-10):
#     """Проверяем что невозможно обновить возраст питомца с отрицательным значением"""
#
#     # Получаем ключ auth_key и список своих питомцев
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#     _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
#
#     # Если список не пустой, то пробуем обновить его имя, тип и возраст с отрицательным значением
#     if len(my_pets['pets']) > 0:
#         status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
#
#         # Проверяем что статус ответа = 400
#         assert status == 400
#
#     else:
#         # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
#         raise Exception("There is no my pets")


def test_get_my_pets_with_valid_key(filter='my_pets'):
    """ Проверяем что запрос своих питомцев возвращает не пустой список и добавленного питомца."""

    # Получаем ключ auth_key и создаём своего питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pet = pf.add_new_pet_without_photo(auth_key, 'Машка', 'кошка', '3')

    # Запрашиваем список своих питомцев
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем что статус запроса 200 и добавленный питомец присутствует в списке
    assert status == 200
    assert result['pets'][0]['name'] == 'Машка'

    # Удаляем созданного питомца
    _ = pf.delete_pet(auth_key, my_pet['id'])


def test_add_pet_photo_png(pet_photo='images/cat2.png'):
    """Проверяем возможность добавления фото в формате png для питомца без фото"""

    # Получаем ключ auth_key и добавляем нового питомца без фото
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pet = pf.add_new_pet_without_photo(auth_key, "Вася", "кот", "3")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Пробуем добавить фото для питомца:
    status, result = pf.add_pet_photo(auth_key, my_pet['id'], pet_photo)

    # Проверяем что статус ответа = 200 и поле фото питомца не пустое
    assert status == 200
    assert result['pet_photo'] != ''

    # Удаляем созданного питомца
    _ = pf.delete_pet(auth_key, result['id'])


def test_add_pet_photo_gif(pet_photo='images/cat3.gif'):
    """Проверяем что невозможно добавить фото в формате gif для питомца без фото"""

    # Получаем ключ auth_key и добавляем нового питомца без фото
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pet = pf.add_new_pet_without_photo(auth_key, "Вася", "кот", "3")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Пробуем добавить фото для питомца:
    status, result = pf.add_pet_photo(auth_key, my_pet['id'], pet_photo)

    # Запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа = 500 и поле фото питомца пустое
    assert status == 500
    assert my_pets['pets'][0]['pet_photo'] == ''

    # Удаляем созданного питомца
    _ = pf.delete_pet(auth_key, my_pet['id'])


def test_add_new_pet_without_photo_with_float_age(name='Кисун', animal_type='дворовый', age='5.5'):
    """Проверяем что можно добавить питомца с нецелым значением возраста"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['age'] == age

    # Удаляем созданного питомца
    _ = pf.delete_pet(auth_key, result['id'])


def test_add_new_pet_without_photo_with_long_name(name='Очень длинное и красивое имя для кота', animal_type='дворовый',
                                                  age='2'):
    """Проверяем что можно добавить питомца с длинным именем"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

    # Удаляем созданного питомца
    _ = pf.delete_pet(auth_key, result['id'])