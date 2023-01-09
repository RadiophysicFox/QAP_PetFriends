from settings import valid_email, valid_password
from api import PetFriends
from datetime import datetime
import pytest


pf = PetFriends()


@pytest.fixture(scope="class")
def get_key(request):
    status, response = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert 'key' in response
    return response


@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    print(f"\nТест шел: {end_time - start_time}")