from django.contrib import admin
from .models import Quiz, Question, QuizQuestion, Answer, ScoreRecord, QuizAttempt, AnswerRecord

# Register your models here.

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(QuizQuestion)
admin.site.register(Answer)
admin.site.register(ScoreRecord)
admin.site.register(QuizAttempt)
admin.site.register(AnswerRecord)

