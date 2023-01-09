from api import PetFriends
import pytest


pf = PetFriends()


def generate_string(n):
    return "x" * n


def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'


class TestUpdatePets:
    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.parametrize("name",
                             [
                                 'Мурзик',
                                 generate_string(255),
                                 generate_string(1001),
                                 russian_chars(),
                                 russian_chars().upper(),
                                 special_chars(),
                                 '123'
                             ],
                             ids=[
                                 'custom',
                                 '255 symbols',
                                 'more than 1000 symbols',
                                 'russian',
                                 'RUSSIAN',
                                 'specials',
                                 'digit'
                             ])
    @pytest.mark.parametrize("animal_type",
                             [
                                 'Котэ',
                                 generate_string(255),
                                 generate_string(1001),
                                 russian_chars(),
                                 russian_chars().upper(),
                                 special_chars(),
                                 '123'
                             ],
                             ids=[
                                 'custom',
                                 '255 symbols',
                                 'more than 1000 symbols',
                                 'russian',
                                 'RUSSIAN',
                                 'specials',
                                 'digit'
                             ])
    @pytest.mark.parametrize("age", ['5'], ids=['not 1'])
    @pytest.mark.parametrize("accept", ['application/json', 'application/xml'], ids=['json', 'xml'])
    def test_successful_update_self_pet_info(self, get_key, name, animal_type, age, accept):
        """Проверяем возможность обновления информации о питомце"""

        # Получаем список своих питомцев
        _, my_pets, _ = pf.get_list_of_pets(get_key, "my_pets", "application/json")

        # Если список не пустой, то пробуем обновить его имя, тип и возраст
        if len(my_pets['pets']) > 0:
            status, result, content_type = pf.update_pet_info(get_key, my_pets['pets'][0]['id'], name, animal_type, age,
                                                              accept)

            # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
            assert status == 200
            assert content_type == 'application/json'
            assert result['name'] == name
            assert result['animal_type'] == animal_type
            assert result['age'] == str(age)
        else:
            # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception("There is no my pets")

    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.skip(reason='Тут баг: питомец с некорректными данными успешно обновляется')
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
    def test_update_self_pet_info_negative(self, get_key, name, animal_type, age, accept):
        """Проверяем возможность обновления информации о питомце"""

        # Получаем список своих питомцев
        _, my_pets, _ = pf.get_list_of_pets(get_key, "my_pets", "application/json")

        # Если список не пустой, то пробуем обновить его имя, тип и возраст
        if len(my_pets['pets']) > 0:
            status, result, content_type = pf.update_pet_info(get_key, my_pets['pets'][0]['id'], name, animal_type, age,
                                                              accept)

            # Проверяем что статус ответа = 400
            assert status == 400
        else:
            # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception("There is no my pets")
