from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from .models import Student, Department
from .serializers import StudentSerializer
from .utils.main import api_response


def root(request):
    return render(request, "myapp/index.html")


def students(request):
    # getting the search query parameter from the requested URL
    search_text = request.GET.get("search", "").strip()

    # define supported sort options
    sort_options = {
        "Name ↑ (A-Z)": (Lower("first_name"), Lower("last_name"), "pk"),
        "Name ↓ (Z-A)": (Lower("first_name").desc(), Lower("last_name").desc(), "pk"),
        "Roll ↑ (Low-High)": ("roll_number",),
        "Roll ↓ (High-Low)": ("-roll_number",),
    }

    # getting the sort query parameter from the requested URL
    sort_by = request.GET.get("sort", "Roll ↑ (Low-High)")

    # validation for unexpected sort options
    if sort_by not in sort_options:
        sort_by = "Roll ↑ (Low-High)"

    # get all students
    allstudents = Student.objects.all()

    # doing search operation on the records
    if search_text:
        allstudents = allstudents.filter(
            Q(first_name__icontains=search_text)
            | Q(last_name__icontains=search_text)
            | Q(roll_number__icontains=search_text)
        )

    # getting the department query parameter from the requested URL
    selected_dept = request.GET.get("department", "").strip()

    dept_options = Department.objects.filter(is_active=True)

    # doing filter operation on the records
    if dept_options.filter(name=selected_dept):
        allstudents = allstudents.filter(department__name=selected_dept)

    # doing sort operation on the records
    allstudents = allstudents.order_by(*sort_options[sort_by])

    # create paginator
    paginator = Paginator(allstudents, 10)

    # getting the requested page number
    page_number = request.GET.get("page")

    # retrieve the requested page
    page_obj = paginator.get_page(page_number)

    # create a mutable copy of the existing query parameters
    query_params = request.GET.copy()

    # remove the page query parameter
    query_params.pop("page", None)

    context = {
        "page_obj": page_obj,
        "sort_options": sort_options,
        "selected_sort": sort_by,
        "search_text": search_text,
        "query_string": query_params.urlencode(),
        "dept_options": dept_options,
        "selected_dept": selected_dept,
    }

    return render(request, "myapp/students.html", context)


def student_profile(request, slug):
    student = get_object_or_404(Student, slug=slug)
    context = {"student": student}
    return render(request, "myapp/student_profile.html", context)


def add_student(request):
    if request.method == "POST":
        dept_code = request.POST.get("department")

        try:
            department = Department.objects.get(code=dept_code, is_active=True)

            student = Student(
                first_name=request.POST.get("first_name"),
                last_name=request.POST.get("last_name"),
                email=request.POST.get("email"),
                roll_number=request.POST.get("roll_number"),
                department=department,
                session_year=request.POST.get("session_year"),
                gender=request.POST.get("gender"),
                phone=request.POST.get("phone"),
                dob=request.POST.get("dob") or None,
            )

            student.full_clean()
            student.save()

        except Department.DoesNotExist:
            return render(
                request,
                "myapp/add_student.html",
                {
                    "errors": ["Please select a valid department!"],
                    "departments": Department.objects.filter(is_active=True),
                },
            )

        except ValidationError as error:
            return render(
                request,
                "myapp/add_student.html",
                {
                    "errors": error.messages,
                    "departments": Department.objects.filter(is_active=True),
                },
            )

        return redirect("students")

    departments = Department.objects.filter(is_active=True)

    return render(request, "myapp/add_student.html", {"departments": departments})


def update_student(request, slug):
    student = get_object_or_404(Student, slug=slug)

    if request.method == "POST":

        try:
            student.first_name = request.POST.get("first_name")
            student.last_name = request.POST.get("last_name")
            student.email = request.POST.get("email")
            student.roll_number = request.POST.get("roll_number")
            student.department = get_object_or_404(
                Department, code=request.POST.get("department")
            )
            student.session_year = request.POST.get("session_year")
            student.gender = request.POST.get("gender")
            student.phone = request.POST.get("phone")
            student.dob = request.POST.get("dob")

            student.full_clean()
            student.slug = ""
            student.save()

        except ValidationError as error:
            return render(
                request,
                "myapp/update_profile.html",
                {
                    "student": student,
                    "departments": Department.objects.filter(is_active=True),
                    "errors": error.messages,
                },
            )

        return redirect("student_profile", slug=student.slug)

    departments = Department.objects.filter(is_active=True)

    context = {"student": student, "departments": departments}

    return render(request, "myapp/update_profile.html", context)


def delete_student(request, slug):
    if request.method == "POST":

        student = get_object_or_404(Student, slug=slug)

        student.delete()

        return redirect("students")

    return redirect("students")


# API Views


@csrf_exempt
def students_api(request):
    # Get all students
    if request.method == "GET":
        students = Student.objects.all()

        serializer = StudentSerializer(students, many=True)

        return api_response(
            True, 200, "Students retrieved successfully", serializer.data
        )

    # Create a new student
    elif request.method == "POST":
        data = JSONParser().parse(request)

        serializer = StudentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return api_response(
                True, 201, "Student created successfully", serializer.data
            )
        return api_response(False, 400, "Student creation failed", serializer.errors)


def single_student_api(request, id):
    # Get a single student
    if request.method == "GET":
        try:
            student = Student.objects.get(id=id)

            serializer = StudentSerializer(student)

            return api_response(
                True, 200, "Student profile fetched successfully", serializer.data
            )
        except Student.DoesNotExist:
            return api_response(False, 404, "Student not found")
