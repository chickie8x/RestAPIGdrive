from django import forms


class InputForm(forms.Form):
    user_input = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder': 'input your google drive link here','size':100}))

