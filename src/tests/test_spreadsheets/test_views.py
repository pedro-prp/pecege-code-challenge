from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date

from .factories import (
    ValidSpreadsheetFactory,
    InvalidSpreadsheetFactory,
)

from rest_framework.test import APITestCase


class TestPersonProcessSpreadsheetView(APITestCase):
    def setUp(self):
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
