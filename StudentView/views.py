from django.shortcuts import render
from FacultyView.models import Student
from django.http import HttpResponseRedirect

present = []

def add_manually_post(request):
    if request.method == "POST":
        student_roll = request.POST.get("student-name")
        if student_roll:
            try:
                student = Student.objects.get(s_roll=student_roll)
                if student not in present:
                    present.append(student)
            except Student.DoesNotExist:
                pass
    return HttpResponseRedirect("/submitted")


def submitted(request):
    return render(request, "StudentView/Submitted.html")