from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ActivitySerializer,RoomSerializer,TopicSerializer,TopicWithCountSerializer,UserSerializer,UserRegistrationSerializer,MessageSerializer
from base.models import Room,Topic,User,Message
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.db.models import Q




@api_view(['GET'])
def getRoutes(request):
    routes = [      
        'GET /api', 
        'GET /api/rooms',
        'GET /api/room/:id',
        'GET /api/user/:id',
        'GET /api/topics',
        'GET /api/topics/:topicName',
        'GET /api/countTopics/',
        'GET /api/user/',
        'POST /api/register',
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True,context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email') 
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        
        user_data = UserSerializer(user,context={'request': request})
        return JsonResponse({'token': token.key, 'user':user_data.data})
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)

@api_view(['POST'])
def createRoom(request):
    topic = request.data.get('topic')
    name = request.data.get('name')
    description = request.data.get('description')
    email = request.data.get("email")
    user = User.objects.get(email=email)
    topic, created = Topic.objects.get_or_create(name=topic)
    Room.objects.create(
            host=user,
            topic = topic,
            name = name,
            description = description
            
        )
    return JsonResponse({"message": "room created successfully"})

@api_view(['POST'])
def createMessage(request):
    message = request.data.get('message')
    roomId = int(request.data.get('roomId'))
    room = Room.objects.get(id=roomId) 
    email = request.data.get('email')
    user = User.objects.get(email=email)
    print(message,roomId,email)
    Message.objects.create(
            user=user,
            room=room,
            body=message,
        )
    return JsonResponse({"message": "message created successfully"})

@api_view(['GET'])
def get_user_details(request):
    user = request.user 
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request,pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False,context={'request': request})
    return Response(serializer.data)
    
    
@api_view(['GET'])
def getTopics(request):
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def searchByTopic(request,topicName):
    topics = Topic.objects.filter(name=topicName)
    serializer = TopicSerializer(topics,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def roomByTopic(request,topicName):  
    if (topicName == 'All'):
      rooms = Room.objects.all()
    else:   
      topic = Topic.objects.get(name=topicName) 
      rooms = Room.objects.filter(topic=topic)  
    serializer = RoomSerializer(rooms, many=True,context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def searchRooms(request, searchParam):
    if(searchParam):
        rooms= Room.objects.filter(Q(topic__name__icontains = searchParam) | Q(name__icontains=searchParam) | Q(description__icontains=searchParam))
    else:
        rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True,context={'request': request})
    return Response(serializer.data)
    
@api_view(['GET'])
def getTopicsCount(request):
    topicsObj = Topic.objects.all()
    topics = []
    for i in topicsObj:
        count = Room.objects.filter(topic=i).count()
        topic_data = TopicSerializer(i).data
        newEl = {'topic': topic_data, 'count': count}
        topics.append(newEl)
    print(topics)
    serializer = TopicWithCountSerializer(topics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getActivity(request,searchWord):
    if(searchWord == 'All' or searchWord == ''):
        activity = Message.objects.all()     
    else:
        activity = Message.objects.filter(Q(room__name__icontains=searchWord) | Q(room__description__icontains=searchWord) |Q(room__topic__name__contains=searchWord))
    serializer = ActivitySerializer(activity,many=True,context={'request': request})
    return Response(serializer.data)


class UserRegistrationView(APIView):
    def post(self, request): 
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

