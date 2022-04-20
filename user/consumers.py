from importlib.resources import contents
import json
from tokenize import String
from channels.generic.websocket import WebsocketConsumer
from django.http import request
from asgiref.sync import async_to_sync
from channels.auth import login
from django.contrib.auth.models import User
from user.models import AuthenticationType, CustomizeUserModel
import paramiko
import re
from io import StringIO
from .models import Message, Room

def shell_escape(arg):
    return "'%s'" % (arg.replace(r"'", r"'\''"), )

def machineInfos(machine):
    if machine=="machine1":
        mInfo = dict();
        mInfo['hostname'] = "192.168.192.128"
        mInfo['username'] = 'deimyon'
        mInfo['password'] = '130245' 
        return mInfo
    if machine=="machine2":
        mInfo2 = dict();
        mInfo2['hostname'] = "192.168.192.130"
        mInfo2['username'] = 'deimyon2'
        mInfo2['password'] = '130245' 
        return mInfo2
    if machine=="machine3":
        mInfo3 = dict();
        mInfo3['hostname'] = "192.168.192.131"
        mInfo3['username'] = 'deimyon3'
        mInfo3['password'] = '130245' 
        return mInfo3
    else:
        pass

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        print(self.scope['user'])
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        newline = ""
        unauthorizedMsg = "Unauthorized"
        #async_to_sync(login)(self.scope, user)
        message = text_data_json['message']
        user = text_data_json['roomName']
        machine = text_data_json['machine']
        machineInfo = machineInfos(machine)
        print(machineInfo)
        print(user)
        strMessage = str(message)
        strContent = strMessage + " / " + machine
        pureCommand = strMessage.split(' ',1)[0]
        #currentUserID = self.user
        userID = User.objects.get(username = user).id
        userAll = User.objects.get(username = user)
        roomID = Room.objects.get(user_id = userID)
        Message.objects.create(content=strContent,user=userAll,room=roomID)
        print(userID)
        currentUser = CustomizeUserModel.objects.get(customizedUser_id=userID)
        print(currentUser) 
        authType = str(currentUser.authType)
        print(authType)
        result = AuthenticationType.objects.filter(id = authType).values()[0]
        print(result)
        self.send(text_data=json.dumps({
            'message': message
        }))
        
        hostname = machineInfo.get("hostname")
        username = machineInfo.get("username")
        password = machineInfo.get("password") 
        print(hostname,username,password)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username, password=password)
        if True:
            
            stdin, stdout, stderr = ssh.exec_command(message, get_pty=True)
            #print içerisi if içerisine alınacak unutma!!! sadece kontrol için burada şuan
            print(result.get(pureCommand))

            for xline in stdout:
                recompiled = re.compile(r'\x1b[^m]*m')
                recompiledd = recompiled.sub('',xline)
                recompiledddd = StringIO(recompiledd)
                line = recompiledddd.read().splitlines()
                self.send(text_data=json.dumps({
                    'message': line
                }))
                #print(recompiledd)
            
            self.send(text_data=json.dumps({
                'message': newline
            }))

            #while True:

            """ recompileddd = StringIO(recompiledd)
            lines = recompileddd.read().splitlines()
            for line in lines:
                print(line)
            
                self.send(text_data=json.dumps({
                    'message': line
                }))  """
            """ nextline2 = stderr.readline().strip()
                self.send(text_data=json.dumps({
                    'message': nextline
                }))
                print(nextline2.strip()) """
                
            """if not nextline:
                break"""

            ssh.close() 
        else:
            self.send(text_data=json.dumps({
                'message': newline
            }))
            
            
        
        