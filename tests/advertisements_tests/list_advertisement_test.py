import pytest

from project import settings
from tests.factories import AdvertisementFactory
from ads.serializers import AdvertisementsListSerializer

@pytest.mark.django_db
def test_get_list_advertisement_by_anonymous(client):#, test_user, test_user_token):
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
def test_get_list_advertisement_by_user(client, test_user, test_user_token):
    items_count = 9
    page_size = settings.REST_FRAMEWORK.get('PAGE_SIZE')

    advertisements = AdvertisementFactory.create_batch(items_count)

    response = client.get('/api/ads/', HTTP_AUTHORIZATION="Bearer " + test_user_token)
    expected_response = {
        "count": items_count,
        "next": 'http://testserver/api/ads/?page=2',
        "previous": None,
        "results": AdvertisementsListSerializer(advertisements[:page_size], many=True).data
    }

    assert response.wsgi_request.user.is_anonymous == False
    assert response.wsgi_request.user.is_authenticated == True
    assert response.wsgi_request.user == test_user
    assert response.status_code == 200
    assert response.json() == expected_response
