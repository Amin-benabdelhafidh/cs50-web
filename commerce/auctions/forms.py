from django import forms
from django.forms import ModelForm
from .models import *

list = Category.objects.all().values_list("category", "category")
c_list = []
for i in list:
    c_list.append(i) 

class CreateListings(ModelForm):
    class Meta:
        model = Listing
        fields = ["category"]
        widgets = {
            "category": forms.Select(choices=c_list, attrs={"class": "form-control"})
        }
    
class category_search(forms.Form):
    search = forms.ChoiceField(label='', choices=c_list, widget=forms.Select(attrs={"class": "form-control filter"}))

class Comment(forms.ModelForm):
    class Meta:
        model = comments
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={"placeholder": "Write your comment...", "class": "form-control add-comn-input"})
        }


            