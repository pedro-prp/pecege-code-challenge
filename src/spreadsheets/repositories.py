from .models import Person


class PersonRepository:
    def __init__(self):
        self.__model = Person

    def update_or_create(self, person_data):
        return self.__model.objects.update_or_create(**person_data)

    def get_all(self):
        return self.__model.objects.filter(is_active=True).values()
