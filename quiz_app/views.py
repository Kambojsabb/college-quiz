from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.utils import timezone
from .models import Question, QuizControl
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.utils.timezone import now
from django.contrib.admin.views.decorators import staff_member_required

User = get_user_model()

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']


        control = QuizControl.objects.first()
        print("CONTROL OBJECT:", control)
        if control:
            print("LOGIN OPEN VALUE:", control.login_open)

        user = authenticate(request, username=username, password=password)
        print("AUTH USER:", user)
        if not control or not control.login_open:
            return render(request, 'login.html', {'error': 'Login Closed'})

        user = authenticate(request, username=username, password=password)
        if user:
            if user.session_key:
                return render(request, 'login.html', {'error': 'User already logged in'})
            login(request, user)
            user.session_key = request.session.session_key
            user.save()
            return redirect('waiting')

    return render(request, 'login.html')


@login_required
def waiting_view(request):
    control = QuizControl.objects.first()

    if control and control.is_quiz_started:
        if not request.user.start_time:
            request.user.start_time = control.start_time
            request.user.save()
        return redirect('quiz')

    return render(request, 'waiting.html', {
        'quiz_started': control.is_quiz_started if control else False
    })



@login_required
def quiz_view(request):
    user = request.user
    question = Question.objects.filter(order=user.current_question).first()

    if not question:
        user.end_time = timezone.now()
        user.is_finished = True
        user.save()
        return redirect('leaderboard')

    return render(request, 'quiz.html', {'question': question})


@login_required
def submit_answer(request):
    if request.method == "POST":
        user = request.user
        selected = request.POST.get('option')
        question = Question.objects.get(order=user.current_question)

        if selected == question.correct_option:
            user.score += 1

        user.current_question += 1
        user.save()

        return JsonResponse({'status': 'next'})


@login_required
def leaderboard_view(request):
    users = User.objects.filter(is_finished=True).order_by('-score', 'end_time')
    return render(request, 'leaderboard.html', {'users': users})


@staff_member_required
def start_quiz(request):
    control = QuizControl.objects.first()
    control.is_quiz_started = True
    control.login_open = False
    control.start_time = now()
    control.save()
    return redirect('/admin/')

@login_required
def tab_warning(request):
    user = request.user
    user.warning_count += 1
    user.save()

    if user.warning_count >= 2:
        logout(request)
        return JsonResponse({'logout': True})

    return JsonResponse({'warning': True})

