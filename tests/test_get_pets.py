from api import PetFriends
import pytest


pf = PetFriends()


def generate_string(n):
    return "x" * n


def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


# Здесь мы взяли 20 популярных китайских иероглифов
def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'


def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'


class TestGetPets:
    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.parametrize("filter", ['', 'my_pets'], ids=['empty string', 'only my pets'])
    @pytest.mark.parametrize("accept", ['application/json', 'application/xml'], ids=['json', 'xml'])
    def test_get_all_pets_with_valid_key(self, get_key, filter, accept):
        """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

        # Создаём своего питомца
        _, my_pet, _ = pf.add_new_pet_without_photo(get_key, 'Машка', 'кошка', '3', 'application/json')

        # Запрашиваем список питомцев
        status, result, content_type = pf.get_list_of_pets(get_key, filter, accept)

        if filter == '':
            assert status == 200
            assert len(result['pets']) > 0
            assert content_type == 'application/json'

        else:
            # Проверяем что статус запроса 200 и добавленный питомец присутствует в списке
            assert status == 200
            assert result['pets'][0]['name'] == 'Машка'
            assert content_type == 'application/json'

        # Удаляем созданного питомца
        _ = pf.delete_pet(get_key, my_pet['id'])

    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.skip(reason='Тут баг: возвращается код ошибки 500 вместо 400')
    @pytest.mark.parametrize("filter",
                        [
                            generate_string(255),
                            generate_string(1001),
                            russian_chars(),
                            russian_chars().upper(),
                            chinese_chars(),
                            special_chars(),
                            123
                        ],
                        ids=
                        [
                            '255 symbols',
                            'more than 1000 symbols',
                            'russian',
                            'RUSSIAN',
                            'chinese',
                            'specials',
                            'digit'
                        ])
    @pytest.mark.parametrize("accept", ['application/json', 'application/xml'], ids=['json', 'xml'])
    def test_get_all_pets_with_negative_filter(self, get_key, filter, accept):
        """ Проверяем что запрос всех питомцев с некорректным фильтром возвращает код 400. """

        # Запрашиваем список питомцев
        status, result, content_type = pf.get_list_of_pets(get_key, filter, accept)

        # Проверяем статус ответа
        assert status == 400
