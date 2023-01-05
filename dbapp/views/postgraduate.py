from django.shortcuts import render,redirect,HttpResponse
from dbapp import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from dbapp.utils.pagination import  Pagination
from  dbapp.utils.bootstrap import BootstrapModelForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db import transaction
import json
import xlrd

from dbapp.views.undergrade import rootPath


def postgraduate_list(request):
    # 首先检验是否是高级查询
    if (request.method == 'POST'):
        data = request.POST
        print(data)
        # __icontains 模糊匹配
        searchlist = models.Postgraduate.objects.filter( gender__icontains=data.get('gender'),
                                                         degree__icontains=data.get('degree'),
                                                         specialty__icontains=data.get('specialty'),
                                                         grade__icontains=data.get('grade'),
                                                         year__icontains=data.get('year'),
                                                         pgraduation__icontains=data.get('pgraduation'),
                                                         rgraduation__icontains=data.get('rgraduation'),
                                                         organization__icontains=data.get('organization'),
                                                         location__icontains=data.get('location'),
                                                         status__icontains=data.get('status'),
                                                         )
    else:
        data_dict = {}
        print('youare list')
        search_data = request.GET.get('q', "")
        if search_data:  # 如果不为空则存在搜索内容
            data_dict['year__contains'] = search_data
        # 按照级别排序
        searchlist = models.Postgraduate.objects.filter(**data_dict)
    form = Postgraduate_form()
    page_object = Pagination(request, searchlist)
    context = {
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()}  # 页码html
    return render(request, 'postgraduate_list.html', context)
class Postgraduate_form(BootstrapModelForm):
    class Meta:
        model=models.Postgraduate
        fields='__all__'
@csrf_exempt
def postgraduate_add(request):
    form = Postgraduate_form(data=request.POST)
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
def postgraduate_detail(request):
    uid=request.GET.get('uid')
    res_dict=models.Postgraduate.objects.filter(id=uid).values().first()
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
def postgraduate_edit(request):
    uid=request.GET.get('uid')
    print('uid'+uid)
    row_object=models.Postgraduate.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({'status':False,'tips':'数据不存在，请刷新重试'})
    form=Postgraduate_form(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        print(form.cleaned_data)
        return JsonResponse({'status':True})
    return JsonResponse({'status':False,'error':form.errors})

#对于含有choice的字段，根据输入字段找数据库中存储的字段
def get_choices_index(choices,str):
    for i in range(len(choices)):
        if choices[i][1]==str:
            return (choices[i][0])
    return -1

# 文件上传
@csrf_exempt
def postgraduate_upload(request):
    file_object = request.FILES.get("myfile")
    print(file_object)
    file_path = rootPath + "\\dbapp\\tempfiles\\" + 'temp.' + file_object.name.split('.',2)[1]
    # 读取文件内容并写入到本地
    f = open(file_path, mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()
    read_file = xlrd.open_workbook(filename=file_path,file_contents=file_object.read())
    file_table = read_file.sheets()[0]
    file_table_rows = file_table.nrows

    with transaction.atomic():
        # 读表格数据，从第二行开始，一般第一行都是说明
        for i in range(1,file_table_rows):
            model=models.Postgraduate()
            models.Undergraduate.objects.get_or_create(gender=get_choices_index(model.gender_choice,file_table.cell(i,0).value),
                                        degree=get_choices_index(model.degree_choice,file_table.cell(i,1).value),
                                        specialty=get_choices_index(model.specialty_choice,file_table.cell(i,2).value),
                                        grade=file_table.cell(i,3).value,
                                        year=file_table.cell(i,4).value,
                                        pgraduation=get_choices_index(model.pgraduation_choice,file_table.cell(i,5).value),
                                        rgraduation=get_choices_index(model.rgraduation_choice,file_table.cell(i,6).value),
                                        organization=file_table.cell(i,7).value,
                                        location=file_table.cell(i, 8).value,
                                        status=file_table.cell(i, 9).value,
                                        )
    return JsonResponse({'status':True})
# @csrf_exempt
# def undergrade_search(request):
#     data=request.POST
#     print(data)
#     # __icontains 模糊匹配
#     searchlist = models.Undergraduate.objects.filter(year__icontains=data.get('year'),
#                                         student_id__icontains=data.get('student_id'),
#                                         gender__icontains=data.get('gender'),
#                                         graduation__icontains=data.get('graduation'),
#                                         organization__icontains=data.get('organization'),
#                                         location__icontains=data.get('location'),
#                                         affiliation__icontains=data.get('affiliation'),
#                                         nature__icontains=data.get('nature'),
#                                         type__icontains=data.get('type'),
#                                         industry__icontains=data.get('industry'))
#     print(len(searchlist))
#     form=Undergrade_form()
#     page_object = Pagination(request, searchlist)
#     context = {
#         "status": True,
#         "form": form,
#         "queryset": page_object.page_queryset,  # 分完页的数据
#         "page_string": page_object.html() }#页码html
#     #return render(request, 'undergrade_list.html',context)
#     return JsonResponse(context)
def postgraduate_delete(request):
    uid=request.GET.get('uid')
    models.Postgraduate.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})
@csrf_exempt
def postgraduate_deleteAll(request):
    data=request.POST
    deletelist = data.getlist('vals')
    for i in range(len(deletelist)):
        if deletelist[i] != "":
            models.Postgraduate.objects.filter(id=int(deletelist[i])).delete()
        else:
            continue
    return JsonResponse({'status':True})
#研究生就业信息统计
def postgraduate_chart(request):
    return render(request,'chart_postgraduate.html')
#就业类型按性别统计
def chart_bar(request):
    data_boy=[0]*8
    data_girl=[0]*8
    liboy =models.Postgraduate.objects.filter(gender=1).values('pgraduation')
    for li in liboy:
        data_boy[li['pgraduation']-1]+=1
    ligirl = models.Postgraduate.objects.filter(gender=2).values('pgraduation')
    for li in ligirl:
        data_girl[li['pgraduation'] - 1] += 1
    print(data_boy,data_girl)
    series= [
                {
                    "name": '男',
                    "type": 'bar',
                    "data": data_boy
                },
                {
                    "name": '女',
                    "type": 'bar',
                    "data": data_girl
                }
            ]
    xaxis=['劳动合同','协议就业','未就业','非派遣','考取升学','自主创业','出国（境）学习','定向就业']
    legend=['男','女']
    result={
        "status":True,
        'data':{
            'legend':legend,
            'series':series,
            'xaxis':xaxis,
        }
    }
    return JsonResponse(result)
#按专业统计
def chart_pie(request):
    data = [0] * 4
    lis= models.Postgraduate.objects.all().values('specialty')
    for li in lis:
        value=li['specialty']
        if value==-1:
            continue
        data[value- 1] += 1
    result={
        'status':True,
        'data':[
            {'value': data[0], 'name': '计算机技术与资源信息工程'},
            {'value': data[1], 'name': '计算机技术'},
            {'value': data[2], 'name': '软件工程'},
            {'value': data[3], 'name': '计算机科学与技术'},
             ]
    }
    return JsonResponse(result)
