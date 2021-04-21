from django.urls import path
from . import views

app_name = 'food_trackers'
urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    # homepage
    path('home/', views.home, name='home'),
    path('register/', views.register_view, name='register'),  # Register Users
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # requires_login -----
    # log_food within create custom
    path('history/', views.history, name='history'),
    path('log_food/', views.log_food, name='log_food'),
    path('create/', views.create, name='create'),
    path('profile/', views.profile, name='profile'),
    path('pie_chart/', views.pie_chart, name='pie_chart'),
    path('update_food/<str:pk>/', views.update_food, name='update_food'),
    path('delete_food/<str:pk>/', views.delete_food, name='delete_food'),
    path('<slug:slug>/', views.food_details, name='food_details'),
    # history

]
