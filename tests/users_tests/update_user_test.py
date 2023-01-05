import pytest

@pytest.mark.django_db
def test_user_info_change_by_owner(client, test_user_token):
    request_data = {
        "first_name": "changed first name",
        "last_name": "changed last name",
        "phone": "+7 123 456-78-90"
    }

    response = client.patch('/api/users/me/', request_data, content_type='application/json', HTTP_AUTHORIZATION="Bearer " + test_user_token)

    assert response.status_code == 200
    assert [request_data.get(field) == response.json().get(field) for field in request_data.keys()]

