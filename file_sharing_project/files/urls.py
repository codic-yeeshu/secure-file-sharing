from django.urls import path
from .views import FileUploadView, FileListView, FileDownloadView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('list/', FileListView.as_view(), name='file-list'),
    path('download/<uuid:file_id>/', FileDownloadView.as_view(), name='file-download'),
]
