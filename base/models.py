from django.db import models
from users.models import CustomUser

    
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    questions = models.ManyToManyField('Question', through='QuizQuestion')
    # q_count = models.IntegerField()
    creator = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return self.title
    

class Question(models.Model):
    text = models.TextField()
    
    def __str__(self):
        return self.text
    

class Answer(models.Model):
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", blank=True, null=True)
    
    def __str__(self):
        return self.text
    

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField()
    # q_count = models.IntegerField()
    
    def __str__(self):
        return self.quiz.title + ' ' + str(self.order)
    

class ScoreRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=True, null=True)
    score = models.IntegerField()
    
    def __str__(self):
        return self.user.username +' ' + self.quiz.title + ' ' + str(self.score)
    
    def total_questions(self):
        return self.quiz.questions.count()
    
    
class QuizAttempt(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username + ' ' + self.quiz.title
    
    
class AnswerRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username + ' ' + self.question.text