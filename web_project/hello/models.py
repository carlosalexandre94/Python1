from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class QuestionFlow(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    next_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='next_questions')

    def __str__(self):
        return f"{self.answer} -> {self.next_question}"

class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255)
    question_ids = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.session_id} - {self.question_ids}"
