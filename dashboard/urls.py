from django.urls import path
from .views import *


urlpatterns = [
    path(r'', DashboardView.as_view(), name='home'),
    # Profile views
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', ProfileUpdateView.as_view(), name='profile-update'),

    # User API details views
    # path('user/api-details/<int:pk>/', )
]
