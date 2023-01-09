from api import PetFriends
from settings import valid_email, valid_password
import lxml.html
import pytest


pf = PetFriends()


@pytest.mark.auth
@pytest.mark.api
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


@pytest.mark.auth
@pytest.mark.api
@pytest.mark.parametrize("email", ['', 'example@tes.com'], ids=['empty', 'not existing'])
@pytest.mark.parametrize("password", ['', 'qwerty'], ids=['empty', 'not existing'])
def test_get_api_key_for_user_negative(email, password):
    """ Проверяем что запрос api ключа возвращает статус 403 и ошибку в случае несуществующего email/password"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Забираем текст ошибки из запроса
    tree = lxml.html.document_fromstring(result)
    error = tree.xpath('/html/body/p/text()')

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert error[0] == "This user wasn\'t found in database"
