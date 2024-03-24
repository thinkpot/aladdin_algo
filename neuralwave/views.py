from django.views.generic import TemplateView
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
import requests as req
import json


class MainTradeHandler(TemplateView):
    template_name = 'tradecontroler.html'


class ClosePosition(APIView):
    def post(self, request, *args, **kwargs):
        request_obj = req.post(data={"AS":"BANKNIFTY","E":"NFO","AT":"ALICEBLUEV2"},
        url='https://webhook.nextlevelbot.com/series/TFhCYUppeEVlRVJudWhpMEM5cmI1UDBoL0VSVmFHaTl6cUx5L3N4eW1Tb1haNUlUY0FnbDJWUnRSd21XOEhwUw==')
        response = request_obj.json()
        return JsonResponse({'type': 'success'}, status=status.HTTP_200_OK)
