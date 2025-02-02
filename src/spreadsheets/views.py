from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponse

from .serializers import PersonSerializer
from .services import PersonService


# TODO: Implement swagger_auto_schema decorator
# from drf_yasg.utils import swagger_auto_schema


class PersonProcessSpreadsheetView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = PersonService()

    def post(self, request):

        try:
            file = request.FILES.get("file")

            processed_data = self.__service.process_spreadsheet(file)

            serializer = PersonSerializer(data=processed_data, many=True)

            if serializer.is_valid():
                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED,
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
