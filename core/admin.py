from django.contrib import admin

from core.models import College, Unit, Department, Staff


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name']
    search_fields = ['name', 'short_name']
    list_filter = ['name', ]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'college']
    search_fields = ['name', 'short_name']
    list_filter = ['name', 'college']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'unit']
    search_fields = ['name', 'short_name']
    list_filter = ['name', 'unit']


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'gender', 'type', 'unit', 'campus', 'phone_number']
    search_fields = ['user', 'first_name', 'last_name', 'user__email']
    list_filter = ['gender', 'type', 'unit', 'campus']

