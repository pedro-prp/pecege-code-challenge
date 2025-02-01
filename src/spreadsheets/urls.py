from django.urls import path
from .views import PersonProcessSpreadsheetView

urlpatterns = [
    path(
        "upload-planilha/",
        PersonProcessSpreadsheetView.as_view(),
        name="process_spreadsheet",
    ),
]
