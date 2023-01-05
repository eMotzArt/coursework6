import pytest

from ads.models import Comment
from django.core.exceptions import ObjectDoesNotExist


@pytest.mark.django_db
def test_ad_change_by_anonymous(client, test_user_ad, test_user_comment):
    response = client.delete(f'/api/ads/{test_user_ad.id}/comments/{test_user_comment.id}/')

    assert response.status_code == 401


@pytest.mark.django_db
def test_ad_change_by_user(client, test_user_token, test_user_ad, test_user_comment):
    comments_count = len(Comment.objects.all())

    response = client.delete(f'/api/ads/{test_user_ad.id}/comments/{test_user_comment.id}/', HTTP_AUTHORIZATION="Bearer " + test_user_token)
    with pytest.raises(ObjectDoesNotExist):
        comment = Comment.objects.get(pk=test_user_comment.id)

    assert response.status_code == 204
    assert comments_count - 1 == len(Comment.objects.all())
