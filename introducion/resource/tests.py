from datetime import date, timedelta

from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from resource.models import (
    Assignment,
    Resource,
    ResourceAssignee,
    ResourceCategory,
    ResourceStatus,
    ResourceType,
)
from resource.serializers import AssignmentSerializer, ResourceSerializer


class PruebasModeloRecurso(TestCase):
    def setUp(self):
        self.resource_type = ResourceType.objects.create(
            name="Laptop",
            category=ResourceCategory.PHYSICAL,
        )
        self.assignee = ResourceAssignee.objects.create(
            name="Maria Lopez",
            position="Docente",
            area="Sistemas",
            email="maria@example.com",
        )

    def test_no_permite_eliminar_recurso_en_mantenimiento(self):
        resource = Resource.objects.create(
            name="Portatil 1",
            code="LP-001",
            type=self.resource_type,
            status=ResourceStatus.MAINTENANCE,
            responsible_area="Sistemas",
        )

        with self.assertRaises(ValidationError):
            resource.delete()

    def test_no_permite_eliminar_recurso_con_asignacion_activa(self):
        resource = Resource.objects.create(
            name="Portatil 2",
            code="LP-002",
            type=self.resource_type,
            status=ResourceStatus.ASSIGNED,
            responsible_area="Sistemas",
        )
        Assignment.objects.create(resource=resource, assignee=self.assignee)

        self.assertTrue(resource.has_active_assignment)
        self.assertFalse(resource.can_be_deleted())

        with self.assertRaises(ValidationError):
            resource.delete()


class PruebasSerializerRecurso(TestCase):
    def setUp(self):
        self.resource_type = ResourceType.objects.create(
            name="Proyector",
            category=ResourceCategory.PHYSICAL,
        )
        self.assignee = ResourceAssignee.objects.create(
            name="Carlos Rios",
            position="Supervisor",
            area="Audiovisuales",
            email="carlos@example.com",
        )

    def test_creacion_rechaza_estado_inicial_distinto_de_available(self):
        serializer = ResourceSerializer(
            data={
                "name": "Proyector Epson",
                "code": "PY-001",
                "type": self.resource_type.id,
                "technical_description": "Full HD",
                "value": "1500.00",
                "status": ResourceStatus.ASSIGNED,
                "responsible_area": "Audiovisuales",
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)

    def test_creacion_asigna_estado_available_por_defecto(self):
        serializer = ResourceSerializer(
            data={
                "name": "Proyector Epson",
                "code": "PY-001",
                "type": self.resource_type.id,
                "technical_description": "Full HD",
                "value": "1500.00",
                "responsible_area": "Audiovisuales",
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        resource = serializer.save()

        self.assertEqual(resource.status, ResourceStatus.AVAILABLE)

    def test_no_permite_marcar_available_si_tiene_asignacion_activa(self):
        resource = Resource.objects.create(
            name="Impresora",
            code="IM-001",
            type=self.resource_type,
            status=ResourceStatus.ASSIGNED,
            responsible_area="TI",
        )
        Assignment.objects.create(resource=resource, assignee=self.assignee)

        serializer = ResourceSerializer(
            instance=resource,
            data={"status": ResourceStatus.AVAILABLE},
            partial=True,
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)


    def test_codigo_de_recurso_debe_ser_unico(self):
        Resource.objects.create(
            name="Proyector Base",
            code="PY-BASE",
            type=self.resource_type,
            status=ResourceStatus.AVAILABLE,
            responsible_area="Audiovisuales",
        )

        serializer = ResourceSerializer(
            data={
                "name": "Proyector Duplicado",
                "code": "PY-BASE",
                "type": self.resource_type.id,
                "technical_description": "Duplicado",
                "value": "1200.00",
                "responsible_area": "Audiovisuales",
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("code", serializer.errors)


class PruebasSerializerAsignacion(TestCase):
    def setUp(self):
        self.resource_type = ResourceType.objects.create(
            name="Tablet",
            category=ResourceCategory.DIGITAL,
        )
        self.assignee = ResourceAssignee.objects.create(
            name="Ana Perez",
            position="Auxiliar",
            area="Biblioteca",
            email="ana@example.com",
        )

    def test_no_permite_asignar_recurso_en_mantenimiento(self):
        resource = Resource.objects.create(
            name="Tablet 1",
            code="TB-001",
            type=self.resource_type,
            status=ResourceStatus.MAINTENANCE,
            responsible_area="Biblioteca",
        )

        serializer = AssignmentSerializer(
            data={
                "resource": resource.id,
                "assignee": self.assignee.id,
                "start_date": date.today(),
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("resource", serializer.errors)

    def test_crear_asignacion_cambia_recurso_a_assigned(self):
        resource = Resource.objects.create(
            name="Tablet 2",
            code="TB-002",
            type=self.resource_type,
            status=ResourceStatus.AVAILABLE,
            responsible_area="Biblioteca",
        )

        serializer = AssignmentSerializer(
            data={
                "resource": resource.id,
                "assignee": self.assignee.id,
                "start_date": date.today(),
                "expected_return_date": date.today() + timedelta(days=3),
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        resource.refresh_from_db()
        self.assertEqual(resource.status, ResourceStatus.ASSIGNED)

    def test_devolucion_de_asignacion_cambia_recurso_a_available(self):
        resource = Resource.objects.create(
            name="Tablet 3",
            code="TB-003",
            type=self.resource_type,
            status=ResourceStatus.AVAILABLE,
            responsible_area="Biblioteca",
        )
        create_serializer = AssignmentSerializer(
            data={
                "resource": resource.id,
                "assignee": self.assignee.id,
                "start_date": date.today(),
            }
        )
        self.assertTrue(create_serializer.is_valid(), create_serializer.errors)
        assignment = create_serializer.save()
        resource.refresh_from_db()
        self.assertEqual(resource.status, ResourceStatus.ASSIGNED)

        serializer = AssignmentSerializer(
            instance=assignment,
            data={"returned_at": date.today() + timedelta(days=1)},
            partial=True,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        resource.refresh_from_db()
        self.assertEqual(resource.status, ResourceStatus.AVAILABLE)

    def test_modelo_impide_dos_asignaciones_activas_para_mismo_recurso(self):
        resource = Resource.objects.create(
            name="Tablet 4",
            code="TB-004",
            type=self.resource_type,
            status=ResourceStatus.AVAILABLE,
            responsible_area="Biblioteca",
        )
        Assignment.objects.create(resource=resource, assignee=self.assignee)

        with self.assertRaises(ValidationError):
            Assignment.objects.create(resource=resource, assignee=self.assignee)


    def test_asignacion_conserva_relacion_con_recurso_y_responsable(self):
        recurso = Resource.objects.create(
            name="Tablet 5",
            code="TB-005",
            type=self.resource_type,
            status=ResourceStatus.AVAILABLE,
            responsible_area="Biblioteca",
        )

        serializer = AssignmentSerializer(
            data={
                "resource": recurso.id,
                "assignee": self.assignee.id,
                "start_date": date.today(),
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        asignacion = serializer.save()

        self.assertEqual(asignacion.resource_id, recurso.id)
        self.assertEqual(asignacion.assignee_id, self.assignee.id)


class PruebasPermisosViewSetRecurso(APITestCase):
    def setUp(self):
        self.resource_type = ResourceType.objects.create(
            name="Camara",
            category=ResourceCategory.PHYSICAL,
        )
        self.resource = Resource.objects.create(
            name="Camara Canon",
            code="CM-001",
            type=self.resource_type,
            status=ResourceStatus.AVAILABLE,
            responsible_area="Comunicaciones",
        )

        self.normal_user = User.objects.create_user(
            username="user_normal",
            password="SecurePass123!",
        )
        self.supervisor_user = User.objects.create_user(
            username="user_supervisor",
            password="SecurePass123!",
        )
        supervisor_group = Group.objects.create(name="Supervisor")
        self.supervisor_user.groups.add(supervisor_group)

    def test_listado_requiere_autenticacion(self):
        response = self.client.get("/api/resource/resource/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_actualizacion_denegada_para_usuario_sin_grupo_permitido(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.patch(
            f"/api/resource/resource/{self.resource.id}/",
            {"name": "Camara Sony"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_actualizacion_permitida_para_supervisor(self):
        self.client.force_authenticate(user=self.supervisor_user)

        response = self.client.patch(
            f"/api/resource/resource/{self.resource.id}/",
            {"name": "Camara Nikon"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.resource.refresh_from_db()
        self.assertEqual(self.resource.name, "Camara Nikon")
