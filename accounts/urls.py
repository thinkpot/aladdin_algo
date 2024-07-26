from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('success/', SuccessView.as_view(), name='success'),

    # APIs for Client
    path('api/v1/add-client/', ADDClientViewSet.as_view({'post': 'create'}), name='add-client-api'),
    path('api/v1/update-client/<int:pk>/', ADDClientViewSet.as_view({'patch': 'partial_update'}), name='update-client-api'),
    path('api/v1/authenticate-api/<int:client_id>/', AuthenticateClientAPI.as_view(), name='authenticate_client_api'),

    ] + router.urls
