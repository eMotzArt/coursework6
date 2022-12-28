pytest_plugins = 'tests.fixtures'

from pytest_factoryboy import register

from tests.factories import AdvertisementFactory, UserFactory, CommentsFactory

register(AdvertisementFactory)
register(UserFactory)
register(CommentsFactory)
