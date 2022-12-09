from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
def chart_list(request):
    return render(request,'chart_list.html')
def chart_pie(request):
    result={
        'status':True,
        'data':[
                            {'value': 1048, 'name': 'Search Engine'},
                            {'value': 735, 'name': 'Direct'},
                            {'value': 580,'name': 'Email'},
                            {'value': 484, 'name': 'Union Ads'},
                            {'value': 300, 'name': 'Video Ads'}
                        ]
    }
    return JsonResponse(result)
def chart_line(request):
    result={
        'status':True,
        'data':{
        'series':[150, 230, 224, 218, 135, 147, 260],
        'xaxis':['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    }
    }
    return JsonResponse(result)