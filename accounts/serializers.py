from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Client


class ADDClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['broker', 'client_id', 'client_secret', 'totp', 'client_user_id', 'client_password']

    def validate(self, data):
        # Ensure client_id and client_secret are unique for each user
        user = self.context['request'].user
        client_id = data.get('client_id')
        client_secret = data.get('client_secret')
        existing_clients = Client.objects.filter(user=user, client_id=client_id)
        if existing_clients.exists():
            raise serializers.ValidationError("Client with this client_id already exists for this user.")
        existing_clients = Client.objects.filter(user=user, client_secret=client_secret)
        if existing_clients.exists():
            raise serializers.ValidationError("Client with this client_secret already exists for this user.")
        return data

    def create(self, validated_data):
        Model = self.Meta.model
        request = self.context.get('request')
        instance = Model.objects.create(user_id=request.user.id, **validated_data)
        instance.save()
        return validated_data