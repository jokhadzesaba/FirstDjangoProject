from django.urls import path
from . import views
from .views import UserRegistrationView,CreateRoomView

urlpatterns = [
    path('', views.getRoutes),
    path('rooms', views.getRooms),
    path('room/<str:pk>', views.getRoom),
    path('create-room', CreateRoomView.as_view()),
    path('deleteRoom/<str:id>', views.deleteRoom),
    path('userById/<str:id>',views.getUserById),
    path('search/<str:searchParam>', views.searchRooms),
    path('selectedUserFeed/<str:userId>',views.getSelectedUserFeed),
    path('topic/<str:topicName>', views.roomByTopic),
    path('topics', views.getTopics ),
    path('countTopics', views.getTopicsCount),
    path('topics/<str:topicName>', views.searchByTopic),
    path('register', UserRegistrationView.as_view()),
    path('login', views.login_user),
    path('update-profile', views.updateProfile),
    path('create-message', views.createMessage),
    path('activity/<str:searchWord>', views.getActivity),
    path('getCurrentUser', views.get_current_user),
    
    


]

