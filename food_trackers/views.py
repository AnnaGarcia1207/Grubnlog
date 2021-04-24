from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CreateUserForm, LogFoodForm, AddFoodForm, ProfileForm
from .models import Food, Profile, Log, Diet
from django.utils import timezone
from datetime import date
from datetime import timedelta


# Create your views here.
def landing_page(request):
    food = Food.objects.all()[:100]
    return render(request, 'food_trackers/landing_page.html', {'food': food})


def food_details(request, slug):
    food = Food.objects.get(slug=slug)
    return render(request, 'food_trackers/food_details.html', {'food': food})


def register_view(request):
    # form = CreateUserForm()
    #
    # if request.method == 'POST':
    #     form = CreateUserForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('food_trackers:profile')
    #     else:
    #         form = CreateUserForm()
    # return render(request, 'food_trackers/register.html', {'form': form})
    if request.user.is_authenticated:
        return redirect('food_trackers:profile')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)  # Used to be UserCreationForm
            if form.is_valid():
                user = form.save()
                # log the user in
                login(request, user)
                return redirect('food_trackers:profile')
        else:
            form = CreateUserForm()
        return render(request, 'food_trackers/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('food_trackers:profile')
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
                    return redirect('food_trackers:profile')
            else:
                messages.info(request, 'Username or password is incorrect')
        else:
            form = AuthenticationForm()
        return render(request, 'food_trackers/login.html', {'form': form})


def logout_view(request):
    # if request.method == 'POST':
    logout(request)
    return redirect('food_trackers:landing_page')


@login_required(login_url='food_trackers:login')
def history(request):
    user_logs = [log for log in Log.objects.filter(profile=request.user.profile)]
    food = Food.objects.filter(log__in=user_logs)
    return render(request, 'food_trackers/history.html', {'food': food})


@login_required(login_url='food_trackers:login')
def log_food(request):  # uses log food form
    person = Profile.objects.get(profile_of=request.user)
    food_items = []
    form = LogFoodForm(request.user, instance=person)

    if request.method == 'POST':
        form = LogFoodForm(request.user, request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('food_trackers:home')
    else:
        form = LogFoodForm(request.user)

        food_items = Food.objects.filter(creator=request.user)

        context = {'form': form, 'food_items': food_items}
        return render(request, 'food_trackers/log_food.html', context)


@login_required(login_url='food_trackers:login')
def log_food_v2(request, pk):
    if request.method == 'POST':
        return redirect('food_trackers:home')
    else:
        most_recent_log = Log.objects.filter(profile=request.user.profile).order_by("-date").first()

        if most_recent_log is None or most_recent_log.date != date.today():
            most_recent_log = Log.objects.create(profile=request.user.profile)

        food = Food.objects.get(id=pk)
        food.log = most_recent_log
        food.save()

        form = LogFoodForm(request.user)

        food_items = Food.objects.filter(creator=request.user)

        context = {'form': form, 'food_items': food_items}

    return render(request, 'food_trackers/log_food.html', context)


@login_required(login_url='food_trackers:login')
def create(request):  # uses addfoodform
    food_items = []
    form = AddFoodForm(request.POST)
    if request.method == 'POST':
        form = AddFoodForm(request.POST)
        if form.is_valid():
            food = form.save()
            food.creator = request.user
            food.save()
            return redirect('food_trackers:log_food')
    else:
        form = AddFoodForm()
    # To filter Food
    # custom_filter = FoodFilter(request.GET, queryset=food_items)
    # food_items = custom_filter.qs
    context = {'form': form, 'food_items': food_items}
    return render(request, 'food_trackers/create_food.html', context)


@login_required(login_url='food_trackers:login')
def update_food(request, pk):
    food_item = Food.objects.get(id=pk)
    form = AddFoodForm(instance=food_item)
    if request.method == 'POST':
        form = AddFoodForm(request.POST, instance=food_item)
        if form.is_valid():
            form.save()
            return redirect('food_trackers:profile')
    return render(request, 'food_trackers/create_food.html', {'form': form})


@login_required(login_url='food_trackers:login')
def delete_food(request, pk):
    food_item = Food.objects.filter(id=pk).first()
    if request.method == 'POST':
        food_item.delete()
        return redirect('food_trackers:profile')
    return render(request, 'food_trackers/delete.html', {'food': food_item})


@login_required(login_url='food_trackers:login')
def profile(request):
    person = Profile.objects.filter(profile_of=request.user).last()
    form = ProfileForm(instance=person)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('food_trackers:profile')
    else:
        form = ProfileForm(instance=person)

    records = []
    past_entries = timezone.now().date() - timedelta(days=7)
    logs = Log.objects.filter(profile=request.user.profile, date__gte=past_entries)

    for log in logs:
        food = Food.objects.filter(log=log)

        calories_consumed = 0
        for item in food:
            calories_consumed += item.calories * item.quantity

        records.append({
            "date": log.date,
            "total_calorie": calories_consumed,
            'calorie_goal': request.user.profile.calorie_goal
        })

    food_items = Food.objects.filter(log__in=logs)

    context = {'form': form, 'food_items': food_items, 'records': records}
    return render(request, 'food_trackers/profile.html', context)


@login_required(login_url='food_trackers:login')  # This protects this view
def home(request):
    calorie_goal = request.user.profile.calorie_goal

    most_recent_log = Log.objects.filter(profile=request.user.profile).order_by("-date").first()

    if most_recent_log is None or most_recent_log.date != date.today():
        most_recent_log = Log.objects.create(profile=request.user.profile)

    food_items = [food for food in Food.objects.filter(log=most_recent_log)]

    # TODO iterate over the food_items and collect nutrition info
    carbohydrates = 0
    protein = 0
    fats = 0
    calories_consumed_today = 0
    for food_item in food_items:
        calories_consumed_today += food_item.calories * food_item.quantity
        carbohydrates += food_item.carbs
        protein += food_item.proteins
        fats += food_item.fats

    labels = ['Carbohydrates', 'Protein', 'Fats']
    data = [carbohydrates, protein, fats]

    # TODO iterate over today's log and mathematically find the calorie count.
    calorie_goal_status = calorie_goal - calories_consumed_today
    over_calorie = 0

    if calorie_goal_status < 0:
        over_calorie = abs(calorie_goal_status)

    context = {
        'total_calorie': calories_consumed_today,  #
        'calorie_goal': calorie_goal,
        'calorie_goal_status': calorie_goal_status,
        'over_calorie': over_calorie,
        'food_selected_today': food_items,
        'labels': labels,
        'data': data
    }

    return render(request, 'food_trackers/home.html', context)


def pie_chart(request):
    most_recent_log = Log.objects.filter(profile=request.user.profile).order_by("-date").first()
    if most_recent_log is None or most_recent_log.date != date.today():
        most_recent_log = Log.objects.create(profile=request.user.profile)

    food_items = [food for food in Food.objects.filter(log=most_recent_log)]

    # TODO iterate over the food_items and collect nutrition info
    carbohydrates = 0
    protein = 0
    fats = 0
    for an_item in food_items:
        carbohydrates += an_item.carbs
        protein += an_item.proteins
        fats += an_item.fats
    labels = ['Carbohydrates', 'Protein', 'Fats']
    data = [carbohydrates, protein, fats]
    # data = [0, 0, 0]

    chart_data = {
        # 'food_selected_today': most_recent_log
        'labels': labels,
        'data': data
    }

    return render(request, 'food_trackers/pie_chart.html', chart_data)

