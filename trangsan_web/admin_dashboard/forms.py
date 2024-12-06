from django import forms    

# CHANGE THIS
class login_member_form(forms.Form):
    username = forms.CharField(label="Username", max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Password", required=True)