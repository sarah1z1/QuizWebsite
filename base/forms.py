from django import forms
from django.forms import inlineformset_factory
from .models import Quiz, Question, Answer, QuizQuestion

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']


class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ['order']


QuestionFormSet = inlineformset_factory(Quiz, QuizQuestion, form=QuizQuestionForm, extra=3)
AnswerFormSet = inlineformset_factory(Question, Answer, form=AnswerForm, extra=3)
