from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Student, Branch, Section, Year
import qrcode
import socket
from StudentView.views import present


def qrgenerator():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]

    link = f"http://{ip}:8000/add_manually"

    def generate_qr_code(link):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("FacultyView/static/FacultyView/qrcode.png")

    generate_qr_code(link)


def faculty_view(request):
    if request.method == "POST":
        student_roll = request.POST["student_id"]
        student = Student.objects.get(s_roll=student_roll)
        if student in present:
            present.remove(student)
        return HttpResponseRedirect("/")

    else:
        qrgenerator()
        return render(
            request,
            "FacultyView/FacultyViewIndex.html",
            {
                "students": present,
            },
        )


def add_manually(request):
    students = Student.objects.all().order_by("s_roll")
    return render(
        request,
        "StudentView/StudentViewIndex.html",
        {
            "students": students,
        },
    )


def add_student(request):
    branches = Branch.objects.all()
    sections = Section.objects.all()
    years = Year.objects.all()

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        matricule = request.POST.get("matricule", "").strip()

        # Split full name into first and last
        parts = full_name.split(" ", 1)
        fname = parts[0]
        lname = parts[1] if len(parts) > 1 else ""

        # Use first available branch/section/year as default
        branch = Branch.objects.first()
        section = Section.objects.first()
        year = Year.objects.first()

        if matricule and not Student.objects.filter(s_roll=matricule).exists():
            Student.objects.create(
                s_roll=matricule,
                s_fname=fname,
                s_lname=lname,
                s_branch=branch,
                s_section=section,
                s_year=year,
            )

        return redirect("faculty_view")

    return render(request, "FacultyView/AddStudent.html", {
        "branches": branches,
        "sections": sections,
        "years": years,
    })