from rest_framework import serializers
from .models import PDFDocument

class PDFDocumentSerializer(serializers.ModelSerializer):
  class Meta:
    model = PDFDocument
    fields = ['id', 'user', 'title', 'public_id', 'summary', 'created_at']
    read_only_fields = ['user', 'created_at']
