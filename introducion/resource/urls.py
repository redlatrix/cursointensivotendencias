from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResourcceViewSet

router = DefaultRouter()
router.register(r'resource', ResourcceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]