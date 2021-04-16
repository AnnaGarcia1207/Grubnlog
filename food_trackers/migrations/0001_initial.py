# Generated by Django 3.1.7 on 2021-03-24 00:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('brand', models.CharField(blank=True, max_length=100)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('calories', models.FloatField(blank=True, default=0)),
                ('proteins', models.FloatField(blank=True, default=0)),
                ('fats', models.FloatField(blank=True, default=0)),
                ('carbs', models.FloatField(blank=True, default=0)),
                ('cholesterol', models.FloatField(blank=True, default=0)),
                ('sodium', models.FloatField(blank=True, default=0)),
                ('potassium', models.FloatField(blank=True, default=0)),
                ('sugar', models.FloatField(blank=True, default=0)),
                ('ingredients', models.TextField(blank=True)),
                ('allergens', models.TextField(blank=True)),
                ('diet', multiselectfield.db.fields.MultiSelectField(choices=[('Paleo', 'Paleo'), ('Keto', 'Keto'), ('Vegan', 'Vegan'), ('Vegetarian', 'Vegetarian'), ('None Specific', 'None Specific')], default='None Specific', max_length=100)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='PostFood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calorie_amount', models.FloatField(blank=True, default=0, null=True)),
                ('amount', models.FloatField(default=0)),
                ('created_on', models.TimeField()),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_trackers.food')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diet', models.CharField(choices=[('Paleo', 'Paleo'), ('Keto', 'Keto'), ('Vegan', 'Vegan'), ('Vegetarian', 'Vegetarian'), ('None Specific', 'None Specific')], default='None Specific', max_length=20)),
                ('quantity', models.FloatField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField()),
                ('total_calorie', models.FloatField(default=0, null=True)),
                ('calorie_goal', models.PositiveIntegerField(default=0)),
                ('all_food_selected_today', models.ManyToManyField(related_name='inventory', through='food_trackers.PostFood', to='food_trackers.Food')),
                ('food_selected', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='food_trackers.food')),
                ('profile_of', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='postfood',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_trackers.profile'),
        ),
    ]
