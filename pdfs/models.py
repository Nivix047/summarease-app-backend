from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class PDFDocument(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pdf_documents')
  title = models.CharField(max_length=255)
  public_id = models.CharField(max_length=255, blank=True, null=True)
  summary = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title