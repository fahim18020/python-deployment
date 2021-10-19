from django.shortcuts import render
from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from App_Login.forms import CreateNewUser,EditProfile
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse,reverse_lazy
from App_Login.models import UserProfile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from App_Login.models import UserProfile
from App_Shop.models import Product,Category

from django.contrib import messages



def sign_up(request):
    form = CreateNewUser()
    registered = False
    if request.method == 'POST':
        form = CreateNewUser(data=request.POST)
        if form.is_valid():
            user = form.save()
            registered = True
            user_profile = UserProfile(user=user)
            user_profile.save()
            messages.success(request,"Account Created Successfully!")
            return HttpResponseRedirect(reverse('App_Login:login'))

    return render(request,'App_Login/sign_up.html',context={'title':'Ecommerce Website','form':form})

def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('App_Shop:home'))

    return render(request,'App_Login/login.html',context={'title':'Login','form':form})

@login_required
def logout_user(request):
    logout(request)
    messages.warning(request,"You are Logout !")
    return HttpResponseRedirect(reverse('App_Shop:home'))

@login_required
def edit_profile(request):
    current_user = UserProfile.objects.get(user=request.user)
    form = EditProfile(instance=current_user)
    if request.method == 'POST':
        form = EditProfile(request.POST,request.FILES,instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request,"Profile Updated Successfully!")
            form = EditProfile(instance=current_user)
    return render(request,'App_Login/change_profile.html',context={'form':form})
