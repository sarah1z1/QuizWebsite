from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    
    path('quiz/<int:quizId>/', views.quizInfo, name="quiz_info"),
    path('quiz/<int:quizId>/question/<int:order>/', views.quizStart, name="quiz"),
    path('quiz/<int:quizId>/complete/', views.quizComplete, name="quiz_complete"),
    
    path('quiz/create/', views.createQuiz, name="create_quiz"),
    path('quiz/<int:quizId>/add_questions/', views.addQuestions, name="add_questions"),
    
    path('profile/', views.profile, name="profile"),
]
