from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


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


# now let's create login view
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        userpass = request.POST['password']
        try:
            user_obj = authenticate(username=username, password=userpass)
            login(request, user_obj)
            request.session['username'] = username
            # after the user logged in we return the user to the home page
            return redirect('home')
        # if it doesn't work...
        except:
            messages.add_message(request, messages.ERROR, "Can not log in")
            return render(request, "user_profile/login.html")

    # if it is not post request (which means the user not fill and submitted form)
    # just take the user to the login page
    else:
        return render(request, 'user_profile/login.html')


# now this is a logout view
def user_logout(request):
    # it has the same pattern
    try:
        logout(request)
        messages.add_message(request, messages.INFO, "You're logged out")
    except:
        messages.add_message(request, messages.ERROR, "Can not log out")
    return redirect('home')


# last thing that I want to create is user profile view
# so this will be user profile which they will be able to see their profile
# only they are logged in it
# to do that we use decorator login required
@login_required
def user_profile(request, user_id):
    # the same pattern again
    # if the user POST request or NOT POST request
    if request.method == "POST":
        user_obj = User.objects.get(id=user_id)
        user_profile_obj = UserProfile.objects.get(id=user_id)

        try:
            # what we have in the front end is the input of an image
            # so, we are going to get this from request FILES
            user_img = request.FILES['user_img']
            # here the image is going to be stored on the file system
            # better not overwhelm your database
            fs_handle = FileSystemStorage()
            img_name = 'images/user_{0}'.format(user_id)

            # we are using this handle if the files exists overwrite it!
            if fs_handle.exists(img_name):
                fs_handle.delete(img_name)

            # after that we are going to save the new image
            fs_handle.save(img_name, user_img)

            # we need to update user profile obj to new image name
            user_profile_obj.profile_img = img_name
            user_profile_obj.save()
            user_profile_obj.refresh_from_db()

        except:
            messages.add_message(request, messages.ERROR, "Unable to update image..")

        return render(request, 'user_profile/my_profile.html', {'my_profile': user_profile_obj})

    # if the user just want to see his/her profile
    if request.user.is_authenticated and request.user.id == user_id:
        user_obj = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(id=user_id)

        return render(request, 'user_profile/my_profile.html', {'my_profile': user_profile})
