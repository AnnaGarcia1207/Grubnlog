from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CreateUserForm, LogFoodForm, AddFoodForm, ProfileForm
from .models import Food, Profile, PostFood
from .filters import FoodFilter
from django.utils import timezone
from datetime import date
from datetime import datetime
from datetime import timedelta


# Create your views here.
def landing_page(request):
    food = Food.objects.all()
    return render(request, 'food_trackers/landing_page.html', {'food': food})


def food_details(request, slug):
    food = Food.objects.get(slug=slug)
    return render(request, 'food_trackers/food_details.html', {'food': food})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('food_trackers:home')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)  # Used to be UserCreationForm
            if form.is_valid():
                user = form.save()
                # log the user in
                login(request, user)
                return redirect('food_trackers:home')
        else:
            form = CreateUserForm()
        return render(request, 'food_trackers/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('food_trackers:home')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                # login the user
                user = form.get_user()  # retrieve the user
                login(request, user)  # logging in the user
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('food_trackers:home')
        else:
            form = AuthenticationForm()
        return render(request, 'food_trackers/login.html', {'form': form})


def logout_view(request):
    # if request.method == 'POST':
    logout(request)
    return redirect('food_trackers:login')


@login_required(login_url='food_trackers:login')
def history(request):
    food = Food.objects.filter(profile_of=request.user)
    return render(request, 'food_trackers/history.html', {'food': food})


@login_required(login_url='food_trackers:login')
def log_food(request):  # uses log food form
    person = Profile.objects.filter(profile_of=request.user).last()
    food_items = Food.objects.filter(profile_of=request.user)
    form = LogFoodForm(request.user, instance=person)

    if request.method == 'POST':
        form = LogFoodForm(request.user, request.POST, instance=person)
        if form.is_valid():
            # profile = form.save(commit=False)
            # profile.profile_of = request.user
            # profile.save()
            form.save()
            return redirect('food_trackers:home')
    else:
        form = LogFoodForm(request.user)
    context = {'form': form, 'food_items': food_items}
    return render(request, 'food_trackers/log_food.html', context)


@login_required(login_url='food_trackers:login')
def create(request):  # uses addfoodform
    food_items = Food.objects.filter(profile_of=request.user)
    form = AddFoodForm(request.POST)
    if request.method == 'POST':
        form = AddFoodForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.profile_of = request.user
            profile.save()
            return redirect('food_trackers:profile')
    else:
        form = AddFoodForm()
    # To filter Food
    custom_filter = FoodFilter(request.GET, queryset=food_items)
    food_items = custom_filter.qs
    context = {'form': form, 'food_items': food_items, 'custom_filer': custom_filter}
    return render(request, 'food_trackers/create_food.html', context)


@login_required(login_url='food_trackers:login')
def update_food(request, pk):
    food_items = Food.objects.filter(profile_of=request.user)
    food_item = Food.objects.get(id=pk)
    form = LogFoodForm(request.user, request.POST,instance=food_item)
    if request.method == 'POST':
        form = LogFoodForm(request.POST, instance=food_item)
        if form.is_valid():
            form.save()
            return redirect('food_trackers:profile')
    my_filter = FoodFilter(request.GET, queryset=food_items)
    context = {'form': form, 'food_items': food_items, 'my_filter': my_filter}
    return render(request, 'food_trackers/log_food.html', context)


@login_required(login_url='food_trackers:login')
def delete_food(request, pk):
    food_item = Food.objects.filter(pk=pk).first()
    if request.method == 'POST':
        food_item.delete()
        return redirect('food_trackers:profile')
    return render(request, 'food_trackers/delete.html', {'food': food_item})


@login_required(login_url='food_trackers:login')
def profile(request):
    person = Profile.objects.filter(profile_of=request.user).last()
    food_items = Food.objects.filter(profile_of=request.user)
    form = ProfileForm(instance=person)
    if request.method =='POST':
        form = ProfileForm(request.POST,instance=person)
        if form.is_valid():
            form.save()
            return redirect('food_trackers:profile')
    else:
        form = ProfileForm(instance=person)
    past_entries = timezone.now().date() - timedelta(days=1)
    records = Profile.objects.filter(date__gte=past_entries, date__lt=timezone.now().date(),
                                     profile_of=request.user)

    context = {'form':form, 'food_items': food_items, 'records': records}
    return render(request, 'food_trackers/profile.html', context)


@login_required(login_url='food_trackers:login')  # This protects this view
def home(request):
    # food = Food.objects.filter(profile_of=request.user)
    # return render(request, 'food_trackers/home.html', {'food': food})
    calories = Profile.objects.filter(profile_of=request.user).last()
    calorie_goal = calories.calorie_goal

    if date.today() > calories.date:
        profile = Profile.objects.create(profile_of=request.user)
        profile.save()
    calories = Profile.objects.filter(profile_of=request.user).last()

    all_logs_today = PostFood.objects.filter(profile=calories)

    calorie_goal_status = calorie_goal - calories.total_calorie
    over_calorie = 0

    if calorie_goal_status < 0:
        over_calorie = abs(calorie_goal_status)

    context = {
        'total_calorie': calories.total_calorie,
        'calorie_goal': calorie_goal,
        'calorie_goal_status': calorie_goal_status,
        'over_calorie': over_calorie,
        'food_selected_today': all_logs_today
    }

    return render(request, 'food_trackers/home.html', context)