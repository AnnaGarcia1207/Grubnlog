from django.db import models
from django.contrib.auth.models import User
from datetime import date
from multiselectfield import MultiSelectField

# Create your models here.

DIET_CHOICES = (("Paleo", "Paleo"),
                ("Keto", "Keto"),
                ("Vegan", "Vegan"),
                ("Vegetarian", "Vegetarian"), ("None", "None"))


class Diet(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def str(self):
        return self.title


class Food(models.Model):
    id = models.AutoField(primary_key=True)
    # about the food
    title = models.CharField(max_length=100, null=False)
    brand = models.CharField(max_length=100, blank=True)

    # TODO Create a dedicated object for food and qty for a production implementation.
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
    ingredients = models.CharField(blank=True, max_length=100)
    allergens = models.CharField(blank=True, max_length=100)

    # required
    # diet = models.ManyToManyField("Diet")
    diet = MultiSelectField(max_length=100, choices=DIET_CHOICES, max_choices=4, default='None')
    slug = models.SlugField()

    log = models.ForeignKey("Log", on_delete=models.CASCADE, null=True)

    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    # required
    profile_of = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # diet = models.ForeignKey("Diet", on_delete=models.DO_NOTHING, null=True)
    diet = models.CharField(max_length=100, choices=DIET_CHOICES, default='None')

    calorie_goal = models.PositiveIntegerField(default=800)

    def __str__(self):
        return str(self.profile_of)


class Log(models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="logs")
    date = models.DateField(auto_now_add=True)
