from django import forms
from .models import Test, Question, Choice

class TestCreateNameForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('name','start_date', 'start_time', 'duration',)

class TestCreateQuestionForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(TestCreateQuestionForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = Question
        fields = ('question',)

class TestCreateChoiceForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(TestCreateChoiceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Choice
        fields = ('choice', 'answer',)