from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from stockmgmt.models import *
from pine.models import *
from django.db.models import Sum
from chat.models import *
from chat.forms import *
from notification_app.models import *
from user.decorators import *
from django.contrib import messages
from user.models import UserProfile
from user.forms import *
from pine.forms import *

@unauthenticated_user
def main(request):
    return render(request, 'home.html')

@login_required(login_url='login')
@admin_only
def index(request):
    crops = Crop.objects.all()
    stock = Stock.objects.all()
# room chat
    rooms = Room.objects.all()
    if request.method == 'POST':
        roomform = RoomForm(request.POST)

        if roomform.is_valid():
            roomform.save()
            return redirect('index')
        
    else:
        roomform = RoomForm()
# end room chat

# yield
    total_yield = Yield.objects.aggregate(total_yield=models.Sum('number_yield'))['total_yield']

    pine_value = PineValue.objects.first()
    value = None
    if total_yield is not None and pine_value is not None:
        value = total_yield * pine_value.value
    else:
        value = 0
# end yield

# crop 
    total_planted = Crop.objects.aggregate(total_planted=Sum('number_planted'))['total_planted']

    pine_price = PinePrice.objects.first()
    cost = None

    if total_planted is not None and pine_price is not None:
        cost = total_planted * pine_price.price
    else:
        cost = 0
# end crop

# stocks
    total_stock_costs = [stocks.quantity * stocks.price for stocks in stock]
    overall_total_cost = sum(total_stock_costs)
    total_expenses = (cost + overall_total_cost)

    total_profit = (
        value - total_expenses
    )
# end stocks

# --YIELD DATA--//
    yields = Yield.objects.all().order_by('harvest_date')

    # Calculate the total yield for each category and each date
    hawaii_yields = (
        Yield.objects.filter(category__name='Hawaii')
        .values('harvest_date')
        .annotate(total_yield=Sum('number_yield'))
        .order_by('harvest_date')
    )
    pormosa_yields = (
        Yield.objects.filter(category__name='Pormosa')
        .values('harvest_date')
        .annotate(total_yield=Sum('number_yield'))
        .order_by('harvest_date')
    )

    # Get the PineValue objects for each category
    hawaii_pine_value = PineValue.objects.filter(category='2').first()
    pormosa_pine_value = PineValue.objects.filter(category='1').first()

    # Calculate the value for each category and each date
    for item in hawaii_yields:
        item['value'] = float(item['total_yield']) * (float(hawaii_pine_value.value) if hawaii_pine_value else 0)
    total_value_hawaii = sum(item['value'] for item in hawaii_yields)

    for item in pormosa_yields:
        item['value'] = float(item['total_yield']) * (float(pormosa_pine_value.value) if pormosa_pine_value else 0)
    total_value_pormosa = sum(item['value'] for item in pormosa_yields)

    # Iterate through Hawaii yield data and calculate the calculated_value
    for item in hawaii_yields:
        harvest_date = item['harvest_date']
        value_date = hawaii_pine_value.date

        # Calculate the difference in days between harvest_date and value_date
        days_difference = (harvest_date - value_date).days

        # Calculate the calculated_value based on the total_yield and PineValue
        item['calculated_value'] = float(item['total_yield']) * (float(hawaii_pine_value.value) if hawaii_pine_value else 0) * (1 - days_difference * 0.01)

    # Iterate through Pormosa yield data and calculate the calculated_value
    for item in pormosa_yields:
        harvest_date = item['harvest_date']
        value_date = pormosa_pine_value.date

        # Calculate the difference in days between harvest_date and value_date
        days_difference = (harvest_date - value_date).days

        # Calculate the calculated_value based on the total_yield and PineValue
        item['calculated_value'] = float(item['total_yield']) * (float(pormosa_pine_value.value) if pormosa_pine_value else 0) * (1 - days_difference * 0.01)
    total_hawaii_pineapples_by_date = hawaii_yields.aggregate(total_pineapples=Sum('total_yield'))['total_pineapples']
    total_pormosa_pineapples_by_date = pormosa_yields.aggregate(total_pineapples=Sum('total_yield'))['total_pineapples']

    # Calculate other values as per your existing code
    total_planted = Crop.objects.aggregate(total_planted=Sum('number_planted'))['total_planted']
    pine_price = PinePrice.objects.first()
    stocks = Stock.objects.all()
    cost = float(total_planted) * float(pine_price.price) if total_planted is not None and pine_price is not None else 0 
    total_stock_costs = [float(stock.quantity) * float(stock.price) for stock in stocks]
    overall_total_cost = sum(total_stock_costs)
    total_expenses = cost + overall_total_cost
    total_value = sum(item['calculated_value'] for item in hawaii_yields) + sum(item['calculated_value'] for item in pormosa_yields)

# --YIELD END

# --CROP--
    crops = Crop.objects.all()
    hawaii_crop = (
    Crop.objects.filter(category__name='Hawaii')
    .values('plant_date')
    .annotate(total_planted=Sum('number_planted'))
    .order_by('plant_date')
    )

    pormosa_crop = (
        Crop.objects.filter(category__name='Pormosa')  # <-- This line should filter 'Pormosa' category, not 'Hawaii'
        .values('plant_date')
        .annotate(total_planted=Sum('number_planted'))
        .order_by('plant_date')
    )

    
    context = {
        'hawaii_crop': hawaii_crop,
        'pormosa_crop': pormosa_crop,
        'crops': crops,
        'yields': yields,
        'total_value_hawaii': total_value_hawaii, 
        'total_value_pormosa': total_value_pormosa,
        'total_hawaii_pineapples_by_date': total_hawaii_pineapples_by_date,
        'total_pormosa_pineapples_by_date': total_pormosa_pineapples_by_date,
        'hawaii_yields': hawaii_yields,
        'pormosa_yields': pormosa_yields,
        'total_expenses': total_expenses,
        'cost': cost,
        'total_stock_costs': total_stock_costs,
        'overall_total_cost': overall_total_cost,
        
         'total_planted': total_planted,
         'total_yield': total_yield,
         'value': value,
         
         'stock': stock,
         'total_profit': total_profit,
         'rooms': rooms, 
         'total_value': total_value,
         'room_name': "broadcast",
         'roomform': roomform
    }
    return render(request, 'core/index.html', context)

# users
@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def employee(request):
    c = Crop.objects.exclude() 
    y = Yield.objects.all()
    rooms = Room.objects.filter(slug="employee")

    total_planted = Crop.objects.aggregate(total_planted=Sum('number_planted'))['total_planted']
    total_harvest = Yield.objects.aggregate(total_harvest=Sum('number_yield'))['total_harvest']
    context = {'c': c, 'y': y,
               'total_planted': total_planted,
               'total_harvest': total_harvest,
               'rooms':rooms,}
    return render(request, 'core/employee.html', context)


def buyer(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms,}

    return render(request, 'core/buyer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['supplier'])
def supplier(request):
    rooms = Room.objects.filter(slug="supplier")

    return render(request, 'core/supplier.html', {'rooms':rooms})

# 'end users'

@login_required(login_url='login')
def user_list(request):
    role_filter = request.GET.get('role', None)  # Get the 'role' query parameter from the URL
    users = User.objects.exclude(groups__name='admin')

    # Filter users based on the 'role' query parameter
    if role_filter:
        users = users.filter(userprofile__role=role_filter)

    add_user = CreateUserForm()

    if request.method == 'POST':
        add_user = CreateUserForm(request.POST, request.FILES)
        if add_user.is_valid():
            user = add_user.save()
            username = add_user.cleaned_data.get('username')
            role = add_user.cleaned_data.get('role')
            UserProfile.objects.create(user=user, role=role)
            return redirect('list-user')
        else:
            for error in add_user.errors.values():
                messages.error(request, error)

    context = {'users': users, 'add_user': add_user, 'selected_role': role_filter}
    return render(request, 'core/list_user.html', context)

from django.http import JsonResponse
def user_delete(request, pk):
    try:
        user = User.objects.get(id=pk)
        user.delete()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False})


@login_required(login_url='login')
def expenses(request):
    wp = WorkerPays.objects.all()
    total_planted = Crop.objects.aggregate(total_planted=Sum('number_planted'))['total_planted']
    pine_price = PinePrice.objects.first()
    stocks = Stock.objects.all()
    cost = None
    if total_planted is not None and pine_price is not None:
            cost = total_planted * pine_price.price
    else:
        cost = 0 
    # Get all Crop objects and order them by plant_date
    hawaii_crops = (
        Crop.objects.filter(category__name='Hawaii')
        .values('plant_date')
        .annotate(total_planted=Sum('number_planted'))
        .order_by('plant_date')
    )
    pormosa_crops = (
        Crop.objects.filter(category__name='Pormosa')
        .values('plant_date')
        .annotate(total_planted=Sum('number_planted'))
        .order_by('plant_date')
    )

    # Get the PinePrice objects for each category
    haw_pine_price = PinePrice.objects.values_list('price', flat=True).filter(category='2').first()
    hawaii_pine_price = PinePrice.objects.filter(category='2').first()
    pormosa_pine_price = PinePrice.objects.filter(category='2').first()

    # Calculate the expenses for each category and each date
    for item in hawaii_crops:
        item['expense'] = float(item['total_planted']) * (float(hawaii_pine_price.price) if hawaii_pine_price else 0)

    for item in pormosa_crops:
        item['expense'] = float(item['total_planted']) * (float(pormosa_pine_price.price) if pormosa_pine_price else 0)

    # Calculate the total expenses for each category
    total_expense_hawaii = sum(item['expense'] for item in hawaii_crops)
    total_expense_pormosa = sum(item['expense'] for item in pormosa_crops)

    # Calculate other values as per your existing code
    total_stock_costs = [float(stock.quantity) * float(stock.price) for stock in stocks]
    cost = float(cost) 
    overall_total_cost = sum(total_stock_costs)
    total_expenses = cost + sum(total_stock_costs)

    context = {
        'total_expense_hawaii': total_expense_hawaii,
        'total_planted': total_planted,
        'total_expense_pormosa': total_expense_pormosa,
        'hawaii_crops': hawaii_crops,
        'pormosa_crops': pormosa_crops,
        'total_expenses': total_expenses,
        'cost': cost,
        'total_stock_costs': total_stock_costs,
        'overall_total_cost': overall_total_cost,
        'haw_pine_price': haw_pine_price,
        'wp': wp
    }

    return render(request, 'rev_expe/expenses.html', context)



@login_required(login_url='login')
def revenues(request):
    # Get all Yield objects and order them by harvest_date
    yields = Yield.objects.all().order_by('harvest_date')

    # Calculate the total yield for each category and each date
    hawaii_yields = (
        Yield.objects.filter(category__name='Hawaii')
        .values('harvest_date')
        .annotate(total_yield=Sum('number_yield'))
        .order_by('harvest_date')
    )
    pormosa_yields = (
        Yield.objects.filter(category__name='Pormosa')
        .values('harvest_date')
        .annotate(total_yield=Sum('number_yield'))
        .order_by('harvest_date')
    )

    # Get the PineValue objects for each category
    hawaii_pine_value = PineValue.objects.filter(category='2').first()
    pormosa_pine_value = PineValue.objects.filter(category='1').first()

    # Calculate the value for each category and each date
    for item in hawaii_yields:
        item['value'] = float(item['total_yield']) * (float(hawaii_pine_value.value) if hawaii_pine_value else 0)
    total_value_hawaii = sum(item['value'] for item in hawaii_yields)

    for item in pormosa_yields:
        item['value'] = float(item['total_yield']) * (float(pormosa_pine_value.value) if pormosa_pine_value else 0)
    total_value_pormosa = sum(item['value'] for item in pormosa_yields)

    # Iterate through Hawaii yield data and calculate the calculated_value
    for item in hawaii_yields:
        harvest_date = item['harvest_date']
        value_date = hawaii_pine_value.date

        # Calculate the difference in days between harvest_date and value_date
        days_difference = (harvest_date - value_date).days

        # Calculate the calculated_value based on the total_yield and PineValue
        item['calculated_value'] = float(item['total_yield']) * (float(hawaii_pine_value.value) if hawaii_pine_value else 0) * (1 - days_difference * 0.01)

    # Iterate through Pormosa yield data and calculate the calculated_value
    for item in pormosa_yields:
        harvest_date = item['harvest_date']
        value_date = pormosa_pine_value.date

        # Calculate the difference in days between harvest_date and value_date
        days_difference = (harvest_date - value_date).days

        # Calculate the calculated_value based on the total_yield and PineValue
        item['calculated_value'] = float(item['total_yield']) * (float(pormosa_pine_value.value) if pormosa_pine_value else 0) * (1 - days_difference * 0.01)
    total_hawaii_pineapples_by_date = hawaii_yields.aggregate(total_pineapples=Sum('total_yield'))['total_pineapples']
    total_pormosa_pineapples_by_date = pormosa_yields.aggregate(total_pineapples=Sum('total_yield'))['total_pineapples']

    # Calculate other values as per your existing code
    total_planted = Crop.objects.aggregate(total_planted=Sum('number_planted'))['total_planted']
    pine_price = PinePrice.objects.first()
    stocks = Stock.objects.all()
    cost = float(total_planted) * float(pine_price.price) if total_planted is not None and pine_price is not None else 0 
    total_stock_costs = [float(stock.quantity) * float(stock.price) for stock in stocks]
    overall_total_cost = sum(total_stock_costs)
    total_expenses = cost + overall_total_cost
    total_value = sum(item['calculated_value'] for item in hawaii_yields) + sum(item['calculated_value'] for item in pormosa_yields)

    

    context = {
        'yields': yields,
        'total_value_hawaii': total_value_hawaii,
        'total_value_pormosa': total_value_pormosa,
        'total_hawaii_pineapples_by_date': total_hawaii_pineapples_by_date,
        'total_pormosa_pineapples_by_date': total_pormosa_pineapples_by_date,
        'hawaii_yields': hawaii_yields,
        'pormosa_yields': pormosa_yields,
        'total_expenses': total_expenses,
        'cost': cost,
        'total_stock_costs': total_stock_costs,
        'overall_total_cost': overall_total_cost,
        'total_value': total_value,
    }

    return render(request, 'rev_expe/revenues.html', context)
def workers_pay(request):
    wp = WorkerPays.objects.all()
    if request.method == 'POST':
        form = WorkerPayForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expenses')
    else:
        form = WorkerPayForm()

    context = {
        'wp': wp,
        'form': form,
    }

    return render(request, 'worker.html', context)

def other_expenses(request):
    return render(request, 'rev_expe/other_expenses.html')

from django.contrib.auth import authenticate, login, logout
@unauthenticated_user
def user_login(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user is not None and user.check_password(password):
            login(request, user)
            return redirect('index')
        else:
            if user is None:
                messages.error(request, 'Username does not exist.')
            else:
                messages.error(request, 'Incorrect password.')

    return render(request, 'home.html', {'page': page})

def all_notifications(request):
    all_notifications = BroadcastNotification.objects.all()
    return render(request, 'all_notifications.html', {'notifications': all_notifications})
    


