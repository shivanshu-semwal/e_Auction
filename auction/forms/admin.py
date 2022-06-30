from unicodedata import category
from django import forms
from auction.models import Category, Session


# class DateTimeInput(forms.DateTimeInput):
#     input_type = 'datetime-local'


# class NewCategoryForm(forms.ModelForm):
#     class Meta():
#         model = Category
#         fields = "__all__"


# class NewSessionForm(forms.ModelForm):
#     start_time = forms.DateTimeField(
#         widget=DateTimeInput(), label='Start Time')
#     end_time = forms.DateTimeField(widget=DateTimeInput(), label='End Time')

#     class Meta():
#         model = Session
#         fields = "__all__"
