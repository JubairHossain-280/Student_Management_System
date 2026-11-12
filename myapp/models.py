from django.db import models
from django.db.models import Q
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils.text import slugify

# Create your models here.


# gender choices
class Gender(models.TextChoices):
    MALE = "Male", "Male"
    FEMALE = "Female", "Female"
    OTHER = "Other", "Other"


# Student model
class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    roll_number = models.PositiveIntegerField(
        unique=True, validators=[MinValueValidator(100000), MaxValueValidator(999999)]
    )
    department = models.ForeignKey(
        "Department", on_delete=models.PROTECT, related_name="students"
    )
    session_year = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                regex=r"^\d{4}-\d{2}$",
                message="Enter a valid session year (e.g., 2022-23)",
            )
        ],
    )
    phone = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r"^01[3-9]\d{8}$", message="Enter a valid phone number"
            )
        ],
    )
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.first_name}-{self.last_name}")
            slug = base_slug
            counter = 1

            while Student.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

        constraints = [
            models.CheckConstraint(
                condition=Q(roll_number__gte=100000, roll_number__lte=999999),
                name="6_digit_roll_number",
            ),
            models.CheckConstraint(
                condition=Q(session_year__regex=r"^\d{4}-\d{2}$"),
                name="valid_session_year",
            ),
            models.CheckConstraint(
                condition=Q(phone__regex=r"^01[3-9]\d{8}$"),
                name="valid_bangladeshi_phone",
            ),
            models.CheckConstraint(
                condition=Q(gender__in=Gender.values),
                name="valid_student_gender",
            ),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Department model
class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=100)
    code = models.CharField(unique=True, max_length=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name
