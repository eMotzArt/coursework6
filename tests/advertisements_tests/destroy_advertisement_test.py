import pytest

from ads.models import Ad
from django.core.exceptions import ObjectDoesNotExist

@pytest.mark.django_db
def test_ad_change_by_user(client, test_user, test_user_token, test_user_ad):
    ad_count = len(Ad.objects.all())
    response = client.delete(f'/api/ads/{test_user_ad.id}/', HTTP_AUTHORIZATION="Bearer " + test_user_token)
    with pytest.raises(ObjectDoesNotExist):
        ad = Ad.objects.get(pk=test_user_ad.id)

    assert response.status_code == 204
    assert ad_count - 1 == len(Ad.objects.all())
