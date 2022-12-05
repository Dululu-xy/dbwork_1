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