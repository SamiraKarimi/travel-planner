from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request,'index.html')

def registerUser(request):
    # print(request.POST)
    validatorErrors=User.objects.registerationValidator(request.POST)
    if len(validatorErrors)>0:
        for key , value in validatorErrors.items():
            messages.error(request,value)
        return redirect('/')
    hash1 = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
    newUser = User.objects.create(name=request.POST['fname'],user_name=request.POST['uname'],password=hash1)
    print(f'&'*50)
    request.session['loggedinId']=newUser.id
    return redirect('/success')
    
def successUser(request):
    if 'loggedinId' not in request.session:
        return redirect('/')
    context = {
        'logedinUser':User.objects.get(id=request.session['loggedinId']),
         'myTrips': Trip.objects.filter(Q(uploader=User.objects.get(id=request.session['loggedinId']))|Q(planner=User.objects.get(id=request.session['loggedinId']))),
         'notmyTrips': Trip.objects.exclude(Q(uploader=User.objects.get(id=request.session['loggedinId']))|Q(planner=User.objects.get(id=request.session['loggedinId'])))
    #     'mywishes':Item.objects.filter(Q(uploader=User.objects.get(id=request.session['loggedinId']))|Q(favoritor=User.objects.get(id=request.session['loggedinId']))),
    #     'notmywishes':Item.objects.exclude(Q(uploader=User.objects.get(id=request.session['loggedinId']))|Q(favoritor=User.objects.get(id=request.session['loggedinId'])))
    } 
#     accounts = Account.objects.filter(
# Q(account_type=3) | Q(account_type=4)) 
    return render(request,'home.html',context)

def logoutUser(request):
    request.session.clear()
    return redirect('/')


def loginUser(request):
    print(f"****loginInfo*****"*5)
    print(request.POST)
    vloginerror=User.objects.loginValidator(request.POST)
    print(vloginerror)
    if len(vloginerror)>0:
        for key,value in vloginerror.items():
            messages.error(request,value)
        return redirect ('/')
    user = User.objects.get( user_name= request.POST['uname'])
    request.session['loggedinId']=user.id
    return redirect('/success')

def tripAdd(request):
    return render(request,'addtrip.html')

def goHome(request):
    return render(request,'home.html') 

def create(request):
    print("*******************************8")
    print(request.POST)
    #send info to validator
    validationEr = Trip.objects.validateItem(request.POST)
    if len(validationEr)>0:
        for key,value in validationEr.items():
            messages.error(request,value)
        return redirect('/trip/add')
    loggedInUser=User.objects.get(id=request.session['loggedinId'])
    print(loggedInUser)   
    newTrip = Trip.objects.create(destination=request.POST['dest'],description = request.POST['descrip'] ,uploader=loggedInUser,DateTo=request.POST['dateTo'],DateFrom=request.POST['dateFrom'])
    print(newTrip)
    return redirect("/success")


def join(request,tripid):
    loggedin = User.objects.get(id = request.session['loggedinId'])
    trip=Trip.objects.get(id=tripid) 
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^6666')
    print(trip)
    print(loggedin)
    trip.planner.add(loggedin)
    print(trip.destination)
    return redirect('/success')

def trip_info(request,id):
    print('*************')
    loggedin = User.objects.get(id = request.session['loggedinId'])
    tripInfo = Trip.objects.get(id = id)
    planners=tripInfo.planner.all()


    context = {
        'tripInfo':tripInfo,
        'loggedin': loggedin,
        'planners':planners
    }
    return render(request,'dest.html',context)

def signUp(request):
    return redirect('/')

