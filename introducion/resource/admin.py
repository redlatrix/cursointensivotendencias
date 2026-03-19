from django.contrib import admin

from .models import Assignment, Resource, ResourceAssignee, ResourceType


@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name", "description")


@admin.register(ResourceAssignee)
class ResourceAssigneeAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "area", "email")
    list_filter = ("area", "position")
    search_fields = ("name", "email", "area")


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "type", "status", "responsible_area")
    list_filter = ("status", "type__category", "responsible_area")
    search_fields = ("code", "name", "responsible_area", "technical_description")
    autocomplete_fields = ("type",)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "resource",
        "assignee",
        "start_date",
        "expected_return_date",
        "returned_at",
    )
    list_filter = ("start_date", "returned_at", "resource__status", "assignee__area")
    search_fields = ("resource__code", "resource__name", "assignee__name", "assignee__email")
    autocomplete_fields = ("resource", "assignee")
