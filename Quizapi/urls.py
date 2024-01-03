from django.urls import path
from .views import quiz, quizsList
urlpatterns = [
    path('quiz', quizsList.QuizAPIView.as_view()),
    path('quiz/<str:quiz_id>',quiz.QuestionDetailView.as_view())

]

