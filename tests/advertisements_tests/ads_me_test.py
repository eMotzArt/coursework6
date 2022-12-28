import pytest

from project import settings
from tests.factories import AdvertisementFactory
from ads.serializers import AdvertisementsListSerializer
from ads.models import Ad

@pytest.mark.django_db
def test_get_owner_list_advertisement_by_anonymous(client):
    items_count = 9
    page_size = settings.REST_FRAMEWORK.get('PAGE_SIZE')

    advertisements = AdvertisementFactory.create_batch(items_count)

    response = client.get('/api/ads/')
    expected_response = {
        "count": items_count,
        "next": 'http://testserver/api/ads/?page=2',
        "previous": None,
        "results": AdvertisementsListSerializer(advertisements[:page_size], many=True).data
    }

    assert response.wsgi_request.user.is_anonymous == True
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.django_db
def test_get_owner_list_advertisement(client, test_user, test_user_token):
    assert len(Ad.objects.all()) == 0
    request_data_first_ad = {
        "title": "first test ad title",
        "price": 12345,
        "description": "first test description",
    }

    request_data_second_ad = {
        "title": "second test ad title",
        "price": 12345,
        "description": "second test description",
    }

    response_create_first = client.post('/api/ads/', data=request_data_first_ad, content_type='application/json', HTTP_AUTHORIZATION="Bearer " + test_user_token)
    assert len(Ad.objects.all()) == 1

    response_create_second = client.post('/api/ads/', request_data_second_ad, content_type='application/json', HTTP_AUTHORIZATION="Bearer " + test_user_token)
    assert len(Ad.objects.all()) == 2

    expected_response = {
        "count": 2,
        "next": None,
        "previous": None,
        "results": AdvertisementsListSerializer(Ad.objects.all(), many=True).data
    }

    response = client.get('/api/ads/me/', HTTP_AUTHORIZATION="Bearer " + test_user_token)

    assert response.status_code == 200
    assert expected_response == response.json()

