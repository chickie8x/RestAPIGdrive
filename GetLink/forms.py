from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class InputForm(forms.Form):
    user_input = forms.CharField(max_length=250, widget=forms.TextInput(
        attrs={'placeholder': ' enter google drive link or file name to seach ', 'class': 'mainform'}), label=False)


class SignUpForm(UserCreationForm):
    use_required_attribute = 'signup'
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20,
                               widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'Username'}), label=False)
    password = forms.CharField(max_length=20,
                               widget=forms.PasswordInput(attrs={'id': 'password', 'placeholder': 'Password'}),
                               label=False)
# class PasswordResetForm(forms.Form):
#     email = forms.EmailField(required=True,max_length=250, widget=forms.TextInput(attrs={'id':'resetpass','placeholder':'Enter your email to get password reset link'}))
