from django import forms
from .models import Calf,Cow,Milk,Feed,Worker,farm_manager
class calform(forms.ModelForm):
    class Meta:
        model=Calf
        fields=["name","breed"]

class cowform(forms.ModelForm):
    class Meta:
        model=Cow
        fields={"name","breed"}

class milkform(forms.ModelForm):
    class Meta:
        model=Milk
        fields="__all__"
class workerform(forms.ModelForm):
    class Meta:
        model=Worker
        fields="__all__"   

class feedform(forms.ModelForm):
    class Meta:
        model=Feed
        fields= "__all__" 

class farmerform(forms.ModelForm):
    class Meta:
        model=farm_manager
        fields="__all__"
        