from django.db import models
from users.models import User
import uuid
import os

def generate_unique_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads/', filename)

class File(models.Model):
    ALLOWED_EXTENSIONS = ['.pptx', '.docx', '.xlsx']
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    file = models.FileField(upload_to=generate_unique_filename)
    original_filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    download_token = models.UUIDField(unique=True, default=uuid.uuid4)
    
    def __str__(self):
        return self.original_filename

    def save(self, *args, **kwargs):
        # Validate file extension
        ext = os.path.splitext(self.original_filename)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            raise ValueError("File type not allowed")
        super().save(*args, **kwargs)
