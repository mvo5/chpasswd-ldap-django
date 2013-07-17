from django import forms


class ChpasswdForm(forms.Form):
    user = forms.CharField()
    old_pass = forms.CharField()
    new_pass1 = forms.CharField()
    new_pass2 = forms.CharField()
