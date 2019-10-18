from django.db import models
from django.contrib.auth.models import User

# # Create your models here.
# class Test(models.Model):
#     id = models.AutoField(primary_key=True)
#     # question =  models.ManyToManyField(Question, blank=False, related_name="")
#     activationTime = models.DateTimeField
#     # link = models.CharField(blank=False) Generate it

#     def __str__(self):
#         pass
class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)

class Test(models.Model):
    user = models.ForeignKey("Users", on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    start_time = models.TimeField()
    duration = models.TimeField()

    def __str__(self):
        return str(self.id) + " " + self.name

class Question(models.Model):
    # question_id = models.AutoField(primary_key=True)
    test = models.ForeignKey("Test", related_name="questions", on_delete=models.CASCADE)
    question = models.CharField(max_length=500)

    def __str__(self):
        return str(self.test) + " - " + str(self.question)

class Choice(models.Model):
    choice_id = models.AutoField(primary_key=True)
    question = models.ForeignKey("Question", related_name="choices", on_delete=models.CASCADE)
    choice = models.CharField(max_length=50)
    answer = models.BooleanField(default=False)

    def __str__(self):
        return str(self.question) + " - " +str(self.choice_id)

class Marks(models.Model):
    id = models.AutoField(primary_key=True)
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    student = models.ForeignKey('Users', on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.test_id) + '-' + str(self.student) + '-' + str(self.marks)