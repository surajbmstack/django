from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import Room,Topic,Message
from . forms import RoomForm
from . forms import UserForm
# Create your views here.
def loginPage(request):
    page='login'
    context={'page':page}
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
            
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
             messages.error(request,'Username or password doesnt exist')
    return render(request, 'base/login_register.html',context)

def registerPage(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.save()
            login(request,user)
            return redirect('home')
        else:
             messages.error(request,'Username or password doesnt exist')
    context={'form':form}
    return render(request, 'base/login_register.html',context)
def logoutUser(request):
    logout(request)
    return redirect('home')
def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms=Room.objects.filter(Q(topic__name__contains=q)|Q(name__contains=q)|Q(description__contains=q))
    topics=Topic.objects.all()
    rooms_count=rooms.count()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    context={'rooms':rooms,'topics':topics,'rooms_count':rooms_count,'room_messages':room_messages}
    
    return render(request, 'base/home.html',context)

def room(request,id):
    room=Room.objects.get(id=id)
    room_messages=room.message_set.all().order_by('-created')
    participants=room.participants.all()
    if request.method=='POST':
        message=Message.objects.create(user=request.user,room=room,body=request.POST.get('body'))
        room.participants.add(request.user)
        return redirect('room',id=room.id)
        
    context={'room':room,'room_messages':room_messages,'participants':participants}
    
    return render(request, 'base/room.html',context)
@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.host=request.user
            room.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'base/room_form.html',context)
@login_required(login_url='/login')
def updateRoom(request,id):
    room=Room.objects.get(id=id)
    form=RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    context={'form':form}
    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request,'base/room_form.html',context)



def userProfile(request,id):
    user=User.objects.get(id=id)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={user:'user','rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request, 'base/profile.html',context)

@login_required(login_url='/login')
def deleteRoom(request,id):
   
    room=Room.objects.get(id=id)
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    room.delete()
    return redirect('home')

@login_required(login_url='/login')
def deleteMessage(request,id):
   
    message=Message.objects.get(id=id)
    if request.user != message.user:
        return HttpResponse('You are not allowed here')
    message.delete()
    return redirect('room',id=message.room.id)

@login_required(login_url='/login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)
    if request.method=='POST':
        form=UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'base/update-user.html',context)