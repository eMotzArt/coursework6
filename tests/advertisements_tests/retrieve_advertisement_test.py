import pytest

from ads.serializers import AdvertisementsRetrieveSerializer

@pytest.mark.django_db
def test_get_detail_advertisement_by_anonymous(client, ad):#, test_user, test_user_token):
    response = client.get(f'/api/ads/{ad.id}/')
    expected_response = {
        "detail": 'Authentication credentials were not provided.',
    }

    assert response.status_code == 401
    assert response.json() == expected_response

@pytest.mark.django_db
def test_get_detail_advertisement_by_user(client, test_user, test_user_token, ad):

    response = client.get(f'/api/ads/{ad.id}/', HTTP_AUTHORIZATION="Bearer " + test_user_token)
    expected_response = AdvertisementsRetrieveSerializer(ad).data

    assert response.wsgi_request.user.is_anonymous == False
    assert response.wsgi_request.user.is_authenticated == True
    assert response.wsgi_request.user == test_user
    assert response.status_code == 200
    assert response.json() == expected_response
