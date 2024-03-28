import json
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from Personal.models import Register
import random

from .salesforce_service import create_salesforce_record, query_salesforce, update_salesforce_record
   
def index(request): 
    return render(request, "index.html")
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        query = f"SELECT Id,Name,Email__c,Password__c,OTP__c FROM credential__c WHERE Name='{username}' AND Password__c='{password}'"
        records = query_salesforce(query)
        print(records)
        if len(records)>0:
            return render(request,'index.html', {'message': username})
        else:
            return render(request, 'login.html', {'message': 'Plese Enter Correct Data'})
    else:
        return render(request,'login.html') 

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        phone= request.POST['phone']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        object_type = 'credential__c'
        data = {
        'Firstname__c': first_name,
        'Lastname__c': last_name,
        'Name':username,
        'Phone__c':phone,
        'Email__c':email,
        'Password__c':password1,
        'Password1__c':password2,
        }
        query = f"SELECT Id,Name,Email__c FROM credential__c WHERE Name='{username}' AND Email__c='{email}'"
        records = query_salesforce(query)
        print(records)

        # handle Json As List
        # lis=[]
        # lis.append(records[0]['Name']) 
        # lis.append(records[0]['Email__c'])


        if len(records)==0:
            if password1==password2:
                response = create_salesforce_record(object_type, data)
                if 'id' in response:
                   return render(request, 'login.html', {'message': 'Registered  successfully'})
                else:
                  return render(request, 'Register.html', {'message': 'Failed to create Account'})
            else:
                return render(request, 'Register.html', {'message': 'Password1 and Password2 Should be Same'})
        else:
            # return render(request, 'Register.html', {'data': lis})
                                                        
            return render(request, 'Register.html', {'data': records})
    else:
        return render(request,'Register.html')  

def logout(request):
    auth.logout(request)
    return redirect('/')  
def about(request):
    return render(request,"about.html")       
def contact(request):
    return render(request,"contact.html")  
OTP=0
email=''
username=''
def forget(request):
    if request.method == 'POST':
        global username 
        username = request.POST['username']
        global email 
        email = request.POST['email']
        global OTP
        OTP=random.randint(00000,99999)
        print(OTP)
        query = f"SELECT Id,Name,Email__c FROM credential__c WHERE Name='{username}' AND Email__c='{email}'"
        records = query_salesforce(query)
        if len(records)!=0:
            record_id = records[0]['Id']
            updated_data = {'OTP__c':OTP}
            object_type = 'credential__c'
            code=update_salesforce_record(object_type,record_id, updated_data)
            if code==10:
                return render(request, 'validateOTP.html', {'message': 'Please Enter OTP'})
            else:
                return render(request, 'forget.html', {'message': 'Please enter Correct Data'})
        else:
            return render(request, 'forget.html', {'message': 'Please enter Correct Data'})
    else:
        return render(request,'forget.html') 
def UpdateOTP(request):
    if request.method == 'POST':
        newOTP = request.POST['Enter OTP']
        psw = request.POST['password1']
        psw1 = request.POST['password2']
        query = f"SELECT Id,Name,Email__c,OTP__c FROM credential__c WHERE Name='{username}' AND Email__c='{email}'"
        records = query_salesforce(query)
        record_otp = records[0]['OTP__c']
        if psw==psw1:
            if int(newOTP)==int(record_otp):
                query = f"SELECT Id,Name,Email__c,OTP__c FROM credential__c WHERE Name='{username}' AND Email__c='{email}'"
                records = query_salesforce(query)
                record_id = records[0]['Id']
                updated_data = {
                    'Password__c':psw,
                    'Password1__c':psw1,
                    }
                object_type = 'credential__c'
                code=update_salesforce_record(object_type,record_id, updated_data)
                if code==10:
                    return render(request, 'login.html', {'message': 'Successfully Validated, please Login'})
                else:
                    return render(request, 'forget.html', {'message': 'Failed to get OTP'})
            else:
                return render(request, 'validateOTP.html', {'message': 'please enter Correct OTP'})
        else:
            return render(request, 'validateOTP.html', {'message': 'Please enter Correct Password'})
    
