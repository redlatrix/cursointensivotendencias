"""
URL configuration for introducion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('resource.urls')),  # rutas de la app

    # Rutas de Swagger:
    # 1. El archivo del esquema (YAML/JSON)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # 2. La interfaz de Swagger (la más común)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # 3. Interfaz alternativa (Redoc)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
