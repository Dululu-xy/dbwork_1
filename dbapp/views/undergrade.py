from django.shortcuts import render,redirect
from dbapp import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from dbapp.utils.pagination import  Pagination
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
class Undergrade_form(forms.ModelForm):
    #自定义属性格式，后面会校验 方式1
    moblie=forms.CharField(min_length=11,label='号码',
        validators=[RegexValidator(r'^1[3-9]\d{9}$','号码格式错误')])
    class Meta:
        model=models.Undergraduate
        fields='__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,filed in self.fields.items():
            filed.widget.attrs={'class':'form-control'}
def undergrade_add(request):
    pass