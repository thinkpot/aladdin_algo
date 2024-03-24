from django.shortcuts import render
from django.views.generic import TemplateView


class LandingPageHome(TemplateView):
    template_name = 'landingpage/home.html'


class LandingPageAbout(TemplateView):
    template_name = 'landingpage/about.html'


class LandingPageServices(TemplateView):
    template_name = 'landingpage/services.html'


class LandingPageContact(TemplateView):
    template_name = 'landingpage/contact.html'