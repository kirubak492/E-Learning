from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
    context={'room':room}

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
    if request.method=='POST':
        room.delete() 
        return redirect('home')
    
    return render(request,'secondapp/delete.html',{'obj':room})

def login_register(request):

    if request.method=="POST":
        
        username=request.POST.get('username')
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


    context={}
    return render(request,'secondapp/register.html',context)

def logout_user(request):
    logout(request)
    return redirect('home')
 
