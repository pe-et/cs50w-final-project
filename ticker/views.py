import os
import requests
import json
from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Transaction, Benchmark


# API key(s)
parameters = {
    # openexchangerates.org api key
    'app_id': os.environ['OPENEXCHANGERATES_API']
}

# Function calculates Average Entry Price (AEP) or Average Sell Price (ASP) based on direction parameter
def average_price(transactions, direction):

    units = 0
    cost = 0

    # Determine direction, sum total and convert to positive number
    if direction == 'buy':

        # Sum cost_basis and convert to positive number
        buys = transactions.filter(cost_basis__lt=0)
        cost = buys.aggregate(Sum('cost_basis'))
        cost = cost['cost_basis__sum'] * -1

        # Sum total units
        units = buys.aggregate(Sum('units'))
        units = units['units__sum']

    else:

        # Sum total units and convert to positive number
        sells = transactions.filter(units__lt=0)
        units = sells.aggregate(Sum('units'))
        units = units['units__sum'] * -1

        # Sum total cost_basis
        cost = sells.aggregate(Sum('cost_basis'))
        cost = cost['cost_basis__sum']

    # Return average price
    return cost/units

# Implements pagination to given collection of objects
def paginate_me(objects, request):

    paginator = Paginator(objects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj

# Returns asset's current price
def rate(ticker):
    response = requests.get('https://openexchangerates.org/api/latest.json', params=parameters)

    # Convert response format
    convert = response.json()
    rates = convert['rates']

    # Reverse rates (free API key only allows USD as base)
    current_price = 1/rates[ticker.upper()]

    return current_price

# Returns sum of funds
def sum_funds(user, funds, direction):

    user_funds = 0

    if direction != 'buy' and Benchmark.objects.filter(user=user).exists():
        initial_stack = Benchmark.objects.filter(user=user).aggregate(Sum(funds))
        user_funds += initial_stack[f"{funds}__sum"]

    if Transaction.objects.filter(user=user).exists():
        transactions = Transaction.objects.filter(user=user).aggregate(Sum(funds))
        user_funds += transactions[f"{funds}__sum"]

    return user_funds




# If user is logged in, load default view: market.html, else redirect to login view
def market(request):
    if request.user.is_authenticated:
        return render(request, 'ticker/market.html')
    else:
        return render(request, 'ticker/login.html')

# Loads page displaying transaction history
@login_required
def transactions(request):

    # Get all user's transaction
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')

    # Cast to list and add 'current price'
    transaction_list = list(transactions)
    for transaction in transaction_list:
        transaction.current_price = (transaction.cost_basis / transaction.units) * -1


    return render(request, 'ticker/transactions.html', {
        "page_obj": paginate_me(transaction_list, request),
    })

# Handles buy orders
@login_required
def buy(request):
    if request.method == "POST":

        user = request.user

        # Get input values
        asset = Decimal(request.POST['buy-asset'])
        cash = Decimal(request.POST['sell-cash'])

        # Sum user's current cash balance
        user_funds = sum_funds(user, 'cost_basis', 'buy')

        # Ensure user has sufficient funds to cover order
        if user_funds > cash:

            # Buy = negative cash quantity
            cost_basis = cash * -1

            # Add transaction to database
            transaction = Transaction(user=request.user, ticker='BTC', units=asset,
            cost_basis=cost_basis, quote_currency='USD')
            transaction.save()

            # Display success messages & redirect user
            messages.success(request, f"Bought {asset:.8f} {transaction.ticker}!")
            return HttpResponseRedirect(reverse('transactions'))

        else:

            # Display error message and reload the page
            messages.error(request, 'Insufficient funds')
            return render(request, 'ticker/market.html')

# Handles sell orders
@login_required
def sell(request):
    if request.method == "POST":

        user = request.user

        # Get input values
        asset = Decimal(request.POST['sell-asset'])
        cash = Decimal(request.POST['buy-cash'])

        # Sum user's current asset balance
        user_funds = sum_funds(user, 'units', 'sell')

        # Ensure user has sufficient funds to cover order
        if user_funds > asset:

            # Sell = negative units quantity
            units = asset * -1

            # Add transaction to database
            transaction = Transaction(user=request.user, ticker='BTC', units=units,
             cost_basis=cash, quote_currency='USD')
            transaction.save()

            # Display success message & redirect user
            messages.success(request, f"Sold {asset:.8f} {transaction.ticker}!")
            return HttpResponseRedirect(reverse('transactions'))

        else:

            # Display error message and reload the page
            messages.error(request, 'Insufficient funds')
            return render(request, 'ticker/market.html')

# Loads analysis page
@login_required
def analysis(request):

    # Average Entry Price
    aep = "n/a"
    # Average Sell Price
    asp = "n/a"

    # Get user, benchmark units & current asset price
    user = request.user
    initial_units = Benchmark.objects.filter(user=user).aggregate(Sum('units'))
    asset_price = Decimal(rate('BTC'))

    # Add benchmark to user_sum, declare and initialize cash variable
    user_sum = initial_units['units__sum']
    cash = 0

    # If user has transactions
    transactions = Transaction.objects.filter(user=user)
    if transactions.exists():

        # Add sum of transactions to user_sum
        sum = transactions.aggregate(Sum('units'))
        user_sum += sum['units__sum']

        # Add transaction cost basis to cash
        cost_basis = transactions.aggregate(Sum('cost_basis'))
        cash += cost_basis['cost_basis__sum']

        # If user has buy orders, calculate AEP
        if transactions.filter(cost_basis__lt=0):
            aep = f"${average_price(transactions, 'buy'):.2f}"

        # If user has sell orders, calculate ASP
        if transactions.filter(units__lt=0):
            asp = f"${average_price(transactions, 'sell'):.2f}"

    # Calculate total value
    benchmark = asset_price * initial_units['units__sum']
    portfolio = (user_sum * asset_price) + cash


    context = {
        'asset': user_sum,
        'cash': cash,
        'user': user,
        'portfolio': portfolio,
        'benchmark': benchmark,
        'initial_units': initial_units['units__sum'],
        'aep': aep,
        'asp': asp,
    }
    return render(request, 'ticker/analysis.html', context)

# Get request loads login view, post request handles login form submission
def login_view(request):
    if request.method == "POST":

        # Sign user in
        username = request.POST['username']
        password = request.POST['pwd']
        user = authenticate(request, username=username, password=password)

        # If authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('market'))
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'ticker/login.html')
    else:
        return render(request, 'ticker/login.html')

# Logs user out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('market'))

# Get request loads register form, post request handles registration form submission
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['pwd']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            messages.error(request, 'Passwords must match.')
            return render(request, 'ticker/register.html')

        # Create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, 'Username already taken')
            return render(request, 'ticker/register.html')

        login(request, user)

        # Get benchmark values
        ticker = request.POST['bTicker']
        units = request.POST['bAmount']

        # Ensure ticker and units were not left blank
        if not ticker or not units:
            messages.error(request, 'Benchmark asset and quantity are required fields.')
            return render(request, 'ticker/register.html')

        # Create benchmark entry
        try:
            benchmark = Benchmark(user=request.user, ticker=ticker, units=units)
            benchmark.save()
        except:
            raise Exception('Error when saving benchmark asset to database')


        # Redirect user to main page
        return HttpResponseRedirect(reverse('market'))
    else:
        return render(request, 'ticker/register.html')
