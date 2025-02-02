from django.urls import path
from .views import PersonProcessSpreadsheetView, PersonListSpreadsheetView

urlpatterns = [
    path(
        "upload-planilha/",
        PersonProcessSpreadsheetView.as_view(),
        name="process_spreadsheet",
    ),
    path(
        "download-planilha/",
        PersonListSpreadsheetView.as_view(),
        name="list_spreadsheet",
    ),
]
