from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('waiting/', views.waiting_view, name='waiting'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('submit/', views.submit_answer, name='submit'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('start-quiz/', views.start_quiz, name='start_quiz'),
    path('tab-warning/', views.tab_warning),

]
