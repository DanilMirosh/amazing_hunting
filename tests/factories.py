import factory.django

from authentication.models import User
from vacancies.models import Vacancy


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "test"
    password = "123qwe"


class VacancyFactory(factory.django.DjangoModelFactory):
    class Mate:
        model = Vacancy

    slug = "test"
    text = "test text"
    user = factory.SubFactory(UserFactory)
