from django import forms
from .models import *

class ResearchFileForm(forms.ModelForm):
    class Meta:
        model = ResearchFile
        fields = ('file',)


class ResearchForm(forms.ModelForm):
    class Meta:
        model = Research
        fields = ['comment', 'result']