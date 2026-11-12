from django.contrib import admin
from .models import Student, Department


# Register your models here.
class student_admin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "created_at")
    # prepopulated_fields = {"slug": ("first_name", "last_name")}


class department_admin(admin.ModelAdmin):
    list_display = ("name", "code")


admin.site.register(Student, student_admin)
admin.site.register(Department, department_admin)
