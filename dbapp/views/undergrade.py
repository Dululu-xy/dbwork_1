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

rootPath = str(settings.BASE_DIR)
@csrf_exempt
def undergrade_list(request):
    #首先检验是否是高级查询
    if(request.method=='POST'):
        data = request.POST
        print(data)
        # __icontains 模糊匹配
        searchlist = models.Undergraduate.objects.filter(year__icontains=data.get('year'),
                                                         student_id__icontains=data.get('student_id'),
                                                         gender__icontains=data.get('gender'),
                                                         graduation__icontains=data.get('graduation'),
                                                         organization__icontains=data.get('organization'),
                                                         location__icontains=data.get('location'),
                                                         affiliation__icontains=data.get('affiliation'),
                                                         nature__icontains=data.get('nature'),
                                                         type__icontains=data.get('type'),
                                                         industry__icontains=data.get('industry'))
    else:
        data_dict = {}
        print('youare list')
        search_data = request.GET.get('q', "")
        if search_data:  # 如果不为空则存在搜索内容
            data_dict['student_id__contains'] = search_data
        # 按照级别排序
        searchlist = models.Undergraduate.objects.filter(**data_dict)
    form=Undergrade_form()
    page_object = Pagination(request, searchlist)
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

#对于含有choice的字段，根据输入字段找数据库中存储的字段
def get_choices_index(choices,str):
    for i in range(len(choices)):
        if choices[i][1]==str:
            return (choices[i][0])
    return -1

# 文件上传
@csrf_exempt
def undergrade_upload(request):
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
            model=models.Undergraduate()
            models.Undergraduate.objects.get_or_create(year=file_table.cell(i,0).value,
                                        student_id=file_table.cell(i,1).value,
                                        gender=get_choices_index(model.gender_choice,file_table.cell(i,2).value),
                                        graduation=get_choices_index(model.graduation_choice,file_table.cell(i,3).value),
                                        organization=file_table.cell(i,4).value,
                                        location=file_table.cell(i,5).value,
                                        affiliation=file_table.cell(i,6).value,
                                        nature=get_choices_index(model.nature_choice,file_table.cell(i,7).value),
                                        type=get_choices_index(model.type_choice,file_table.cell(i,8).value),
                                        industry=get_choices_index(model.industry_choice,file_table.cell(i,9).value)
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
def undergrade_delete(request):
    uid=request.GET.get('uid')
    models.Undergraduate.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})
@csrf_exempt
def undergrade_deleteAll(request):
    data=request.POST
    deletelist = data.getlist('vals')
    for i in range(len(deletelist)):
        if deletelist[i] != "":
            models.Undergraduate.objects.filter(id=int(deletelist[i])).delete()
        else:
            continue
    return JsonResponse({'status':True})
#本科生就业信息统计
def undergrade_chart(request):
    return render(request,'chart_undergrade.html')
#就业类型按性别统计
def chart_bar(request):
    data_boy=[0]*6
    data_girl=[0]*6
    liboy =models.Undergraduate.objects.filter(gender=1).values('graduation')
    for li in liboy:
        data_boy[li['graduation']-1]+=1
    ligirl = models.Undergraduate.objects.filter(gender=2).values('graduation')
    for li in ligirl:
        data_girl[li['graduation'] - 1] += 1
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
    xaxis=['升学','非派遣/劳动合同','签约就业','出国学习','定向就业','灵活就业']
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
#就业按行业性质统计
def chart_pie(request):
    data = [0] * 12
    lis= models.Undergraduate.objects.all().values('industry')
    for li in lis:
        value=li['industry']
        if value==-1:
            continue
        data[value- 1] += 1
    result={
        'status':True,
        'data':[
            {'value': data[0], 'name': '制造业'},
            {'value': data[1], 'name': '信息传输软件和信息技术服务业'},
            {'value': data[2], 'name': '采矿业'},
            {'value': data[3], 'name': '交通运输、仓储和邮政业'},
            {'value': data[4], 'name': '租赁和商业服务业'},
            {'value': data[5], 'name': '金融业'},
            {'value': data[6], 'name': '建筑业'},
            {'value': data[7], 'name': '科学研究和技术服务业'},
            {'value': data[8], 'name': '军队'},
            {'value': data[9], 'name': '教育'},
            {'value': data[10], 'name': '其他'},
            {'value': data[11], 'name': '制造业'},
             ]
    }
    return JsonResponse(result)
