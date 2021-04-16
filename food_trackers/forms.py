from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Food, Profile
from django import forms


# Customize our own UserCreationForm or Register form
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Customize our own Log Food form
class LogFoodForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('food_selected', 'quantity',)

    def __init__(self, user, *args, **kwargs):
        super(LogFoodForm, self).__init__(*args, **kwargs)
        self.fields['food_selected'].queryset = Food.objects.filter(profile_of=user)


class AddFoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ('title', 'slug', 'brand', 'quantity', 'calories', 'proteins', 'fats', 'carbs',
                  'cholesterol', 'sodium', 'potassium', 'sugar', 'ingredients', 'allergens',
                  'diet')
        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'input'}),
        #     'brand': forms.TextInput(attrs={'class': 'input'}),
        #     'quantity': forms.TextInput(attrs={'class': 'input'}),
        #     'calories': forms.TextInput(attrs={'class': 'input'}),
        #     'proteins': forms.TextInput(attrs={'class': 'input'}),
        #     'fats': forms.TextInput(attrs={'class': 'input'}),
        #     'carbs': forms.TextInput(attrs={'class': 'input'}),
        #     'cholesterol': forms.TextInput(attrs={'class': 'input'}),
        #     'sodium': forms.TextInput(attrs={'class': 'input'}),
        #     'potassium': forms.TextInput(attrs={'class': 'input'}),
        #     'sugar': forms.TextInput(attrs={'class': 'input'}),
        #     'ingredients': forms.Textarea(attrs={'class': 'input'}),
        #     'allergens': forms.Textarea(attrs={'class': 'input'}),
        #     'diet': forms.Select(attrs={'class': 'input'}),
        # }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('calorie_goal',)
        # maybe include diet?
