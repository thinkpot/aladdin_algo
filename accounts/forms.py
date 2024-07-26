from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from neuralwave.validators import validate_phone_number
from .models import Client, Broker


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True, validators=[validate_phone_number])
    terms_accepted = forms.BooleanField(label='I accept the terms and agreements', required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email', 'phone_number', 'password1', 'password2', 'terms_accepted')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.terms_accepted = self.cleaned_data['terms_accepted']
        print("called")
        if commit:
            print("Ssss")
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class ClientForm(forms.ModelForm):
    broker = forms.ModelChoiceField(queryset=Broker.objects.all(), empty_label="Select Broker")

    class Meta:
        model = Client
        fields = ['broker', 'client_id', 'client_secret']