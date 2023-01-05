import pytest
from ads.models import Ad, Comment
from ads.serializers import AdvertisementsRetrieveSerializer, CommentsListSerializer

@pytest.mark.django_db
def test_comment_create_by_anonymous(client, test_user, ad):
    request_data = {
        "text": "test comment"
    }

    expected_response = {
        "detail": 'Authentication credentials were not provided.'
    }

    response = client.post(f'/api/ads/{ad.id}/comments/', request_data, content_type='application/json')

    assert response.wsgi_request.user.is_anonymous == True
    assert response.status_code == 401
    assert expected_response == response.json()


@pytest.mark.django_db
def test_ad_create_by_user(client, test_user, test_user_token, ad):
    request_data = {
        "text": "test comment"
    }

    response = client.post(f'/api/ads/{ad.id}/comments/', request_data, content_type='application/json', HTTP_AUTHORIZATION="Bearer " + test_user_token)
    comment_id = response.data.get('pk')
    comment = Comment.objects.get(pk=comment_id)

    assert response.wsgi_request.user == test_user
    assert response.status_code == 201
    assert response.json() == CommentsListSerializer(comment).data

