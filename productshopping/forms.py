from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.http import request

from productshopping import models
from productshopping.models import Profile, Sizes


class MyRegisterForm(forms.ModelForm):
    username=forms.CharField(label="Username",max_length=100,required=True)
    password1=forms.CharField(label="Password",widget=forms.PasswordInput,required=True)
    password2=forms.CharField(label="Confirm Password",widget=forms.PasswordInput,required=True)
    email = forms.EmailField(label="Email ID", required=True)

    class Meta:
        model=User
        fields= ('username','email',)

    def clean_password(self):
        pass1=self.cleaned_data.get("password1")
        pass2=self.cleaned_data.get("password2")
        if pass1 and pass2 and pass1!=pass2:
            raise forms.ValidationError("Password doesn't matched")
        return pass2

    def save(self,commit=True):
        userobj=super(MyRegisterForm,self).save(commit=True)
        userobj.set_password(self.cleaned_data["password2"])

        if commit:
            userobj.save()

        return userobj


class MyLoginForm(forms.Form):
    username1=forms.CharField(label="Username",required=True)
    password1=forms.CharField(label="Password", widget=forms.PasswordInput,required=True)

    def clean(self):
        uname=self.cleaned_data.get("username1")
        pass1=self.cleaned_data.get("password1")
        userobj=authenticate(request,username=uname,password=pass1)

        if userobj is None:
            raise forms.ValidationError("Invalid username/password")

        return super(MyLoginForm,self).clean()

# custom widget

class DateInput(forms.DateInput):
    input_type = 'date'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_pic','birth_date','address','phone')
        widgets = {
            'birth_date': DateInput()
        }


#
SIZES= (
    ('XXXL', 'XXXL,'),
    ('XXL', 'XXL,'),
    ('XL', 'XL,'),
    ('L', 'L,'),
    ('M', 'M,'),
    ('S', 'S,'),
    ('XS', 'XS,'),
)

class SizeAdminForm(ModelForm):
    size = forms.MultipleChoiceField(choices = SIZES)

    class Meta:
        model = Sizes
        fields = '__all__'

    def clean_size(self):
        size = self.cleaned_data['size']
        if not size:
            raise forms.ValidationError("Error")

        size = ','.join(size)
        return size



