from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .forms import TestCreateNameForm, TestCreateQuestionForm, TestCreateChoiceForm
from .models import Test, Users, User, Question, Choice, Marks
from datetime import datetime, date, time, timedelta
import base64
# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        user = Users.objects.filter(user=request.user)[0]
        if user.is_student:
            return redirect('mcq_test:dashboard_student')
        if user.is_faculty:
            return redirect('mcq_test:dashboard_faculty')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        userObject = User.objects.filter(username=username)
        userObject = authenticate(username=username, password=password)
        if userObject:
            login(request, userObject)
            user = Users.objects.filter(user=userObject)
            if user and user[0].is_faculty:
                return redirect('mcq_test:dashboard_faculty')

            elif user and user[0].is_student:
                return redirect('mcq_test:dashboard_student')
                
            else:
                return render(request, 'mcq_test/login.html', {'i': 'Invalid ID/Password'})
        else:
                return render(request, 'mcq_test/login.html', {'i': 'Invalid ID/Password'})
    else:
        return render(request,'mcq_test/login.html')

def logout_view(request):
    logout(request)
    return redirect("/")

def create_test_page1(request) :
    # print(request.user.is_faculty)
    user = Users.objects.filter(user=request.user)[0]
    if request.user.is_authenticated and user.is_faculty:
        if request.method == "POST" :
            form = TestCreateNameForm(request.POST) #, user=request.user)
            if form.is_valid():
                test = form.save(commit=False)
                # test.author = request.user
                # test.published_date = timezone.now()
                test.name = request.POST.get('name')
                start_date = request.POST.get('start_date')
                test.start_date = date(year=int(start_date[0:4]), month=int(start_date[5:7]), day=int(start_date[8:10]))
                start_time = request.POST.get('start_time')
                test.start_time = time(hour=int(start_time[0:2]), minute=int(start_time[3:5]), second=int(start_time[6:8]))
                duration = request.POST.get('duration')
                test.duration = timedelta(days=0, hours=int(duration[0:2]), minutes=int(duration[3:5]), seconds=(int(duration[6:8])))
                test.user = user
                test.save()
                return redirect('mcq_test:create_test_page2', tid=test.id)
            else:
                form = TestCreateNameForm()
                return render(request, 'mcq_test/create_test_page1.html', {'form': form, 'error': 'error'})
        else:
            form = TestCreateNameForm()
            return render(request, 'mcq_test/create_test_page1.html', {'form': form})
    else:
        return redirect('mcq_test:login_view')

def create_test_page2(request, tid) :
    # if request.user.is_authenticated() and request.user.is_faculty:
    test = get_object_or_404(Test, id=tid)
    if request.method == "POST" :
        form1 = TestCreateQuestionForm(request.POST, prefix="q") #, user=request.user)
        form2 = TestCreateChoiceForm(request.POST, prefix="c1") #, user=request.user)
        form3 = TestCreateChoiceForm(request.POST, prefix="c2") #, user=request.user)
        form4 = TestCreateChoiceForm(request.POST, prefix="c3") #, user=request.user)
        form5 = TestCreateChoiceForm(request.POST, prefix="c4") #, user=request.user)
        if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid():
            question = form1.save(commit=False)
            question.test = test
            question.question = form1.cleaned_data['question']
            question.save()
        #     question = get_object_or_404()
            choice1 = form2.save(commit=False)
            choice1.question = question
            choice1.choice = form2.cleaned_data['choice']
            choice1.answer = form2.cleaned_data['answer']
            choice1.save()
            choice2 = form3.save(commit=False)
            choice2.question = question
            choice2.choice = form3.cleaned_data['choice']
            choice2.answer = form3.cleaned_data['answer']
            choice2.save()
            choice3 = form4.save(commit=False)
            choice3.question = question
            choice3.choice = form4.cleaned_data['choice']
            choice3.answer = form4.cleaned_data['answer']
            choice3.save()
            choice4 = form5.save(commit=False)
            choice4.question = question
            choice4.choice = form5.cleaned_data['choice']
            choice4.answer = form5.cleaned_data['answer']
            choice4.save()
            
            if request.POST.get("next"):
                return redirect('mcq_test:create_test_page2', tid=test.id)
            elif request.POST.get("submit"):
                return redirect('mcq_test:dashboard_faculty')                
    else:
        form1 = TestCreateQuestionForm(prefix="q")
        form2 = TestCreateChoiceForm(prefix="c1")
        form3 = TestCreateChoiceForm(prefix="c2")
        form4 = TestCreateChoiceForm(prefix="c3")
        form5 = TestCreateChoiceForm(prefix="c4")
        return render(request, 'mcq_test/create_test_page2.html', {'form1': form1, 'form2':form2, 'form3': form3, 'form4':form4, 'form5': form5, 'tid':tid})

def display_test_faculty(request, tid):
    user = Users.objects.filter(user=request.user)[0]
    tests = Test.objects.filter(user=user)
    if request.user.is_authenticated and user.is_faculty and tests:
        test = Test.objects.filter(id=tid)[0]
        questions = Question.objects.filter(test=test)
        choices=Choice.objects.none()
        for question in questions:
            choices = choices | Choice.objects.filter(question=question)
        return render(request, 'mcq_test/display_test_faculty.html', {'test':test, 'questions':questions, 'choices':choices})
    else:
        return redirect('mcq_test:login_view')

    

def dashboard_faculty(request):
    user = Users.objects.filter(user=request.user)[0]
    if request.user.is_authenticated and user.is_faculty:
        tests = Test.objects.filter(user=user)
        return render(request, 'mcq_test/dashboard_faculty.html', {'tests': tests})
    else:
        return redirect('mcq_test:login_view')

def dashboard_student(request):
    user = Users.objects.filter(user=request.user)[0]
    if request.user.is_authenticated and user.is_student:
        marks = Marks.objects.filter(student=user)
        tests = Test.objects.none()
        for mark in marks:
            tests = tests | Test.objects.filter(id=mark.test.id)
        return render(request, 'mcq_test/dashboard_student.html', {'tests': tests, 'marks': marks})
    else:
        return redirect('mcq_test:login_view')

def leaderboard(request, tid):
    if request.user.is_authenticated:
        test = Test.objects.filter(id=tid)[0]
        marks = Marks.objects.filter(test=test)
        return render(request, 'mcq_test/leaderboard.html', {'marks': marks, 'tid':test.id})
    else:
        return redirect('mcq_test:login_view')

def test_view(request, tid):
    if request.user.is_authenticated:
        user=Users.objects.filter(user=request.user)[0]
        if user.is_student:
            #Add specific user condition here
            if request.method == "POST":
                test = Test.objects.filter(id=tid)[0]
                questions = Question.objects.filter(test=test)
                marks = Marks.objects.filter(student=user, test=test)
                if marks:
                    return HttpResponse("Can't Submit as You have already taken this test...")
                else:
                    answers = {}
                    answers_selected = {}

                    for question in questions:
                        temp = []
                        for choice in list(Choice.objects.filter(question=question, answer=True)):
                            temp.append(str(choice.choice_id))
                        
                        answers[question.question] = temp

                    for question in questions:
                        answers_selected[question.question] = request.POST.getlist(question.question)
                    
                    marks = 0
                    for question in questions:
                        base = answers[question.question]
                        check = answers_selected[question.question]
                        if base == check:
                            marks+=1
                    marks_object = Marks()
                    marks_object.test = test
                    marks_object.student = user
                    marks_object.marks = marks
                    marks_object.save()
                    return HttpResponse('Thanks...' + str(marks))
            else:
                test = Test.objects.filter(id=tid)[0]
                marks = Marks.objects.filter(student=user, test=test)
                curr = timezone.localtime(timezone.now())
                current = datetime(year=curr.year, month=curr.month, day=curr.day, hour=curr.hour, minute=curr.minute, second=curr.second)
                exam_date = test.start_date
                exam_time = test.start_time
                exam_start = datetime(year=exam_date.year, month=exam_date.month, day=exam_date.day, hour=exam_time.hour, minute=exam_time.minute, second=exam_time.second)
                exam_end = exam_start + test.duration
                if marks:
                    return HttpResponse('You have already taken this test...')
                elif ( current < exam_start):
                    return HttpResponse('Test has not started...')
                    # return the scorecard here
                elif ( current > exam_end):
                    return HttpResponse('Test is over...')
                    # return the scorecard here
                # elif ( current <= exam_start):
                #     return HttpResponse('Test has not started...')
                    # return the scorecard here
                else:
                    test = Test.objects.filter(id=tid)[0]
                    questions = Question.objects.filter(test=test)
                    choices=Choice.objects.none()
                    for question in questions:
                        choices = choices | Choice.objects.filter(question=question)

                    return render(request, 'mcq_test/test_view.html', {'test':test, 'questions':questions, 'choices':choices})
        else:
            return HttpResponse('You are not authorized to take this test')
    else:
        return redirect('mcq_test:login_view')

# def encode(string):
#     base64.b64encode(string.encode('utf-8'))
#     base64.b64decode(encoded_string).decode('utf-8')

