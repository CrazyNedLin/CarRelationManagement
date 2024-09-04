from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from . import models
from .models import User
from .models import Attendance


# Create your views here.
def index(request):
    return render(request, './login/index.html')


def login(request):
    if request.session.get('loginFlag'):
        return redirect('/')

    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        if email and password:
            user = models.User.objects.filter(email=email)
            if user:
                _password = user[0].password
            else:
                return render(request, './login/login.html')
            if password == _password:
                request.session['loginFlag'] = True
                request.session['username'] = user[0].name
                return redirect('/')
            else:
                return render(request, './login/login.html')

    return render(request, './login/login.html')


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        name = request.POST.get('name', None)
        password1 = request.POST.get('password1', None)
        password2 = request.POST.get('password2', None)

        if password1 == password2:
            user = models.User.objects.filter(email=email)
            if user:
                print('error:此信箱已被註冊 請重新註冊')
                return redirect('/register/',{'message':'此信箱已被註冊，請重新註冊。'})
            new_user = models.User.objects.create()
            new_user.name = name
            new_user.email = email
            new_user.password = password1
            new_user.save()
            return redirect('/login/')

    return render(request, './login/register.html')

def logout(request):
    if request.session.get('loginFlag'):
        request.session.flush()
        return redirect('/login/')

    return redirect('/')


def attendance_view(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        action = request.POST.get('action')

        if not User.objects.filter(name=account).exists():
            return JsonResponse({"error": "Invalid account"}, status=400)

        today = timezone.now().date()

        if action == 'check_in':
            existing_attendance = Attendance.objects.filter(
                account=account, check_in_time__date=today).first()

            if existing_attendance:
                return JsonResponse({"error": "Already checked in today"},
                                    status=400)

            Attendance.objects.create(account=account,
                                      check_in_time=timezone.now())

        elif action == 'check_out':
            latest_attendance = Attendance.objects.filter(
                account=account, check_in_time__date=today).last()

            if latest_attendance and not latest_attendance.check_out_time:
                latest_attendance.check_out_time = timezone.now()
                latest_attendance.save()
            else:
                return JsonResponse(
                    {"error": "No valid check-in record found for checkout"},
                    status=400)

        return JsonResponse({"success": "Action completed successfully"})

    return render(request, './login/attendance.html')