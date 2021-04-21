from django.db import models
from django.contrib.auth.models import User
from datetime import date
from multiselectfield import MultiSelectField

# Create your models here.

DIET_CHOICES = (("Paleo", "Paleo"),
                ("Keto", "Keto"),
                ("Vegan", "Vegan"),
                ("Vegetarian", "Vegetarian"), ("None Specific", "None Specific"))


class Food(models.Model):
    # about the foodx
    title = models.CharField(max_length=100, null=False)
    brand = models.CharField(max_length=100, blank=True)
    quantity = models.PositiveIntegerField(null=False, default=1)
    calories = models.FloatField(blank=True, default=0)
    proteins = models.FloatField(blank=True, default=0)
    fats = models.FloatField(blank=True, default=0)
    carbs = models.FloatField(blank=True, default=0)
    # non required
    cholesterol = models.FloatField(blank=True, default=0)
    sodium = models.FloatField(blank=True, default=0)
    potassium = models.FloatField(blank=True, default=0)
    sugar = models.FloatField(blank=True, default=0)
    ingredients = models.TextField(blank=True)
    allergens = models.TextField(blank=True)
    created_on = models.DateField(auto_now_add=True)
    # required
    diet = MultiSelectField(max_length=100, choices=DIET_CHOICES, max_choices=4, default='None Specific')
    slug = models.SlugField()
    profile_of = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Profile(models.Model):
    # required
    profile_of = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    diet = models.CharField(max_length=20, choices=DIET_CHOICES, default='None Specific')

    food_selected = models.ForeignKey(Food, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.FloatField(null=False, default=1)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now=True)
    total_calorie = models.FloatField(default=0, null=True)
    calorie_goal = models.PositiveIntegerField(default=0)
    all_food_selected_today = models.ManyToManyField(Food, through='PostFood', related_name='inventory')

    def save(self, *args, **kwargs):
        if self.food_selected is not None:
            self.amount = (self.food_selected.calories * self.food_selected.quantity)
            self.calorie_count = self.amount * self.quantity
            self.total_calorie = self.calorie_count + self.total_calorie
            calories = Profile.objects.filter(profile_of=self.profile_of).last()
            PostFood.objects.create(profile=calories, food=self.food_selected, calorie_amount=self.calorie_count,
                                    amount=self.quantity, created_on=self.time)
            self.food_selected = None
            super(Profile, self).save(*args, **kwargs)

        else:
            super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.profile_of)


class PostFood(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    calorie_amount = models.FloatField(default=0, null=True, blank=True)
    amount = models.FloatField(default=0)
    created_on = models.TimeField(auto_now=True)

    def __str__(self):
        return self.food.title
