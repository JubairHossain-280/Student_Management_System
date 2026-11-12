from django.urls import path
from . import views

urlpatterns = [
    path("", views.root, name="root"),
    path("students/", views.students, name="students"),
    path("students/profile/<slug:slug>", views.student_profile, name="student_profile"),
    path("add-new/", views.add_student, name="add_student"),
    path(
        "students/profile/update/<slug:slug>",
        views.update_student,
        name="update_student",
    ),
    path(
        "students/profile/delete/<slug:slug>",
        views.delete_student,
        name="delete_student",
    ),
    # API Routes
    path("api/students/", views.students_api, name="students_api"),

    path("api/students/<int:id>", views.single_student_api, name="single_student_api"),
]
