from django.template import RequestContext, context
from django.shortcuts import render,redirect
import user

from user.models import AuthenticationType, CustomizeUserModel
from .forms import LoginForm, RegisterForm, ExecuteCommand

from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required

from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse
import paramiko
from .models import Room
# Create your views here.


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        newUser = User(username = username)
        newUser.set_password(password)

        newUser.save()
        login(request,newUser)
        messages.success(request,"Registration successful.")

        return redirect("index")
    context = {
        "form" : form
    }

    return render(request,"register.html",context)
    
def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form" : form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username, password = password)
        #login(request,user)
        if user is None:
            messages.info(request,"Username or Password is invalid")
            return render(request,"login.html",context)
        
        messages.success(request,"Logged in successfully.")
        login(request,user)
        return redirect("index")

    return render(request,"login.html",context)

def logoutUser(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect("index")


def executeCommand(request):
    form = ExecuteCommand(request.POST or None)
    context = {
        "form" : form
    }
    if form.is_valid():
        command = form.cleaned_data.get("command")
        strCommand = str(command)
        pureCommand = strCommand.split(' ',1)[0]
        messages.success(request,pureCommand)
        currentUserID = request.user.id
        messages.success(request,currentUserID)
        currentUser = CustomizeUserModel.objects.get(customizedUser_id=currentUserID)
        messages.success(request,str(currentUser.authType))
        authType = str(currentUser.authType)
        result = AuthenticationType.objects.filter(id = authType).values()[0]
        if result.get(pureCommand):
            """ hostname = '192.168.192.128'
            username = 'deimyon'
            password = '130245'

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=hostname, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)

            while True:
                nextline = stdout.readline().strip()  
                # print(nextline.strip())
                request.websocket.send(nextline) 
                
                if not nextline:
                    break

            ssh.close()  """
        else:
            messages.warning(request,"Unauthorized command")
        messages.success(request,result.get(pureCommand))

    return render(request,"execute.html",{"form":form})

@login_required(login_url='/user/login/')
def executeCommand2(request,room_name):
    room_name = request.user.username
    print(room_name)
    try:
        room = Room.objects.get(user=request.user)
    except Room.DoesNotExist:
        Room.objects.create(user=request.user)
    return render(request,"execute2.html",{'room_name': room_name})