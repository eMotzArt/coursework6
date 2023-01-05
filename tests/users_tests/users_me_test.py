import pytest

from tests.factories import UserFactory
from users.serializers import UserSerializer

@pytest.mark.django_db
def test_get_user_owner_list_by_anonymous(client):
    items_count = 3
    users = UserFactory.create_batch(items_count)

    response = client.get('/api/users/me/')
    expected_response = {
        "detail": 'Authentication credentials were not provided.',
    }

    assert response.wsgi_request.user.is_anonymous == True
    assert response.status_code == 401
    assert response.json() == expected_response

@pytest.mark.django_db
def test_get_user_owner_list(client, test_user, test_user_token):

    response = client.get('/api/users/me/', HTTP_AUTHORIZATION="Bearer " + test_user_token)

    assert response.status_code == 200
    assert UserSerializer(test_user).data == response.json()

