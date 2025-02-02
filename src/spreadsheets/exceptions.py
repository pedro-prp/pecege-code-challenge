class SpreadsheetHeaderException(Exception):
    def __init__(self, *args):
        self.message = (
            "Cabeçalho inválido. Verifique se todas as colunas estão preenchidas."
        )

        super().__init__(self.message)


class InvalidBirthDateException(Exception):
    def __init__(self, *args):
        self.message = "Data de nascimento com formato inválido."

        super().__init__(self.message)
