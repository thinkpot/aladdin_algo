from django.shortcuts import render
from .forms import CustomUserCreationForm, LoginForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .models import CustomUser, Client, Broker
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
import requests
from rest_framework import status
from .serializers import ADDClientSerializer
from django.http import JsonResponse
from time import timezone
# from alice_blue import *
from pya3 import *
from SmartApi import SmartConnect
import pyotp
from logzero import logger

import logging
logging.basicConfig(level=logging.DEBUG)


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


class ADDClientViewSet(ModelViewSet):
    serializer_class = ADDClientSerializer
    queryset = Client.objects.all()

    def get_queryset(self):
        query_params = self.request.query_params
        filters = {'{}'.format(key): value for key, value in query_params.items()}
        return self.queryset.filter(**filters)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse({"type": "success", "data": serializer.data})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance.connected = False
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class AuthenticateClientAPI(APIView):
    def post(self, request, client_id):
        try:
            client = Client.objects.get(id=client_id, user=request.user)
        except Client.DoesNotExist:
            return JsonResponse({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

        broker_symbol = client.broker.broker_symbol

        if broker_symbol == "ALCB":
            alice = Aliceblue(user_id=client.client_user_id, api_key=client.client_id)
            session_id = alice.get_session_id()
            if session_id:
                # Saving session id
                client.session_id = session_id.get('sessionID')
                client.connected = True
                client.save()
                return JsonResponse({'type': 'success', 'connected':True})

        if broker_symbol == 'ANGL':
            request_data = self.request.data

            api_key = client.client_id
            username = client.client_user_id
            pwd = client.client_password

            smartApi = SmartConnect(api_key)
            try:
                token = client.totp
                totp = pyotp.TOTP(token).now()
            except Exception as e:
                logger.error("Invalid Token: The provided token is not valid.")
                raise e

            correlation_id = "abcde"
            data = smartApi.generateSession(username, pwd, totp)

            if data['status'] == False:
                logger.error(data)
            else:
                # login api call
                # logger.info(f"You Credentials: {data}")
                authToken = data['data']['jwtToken']
                refreshToken = data['data']['refreshToken']

                client.refresh_token = refreshToken
                client.access_token = authToken
                client.connected = True
                client.save()

                # fetch the feedtoken
                feedToken = smartApi.getfeedToken()
                # fetch User Profile
                res = smartApi.getProfile(refreshToken)
                smartApi.generateToken(refreshToken)
                exchanges = res['data']['exchanges']
                print(res)
                return JsonResponse({'type': 'success', 'connected': True})

        return JsonResponse({})