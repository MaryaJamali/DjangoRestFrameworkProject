"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Addressing App
urlpatterns = [
    path('', include('base.urls')),
    path('todos/', include('todo.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('auth-token/', obtain_auth_token, name='generate_auth_token'),
    # Addresses related to djangorestframework-simplejwt
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Addresses related to drf_spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # YOUR PATTERNS
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Optional UI
    path('admin/', admin.site.urls),
]
