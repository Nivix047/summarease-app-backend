import logging
import tempfile
import os
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import PDFDocument
from .serializers import PDFDocumentSerializer
from .pdf_summarizer import extract_text_from_pdf, recursively_summarize

logger = logging.getLogger(__name__)

class PDFDocumentViewSet(viewsets.ModelViewSet):
  queryset = PDFDocument.objects.all()
  serializer_class = PDFDocumentSerializer
  permission_classes = [IsAuthenticated]

  def perform_create(self, serializer):
    user = self.request.user
    title = self.request.data.get('title')
    pdf_file = self.request.FILES.get('file')

    if title and pdf_file:
      # Save the PDF document
      pdf_document = serializer.save(user=user, title=title, public_id=None)

      # Create a temporary file to save the uploaded PDF
      with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        for chunk in pdf_file.chunks():
          temp_file.write(chunk)
        temp_file_path = temp_file.name

      # Extract text and summarize using the temporary file path
      text = extract_text_from_pdf(temp_file_path)

      if text:
        summary = recursively_summarize(text)
        pdf_document.summary = summary
        pdf_document.save()
        logger.info("PDF summarized successfully.")

        # Clean up the temporary file after use
        os.remove(temp_file_path)

        return Response({'summary': summary, 'id': pdf_document.id}, status=status.HTTP_201_CREATED)
      else:
        logger.error("Failed to extract text from PDF")
        os.remove(temp_file_path)
        return Response({"error": "Failed to extract text from PDF."}, status=status.HTTP_400_BAD_REQUEST)

    logger.error("Title and file are required.")
    return Response({"error": "Title and file are required"}, status=status.HTTP_400_BAD_REQUEST)