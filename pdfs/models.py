from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PDFDocument(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pdf_documents')
  title = models.CharField(max_length=255)
  file= models.FileField(upload_to='pdfs/')
  summary = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title