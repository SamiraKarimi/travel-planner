from django.urls import path
from . import views


urlpatterns = [
    path('', views.index ),
    path('signUp',views.signUp),
    path('register',views.registerUser),
    path('success',views.successUser),
    path('logOut',views.logoutUser),
    path('login',views.loginUser),
    path('trip/add',views.tripAdd),
    path('home',views.goHome),
    path('createTrip',views.create),
    path('join/<int:tripid>',views.join),
    path('tripInfo/<int:id>',views.trip_info)
]
