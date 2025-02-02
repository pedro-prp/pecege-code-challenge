from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# TODO: setup admin

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

            print("PROCESSED DATA:", processed_data)

            # serializer = PersonSerializer(data=processed_data, many=True)

            # if serializer.is_valid():
            return Response(
                data=processed_data,
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                data={"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
