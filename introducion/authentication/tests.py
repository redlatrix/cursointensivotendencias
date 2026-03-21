from django.contrib.auth.models import Group, User
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase

from authentication.models import Profile
from authentication.permissions import IsSupervisorOrAdmin
from introducion.choises import DependenceChoices


class PruebasModeloPerfil(TestCase):
    def test_perfil_tiene_dependencia_por_defecto_y_str_correcto(self):
        user = User.objects.create_user(username="ana", password="StrongPass123!")
        profile = Profile.objects.create(user=user, identitydocument="12345")

        self.assertEqual(profile.dependence, DependenceChoices.SYSTEMS)
        self.assertEqual(str(profile), "Perfil de ana")


class PruebasPermisoSupervisorOAdmin(TestCase):
    def setUp(self):
        self.permission = IsSupervisorOrAdmin()
        self.factory = APIRequestFactory()

    def test_deniega_usuario_anonimo(self):
        request = self.factory.get("/api/resource/")
        request.user = AnonymousUser()
        self.assertFalse(self.permission.has_permission(request, view=None))

    def test_permite_usuario_del_grupo_supervisor(self):
        user = User.objects.create_user(username="super1", password="StrongPass123!")
        supervisor_group = Group.objects.create(name="Supervisor")
        user.groups.add(supervisor_group)

        request = self.factory.get("/api/resource/")
        request.user = user

        self.assertTrue(self.permission.has_permission(request, view=None))

    def test_deniega_usuario_sin_grupos_permitidos(self):
        user = User.objects.create_user(username="normal1", password="StrongPass123!")
        standard_group = Group.objects.create(name="Estandar")
        user.groups.add(standard_group)

        request = self.factory.get("/api/resource/")
        request.user = user

        self.assertFalse(self.permission.has_permission(request, view=None))


class PruebasApiAutenticacion(APITestCase):
    def test_registro_crea_usuario_y_encripta_password(self):
        payload = {
            "username": "nuevo_user",
            "password": "SecurePass123!",
            "email": "nuevo@example.com",
            "first_name": "Nuevo",
            "last_name": "Usuario",
        }

        response = self.client.post("/api/authentication/register/", payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertNotIn("password", response.data)

        user = User.objects.get(username="nuevo_user")
        self.assertTrue(user.check_password("SecurePass123!"))
        self.assertEqual(user.email, "nuevo@example.com")

    def test_me_requiere_autenticacion(self):
        response = self.client.get("/api/authentication/me/")
        self.assertEqual(response.status_code, 401)

    def test_me_retorna_datos_del_usuario_autenticado_con_jwt(self):
        User.objects.create_user(
            username="jwt_user",
            password="SecurePass123!",
            email="jwt@example.com",
            first_name="Jwt",
            last_name="User",
        )

        login_response = self.client.post(
            "/api/authentication/login/",
            {"username": "jwt_user", "password": "SecurePass123!"},
            format="json",
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertIn("access", login_response.data)

        access_token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        me_response = self.client.get("/api/authentication/me/")

        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.data["username"], "jwt_user")
        self.assertEqual(me_response.data["email"], "jwt@example.com")
