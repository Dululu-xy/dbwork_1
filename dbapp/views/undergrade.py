from django.shortcuts import render,redirect
def undergrade_list(request):
    return render(request, 'undergrade_list.html')