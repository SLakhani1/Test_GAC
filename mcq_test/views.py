from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .forms import TestCreateNameForm, TestCreateQuestionForm, TestCreateChoiceForm
from .models import Test

# Create your views here.

def login_view(request):
    # if request.user.is_authenticated() and request.user.is_student:
    #     return redirect('dashboard_student')
    #  if request.user.is_authenticated() and request.user.is_faculty:
    #     return redirect('dashboard_student')
    pass

def logout_view(request):
    logout(request)
    return redirect("/")

def create_test_page1(request) :
    # if request.user.is_authenticated() and request.user.is_faculty:
    if request.method == "POST" :
        form = TestCreateNameForm(request.POST) #, user=request.user)
        if form.is_valid():
            test = form.save(commit=False)
            # test.author = request.user
            # test.published_date = timezone.now()
            test.name = request.POST.get('name')
            test.save()
            return redirect('mcq_test:create_test_page2', tid=test.id)
    else:
        form = TestCreateNameForm()
        return render(request, 'mcq_test/create_test_page1.html', {'form': form})

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
            # if next button new test_page2 instance else home of faculty
        #     if
            if request.POST.get("next"):
                return redirect('mcq_test:create_test_page2', tid=test.id)
            elif request.POST.get("submit"):
                return redirect('mcq_test:teacher_dashboard')                
                #         return HttpResponseRedirect(reverse('portal_home'))
                # elif request.POST.get("save_next"):  # You can use else in here too if there is only 2 submit types.
                #         return HttpResponseRedirect(reverse('portal_sec2'))
    else:
        form1 = TestCreateQuestionForm(prefix="q")
        form2 = TestCreateChoiceForm(prefix="c1")
        form3 = TestCreateChoiceForm(prefix="c2")
        form4 = TestCreateChoiceForm(prefix="c3")
        form5 = TestCreateChoiceForm(prefix="c4")
        return render(request, 'mcq_test/create_test_page2.html', {'form1': form1, 'form2':form2, 'form3': form3, 'form4':form4, 'form5': form5, 'tid':tid})

def display_test(request):
    pass