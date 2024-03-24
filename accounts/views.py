from django.shortcuts import render
from .forms import CustomUserCreationForm, LoginForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .models import CustomUser
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/auth-register-basic.html'
    success_url = reverse_lazy('accounts:success')

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class LoginView(FormView):
    template_name = 'accounts/auth-login-basic.html'
    form_class = LoginForm
    success_url = reverse_lazy('dashboard:home')  # Change this to your desired URL after login

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        return self.success_url

    def form_invalid(self, form):
        print("Invalid Form ", form)
        return super().form_invalid(form)


class SuccessView(TemplateView):
    template_name = 'accounts/success-page.html'
