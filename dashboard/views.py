from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import *
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from accounts.models import CustomUser
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView

from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'


class ProfileDetailView(DetailView):
    template_name = 'dashboard/profile_settings/profile-page.html'
    model = CustomUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = CustomUser.objects.filter(id=self.request.user.id).first()
        return context


class ProfileUpdateView(UpdateView):
    model = CustomUser
    success_url = reverse_lazy('dashboard:home')
    fields = ('first_name', 'last_name', 'email', 'phone_number')
    template_name = 'dashboard/profile_settings/profile-page.html'

    def form_invalid(self, form):
        # Form data is invalid, handle the invalid form data
        # Example: Display error messages to the user
        print(form.errors)
        return super().form_invalid(form)

    def get_object(self, queryset=None):
        # Return the object to be updated
        print("User ",CustomUser.objects.get(pk=self.kwargs['pk']) )
        return CustomUser.objects.get(pk=self.kwargs['pk'])


class UserAPIView(TemplateView):
    template_name = 'dashboard/user-api.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = CustomUser.objects.filter(id=self.request.user.id).first()
        return context