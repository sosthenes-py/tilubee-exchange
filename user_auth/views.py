from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.decorators import custom_login_required


# Create your views here.
def boarding(request, page=1):
    if 1 <= page <= 3 and request.method == 'GET':
        return render(request, f'user_auth/boarding{page}.html')
    return HttpResponse(status=404)


@custom_login_required
def last_boarding(request):
    return render(request, 'user_auth/boarding_last.html')


def account_login(request):
    return redirect('user_auth:login')