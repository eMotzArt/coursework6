import pytest

from tests.factories import CommentsFactory
from ads.serializers import CommentsListSerializer

@pytest.mark.django_db
def test_get_list_comments_by_anonymous(client):
    items_count = 9
    comments = CommentsFactory.create_batch(items_count)

    ad_id = comments[0].ad_id

    expected_response = {
        "detail": 'Authentication credentials were not provided.'
    }

    response = client.get(f'/api/ads/{ad_id}/comments/')

    assert response.wsgi_request.user.is_anonymous == True
    assert response.status_code == 401
    assert response.json() == expected_response

@pytest.mark.django_db
def test_get_list_comments_by_user(client, test_user, test_user_token):
    items_count = 9
    comments = CommentsFactory.create_batch(items_count)

    ad_id = comments[0].ad_id

    expected_response = {
        "count": items_count,
        "next": None,
        "previous": None,
        "results": CommentsListSerializer(comments, many=True).data
    }

    response = client.get(f'/api/ads/{ad_id}/comments/', HTTP_AUTHORIZATION="Bearer " + test_user_token)


    assert response.wsgi_request.user.is_anonymous == False
    assert response.wsgi_request.user.is_authenticated == True
    assert response.wsgi_request.user == test_user
    assert response.status_code == 200
    assert response.json() == expected_response
