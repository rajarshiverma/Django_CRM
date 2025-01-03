from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()
    # check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,('You have been logged in!'))
            return redirect('home')
        else:
            messages.success(request,('Error logging in - Please try again'))
            return redirect('home') 
    else:
        return render(request,'home.html',{'records':records})

# def login_user(request):
#     pass

def logout_user(request):
    logout(request)
    messages.success(request,('You have been logged out'))
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            print("password ::", password)
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,'You have been registered')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request,'register.html',{'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request,'record.html',{'customer_record':customer_record})
    else:
        messages.success(request,'You must be logged in to view that page')
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        customer_record.delete()
        messages.success(request,'Record deleted successfully')
        return redirect('home')
    else:
        messages.success(request,'You must be logged in to delete record')
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request,'Record added successfully')
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request,'You must be logged in to add record')
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        # if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request,'Record updated successfully')
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request,'You must be logged in to update record')
        return redirect('home')