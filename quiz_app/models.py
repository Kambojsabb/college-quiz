from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    score = models.IntegerField(default=0)
    current_question = models.IntegerField(default=1)
    warning_count = models.IntegerField(default=0)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_finished = models.BooleanField(default=False)
    session_key = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username


class Question(models.Model):
    order = models.IntegerField(unique=True)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1)

    def __str__(self):
        return f"Q{self.order}"


class QuizControl(models.Model):
    is_quiz_started = models.BooleanField(default=False)
    login_open = models.BooleanField(default=True)
    start_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Quiz Control"
