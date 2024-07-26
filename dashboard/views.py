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
from accounts.models import Broker, Client
from .helpers import AliceBlue, Angelone
from rest_framework.views import APIView
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import TradeSignals
from pya3 import *
import pya3 as ab


class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cv'] = dict()

        user = self.request.user
        client = Client.objects.get(user=user)
        if client.broker.broker_symbol == 'ALCB':
            alice = AliceBlue(user)
            alice.get_profile(context['cv'])
            alice.get_position_book(context['cv'])
        if client.broker.broker_symbol == 'ANGL':
            angel = Angelone(user)
            angel.get_profile(context['cv'])
            angel.get_position_book(context['cv'])
            angel.get_capital(context['cv'])
        return context


class TradeBook(TemplateView):
    template_name = 'dashboard/trade_book.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cv'] = dict()
        user = self.request.user
        client = Client.objects.get(user=user)
        if client.broker.broker_symbol == 'ALCB':
            alice = AliceBlue(user)

        if client.broker.broker_symbol == 'ANGL':
            angel = Angelone(user)
            angel.get_trade_book(context['cv'])

        return context



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


class APIDetailsView(TemplateView):
    template_name = 'dashboard/profile_settings/user-api.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_details'] = dict()

        brokers_list = Broker.objects.all()
        api_details = Client.objects.filter(user=self.request.user)
        if api_details.exists():
            context['api_details']['details'] = api_details.first()
            context['api_details']['is_have'] = True
        else:
            context['api_details']['is_have'] = False

        context['brokers_list'] = brokers_list
        return context


def signal_webhook(request):
    if request.method == 'POST':
        try:
            print("Here", request)
            # json_str = str(request.body.decode('utf-8'))
            # print("String", json_str)
            # payload = json.loads(json_str)
            # print("JSON ", payload)
            # script_name = payload['script_name']
            # price = payload['price']
            # type = payload['type']
            # print("Working here ")
            # trade_signal = TradeSignals.objects.create(script_name=script_name, price=price, type=type)
            # trade_signal.save()
            print("hereeree")
            user = request.user
            print(user)
            client = Client.objects.get(user=user)
            print(client.broker.broker_symbol)
            if client.broker.broker_symbol == 'ALCB':
                print("here")
                # alice = AliceBlue(user)
                # alice.place_options_order('NIFTY')
                alice_b = ab.Aliceblue(user_id=client.client_user_id, api_key=client.client_id)
                alice_b.get_session_id()
                alice_b.place_order(
                    transaction_type=ab.TransactionType.Buy,
                    instrument=alice_b.get_instrument_by_symbol('NSE', 'NIFTY'),
                    quantity=25,
                    order_type=OrderType.Market,
                    product_type=ProductType.Intraday,
                    price=0.0,
                    trigger_price=None,
                    stop_loss=None,
                    square_off=None,
                    trailing_sl=None,
                    is_amo=False,
                    order_tag='order1',
                )

            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)


class RealtimeSignals(TemplateView):
    template_name = 'dashboard/signals.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context