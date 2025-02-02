from django.db import models

from django.core.validators import EmailValidator

from uuid import uuid4


class Person(models.Model):
    id_person = models.CharField(max_length=100, primary_key=True, default=uuid4)

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )

    email = models.EmailField(
        blank=False,
        null=False,
        validators=[
            EmailValidator(message="O e-mail informado é inválido."),
        ],
        unique=True,
    )

    birth_date = models.DateField(
        blank=False,
        null=False,
    )

    is_active = models.BooleanField()

    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
