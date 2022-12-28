import pytest
from ads.models import Ad, Comment

TEST_USER_EMAIL = "test_user@email.ru"
TEST_ADMIN_EMAIL = "test_admin@email.ru"

TEST_USER_PASSWORD = "testuserpassword"
TEST_ADMIN_PASSWORD = "testuserpassword"


@pytest.fixture
@pytest.mark.django_db
def test_user(django_user_model):
    user_data = {
        "first_name": "test user first name",
        "last_name": "test user last name",
        "password": TEST_USER_PASSWORD,
        "email": TEST_USER_EMAIL,
        "phone": "+7 914 123-45-67"
    }
    user = django_user_model.objects.create(**user_data)
    user.set_password(user.password)
    user.save()

    return user


@pytest.fixture
@pytest.mark.django_db
def test_admin(django_user_model):
    admin_data = {
        "first_name": "test admin first name",
        "last_name": "test admin last name",
        "password": TEST_ADMIN_PASSWORD,
        "email": TEST_ADMIN_EMAIL,
        "phone": "+7 914 987-65-43"
    }
    admin = django_user_model.objects.create(**admin_data)
    admin.set_password(admin.password)
    admin.role = 'admin'
    admin.save()

    return admin


@pytest.fixture
@pytest.mark.django_db
def test_user_token(client, test_user):
    response = client.post(
        '/api/token/',
        {"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD},
        format="json"
    )

    return response.data["access"]

@pytest.fixture
@pytest.mark.django_db
def test_admin_token(client, test_admin):
    response = client.post(
        '/api/token/',
        {"email": TEST_ADMIN_EMAIL, "password": TEST_ADMIN_PASSWORD},
        format="json"
    )

    return response.data["access"]


@pytest.fixture
@pytest.mark.django_db
def test_user_ad(client, test_user_token):

    request_data = {
        "title": "test ad title",
        "price": 12345,
        "description": "test description",
    }
    response = client.post('/api/ads/', request_data, content_type='application/json', HTTP_AUTHORIZATION="Bearer " + test_user_token)

    ad = Ad.objects.get(pk=response.data['pk'])
    return ad

@pytest.fixture
@pytest.mark.django_db
def test_user_comment(client, test_user_token, test_user_ad):

    request_data = {
        "text": "comment text"
    }
    response = client.post(f'/api/ads/{test_user_ad.id}/comments/', request_data, content_type='application/json', HTTP_AUTHORIZATION="Bearer " + test_user_token)

    comment = Comment.objects.get(pk=response.data['pk'])
    return comment
