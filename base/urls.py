from django.urls import path
from base import views

urlpatterns = [
    
    path('login',views.loginPage, name='login'),
    path('registerPage',views.registerPage, name='registerPage'),
    path('logout',views.logOutUser, name='logout'),
    path('',views.home, name='home'),
    path('room/<str:pk>/',views.room, name='room'),
    path('create-room/',views.createRoom, name='create-room'),
    path('update-room/<str:pk>/',views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/',views.deleteRoom, name='delete-room'),
    path('delete-message/<str:pk>/',views.deleteMessage, name='delete-message'),
    
]