from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic,Messages
from .forms import RoomForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


# Create your views here.


def home(request):

    q=request.GET.get('q') if request.GET.get('q') !=None else ''

    rooms=Room.objects.filter(
        Q(topic__topic__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)

        )
    room_count=rooms.count() 

    topics=Room.objects.all()
    
    context={'names':rooms,'topics':topics,'room_count':room_count}
    
    return render(request,'secondapp/home.html',context)

def room(request,pk):

    room=Room.objects.get(id=pk)
    room_messages=room.messages_set.all().order_by('-created')
    participants=room.participants.all()
    
    if request.method=='POST':
        message=Messages.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        ) 
        return redirect('room',pk=room.id)
    room.participants.add(request.user)
    context={'room':room,'room_messages':room_messages,'participants':participants}


    return render(request,'secondapp/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    if request.method=="POST":
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    
    return render(request,'secondapp/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):

    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.user!=room.host:
        return HttpResponse('You are not allowed to edit')
    

    if request.method=="POST":
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save() 
            return redirect('home')
    context={'form':form}

    return render(request,'secondapp/room_form.html',context)
 
@login_required(login_url='login')
def deleteRoom(request,pk):

    room=Room.objects.get(id=pk)
    # print(Room.objects.all())

    if request.user!=room.host:
        return HttpResponse("You are not allowed here!!")
    
    if request.method=='POST':
        room.delete() 
        return redirect('home')
    
    return render(request,'secondapp/delete.html',{'obj':room})

@login_required(login_url='login')
def deleteMessage(request,pk):

    message=Messages.objects.get(id=pk)
    # print(Room.objects.all())
    if request.user!=message.user:
        return HttpResponse("You are not allowed here!!")
    
    if request.method=='POST':
        message.delete() 
        return redirect('home')
    
    return render(request,'secondapp/delete.html',{'obj':message})

 
def login_register(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home') 

    if request.method=="POST":
        
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
            # print("user not exist")

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')


    context={'page':page}
    return render(request,'secondapp/register.html',context)

def logout_user(request):
    logout(request)
    return redirect('home')
 

def register_user(request):
    page='register'
    form=UserCreationForm()
    context={'page':page,'form':form}

    if request.method=="POST":
        form=UserCreationForm(request.POST)
        #print(form)
        if form.is_valid:
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()

            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, 'An error occured during registration')


    return render(request,'secondapp/register.html',context)

