from UserApp.admin import CustomUser
from django.db import models
from UserApp.models import CustomUser
import uuid
from django.utils import timezone

class QuizTaken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    date_test_given = models.DateTimeField(default=timezone.now)

class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=1000)

    def __str__(self):

        return self.question


class Options(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.CharField(max_length=200)
    marks = models.IntegerField()

    def __str__(self) :
        return self.option

class QuizAttemptAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=200)
    answer = models.ForeignKey(Options, on_delete=models.CASCADE)
    quiz_taken = models.ForeignKey(QuizTaken, on_delete=models.CASCADE)
    
