from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=30)
    password = forms.CharField(label='password')

class RegisterForm(forms.Form):
    firstname = forms.CharField(label='firstname', max_length=30)
    lastname = forms.CharField(label='lastname', max_length=150)
    email = forms.CharField(label='email')
    username = forms.CharField(label='username', max_length=30)
    password = forms.CharField(label='password')

class PizzaOrderForm(forms.Form):
    pizza_type = forms.CharField(label='pizzaType', max_length=30)
    size = forms.CharField(label='pizzaSize', max_length=30)
    name = forms.CharField(label='pizzaName', max_length=30)
