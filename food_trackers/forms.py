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
        fields = ()

    def __init__(self, user, *args, **kwargs):
        super(LogFoodForm, self).__init__(*args, **kwargs)
        # self.fields['all_food_selected_today'].queryset = Food.objects.filter(profile_of=user)


class AddFoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ['title', 'slug', 'brand', 'quantity', 'calories', 'proteins', 'fats', 'carbs',
                  'cholesterol', 'sodium', 'potassium', 'sugar', 'ingredients', 'allergens',
                  'diet']



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # fields = ('calorie_goal',)
        fields = ('calorie_goal', 'diet')
        # maybe include diet?
