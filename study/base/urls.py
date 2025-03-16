from django.contrib import admin
from django.urls import path
from .views import home,room,create_room,update_room,delete,loginpage,logoutUser,registerpage,deletemessage,userProfile




urlpatterns = [
    path('register/', registerpage, name='registerpage'),
    path('login/', loginpage, name='loginpage'),
    path('logout/', logoutUser, name='logout'),
    path('',home,name='home'),
    path('room/<int:pk>/', room, name='room_detail'),
    path('create-room/', create_room, name='create_room'),
    path('update-room/<int:pk>', update_room, name='update_room'),
    path('delete/<int:pk>', delete, name='delete'),
    path('delete-message/<int:pk>', deletemessage, name='delete-message'),
    path('profile/<str:username>/', userProfile, name='user-profile'),

]
