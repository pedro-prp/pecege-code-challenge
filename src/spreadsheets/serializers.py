from rest_framework import serializers
from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["name", "email", "age", "is_active", "value"]
        extra_kwargs = {
            "name": {"required": True},
            "email": {"required": True},
            "age": {"required": True, "min_value": 0, "max_value": 150},
            "is_active": {"required": True},
            "value": {"required": True},
        }
