from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.contrib.auth.models import User
from django import forms

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False,default='')
    sub_category = models.ForeignKey(Subcategory, on_delete=models.CASCADE,null=False,default='')
    image = models.ImageField(upload_to='ecommerce/pimg')
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        error_messages={"exist": "This Email Already Exists"},
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({"placeholder": "User Name", "class": "form-control"})
        self.fields["email"].widget.attrs.update({"placeholder": "Enter your email", "class": "form-control"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Password", "class": "form-control"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Confirm Password", "class": "form-control"})

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password1"])  # Hashing password
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exist'])  # Fixed error message
        return self.cleaned_data['email']
