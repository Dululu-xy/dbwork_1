from django.db import models

# Create your models here.
from django.db import models
#本科生表
class Undergraduate(models.Model):
    year=models.CharField(verbose_name='年度',max_length=4)
    student_id=models.CharField(verbose_name='学号',max_length=10)
    gender_choice = (
        (1, "男"),
        (2, "女")
    )  # 使用的时候使用get_gender_display还原
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choice)
    graduation_choice = (
        (1, '升学'),
        (2, '非派遣/劳动合同'),
        (3, '签约就业'),
        (4, '出国学习'),
        (5,'定向就业'),
        (6,'灵活就业')
    )
    graduation = models.SmallIntegerField(verbose_name='毕业去向', choices=graduation_choice)
    organization=models.CharField(verbose_name='实际单位',max_length=100,null=True,blank=True)
    location=models.CharField(verbose_name='单位所在地',max_length=50)
    affiliation=models.CharField(verbose_name='单位隶属',max_length=50,blank=True,null=True)
    nature_choice = (
        (1, '三资企业'),
        (2, '国有企业'),
        (3, '升学'),
        (4, '出国、出境'),
        (5, '灵活就业'),
        (6, '科研设计单位'),
        (7, '艰苦行业企业'),
        (8, '其他企业'),
        (9, '未就业'),
    )
    nature = models.SmallIntegerField(verbose_name='单位性质', choices=nature_choice)
    type_choice = (
        (1, '211院校'),
        (2, '985院校'),
        (3, '世界500强'),
        (4, '其他'),
    )
    type = models.SmallIntegerField(verbose_name='单位类型', choices=type_choice)
    industry_choice = (
        (1, '制造业'),
        (2, '信息传输软件和信息技术服务业'),
        (3, '采矿业'),
        (4, '交通运输、仓储和邮政业'),
        (5, '租赁和商业服务业'),
        (6, '金融业'),
        (7, '建筑业'),
        (8, '科学研究和技术服务业'),
        (9, '科学研究和技术服务业'),
        (10, '军队'),
        (11, '教育'),
        (12, '其他'),
    )
    industry = models.SmallIntegerField(verbose_name='行业性质', choices=industry_choice)



#研究生表
class Postgraduate(models.Model):
    gender_choice = (
        (1, "男"),
        (2, "女")
    )  # 使用的时候使用get_gender_display还原
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choice)

    degree_choice = (
        (1, "硕士生毕业"),
        (2, "博士生毕业")
    )  # 使用的时候使用get_gender_display还原
    degree = models.SmallIntegerField(verbose_name='学历', choices=degree_choice)
    specialty_choice = (
        (1, "计算机技术与资源信息工程"),
        (2, "计算机技术"),
        (3, "软件工程"),
        (4, "计算机科学与技术"),
    )  # 使用的时候使用get_gender_display还原
    specialty = models.SmallIntegerField(verbose_name='专业', choices=specialty_choice)

    grade = models.CharField(verbose_name='年级', max_length=4)
    year = models.CharField(verbose_name='毕业年度', max_length=4)

    pgraduation_choice = (
        (1, '劳动合同'),
        (2, '协议就业'),
        (3, '未就业'),
        (4, '非派遣'),
        (5,'考取升学'),
        (6,'自主创业'),
        (7,'出国（境）学习'),
        (8,'定向就业'),

    )
    pgraduation = models.SmallIntegerField(verbose_name='预计就业类型', choices=pgraduation_choice)

    rgraduation_choice = (
        (1, '劳动合同'),
        (2, '协议就业'),
        (3, '未就业'),
        (4, '非派遣'),
        (5, '升学'),
        (6, '自主创业'),
        (7, '出国'),
        (8, '定向'),
        (9,'部队文职'),
    )
    rgraduation = models.SmallIntegerField(verbose_name='实际就业类型', choices=rgraduation_choice)

    organization=models.CharField(verbose_name='就业升学单位',max_length=100,null=True,blank=True)
    location=models.CharField(verbose_name='单位所在地',max_length=50)
    status=models.CharField(verbose_name='目前状况',max_length=50,blank=True,null=True)
