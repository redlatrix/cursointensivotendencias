from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ResourceViewSet, 
    ResourceTypeViewSet, 
    AssignmentViewSet, 
    ResourceAssigneeViewSet
)

router = DefaultRouter()

# Estas rutas aparecerán como "secciones" en Swagger
router.register(r"resources", ResourceViewSet, basename="resources")
router.register(r"resource-types", ResourceTypeViewSet, basename="resource-types")
router.register(r"assignments", AssignmentViewSet, basename="assignments")
router.register(r"assignees", ResourceAssigneeViewSet, basename="assignees")

urlpatterns = [
    # No necesitas path("resources/create/"), el router ya lo hace en POST /resources/
    path("", include(router.urls)),
]