from django.http import FileResponse
from wsgiref.util import FileWrapper
import pandas as pd
import os

# Create your views here.
from .models import Books
from rest_framework.response import Response
from rest_framework import status, generics
from . import serializers
from django.conf import settings

class DownloadView(generics.GenericAPIView):
    serializer_class = serializers.BookSerializer

    def get_queryset(self):
        return Books.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        dataexcel = list(queryset.values())
        df = pd.DataFrame(dataexcel)
        # Use a local file path on your server's file system to save the Excel file
        excel_file_path = 'books.xlsx'
        df.to_excel(excel_file_path, index=False)
        serializer = self.serializer_class(queryset, many=True)

        # Check if the file exists and can be opened
        if os.path.exists(excel_file_path):
            # Open the file using FileWrapper and create FileResponse
            with open(excel_file_path, 'rb') as file:
                response = FileResponse(FileWrapper(file))
                response['Content-Disposition'] = 'attachment; filename="books.xlsx"'

                # Convert the local file path to a publicly accessible URL
                file_url = request.build_absolute_uri(settings.MEDIA_URL + excel_file_path)
                return Response(data={'serializer_data': serializer.data, 'excel_file_url': file_url},
                                status=status.HTTP_200_OK)

        # If the file cannot be generated or does not exist, return the data and file path in the response
        return Response(data={'serializer_data': serializer.data, 'excel_file_url': None},
                        status=status.HTTP_200_OK)


