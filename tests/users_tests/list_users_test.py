import pytest

from tests.factories import UserFactory
from users.models import User
from users.serializers import UserSerializer



@pytest.mark.django_db
def test_get_list_users_by_anonymous(client):
    items_count = 3
    users = UserFactory.create_batch(items_count)

    expected_response = {
        "detail": "Authentication credentials were not provided.",
    }

    response = client.get(f'/api/users/')

    assert response.status_code == 401
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_list_users_by_user(client, test_user, test_user_token):
    items_count = 3
    users = UserFactory.create_batch(items_count)

    expected_response = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [UserSerializer(test_user).data]

    }

    response = client.get(f'/api/users/', HTTP_AUTHORIZATION="Bearer " + test_user_token)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_list_users_by_admin(client, test_admin, test_admin_token):
    items_count = 3
    users = UserFactory.create_batch(items_count)

    expected_response = {
        "count": 4,
        "next": None,
        "previous": None,
        "results": UserSerializer(User.objects.all(), many=True).data

    }

    response = client.get(f'/api/users/', HTTP_AUTHORIZATION="Bearer " + test_admin_token)

    assert response.status_code == 200
    assert response.json() == expected_response




