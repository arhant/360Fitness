from __future__ import print_function
import boto3
import json
from decimal import *

MY_ACCESS_KEY_ID = ''
MY_SECRET_ACCESS_KEY = ''

dynamodb = boto3.resource('dynamodb', aws_access_key_id = MY_ACCESS_KEY_ID, aws_secret_access_key = MY_SECRET_ACCESS_KEY, region_name='us-east-2')

table = dynamodb.Table('gymdataset')

with open("gymdataset.json") as json_file:
    workouts = json.load(json_file)
    for workout in workouts:
        exercise = workout['exercise']
        description = workout['description']
        category = workout['category']

        table.put_item(
           Item={
               'exercise': exercise,
               'description': description,
               'category': category,
            }
        )

        print("Adding workout:", exercise)