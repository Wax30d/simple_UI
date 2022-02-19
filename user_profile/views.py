from django.shortcuts import render, redirect
from django.contrib import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.

# view function for home page
def home(request):
    return render(request, "user_profile/home.html")


# user sign up view
def user_signup(request):
    # in this case we have 2 options:

    # 1. if the user wants to see the signup page!
    # in this case there is no request!!!

    # and the case when there is a request.
    # when the user actually submits a request to signup as a member
    # that is the second case
    if request.method == "POST":
        # objects that we are going to get the form
        user_email = request.POST['email']
        username = request.POST['username']
        userpass = request.POST['password']
        # those 3 object will be at the front end
        # And they are an input field

        # we are going to create new user object from the attributes that received on the first request
        try:
            user_obj = User.objects.create(username=username, email=user_email)
            user_obj.set_password(userpass)
            # then save this object
            user_obj.save()

            # after that authenticate the user
            user_auth = authenticate(username=username, password=userpass)

            # after that we are going to log in using this user_auth object
            login(request, user_auth)

            # and then return redirect to home page
            return redirect("home")

        # you can also send success message
        except:
            # ERROR sign up
            messages.add_message(request, message.ERROR, "Can not sign up")
            return render(request, 'user_profile/signup.html')

    # if the user wants to see the signup page
    return render(request, 'user_profile/signup.html')
