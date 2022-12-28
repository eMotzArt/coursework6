import pytest
from ads.models import Ad
from ads.serializers import AdvertisementsRetrieveSerializer

@pytest.mark.django_db
def test_ad_create_by_anonymous(client):
    request_data = {
        "title": "test ad title",
        "price": 12345,
        "description": "test description",
    }

    expected_response = {
        "detail": 'Authentication credentials were not provided.'
    }

    response = client.post('/api/ads/', request_data, format='json')

    assert response.wsgi_request.user.is_anonymous == True
    assert response.status_code == 401
    assert expected_response == response.json()


@pytest.mark.django_db
def test_ad_create_by_user(client, test_user, test_user_token):
    request_data = {
        "title": "test ad title",
        "price": 12345,
        "description": "test description",
    }

    response = client.post('/api/ads/', request_data, content_type='application/json', HTTP_AUTHORIZATION="Bearer " + test_user_token)
    ad = Ad.objects.get(pk=response.json().get('pk'))

    assert response.wsgi_request.user == test_user
    assert response.status_code == 201
    assert response.json() == AdvertisementsRetrieveSerializer(ad).data

