from django.shortcuts import render
from LoginApp.forms import *
from django.contrib.auth.models import User
from LoginApp.models import UserInfo

def index(request):
    diction ={
        'title':"HOME"
        }
    if request.user.is_authenticated:
        current_user=request.user
        user_id= current_user.id
        user_basic_info = User.objects.get(pk=user_id)
        user_more_info = UserInfo.objects.get(user__pk =user_id)  
        #first name (user ) will be onetoone relationship colum Name and secod(pk or id) explample user__pk
        diction.update ({
            'user_basic_info':user_basic_info,
            'user_more_info': user_more_info
        })
       
  
    return render(request,'LoginApp/index.html',context=diction)
 


from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse ,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_app:index'))
 


def login_page(request):
    return render(request,'LoginApp/login.html')

def user_login(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('login_app:index'))
            else:
                return HttpResponse("Account is not active")
            
        else:
            return HttpResponse("Login detailse are not valid")

    else:
        return HttpResponseRedirect(reverse("login_app:login"))



def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        user_info_form = UserInfoForm(data=request.POST)

        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_info = user_info_form.save(commit=False)
            user_info.user = user

            if 'profile_pic' in request.FILES:
                user_info.profile_pic = request.FILES['profile_pic']

            user_info.save()  # Save user information after saving the user

            registered = True
            login(request, user)  # Log in the newly registered user

        else:
            # Handle form validation errors (e.g., display error messages)
            context = {'user_form': user_form, 'user_info_form': user_info_form}
            return render(request, 'LoginApp/register.html', context=context)

    else:
        user_form = UserForm()  # Create empty forms for GET requests
        user_info_form = UserInfoForm()

    context = {'title': 'Register', 'user_form': user_form, 'user_info_form': user_info_form, 'registered': registered}
    return render(request, 'LoginApp/register.html', context=context)
