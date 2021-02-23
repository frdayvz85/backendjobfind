from django import forms
from .models import Post, Comment, ContactFormMessage, Author, Employer, Job,CustomUser
from django.forms import ModelForm, TextInput, Textarea, EmailInput, PasswordInput,URLField, IntegerField,ChoiceField, Select,NumberInput,URLInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from django.db import transaction


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        exclude = ['user']

class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = '__all__'
        exclude = ['user']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ['create_at','update_at','employer']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'overview', 'content','image',
        'categories','tags','slug','featured')

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control','id':'password1','placeholder': 'Password'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control','id':'password2', 'placeholder': 'Password confirm'}))

    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name', 'email', 'password1', 'password2']
        widgets = {
            'username':    TextInput(attrs={'class': 'form-control','id':'username',  'placeholder': 'Username'}),
            'first_name':  TextInput(attrs={'class': 'form-control','id':'firstname', 'placeholder': 'First name'}),
            'last_name':   TextInput(attrs={'class': 'form-control','id':'lastname', 'placeholder': 'Last name'}),
            'email':       EmailInput(attrs={'class': 'form-control','id':'email', 'placeholder': 'Your email'}),           
        }


CITY_CHOICES = (
    ("Baku", ("Baku")),
    ("Nakhchivan", ("Nakhchivan")),
    ("Ganja", ("Ganja")),
    ("Shaki", ("Shaki")),
    ("Gadabay", ("Gadabay"))
)
class SignUpFormEmployer(forms.ModelForm):
    city = forms.ChoiceField(choices = CITY_CHOICES,  widget=forms.Select(attrs={'class': 'form-control','id':'city', 'placeholder': 'City'}), required=True)

    class Meta:
        model = Employer
        fields = ['city','phonenumber','website','companyname']
        widgets = { 
            'phonenumber':   NumberInput(attrs={'class': 'form-control','id':'phonenumber', 'placeholder': 'Your phone number'}),
            'companyname':   TextInput(attrs={'class': 'form-control','id':'companyname', 'placeholder': 'Your company name'}), 
            'website':       URLInput(attrs={'class': 'form-control','id':'website', 'placeholder': 'Your website'}),         
        }



class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows':'4'
    }))
    class Meta:
        model = Comment
        fields = ('content',)


class ContactFormu(forms.ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name':    TextInput(attrs={'id': 'name', 'placeholder': 'Name & Surname'}),
            'subject': TextInput(attrs={'id': 'subject', 'placeholder': 'Subject'}),
            'email':   TextInput(attrs={'id': 'email', 'placeholder': 'Email Adress'}),
            'message': Textarea(attrs={'id': 'message', 'placeholder': 'Your Message', 'rows':'10'}),
        }  