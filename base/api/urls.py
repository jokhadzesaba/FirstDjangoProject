from django.urls import path
from . import views
from .views import UserRegistrationView,CreateRoomView

urlpatterns = [
    path('', views.getRoutes),
    path('rooms', views.getRooms),
    path('room/<str:pk>', views.getRoom),
    path('topic/<str:topicName>', views.roomByTopic),
    path('search/<str:searchParam>', views.searchRooms),
    path('topics', views.getTopics ),
    path('countTopics', views.getTopicsCount),
    path('topics/<str:topicName>', views.searchByTopic),
    path('register', UserRegistrationView.as_view()),
    path('login', views.login_user),
    path('create-room', CreateRoomView.as_view()),
    path('create-message', views.createMessage),
    path('activity/<str:searchWord>', views.getActivity),
    


]

