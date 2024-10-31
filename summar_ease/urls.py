from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls')),  # Versioned API
    path('password_reset/', include('django.contrib.auth.urls')),
]
