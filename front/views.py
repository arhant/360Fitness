from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import Template , Context, loader
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_protect
import json
import boto3
import hashlib
import requests
from decimal import *
from botocore.exceptions import ClientError
from django.contrib.auth import logout


MY_ACCESS_KEY_ID = ''
MY_SECRET_ACCESS_KEY = ''

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', aws_access_key_id = MY_ACCESS_KEY_ID, aws_secret_access_key = MY_SECRET_ACCESS_KEY, region_name='us-east-2')
table = dynamodb.Table('users')

# Create your views here.

from django.http import HttpResponse

def index(request):
    return render(request, "front/login.html")

def home(request):
    return render(request,"front/index.html")

def view_a(request):
    return render(request, "front/register.html")

@csrf_protect
def register(request):
    user = str(request.GET.get('user'))
    email = str(request.GET.get('email'))
    password = str(request.GET.get('password'))
    phonenumber = str(request.GET.get('phonenumber'))
    url2 = str(request.GET.get('url2'))
    print(url2)
    data= ""
    try:
        response = table.get_item(
            Key={
                'userid': user
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        try:
            item = response['Item']
            print(json.dumps(item, indent=4, cls=DecimalEncoder))
            print("Already a member")
            data = {
                'user_id' : "not"
            }

        except:
            hash_object = hashlib.sha256(password.encode('utf-8'))
            hex_dig = hash_object.hexdigest()
            response = table.put_item(
                Item={
                    'userid': user,
                    'email': email,
                    'password': hex_dig,
                    'phonenumber': phonenumber
                }
            )
            print("Added " + str(user))
            data = {
                'user_id': "pass"
            }
            url2 = str(url2) + str(phonenumber)
            session = requests.Session()
            session.trust_env = False
            response1 = session.get(url2)

    return JsonResponse(data)

@csrf_protect
def login_check(request):
    user = str(request.GET.get('user'))
    #request.session['user']=user
    password = str(request.GET.get('password'))

    try:
        response = table.get_item(
            Key={
                'userid': user
            }
        )
    except :
        print("User Id doesn't exist")
        data = {
            'user_id': "not"
        }

    else:
        try:
            item = response['Item']
            print("GetItem succeeded:")
            print(json.dumps(item, indent=4, cls=DecimalEncoder))
            print(str(item['userid']) + str(item['password']))
            hash_object = hashlib.sha256(str(password).encode('utf-8'))
            hex_dig = hash_object.hexdigest()

            if hex_dig == item['password'] and user == item['userid']:
                print("successful")  # do something here...............................
                data = {
                    'user_id': user
                }
            else:
                print("Login Failed")
                data = {
                    'user_id': "not"
                }

        except:
            print("User Id Invalid, Please Check")
            data = {
                'user_id': "not"
            }

    return JsonResponse(data)

