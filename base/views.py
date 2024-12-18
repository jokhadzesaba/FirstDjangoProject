
from django.shortcuts import render, redirect
from .models import Room,Topic,Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
       username = str(request.POST.get('username')).lower()
       password = request.POST.get('password')
       try:
           user = User.objects.get(username=username)
           
       except:
           messages.error(request,'No Such an User')
       user = authenticate(request,username=username, password=password)
       if user is not None:
           login(request,user)
           return redirect('home')
       else:
           messages.error(request,'userName or Password does not exists')
           
    context = {'page':page}
    return render(request,'base/login_registrate.html',context)
                
        
        
def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = str(user.username).lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Something Went Wrong!')
    return render(request,'base/login_registrate.html',{'form':form})
    
def logOutUser(request):
    logout(request)
    return redirect('home')           



def home(request):    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms= Room.objects.filter(Q(topic__name__icontains = q) | Q(name__icontains=q) | Q(description__icontains=q))
    count = Room.objects.all().count()
    topics = getTopics()
    recentActivity = Message.objects.filter(Q(room__name__contains=q)).order_by('-created')
    context = {'rooms':rooms, 'topics':topics, 'count':count, 'recentActivity':recentActivity,}
    return render(request,'base/home.html', context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    roomMessages = room.message_set.order_by('-created')
    participants = room.participants.all()
    participantsLength = participants.count()
    topics = Topic.objects.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room':room, 'topics':topics, 'roommessages':roomMessages,'participants':participants,'participantsLength':participantsLength}
    
    return render(request,'base/room.html',context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = getTopics()
    roommessages = user.message_set.all()
    count = Room.objects.all().count()
    context = {'user':user,'rooms':rooms,'topics':topics,'recentActivity':roommessages,'count':count}
    return render(request, 'base/profile.html', context)


@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
            
        )
        return redirect('home')
        
    context = {'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    checkUser(request,room)
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    checkUser(request,room)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})



@login_required(login_url='/login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not Allowed Here')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})


@login_required(login_url='/login')
def updateUser(request):
    user = User.objects.get(id=request.user.id)
    
    return render(request, 'base/update-user.html',)
    

def getTopics():
    topicsObj = Topic.objects.all()
    topics = []
    for i in topicsObj:
        count = Room.objects.filter(topic=i).count()
        newEl = {'topic':i, 'count':count}
        topics.append(newEl)
    return topics
    

def checkUser(request,room):
    if request.user != room.host:
        return HttpResponse('You Shall not Pass!!!!')