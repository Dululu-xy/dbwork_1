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
def postgrauate_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:  # 如果不为空则存在搜索内容
        data_dict['student_id__contains'] = search_data
    # 按照级别排序
    data_list = models.Postgraduate.objects.filter(**data_dict)
    form = Postgrauate_form()
    page_object = Pagination(request, data_list)
    context = {
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()}  # 页码html
    return render(request, 'postgraduate_list.html', context)
class Postgrauate_form(BootstrapModelForm):
    class Meta:
        model=models.Postgraduate
        fields='__all__'