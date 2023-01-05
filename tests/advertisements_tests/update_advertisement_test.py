import pytest


@pytest.mark.django_db
def test_ad_change_by_user(client, test_user, test_user_token, test_user_ad):
    request_data = {
        "title": "test ad title changed",
        "price": 777,
        "description": "test description changed",
    }

    expected_response = {
        "pk": test_user_ad.id,
        "image": None,
        "title": request_data.get('title'),
        "price": request_data.get('price'),
        "phone": test_user.phone,
        "description": request_data.get("description"),
        "author_first_name": test_user.first_name,
        "author_last_name": test_user.last_name,
        "author_id": test_user.id
    }

    response = client.patch(f'/api/ads/{test_user_ad.id}/', request_data, content_type='application/json', HTTP_AUTHORIZATION="Bearer " + test_user_token)

    assert response.status_code == 200
    assert expected_response == response.json()
