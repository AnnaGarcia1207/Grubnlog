# Generated by Django 3.1.7 on 2021-03-28 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food_trackers', '0003_auto_20210327_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postfood',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='food_trackers.profile'),
        ),
    ]
