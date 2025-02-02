from drf_yasg import openapi


def get_upload_planilha_schema():
    return {
        "operation_summary": "Upload de Planilha",
        "operation_description": (
            "Recebe uma planilha Excel (.xlsx) com informações de pessoas, processa os dados e aplica regras de negócio:\n"
            "- Se a pessoa for menor de 18 anos, ela será marcada como inativa.\n"
            "- A lista retornada conterá apenas as pessoas ativas.\n"
            "- Para cada pessoa ativa, será calculado um valor:\n"
            "  - Menores de 21 anos: R$ 100,00.\n"
            "  - Idade entre 21 e 59 anos: R$ 150,00.\n"
            "  - 60 anos ou mais: R$ 200,00."
        ),
        "request_body": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "file": openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description="Arquivo Excel contendo os dados das pessoas (colunas: nome, email, data de nascimento, ativo).",
                )
            },
            required=["file"],
        ),
        "responses": {
            201: openapi.Response(
                description="Planilha processada com sucesso.",
                examples={
                    "application/json": {
                        "result": [
                            {
                                "nome": "Jose Josue",
                                "email": "jose@gmail.com",
                                "birth_date": "2000-05-20",
                                "is_active": True,
                                "value": 150.00,
                            }
                        ],
                        "errors": [],
                    }
                },
            ),
            400: openapi.Response(
                description="Erro ao processar a planilha.",
                examples={
                    "application/json": {
                        "Erro ao processar a planilha": "O arquivo não foi enviado."
                    }
                },
            ),
        },
    }


def get_download_planilha_schema():
    return {
        "operation_summary": "Download de Planilha",
        "operation_description": (
            "Gera uma planilha Excel (.xlsx) contendo as informações das pessoas ativas no sistema.\n\n"
            "A planilha gerada terá as seguintes colunas:\n"
            "- Nome\n"
            "- E-mail\n"
            "- Data de Nascimento\n"
            "- Valor (calculado com base na idade):\n"
            "  - Menores de 21 anos: R$ 100,00.\n"
            "  - Idade entre 21 e 59 anos: R$ 150,00.\n"
            "  - 60 anos ou mais: R$ 200,00."
        ),
        "responses": {
            200: openapi.Response(
                description="Planilha gerada com sucesso.",
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ),
            400: openapi.Response(
                description="Erro ao gerar a planilha.",
                examples={
                    "application/json": {"Erro ao gerar a planilha": "Erro detalhado."}
                },
            ),
        },
    }
