from django.shortcuts import render, redirect  # render for html page,redirect for direct user page to page
from django.http import HttpResponse #  for sending http response to the user
from .models import User  # importing model
def home(request):   #request for home page

    if 'user' in request.session: # checks the user is logged in ,at the time the information about the user will be stored in the session
        current_user = request.session['user'] # stores the user data in a variable
        param = {'current_user': current_user}# passed the variable as a dictionary to a variable
        return render(request, 'base.html', param) # display the home page with the user data
    else:
        return redirect('login') # if the user is not logged in return or display the login page


def signup(request): #  request for the signup page

    if request.method == 'POST': # if the form is submitted
        uname = request.POST.get('uname') # the data in the field named uname is stored in the variable uname
        pwd = request.POST.get('pwd')# the data in the field named pwd is stored in the variable pwd


        if User.objects.filter(username=uname).exists(): # checks if the user is already exists
            return HttpResponse('Username already exists.') # if exists,print this
        else: # if not exists
            try:

                user = User(username=uname, password=pwd) #create  new user
                user.save()#save new user
                return redirect('login') #then redirect to the login page
            except Exception as e:
                return HttpResponse(f"Error: {e}")

    return render(request, 'signup.html')

# Login view function
def login(request):

    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')


        check_user = User.objects.filter(username=uname, password=pwd)
        if check_user:
            request.session['user'] = uname
            return redirect('home')
        else:
            return HttpResponse('Invalid Username or Password.')

    return render(request, 'login.html')

# Logout view function
def logout(request):
    try:
        del request.session['user']
    except KeyError:
        pass
    return redirect('login')

