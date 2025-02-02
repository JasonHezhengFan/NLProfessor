from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from icecream import ic
import sys
import os
sys.path.append(os.getcwd())
from search.keyword_search import classes_db

# define home function
def home(request):
    return HttpResponse('Hello World!')

@csrf_exempt
def webhook(request):
    """
    A bunch of if else loops that determine the logic.
    """
    # build a request object
    req = json.loads(request.body)
    # get action from json
    intent = req.get('queryResult').get('intent').get('displayName')
    params = req.get('queryResult').get('parameters')
    # The ugly part
    if intent == 'Get-Name' and len(params) == 2:
        create_student(params['name'], params['unique_name'])
    elif intent == 'Major' and len(params) == 2:
        add_major_year(params)
    ic(params, intent)

    # return a fulfillment message
    # fulfillmentText = {'fulfillmentText': 'This is Django test response from webhook.'}
    # # return response
    # return JsonResponse(fulfillmentText, safe=False)
    return None

def create_student(name, unique_name):
    stud = Student(name=name, unique_name=unique_name)
    stud.save()
    ic(Student.objects.all(), stud.id)

def add_major_year(params):
    stud = Student.objects.all()[0]
    stud.major = params['major']
    stud.year = params['year']
    stud.save()

def search_class(keywords: str, info: list=["number", "name", "desc", "workload"], db = None) -> list:
    """Search classes based on keywords.

    Input:
    keywords: string, i.e. "Machine Learning"
    info: list, info returned associated with each class in the returned list

    Output:
    A list consists of 6 relevant classes sorted by tf-idf score.
    """
    db = classes_db(db_file="advising_project/webhook/json/classes.json")
    init_result = db.search(keywords)
    post_process = []
    for _dict in init_result:
        new_dict = {}
        for _key in info:
            new_dict[_key] = _dict[_key]
        post_process.append(new_dict)
    return post_process

