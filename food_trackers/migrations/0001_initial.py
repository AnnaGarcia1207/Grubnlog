# Generated by Django 3.1.6 on 2021-04-24 17:43

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
            name='Diet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('diet', models.CharField(choices=[('Paleo', 'Paleo'), ('Keto', 'Keto'), ('Vegan', 'Vegan'), ('Vegetarian', 'Vegetarian'), ('None', 'None')], default='None', max_length=100)),
                ('calorie_goal', models.PositiveIntegerField(default=800)),
                ('profile_of', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='food_trackers.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('brand', models.CharField(blank=True, max_length=100)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('calories', models.FloatField(blank=True, default=0)),
                ('proteins', models.FloatField(blank=True, default=0)),
                ('fats', models.FloatField(blank=True, default=0)),
                ('carbs', models.FloatField(blank=True, default=0)),
                ('cholesterol', models.FloatField(blank=True, default=0)),
                ('sodium', models.FloatField(blank=True, default=0)),
                ('potassium', models.FloatField(blank=True, default=0)),
                ('sugar', models.FloatField(blank=True, default=0)),
                ('ingredients', models.CharField(blank=True, max_length=100)),
                ('allergens', models.CharField(blank=True, max_length=100)),
                ('diet', multiselectfield.db.fields.MultiSelectField(choices=[('Paleo', 'Paleo'), ('Keto', 'Keto'), ('Vegan', 'Vegan'), ('Vegetarian', 'Vegetarian'), ('None', 'None')], default='None', max_length=100)),
                ('slug', models.SlugField()),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('log', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='food_trackers.log')),
            ],
        ),
    ]
