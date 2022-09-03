from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from user.models import User
from .forms import LoginForm, RegisterForm
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm
User = get_user_model()


def index(request):
    return render(request, "index.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
     msg = None
     is_ok = False
     if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                is_ok = True
                return redirect("index")
        else:
            msg = "올바른 유저ID와 패스워드를 입력하세요."
     else:
        form = AuthenticationForm()

     for visible in form.visible_fields():
        visible.field.widget.attrs["placeholder"] = "유저ID" if visible.name == "username" else "패스워드"
        visible.field.widget.attrs["class"] = "form-control"
     
     return render(request, "login.html", {"form": form, "msg": msg, "is_ok": is_ok})


def logout_view(request):
    # TODO: 3. /logout url을 입력하면 로그아웃 후 / 경로로 이동시켜주세요						
    logout(request)
    #return HttpResponseRedirect("/login")
    return redirect("index")

# TODO: 8. user 목록은 로그인 유저만 접근 가능하게 해주세요
@login_required
def user_list_view(request):
    # TODO: 7. /users 에 user 목록을 출력해주세요
    # TODO: 9. user 목록은 pagination이 되게 해주세요
    page = int(request.GET.get("page", 1))
    users = User.objects.all().order_by("-id")
    paginator = Paginator(users, 10)
    users = paginator.get_page(page)
    return render(request, "users.html", {"users": users})
