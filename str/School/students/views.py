from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from .models import Student
from .forms import StudentForm
from django.db.models import Q 
import csv
# Create Student
def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/create_student.html', {'form': form})

# Read Students (List View)
def student_list(request):
    query = request.GET.get('q')  # Get the search term from the query parameter
    if query:
        # Filter students by first name or last name containing the search term
        students = Student.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    else:
        students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students, 'query': query})

# Update Student
def update_student(request, id):
    student = Student.objects.get(id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/update_student.html', {'form': form, 'student': student})

# Delete Student
def delete_student(request, id):
    student = Student.objects.get(id=id)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'students/delete_student.html', {'student': student})

def generate_report(request, student_id):
    # Fetch the specific student or return 404 if not found
    student = get_object_or_404(Student, id=student_id)

    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="student_report_{student_id}.csv"'

    # Create a CSV writer
    writer = csv.writer(response)
    # Write the header row
    writer.writerow(['First Name', 'Last Name', 'Email', 'Age', 'Date Registered'])

    # Write the data row for the specific student
    writer.writerow([student.first_name, student.last_name, student.email, student.age, student.created_at])

    return response