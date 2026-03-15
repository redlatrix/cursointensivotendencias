from rest_framework import permissions

class IsSupervisorOrAdmin(permissions.BasePermission):
    """
    Permiso personalizado para que solo Administradores o Supervisores
    puedan realizar acciones de escritura/borrado.
    """
    def has_permission(self, request, view):
        # 1. Verificamos que el usuario esté logueado (JWT válido)
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 2. Verificamos si pertenece a los grupos permitidos
        # Accedemos al contexto global del usuario
        return request.user.groups.filter(name__in=['Administrador', 'Supervisor']).exists()