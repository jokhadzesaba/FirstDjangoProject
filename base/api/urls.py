from django.urls import path
from . import views
from .views import UserRegistrationView

urlpatterns = [
    path('', views.getRoutes),
    path('rooms', views.getRooms),
    path('room/<str:pk>', views.getRoom),
    path('topic/<str:topicName>', views.roomByTopic),
    path('topics', views.getTopics ),
    path('countTopics', views.getTopicsCount),
    path('topics/<str:topicName>', views.searchByTopic),
    path('register', UserRegistrationView.as_view()),
    path('login', views.login_user),


]

