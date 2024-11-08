import logging
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import PDFDocument
from .serializers import PDFDocumentSerializer
from .pdf_summarizer import extract_text_from_pdf, recursively_summarize

logger = logging.getLogger(__name__)

class PDFDocumentViewSet(viewsets.ModelViewSet):
    queryset = PDFDocument.objects.all().all().order_by('-created_at')
    serializer_class = PDFDocumentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        title = self.request.data.get('title')
        public_id = self.request.data.get('public_id')
        file_url = self.request.data.get('file_url')

        if title and public_id and file_url:
            # Save the PDF document
            pdf_document = serializer.save(user=user, title=title, public_id=public_id)

            # Extract text from the PDF file at the given URL
            text = extract_text_from_pdf(file_url)  # Use the URL directly

            if text:
                summary = recursively_summarize(text)
                pdf_document.summary = summary
                pdf_document.save()
                logger.info("PDF summarized successfully.")

                return Response(status=status.HTTP_201_CREATED)

            logger.error("Failed to extract text from PDF.")
            return Response({"error": "Failed to extract text from PDF."}, status=status.HTTP_400_BAD_REQUEST)

        logger.error("Title, public_id, and file_url are required.")
        return Response({"error": "Title, public_id, and file_url are required."}, status=status.HTTP_400_BAD_REQUEST)
