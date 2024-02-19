from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import College, Unit, Department, Campus, Staff


class Command(BaseCommand):
    help = 'Creates the default groups and assigns permissions'

    def handle(self, *args, **options):
        # Create groups
        staff_group, created = Group.objects.get_or_create(name='Staff')
        unit_manager_group, created = Group.objects.get_or_create(name='Unit Manager')
        campus_manager_group, created = Group.objects.get_or_create(name='Campus Manager')
        admin_group, created = Group.objects.get_or_create(name='Admin')
        superuser_group, created = Group.objects.get_or_create(name='Superuser')

        # Get the content types for your models
        college_content_type = ContentType.objects.get_for_model(College)
        unit_content_type = ContentType.objects.get_for_model(Unit)
        department_content_type = ContentType.objects.get_for_model(Department)
        campus_content_type = ContentType.objects.get_for_model(Campus)
        staff_content_type = ContentType.objects.get_for_model(Staff)

        # Assign permissions to groups
        staff_group.permissions.add(
            Permission.objects.get(content_type=staff_content_type, codename='view_staff'),
        )
        unit_manager_group.permissions.add(
            Permission.objects.get(content_type=unit_content_type, codename='change_unit'),
            Permission.objects.get(content_type=unit_content_type, codename='view_unit'),
            Permission.objects.get(content_type=department_content_type, codename='view_department'),
            Permission.objects.get(content_type=department_content_type, codename='change_department'),
            Permission.objects.get(content_type=staff_content_type, codename='view_staff'),
            Permission.objects.get(content_type=staff_content_type, codename='change_staff'),
        )
        campus_manager_group.permissions.add(
            Permission.objects.get(content_type=college_content_type, codename='change_college'),
            Permission.objects.get(content_type=college_content_type, codename='view_college'),
            Permission.objects.get(content_type=unit_content_type, codename='change_unit'),
            Permission.objects.get(content_type=unit_content_type, codename='view_unit'),
            Permission.objects.get(content_type=staff_content_type, codename='view_staff'),
        )
        admin_group.permissions.add(
            Permission.objects.get(content_type=campus_content_type, codename='change_campus'),
            Permission.objects.get(content_type=campus_content_type, codename='view_campus'),
            Permission.objects.get(content_type=college_content_type, codename='view_college'),
            Permission.objects.get(content_type=unit_content_type, codename='view_unit'),
            Permission.objects.get(content_type=department_content_type, codename='view_department'),
            Permission.objects.get(content_type=staff_content_type, codename='view_staff'),
        )
        superuser_group.permissions.add(*Permission.objects.all())

        self.stdout.write(self.style.SUCCESS('Successfully created groups and assigned permissions'))
