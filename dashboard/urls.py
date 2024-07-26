from django.urls import path
from .views import *


urlpatterns = [
    path(r'', DashboardView.as_view(), name='home'),
    # Profile views
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', ProfileUpdateView.as_view(), name='profile-update'),

    # Api Credentials Page
    path('profile/<int:pk>/api/details/', APIDetailsView.as_view(), name='api-details'),

    # Order Book
    path('trade_book', TradeBook.as_view(), name='trade-book'),

    # Realtime Signals
    path('signals/', RealtimeSignals.as_view(), name='realtime-signals'),

    # Webhook for signals
    path('signal_webook/', signal_webhook, name='signal-webhook')
]
