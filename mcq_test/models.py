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
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

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
    # position = models.IntegerField("position")
    answer = models.BooleanField(default=False)

    # class Meta:
    #     unique_together = [
    #         # no duplicated choice per question
    #         ("question", "choice"), 
    #         # no duplicated position per question 
    #         ("question", "position") 
    #     ]
    #     ordering = ("position",)

    def __str__(self):
        return str(self.question) + " - " +str(self.choice_id)