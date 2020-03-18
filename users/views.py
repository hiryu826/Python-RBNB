from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms, models

# from django.shortcuts import render


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    # initial = {"email": "ryush@naver.com"}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)

        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "Ryu",
        "last_name": "Sehyun",
        "email": "92rsh@naver.com",
    }

    def form_valid(self, form):
        # form이 유요할 시 save가 동작한다.
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.send_verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add succes message
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))


# -----------------------------------
# LoginView를 활용한 인증 기능
# class LoginView(View):
#     def get(self, request):
#         form = forms.LoginForm()
#         return render(request, "users/login.html", {"form": form})

#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():  # 인증 된 유효한 값만을 출력한다.
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse("core:home"))
#         return render(request, "users/login.html", {"form": form})


# def log_out(request):
#     logout(request)
#     return redirect(reverse("core:home"))


# -----------------------------------
# # Function 기반 View
# def login_view(reuqest):
#     if request.method == "GET":
#         pass
#     else requset.method == "POST":
