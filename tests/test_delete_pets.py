from api import PetFriends
import pytest


pf = PetFriends()


class TestDeletePets:
    @pytest.mark.api
    @pytest.mark.event
    def test_successful_delete_self_pet(self, get_key):
        """Проверяем возможность удаления питомца"""

        # Запрашиваем список своих питомцев
        _, my_pets, _ = pf.get_list_of_pets(get_key, "my_pets", "application/json")

        # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet(get_key, "Суперкот", "кот", "3", "images/cat.jpg", "application/json")
            _, my_pets, _ = pf.get_list_of_pets(get_key, "my_pets", "application/json")

        # Берём id первого питомца из списка и отправляем запрос на удаление
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(get_key, pet_id)

        # Ещё раз запрашиваем список своих питомцев
        _, my_pets, _ = pf.get_list_of_pets(get_key, "my_pets", "application/json")

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        assert pet_id not in my_pets.values()
