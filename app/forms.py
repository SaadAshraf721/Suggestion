from django import forms
from app.models import *


class Profileform(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
