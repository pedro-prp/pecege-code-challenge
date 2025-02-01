from django.db import models


class Person(models.Model):
    id_person = models.CharField(max_length=100, primary_key=True)

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )

    email = models.EmailField(
        blank=False,
        null=False,
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

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return f"{self.name} - {self.email}"
