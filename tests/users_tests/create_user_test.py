import pytest
from users.models import User
from users.serializers import UserCreateSerializer

@pytest.mark.django_db
def test_user_create(client):
    request_data = {
        "phone": "+7 914 123-45-67",
        "email": "test_user@create.com",
        "password": "TestUserPassw0rd",
    }

    response = client.post(f'/api/users/', request_data, content_type='application/json')

    user = User.objects.get(pk=response.data.get('id'))
    assert response.status_code == 201
    assert UserCreateSerializer(user).data == response.json()

