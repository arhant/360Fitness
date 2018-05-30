from __future__ import print_function
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
import boto3

MY_ACCESS_KEY_ID = ''
MY_SECRET_ACCESS_KEY = ''

dynamodb = boto3.resource('dynamodb', aws_access_key_id = MY_ACCESS_KEY_ID, aws_secret_access_key = MY_SECRET_ACCESS_KEY, region_name='us-east-2')


def buddysearch(request):
    return render(request, 'FindBuddy/buddy.html')


def chatwithbuddy(request):
    return redirect("http://18.217.55.100:5000")

def buddyinfo(request):
    template = loader.get_template('FindBuddy/buddyinfo.html')
    table = dynamodb.Table('users')
    response = table.scan()
    users = response['Items']
    buddy = []
    friends ={}
    for i in users:
        friends['userid'] = str(i['userid'])
        try:
            friends['height'] = str(i['height'])
            friends['weight'] = str(i['weight'])
            friends['likes'] = str(i['likes'])
        except KeyError:
            pass
        buddy.append(friends.copy())
    print(buddy)
    context = {
        "buddy": buddy,
    }
    return HttpResponse(template.render(context, request))