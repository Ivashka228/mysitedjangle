from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from crm.models import Student, Course, Comments
from django import forms

class RegisterValidation(forms.Form):
    login = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(min_length=6)

class LoginValidation(forms.Form):
    login = forms.CharField(max_length=30)
    password = forms.CharField(min_length=6)

def courses(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        courses = Course.objects.all()
        return render(request, 'courses.html', {'courses': courses})
    if request.method == 'POST':
        name = request.POST.get('name1', '')
        courses = Course.objects.filter(name__contains=name).all()
        return render(request, 'courses2.html', {'courses':courses})


def addcourse(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        return render(request, 'addcourse.html')
    if request.method == 'POST':
        name = request.POST.get('name', '')
        teacher = request.POST.get('teacher', '')
        if name == '' or teacher == '':
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/addcourse')

        course = Course()
        course.name = name
        course.teacher = teacher
        course.save()
        return redirect('/course?id={}'.format(course.id))
def detailscourse(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    id = request.GET.get('id')
    course = Course.objects.get(pk=id)
    return render(request, 'detailscourse.html', {'course': course})

def editcourse(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        id = request.GET.get('id')
        course = Course.objects.get(pk=id)
        return render(request, 'editcourse.html', {'course': course})
    if request.method == 'POST':
        name = request.POST.get('name', '')
        teacher = request.POST.get('teacher', '')
        id = request.GET.get('id')

        if name == '' or teacher == '':
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/editcourse?id='+str(id))

        course = Course.objects.get(pk=id)
        course.name = name
        course.teacher = teacher
        course.save()

        return redirect('/course?id={}'.format(course.id))

def index(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        students = Student.objects.all()
        return render(request, 'index.html', {'students': students})
    if request.method == 'POST':
        name = request.POST.get('name1', '')
        students = Student.objects.filter(name__contains=name).all()
        return render(request, 'index2.html', {'students': students})
def details(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        id = request.GET.get('id')
        student = Student.objects.get(pk=id)
        comments = Comments.objects.filter(student=student)
        return render(request, 'details.html', {'student': student, 'comments': comments})
    if request.method == 'POST':
        id = request.GET.get('id')
        text = request.POST.get('text', '')
        user = request.user
        student = Student.objects.get(pk=id)
        comment = Comments()
        comment.text = text
        comment.student = student
        comment.save()
        comments = Comments.objects.filter(student=student)
        return render(request, 'details.html', {'comments': comments, 'student': student})

def add(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        courses = Course.objects.all()
        return render(request, 'add.html', {'courses': courses})
    if request.method == 'POST':
        name = request.POST.get('name', '')
        surname = request.POST.get('surname', '')
        course_id = request.POST.get('course_id', '')
        email = request.POST.get('email', '')
        room = request.POST.get('room', '')
        description = request.POST.get('description', '')

        if name == '' or surname == '':
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/add')

        student = Student()
        if 'avatar' in request.FILES:
            student.photo = request.FILES['avatar']
        student.name = name
        student.surname = surname
        student.email = email
        student.description = description
        student.room = room
        if course_id != '':
            course = Course.objects.get(pk=course_id)
            student.course = course
        else:
            student.course = None
        student.save()



        return redirect('/student?id={}'.format(student.id))

def edit(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        id = request.GET.get('id')
        courses = Course.objects.all()
        student = Student.objects.get(pk=id)
        return render(request, 'edit.html', {'student': student, 'courses': courses})
    if request.method == 'POST':
        name = request.POST.get('name', '')
        surname = request.POST.get('surname', '')

        id = request.GET.get('id')

        if name == '' or surname == '':
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/edit?id='+str(id))

        student = Student.objects.get(pk=id)
        if 'avatar' in request.FILES:
            student.photo = request.FILES['avatar']
        student.name = name
        student.surname = surname
        student.save()

        return redirect('/student?id={}'.format(student.id))

def delete(request):
    id = request.GET.get('id')
    student = Student.objects.get(pk=id)
    student.delete()

    return redirect('/')

def deletecomment(request):
    id = request.GET.get('id')
    comment = Comments.objects.get(pk=id)
    student = comment.student
    comment.delete()

    return redirect('/student?id='+str(student.id))

def deletecourse(request):
    id = request.GET.get('id')
    course = Course.objects.get(pk=id)
    students = Student.objects.all()
    for student in students:
        if student.course.name == course.name:
            student.course = None
    course.delete()
    return redirect('/courses')


def logout_page(request):
    logout(request)
    return redirect('/login')

def login_page(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = LoginValidation(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/login')

        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.add_message(request, messages.ERROR, 'Введенные данные неверны!')
            return redirect('/login')
        else:
            login(request, user)
            return redirect('/')

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        form = RegisterValidation(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/register')

        user = User()
        user.username = request.POST.get('login')
        user.email = request.POST.get('email')
        user.set_password(request.POST.get('password'))
        user.save()

        login(request, user)

        return redirect('/')

def comments(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    comments = Comments.objects.all()
    return render(request, 'comments.html', {'comments': comments})

def comment(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    id = request.GET.get('id')
    comment = Comments.objects.get(pk=id)
    return render(request, 'comment.html', {'comment': comment})