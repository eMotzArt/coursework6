import pytest

from ads.serializers import CommentsListSerializer
from tests.factories import CommentsFactory


@pytest.mark.django_db
def test_get_detail_comment_by_anonymous(client):
    items_count = 9
    comments = CommentsFactory.create_batch(items_count)

    ad_id = comments[0].ad_id
    retrieved_comment = comments[0]
    retrieved_comment_id = retrieved_comment.id

    response = client.get(f'/api/ads/{ad_id}/comments/{retrieved_comment_id}/')

    expected_response = {
        "detail": 'Authentication credentials were not provided.',
    }

    assert response.status_code == 401
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_detail_comment_by_user(client, test_user, test_user_token):
    items_count = 9
    comments = CommentsFactory.create_batch(items_count)

    ad_id = comments[0].ad_id
    retrieved_comment = comments[0]
    retrieved_comment_id = retrieved_comment.id

    response = client.get(f'/api/ads/{ad_id}/comments/{retrieved_comment_id}/', HTTP_AUTHORIZATION="Bearer " + test_user_token)

    assert response.wsgi_request.user.is_anonymous == False
    assert response.wsgi_request.user.is_authenticated == True
    assert response.wsgi_request.user == test_user
    assert response.status_code == 200
    assert response.json() == CommentsListSerializer(retrieved_comment).data
