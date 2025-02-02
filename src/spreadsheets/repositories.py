from .models import Person


class PersonRepository:
    def __init__(self):
        self.__model = Person

    def create(self, person_data):
        return self.__model.objects.create(**person_data)
