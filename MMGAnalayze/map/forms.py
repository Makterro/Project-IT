from django import forms

from django.forms import ModelForm

# from analyzeDashboard.models import MonitoringObject
# from map.models import Point
#
#
# class ModelNameChoiceField(forms.ModelChoiceField):
#     def label_from_instance(self, obj):
#         return obj.name
#
#
# class PointForm(ModelForm):
#     attrs = {
#         'class': 'form-control w-25',
#     }
#
#     monitoringObject = ModelNameChoiceField(MonitoringObject.objects.all(),
#                                             label='Объект',
#                                             widget=forms.Select(attrs={'class': 'form-select w-25'}))
#     lat = forms.FloatField(label='Широта',
#                            widget=forms.TextInput(attrs=attrs))
#     lon = forms.FloatField(label='Долгота',
#                            widget=forms.TextInput(attrs=attrs))
#
#     class Meta:
#         model = Point
#         fields = ['monitoringObject', 'lat', 'lon']
