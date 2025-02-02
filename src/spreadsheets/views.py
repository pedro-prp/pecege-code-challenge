from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponse

from .serializers import PersonSerializer
from .services import PersonService

from .exceptions import SpreadsheetHeaderException

from drf_yasg.utils import swagger_auto_schema
from .swagger_schemas import get_upload_planilha_schema, get_download_planilha_schema


class PersonProcessSpreadsheetView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = PersonService()

    @swagger_auto_schema(**get_upload_planilha_schema())
    def post(self, request):

        try:
            file = request.FILES.get("file")

            processed_data, error = self.__service.process_spreadsheet(file)

            serializer = PersonSerializer(data=processed_data, many=True)

            if serializer.is_valid():
                response_data = {"result": serializer.data}
                if error:
                    response_data["errors"] = error

                return Response(
                    data=response_data,
                    status=status.HTTP_201_CREATED,
                )

        except AttributeError:
            return Response(
                data={"Erro ao processar a planilha": "O arquivo não foi enviado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except SpreadsheetHeaderException as e:
            return Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                data={"Erro ao processar a planilha": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PersonListSpreadsheetView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = PersonService()

    @swagger_auto_schema(**get_download_planilha_schema())
    def get(self, request):

        try:
            response_file = self.__service.generate_spreadsheet()

            response = HttpResponse(
                response_file.getvalue(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

            response["Content-Disposition"] = "attachment; filename=pessoas.xlsx"

            return response

        except Exception as e:
            return Response(
                data={"Erro ao gerar a planilha": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
