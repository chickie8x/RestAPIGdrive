from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class InputForm(forms.Form):
    user_input = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder': ' input your google drive link here','size':100}))


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

