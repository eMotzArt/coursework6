import pytest
from ads.models import Comment
from ads.serializers import CommentsListSerializer


@pytest.mark.django_db
def test_comment_change_by_anonymous(client, test_user_ad, test_user_comment):
    request_data = {
        "text": "changed text"
    }

    response = client.patch(f'/api/ads/{test_user_ad.id}/comments/{test_user_comment.id}/', request_data, content_type='application/json')

    assert response.status_code == 401


@pytest.mark.django_db
def test_comment_change_by_user(client, test_user_token, test_user_ad, test_user_comment):
    request_data = {
        "text": "changed text"
    }

    response = client.patch(f'/api/ads/{test_user_ad.id}/comments/{test_user_comment.id}/', request_data, content_type='application/json', HTTP_AUTHORIZATION="Bearer " + test_user_token)

    comment = Comment.objects.get(pk=test_user_comment.id)

    assert response.status_code == 200
    assert response.json() == CommentsListSerializer(comment).data
    assert request_data.get('text') == response.json().get('text')
