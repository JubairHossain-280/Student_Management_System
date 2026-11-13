# accounts/management/commands/setup_roles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from myapp.models import Student, Department


class Command(BaseCommand):
    help = "Creates Teacher and Student groups with appropriate permissions"

    def handle(self, *args, **options):
        # Content types
        student_ct = ContentType.objects.get_for_model(Student)
        dept_ct = ContentType.objects.get_for_model(Department)

        # Permissions
        view_student = Permission.objects.get(
            codename="view_student", content_type=student_ct
        )
        add_student = Permission.objects.get(
            codename="add_student", content_type=student_ct
        )
        change_student = Permission.objects.get(
            codename="change_student", content_type=student_ct
        )

        view_dept = Permission.objects.get(
            codename="view_department", content_type=dept_ct
        )

        # 1. Setup Student Group
        student_group, _ = Group.objects.get_or_create(name="Student")
        student_group.permissions.set([view_student, view_dept])
        self.stdout.write(self.style.SUCCESS("✓ Configured 'Student' group"))

        # 2. Setup Teacher Group
        teacher_group, _ = Group.objects.get_or_create(name="Teacher")
        teacher_group.permissions.set(
            [view_student, add_student, change_student, view_dept]
        )
        self.stdout.write(self.style.SUCCESS("✓ Configured 'Teacher' group"))
