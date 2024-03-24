from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path(r'home/', LandingPageHome.as_view(), name='landing_page_home'),
    path(r'about/', LandingPageAbout.as_view(), name='landing_page_about'),
    path(r'services/', LandingPageServices.as_view(), name='landing_page_services'),
    path(r'contact/', LandingPageContact.as_view(), name='landing_page_contact')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
