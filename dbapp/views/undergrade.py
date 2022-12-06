from django.shortcuts import render,redirect,HttpResponse
from dbapp import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from dbapp.utils.pagination import  Pagination
from  dbapp.utils.bootstrap import BootstrapModelForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
def undergrade_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:  # 如果不为空则存在搜索内容
        data_dict['student_id__contains'] = search_data
    # 按照级别排序
    data_list = models.Undergraduate.objects.filter(**data_dict)
    form=Undergrade_form()
    page_object = Pagination(request, data_list)
    context = {
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html() }#页码html
    return render(request, 'undergrade_list.html',context)
class Undergrade_form(BootstrapModelForm):
    class Meta:
        model=models.Undergraduate
        fields='__all__'
@csrf_exempt
def undergrade_add(request):
    form = Undergrade_form(data=request.POST)
    print(request.POST)
    if form.is_valid():
        # 拼接订单号 自动生成
        form.save()
        data = {'status': True}
        return HttpResponse(json.dumps(data))
    else:
        data = {
            'status': False,
            'error': form.errors
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False))
def undergrade_detail(request):
    uid=request.GET.get('uid')
    res_dict=models.Undergraduate.objects.filter(id=uid).values().first()
    print(res_dict)
    if not res_dict:
        context={
            'status':False,
            'error':'数据不存在'
        }
    context={
        'status':True,
        'data':res_dict
    }
    return HttpResponse(json.dumps(context))
@csrf_exempt
def undergrade_edit(request):
    uid=request.GET.get('uid')
    row_object=models.Undergraduate.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({'status':False,'tips':'数据不存在，请刷新重试'})
    form=Undergrade_form(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        print(form.cleaned_data)
        return JsonResponse({'status':True})
    return JsonResponse({'status':False,'error':form.errors})
@csrf_exempt
def undergrade_upload(request):
    file_object = request.FILES['myfile']
    print(file_object)
    return JsonResponse({'status':True})