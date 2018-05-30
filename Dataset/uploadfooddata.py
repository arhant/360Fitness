from __future__ import print_function
import boto3
import json
from decimal import *

MY_ACCESS_KEY_ID = ''
MY_SECRET_ACCESS_KEY = ''

dynamodb = boto3.resource('dynamodb', aws_access_key_id = MY_ACCESS_KEY_ID, aws_secret_access_key = MY_SECRET_ACCESS_KEY, region_name='us-east-2')

table = dynamodb.Table('fooddata')

with open("convertedcsv.json") as json_file:
    foods= json.load(json_file, parse_float = decimal.Decimal)
    for food in foods:
        food_desc_portion = food['food_desc_portion']
        calories = Decimal(food['calories'])
        protein = Decimal(food['protein'])
        fat = Decimal(food['fat'])
        carbohydrate = Decimal(food['carbohydrate'])

        table.put_item(
           Item={
               'food_desc_portion': food_desc_portion,
               'calories': calories,
               'protein': protein,
               'fat': fat,
               'carbohydrate': carbohydrate, 
            }
        )

        print("Adding food:", food_desc_portion)