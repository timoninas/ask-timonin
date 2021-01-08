from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import Question, Profile, Tag, Comment
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(required=True,)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

class AvatarForm(forms.ModelForm):
    avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar']

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.profile.image = self.cleaned_data['avatar']
        user.profile.save()
        return user

class AskForm(forms.ModelForm):
    # tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

# class SignupForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
    # username = forms.CharField(label="Username", required=True)
    # email = forms.EmailField(label="Email", required=True)
    # password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput())
    # repeat_password = forms.CharField(label="Repeat password", required=True, widget=forms.PasswordInput())

class SignupForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class SettingsForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    name = forms.CharField(label="Name", required=True)
    email = forms.EmailField(label="Email", required=True)
    avatar = forms.ImageField(label="Avatar", required=False)
