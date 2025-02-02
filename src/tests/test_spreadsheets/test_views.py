from rest_framework import status

from spreadsheets.models import Person

from .factories import (
    ValidSpreadsheetFactory,
    InvalidSpreadsheetFactory,
)

from rest_framework.test import APITestCase

from django.contrib.auth.models import User

import base64


class TestPersonProcessSpreadsheetView(APITestCase):
    def setUp(self):
        # Criação do usuário para autenticação
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        credentials = f"{self.user.username}:testpassword"
        base64_credentials = base64.b64encode(credentials.encode()).decode()
        self.client.credentials(HTTP_AUTHORIZATION=f"Basic {base64_credentials}")

        self.valid_file = ValidSpreadsheetFactory.generate()
        self.valid_file_minor = ValidSpreadsheetFactory.generate_minor()
        self.invalid_missing_columns_file = (
            InvalidSpreadsheetFactory.generate_missing_columns()
        )
        self.invalid_invalid_dates_file = (
            InvalidSpreadsheetFactory.generate_invalid_dates()
        )
        self.url = "/planilhas/upload-planilha/"

    def test_valid_file_upload(self):
        response = self.client.post(
            self.url, {"file": self.valid_file}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data["result"]), 3)

    def test_missing_columns(self):
        response = self.client.post(
            self.url, {"file": self.invalid_missing_columns_file}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Cabeçalho inválido. Verifique se todas as colunas estão preenchidas.",
            response.data,
        )

    def test_invalid_dates(self):
        response = self.client.post(
            self.url, {"file": self.invalid_invalid_dates_file}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data["errors"]), 1)

    def test_minors_deactivation(self):
        response = self.client.post(
            self.url, {"file": self.valid_file_minor}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(len(response.data["result"]), 0)


class TestPersonListSpreadsheetView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        credentials = f"{self.user.username}:testpassword"
        base64_credentials = base64.b64encode(credentials.encode()).decode()
        self.client.credentials(HTTP_AUTHORIZATION=f"Basic {base64_credentials}")

        Person.objects.create(
            name="João Silva",
            email="joao@example.com",
            birth_date="2000-05-20",
            is_active=True,
            value=150.00,
        )
        Person.objects.create(
            name="Maria Souza",
            email="maria@example.com",
            birth_date="2010-01-01",
            is_active=False,
            value=100.00,
        )
        Person.objects.create(
            name="Carlos Oliveira",
            email="carlos@example.com",
            birth_date="1960-08-15",
            is_active=True,
            value=200.00,
        )

        self.url = "/planilhas/download-planilha/"

    def test_download_spreadsheet_success(self):

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.assertIn(
            "attachment; filename=pessoas.xlsx", response["Content-Disposition"]
        )
