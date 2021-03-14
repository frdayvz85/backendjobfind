from django import forms
from .models import Post, Comment, ContactFormMessage, Author, Employer, Job,CustomUser
from django.forms import ModelForm, TextInput, Textarea, EmailInput, PasswordInput,URLField, IntegerField,ChoiceField, Select,NumberInput,URLInput, ImageField, FileField,FileInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from collections import OrderedDict
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
        widgets = {
            'profile_pic':       FileInput(attrs={'name':'file'}),           
        }

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ['create_at','update_at','employer', 'slug']

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
            'name':    TextInput(attrs={'id': 'name', 'placeholder': 'Name & Surname','required':'required'}),
            'subject': TextInput(attrs={'id': 'subject', 'placeholder': 'Subject','required':'required'}),
            'email':   EmailInput(attrs={'id': 'email', 'placeholder': 'Email Adress','required':'required'}),
            'message': Textarea(attrs={'id': 'message', 'placeholder': 'Your Message', 'rows':'10','required':'required'}),
        }  








#------------- Change Password -----------------------------

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("New password and repeat doesnt match."),
    }
    new_password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control','id':'password1','placeholder': 'New Password'}))
    new_password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control','id':'password2', 'placeholder': 'New Password confirm'}))
    

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
            if password1 == password2:
                if len(password1)<8:
                    raise forms.ValidationError("Password must consist of min 8 characters.")
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': ("Current password is wrong. "
                               "Please write again."),
    })
    old_password = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control','id':'password2', 'placeholder': 'Current Password'}))
    

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password


PasswordChangeForm.base_fields = OrderedDict(
    (k, PasswordChangeForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
)