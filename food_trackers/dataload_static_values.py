import django
import os

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "grubnlog_app.settings"

    django.setup()

    from food_trackers.models import Diet
    from django.contrib.auth.models import User
    # OG
    # DIETS = [
    #     ("Paleo", ""),
    #     ("Keto", ""),
    #     ("Vegan", ""),
    #     ("Vegetarian", "")
    #     ("None", "")
    # ]

    # DIETS = [
    #     "Paleo",
    #     "Keto",
    #     "Vegan",
    #     "Vegetarian"
    # ]

    anna = User(username="annaa", first_name="Anna", last_name="garcia", is_superuser=True, is_staff=True)
    anna.set_password("123")
    anna.save()
    #OG
    # for diet in DIETS:
    #     Diet.objects.create(title=diet[0], description=diet[1])

    # Diet.objects.create(title="PALEO", description="")
    # Diet.objects.create(title="KETOGENIC", description="")
    # Diet.objects.create(title="VEGAN", description="")
    # Diet.objects.create(title="VEGETARIAN", description="")
    # Diet.objects.create(title="NONE", description="")


    # anna.profile.diet = Diet.objects.first()
    # anna.profile.save()
