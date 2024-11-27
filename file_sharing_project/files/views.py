from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import File
from .serializers import FileUploadSerializer, FileListSerializer
from users.permissions import IsOpsUser, IsClientUser
import uuid

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated, IsOpsUser]

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file_instance = serializer.save()
            return Response({
                'message': 'File uploaded successfully',
                'file_id': file_instance.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileListView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request):
        files = File.objects.filter(user=request.user)
        serializer = FileListSerializer(files, many=True)
        return Response(serializer.data)


class FileDownloadView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request, file_id):
        try:
            file_obj = File.objects.get(pk=file_id, user=request.user)
            # Generate temporary download URL
            download_url = f"/secure-download/{file_obj.download_token}"
            return Response({
                'download_link': download_url,
                'message': 'success'
            })
        except File.DoesNotExist:
            return Response({
                'message': 'File not found'
            }, status=status.HTTP_404_NOT_FOUND)
