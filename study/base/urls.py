from django.contrib import admin
from django.urls import path
from .views import home,room,create_room,update_room,delete




urlpatterns = [
    path('',home,name='home'),
    path('room/<int:pk>/', room, name='room_detail'),
    path('create-room/', create_room, name='create_room'),
    path('update-room/<int:pk>', update_room, name='update_room'),
    path('delete/<int:pk>', delete, name='delete'),

]
