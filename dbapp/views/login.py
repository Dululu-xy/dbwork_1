from django.shortcuts import render,redirect

# Create your views here.

# 网站首页
def login(request):
    return render(request, "login.html")
def index(request):
    return render(request, 'index.html')
def test(request):
    return render(request, 'test.html')