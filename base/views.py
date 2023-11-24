from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm
from .models import Course, Lesson, User
from .forms import CourseForm, LessonForm,UserForm, MyUserCreationForm
# from django.http import HttpResponse

# Create your views here

# courses = [
#     {
#         'id': 1, 
#         'name': 'python'
#     },
#     {
#         'id': 2, 
#         'name': 'html'
#     },
#     {
#         'id': 3, 
#         'name': 'css'
#     },
# ]

# Create your views here.


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated: 
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try: 
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user not exist')

        user =authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else: 
            messages.error(request, 'username and pass not exist')


    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    # page = 'register'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else: 
            messages.error(request, 'an error')

    return render(request, 'base/login_register.html', {'form':form})
    

# home page 
def home(request):
    courses = Course.objects.all()
    user = User.objects.all()
    context = {
        'courses': courses,
        'username': user,
        }
    return render(request, 'base/home.html', context)

# home page 
def admin2(request):
    return render(request, 'base/admin2.html')

# # admin: manage course list
# def courseList(request):
#     return render(request, 'base/course_list.html')


# admin: manage course list
def courseList(request, pk):
    # course = None
    # for i in courses:
    #     if i['name'] == str(pk):
    #         course = i
    course = Course.objects.get(course_id=pk)
    context = {'course': course}
    return render(request, 'base/course_list.html',context)

@login_required(login_url='home')
def course(request):
    # course = Course.objects.all(User.objects.all())
    users = User.objects.all()

    user_courses_dict = {}

    for user in users:
        enrolled_courses = user.courses.all()
        user_courses_dict[user] = enrolled_courses
        
    context = {'user_courses_dict': user_courses_dict}
    return render(request, 'base/course.html', context)



@login_required
def view_lessons(request, course_id):
    # Retrieve the course with the specified ID or return a 404 if not found
    course = get_object_or_404(Course, course_id=course_id)

    # Check if the current user's id is associated with the course
    if request.user.id not in course.users.values_list('id', flat=True):
        # If not enrolled, show an error message
        return HttpResponse('you are not enrolled to this couse.')

    # You can add more logic here to retrieve lessons or other information related to the course

    context = {'course': course}
    return render(request, 'base/view_lessons.html', context)


def createCourse(request):
    form = CourseForm()
    if request.method == 'POST':
        # print(request.POST)
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/course_form.html', context)

# def updateCourse(request, pk):
#     course = Course.objects.get(course_id=pk)
#     form = CourseForm(instance=course)
#     context = {'form': form}
#     return render(request, 'base/course_form.html', context)

def createLesson(request):
    form = LessonForm()
    if request.method == 'POST':
        print(request.POST)
    context = {'form': form}
    return render(request, 'base/lesson_form.html', context)





