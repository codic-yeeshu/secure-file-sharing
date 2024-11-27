from rest_framework import serializers
from .models import File
import os

class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = File
        fields = ['file']

    def validate_file(self, value):
        # Validate file extension
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in File.ALLOWED_EXTENSIONS:
            raise serializers.ValidationError(
                "Only .pptx, .docx, and .xlsx files are allowed."
            )
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['original_filename'] = validated_data['file'].name
        return super().create(validated_data)

class FileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'original_filename', 'uploaded_at']
