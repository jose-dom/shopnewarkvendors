from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import User
from .forms import TransactionForm, SearchCustomerForm
import datetime
import boto3
from boto3.dynamodb.conditions import Key, Attr
import uuid

dynamodb = boto3.resource("dynamodb")
dynamoTable_users = dynamodb.Table("Users")
dynamoTable_trans = dynamodb.Table("Transactions")

def home(request):
    return redirect('login')

def about(request):
    return render(request, 'core/about.html')

@login_required
def search_customer(request):
    if request.method == 'POST':
        form = SearchCustomerForm(request.POST)
        if form.is_valid():
            user_phone_number = form.cleaned_data.get('customer')
            response = dynamoTable_users.query(KeyConditionExpression=Key('phone_number').eq(user_phone_number))
            if response['Items']:
                messages.success(request, f'Customer Found!')
                for i in response['Items']:
                    request.session['customer'] = i['phone_number']
                    request.session['user_first_name'] = i['first_name']
                    request.session['user_last_name'] = i['last_name']
                    request.session['user_email'] = i['email']
                ##sending user info to the next form
                ##redirecting to the add transaction form
                return redirect('add-transaction')
            else: 
                messages.warning(request, f'Number not found! Please info customer to register at eatplaystaynewark.com')
                return redirect('search-customer')
    else:
        form = SearchCustomerForm()
    return render(request, 'core/search_customer.html', {'form': form})

@login_required
def add_transaction(request):
    user_phone_number = request.session['customer']
    user_first_name = request.session['user_first_name']
    user_last_name = request.session['user_last_name']
    user_email = request.session['user_email']
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            amount = form.cleaned_data.get('amount')
            options = form.cleaned_data.get('options')
            date = datetime.datetime.now()
            timestamp = str(date.strftime("%A, %B %e, %Y | %I:%M:%S %p"))
            dynamoTable_trans.put_item(
                Item={
                    "uuid": str(uuid.uuid1()),
                    "user_first_name": user_first_name,
                    "user_last_name": user_last_name,
                    "user_phone_number": user_phone_number,
                    "user_email": user_email,
                    "vendor_email": request.user.email,
                    "vendor_company_name": request.user.company_name,
                    "vendor_address": request.user.address,
                    "vendor_website": request.user.website,
                    "date": timestamp,
                    "amount": amount,
                    "options": options,
                }
            )
            messages.warning(request, f'Transaction Added Successfully!')
            return redirect('search-customer')
    else:
        form = TransactionForm()
    return render(request, 'core/add_transaction.html', {'form': form, 'user_phone_number': user_phone_number, 'user_first_name': user_first_name, 'user_last_name': user_last_name, 'user_email': user_email})
