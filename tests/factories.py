import factory, factory.django
import faker

from ads.models import Ad, Comment
from tests.fixtures import test_user_ad
from users.models import User

TEST_USER_EMAIL = "test_user@email.ru"
TEST_USER_PASSWORD = "testuserpassword"

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = "test user first name"
    last_name = "test user last name"
    password = TEST_USER_PASSWORD
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')


class AdvertisementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad
        django_get_or_create = ('title',)

    title = factory.Faker('word')
    price = 12345
    description = "test description"
    author = factory.SubFactory(UserFactory)


class CommentsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    text = factory.Faker('paragraph')
    author = factory.SubFactory(UserFactory)
    ad = factory.SubFactory(AdvertisementFactory, title='ad_for_comments')




