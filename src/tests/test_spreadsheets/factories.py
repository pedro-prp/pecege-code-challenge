from openpyxl import Workbook
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime, timedelta, date
import random


class ExcelFileFactory:
    @staticmethod
    def generate_excel(headers, data_rows):
        wb = Workbook()
        ws = wb.active
        ws.append(headers)
        for row in data_rows:
            ws.append(row)

        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        return SimpleUploadedFile(
            "test.xlsx",
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


class ValidSpreadsheetFactory(ExcelFileFactory):
    @classmethod
    def generate(cls):
        headers = ["nome", "email", "data de nascimento", "ativo"]

        data_rows = [
            [
                "João das Neves",
                "joao@neves.com",
                datetime.now().replace(year=date.today().year - 20),
                True,
            ],
            [
                "Mauricio Serra",
                "mauricio@serrano.com",
                datetime.now().replace(year=date.today().year - 40),
                True,
            ],
            [
                "Carlos Oliveira",
                "carlos@example.com",
                datetime.now().replace(year=date.today().year - 70),
                True,
            ],
        ]

        return cls.generate_excel(headers, data_rows)

    @classmethod
    def generate_minor(cls):
        headers = ["nome", "email", "data de nascimento", "ativo"]

        data_rows = [
            [
                "menor inativo",
                "josue@menor.com",
                datetime.now().replace(year=date.today().year - 17),
                True,
            ],
        ]

        return cls.generate_excel(headers, data_rows)


class InvalidSpreadsheetFactory(ExcelFileFactory):
    @classmethod
    def generate_missing_columns(cls):
        headers = ["nome", "email"]  # Falta "data de nascimento" e "ativo"
        data_rows = [["Ana", "ana@example.com"], ["Pedro", "pedro@example.com"]]
        return cls.generate_excel(headers, data_rows)

    @classmethod
    def generate_invalid_dates(cls):
        headers = ["nome", "email", "data de nascimento", "ativo"]
        data_rows = [
            ["Beltrano", "beltrano@example.com", "invalido", True],
        ]
        return cls.generate_excel(headers, data_rows)
