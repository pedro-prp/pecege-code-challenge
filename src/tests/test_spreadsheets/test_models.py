from django.test import TestCase

from spreadsheets.models import Person


class PersonModelTest(TestCase):
    def setUp(self):
        self.person = Person.objects.create(
            name="Person Test",
            email="test@gmail.com",
            birth_date="1990-01-01",
            is_active=True,
            value=150.00,
        )

    def test_person_successful_created(self):
        self.assertEqual(str(self.person), "Person Test - test@gmail.com")
        self.assertEqual(self.person.name, "Person Test")

        self.assertIsNotNone(self.person.created_at)
        self.assertIsNotNone(self.person.updated_at)

    def test_email_uniqueness(self):
        with self.assertRaises(Exception):
            Person.objects.create(
                name="Person Test 2",
                email="test@gmail.com",
                birth_date="1990-10-10",
                is_active=True,
                value=150.00,
            )
