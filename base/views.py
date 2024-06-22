from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from users.models import CustomUser
from .models import QuizQuestion, Quiz, Question, ScoreRecord, Answer, QuizAttempt, AnswerRecord
from .forms import QuizForm, QuestionForm, QuestionFormSet, AnswerFormSet


def home(request):
    quizes = Quiz.objects.all()
        
    context = {'quizes':quizes}
    return render(request, 'base/home.html', context)


def quizInfo(request, quizId):
    quiz = Quiz.objects.get(id=quizId)
    
    context = {'quiz': quiz}
    return render(request, 'base/quiz.html', context)


@login_required(login_url='/login/')
def quizStart(request, quizId, order):
    quiz = get_object_or_404(Quiz, id=quizId)
    questions = QuizQuestion.objects.filter(quiz=quiz).order_by('order')
    total_questions = questions.count()
    user = request.user
    
    if QuizAttempt.objects.filter(user=user, quiz=quiz).exists():
        return redirect('quiz_complete', quizId=quizId)
    
    if total_questions == 0:
        messages.error(request, 'There are no questions yet in this quiz!')
        return redirect('quiz_info', quizId=quizId)
        
    if order > total_questions:
        QuizAttempt.objects.create(user=user, quiz=quiz)
        return redirect('quiz_complete', quizId=quizId)
    
    current_question = questions[order-1].question

    if AnswerRecord.objects.filter(user=user, question=current_question).exists():
        messages.error(request, 'You can not answer a question twice!!')
        return redirect('quiz',quizId=quizId, order=order+1)
        
    if request.method == 'POST':
        selected_answer_id = request.POST.get('answer')
        selected_answer = Answer.objects.get(id=selected_answer_id)
        AnswerRecord.objects.create(user=request.user, question=current_question)
        score_record, created = ScoreRecord.objects.get_or_create(user=user, quiz=quiz, defaults={'score': 0})
        
        if selected_answer.is_correct:
            score_record.score += 1
            score_record.save()
        
        return redirect('quiz', quizId=quizId, order=order+1)
    
    context = {'quiz':quiz, 'question':current_question, 'total_questions':total_questions, 'order':order}
    return render(request, 'base/quiz_start.html', context)


@login_required(login_url='/login/')
def quizComplete(request, quizId):
    page = 'complete'
    user = request.user
    quiz = get_object_or_404(Quiz, id=quizId)
    score = ScoreRecord.objects.get(user=user, quiz=quiz)
    total_questions = quiz.questions.all().count
    
    context = {'score':score, 'total_questions':total_questions, 'quiz':quiz, 'page':page}
    return render(request, 'base/quiz.html', context)


@login_required(login_url='/login/')
def profile(request):
    user = request.user
    score_records = ScoreRecord.objects.filter(user=user)
    total_questions = {record: record.quiz.questions.count() for record in score_records}
    
    context = {'score_records': score_records, 'total_questions':total_questions}
    return render(request, 'base/profile.html', context)



def check_if_teacher(user):
    return user.is_teacher


@user_passes_test(check_if_teacher)
@login_required(login_url='/login/')
def createQuiz(request):
    form = QuizForm()
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.creator = request.user
            quiz.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request, 'base/create_quiz.html', context)


@user_passes_test(check_if_teacher)
@login_required(login_url='/login/')
def addQuestions(request, quizId):
    quiz = get_object_or_404(Quiz, id=quizId)
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz_info', quizId=quizId)
        
    context = {'form': form}
    return render(request, 'base/add_questions.html', context)