from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'identitydocument', 'dependence', 'phonenumber')
    list_filter = ('dependence',)
    search_fields = ('user__username', 'identitydocument')

    fieldsets = (
        ('Usuario Vinculado', {
            'fields': ('user', 'identitydocument')
        }),
        ('Información de Contacto', {
            'fields': ('phonenumber', 'dependence', 'avatar')
        }),
        ('Información Adicional', {
            'fields': ('bibliography',),
        }),
    )