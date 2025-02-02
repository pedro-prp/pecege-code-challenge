from rest_framework import serializers
from .models import Person

from datetime import datetime


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["name", "email", "birth_date", "is_active", "value"]
        extra_kwargs = {
            "name": {"required": True},
            "email": {"required": True},
            "birth_date": {"required": True},
            "is_active": {"required": True},
            "value": {"required": True},
        }

    def validate_birth_date(self, value):
        if value > datetime.now().date():
            raise serializers.ValidationError(
                "A Data de nascimento não pode ser maior que a data atual.",
            )

        return value
