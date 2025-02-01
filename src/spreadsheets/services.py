from openpyxl import load_workbook

# from .repositories import PersonRepository
from .utils import calculate_age, calculate_value


class PersonService:
    def __init__(self):
        # self.__person_repository = person_repository
        pass

    def process_spreadsheet(self, file):
        workbook = load_workbook(file)
        worksheet = workbook.active

        processed_data = []

        for row in worksheet.iter_rows(min_row=2, values_only=True):
            if not row or all(cell is None for cell in row):
                continue

            try:
                name, email, birth_date, is_active, _ = row

                print(
                    "Nome",
                    name,
                    "Email",
                    email,
                    "Data de Nascimento",
                    birth_date,
                    "Ativo",
                    is_active,
                )

                age = calculate_age(birth_date)

                if age < 18:
                    is_active = False

                value = calculate_value(age)

                person = {
                    "name": name,
                    "email": email,
                    "age": age,
                    "is_active": is_active,
                    "value": value,
                }

                processed_data.append(person)
            except Exception as e:
                print(f"Invalid processing row: {row}. Error: {e}")
                continue

        return processed_data
