from django.apps import AppConfig


class FoodTrackersConfig(AppConfig):
    name = 'food_trackers'

    def ready(self):
        import food_trackers.signals


