from django import forms

from app.models import Question

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']