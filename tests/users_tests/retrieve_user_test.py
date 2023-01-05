import pytest

from tests.factories import UserFactory
from users.serializers import UserSerializer


@pytest.mark.django_db
def test_get_detail_user_by_anonymous(client):
    items_count = 3
    users = UserFactory.create_batch(items_count)

    response = client.get(f'/api/users/{users[0].id}/')

    expected_response = {
        "detail": 'Authentication credentials were not provided.',
    }

    assert response.status_code == 401
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_detail_user_by_user_not_owner(client, test_user, test_user_token):
    items_count = 3
    users = UserFactory.create_batch(items_count)
    expected_response = {
        "detail": "Not found."
    }
    response = client.get(f'/api/users/{users[0].id}/', HTTP_AUTHORIZATION="Bearer " + test_user_token)

    assert response.status_code == 404
    assert response.json() == expected_response

@pytest.mark.django_db
def test_get_detail_user_by_user_owner(client, test_user, test_user_token):
    items_count = 3
    users = UserFactory.create_batch(items_count)

    response = client.get(f'/api/users/{test_user.id}/', HTTP_AUTHORIZATION="Bearer " + test_user_token)

    assert response.status_code == 200
    assert response.json() == UserSerializer(test_user).data
