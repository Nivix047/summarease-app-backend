from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, login_view
from pdfs.views import PDFDocumentViewSet

router = DefaultRouter()
router.register(r'', CustomUserViewSet, basename='user')

urlpatterns = [
    path('register/', CustomUserViewSet.as_view({'post': 'register'}), name='register'),  # Custom route for registration
    path('login/', login_view, name='login'),
    path('pdfs/', PDFDocumentViewSet.as_view({'post': 'create'}), name='upload_pdf'),
    path('', include(router.urls)),  # All other user routes
]
 