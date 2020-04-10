from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, LoginForm, SpecialUpdateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import User
import boto3
from boto3.dynamodb.conditions import Key, Attr
import uuid

dynamodb = boto3.resource("dynamodb")
dynamoTable = dynamodb.Table("Vendors")
dynamoTable_trans = dynamodb.Table("Transactions")

def register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            dynamoTable.put_item(
                Item={
                    "uuid": str(uuid.uuid1()),
                    "company_name": form.cleaned_data.get('company_name'),
                    "email": form.cleaned_data.get('email'),
                    "address": form.cleaned_data.get('address'),
                    "business_type": form.cleaned_data.get('business_type'),
                    "phone_number": form.cleaned_data.get('phone_number'),
                    "website": form.cleaned_data.get('website'),
                }
            )
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('dashboard')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/dashboard.html', context)

def terms_conditions(request):
    return render(request, 'users/terms_conditions.html')

def logout_view(request):
    logout(request)
    return render(request, 'users/logout.html')

def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('dashboard')

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user and user.approved == 'YES':
                login(request, user)
                return redirect('dashboard')
            elif user:
                messages.info(request, f'Your Vendor application is waiting for approval please email us at admin@propertytaxcard.com')
                return redirect('login')
    else:
        form = LoginForm()
    context['form'] = form

    return render(request, "users/login.html", context)

@login_required
def transaction_data(request):
    transactions = []
    results = dynamoTable_trans.scan()

    for result in results['Items']:
        if result['vendor_email'] == request.user.email:
            trans_id = result['uuid']
            trans_user_first_name = result['user_first_name']
            trans_user_last_name = result['user_last_name']
            trans_user_email = result['user_email']
            trans_user_phone_number = result['user_phone_number']
            trans_date = result['date']
            trans_amount = result['amount']
            options = result['options']
            trans = [
                trans_id, 
                trans_user_first_name,
                trans_user_last_name,
                trans_user_email,
                trans_user_phone_number,
                trans_date,
                trans_amount,
                options,
            ]
            transactions.append(trans)

    context = {
        'transactions': transactions
    }
    return render(request, "users/transaction_data.html", context)

@login_required
def special(request):
    if request.method == 'POST':
        s_form = SpecialUpdateForm(request.POST, instance=request.user)
        
        if s_form.is_valid():
            s_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('special')
    else:
        s_form = SpecialUpdateForm(instance=request.user)
    
    context = {
        'form': s_form,
    }
    return render(request, "users/special.html", context)

class UserView(ListView):
    model = User
    paginate_by = 10
    template_name = "users/advanced.html"