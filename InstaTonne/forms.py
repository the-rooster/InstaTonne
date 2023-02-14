from django import forms


class RegisterForm(forms.Form):

    username = forms.CharField(label="Username",max_length=20)
    password = forms.CharField(label="Password",min_length=8)
    check_password = forms.CharField(label="Password Again")

class LoginForm(forms.Form):

    username = forms.CharField(label="Username",max_length=20)
    password = forms.CharField(label="Password",min_length=8)