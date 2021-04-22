from django import forms


class UserForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=16, required=True)
    password = forms.CharField(max_length=16, required=True)
