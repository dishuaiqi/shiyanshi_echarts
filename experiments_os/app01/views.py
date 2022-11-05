from django.shortcuts import render,HttpResponse
import datetime
from django import forms
from app01 import models
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
from django_pandas.io import read_frame
import pandas as pd
import numpy as np
import openpyxl
start = datetime.datetime.now()
start=datetime.datetime(year=start.year,month=start.month-2,day=28)

class pcrModleform(forms.ModelForm):
    class Meta:
        model=models.BingYuan
        fields="__all__"


# Create your views here.
def pcr_list(request):
    form=pcrModleform()
    queryset=models.BingYuan.objects.all().order_by('-id')

    return render(request,'pcr_list.html',{'querryset':queryset,'form':form})

@csrf_exempt
def pcr_add(request):
    # print(request.POST)
    form=pcrModleform(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status':True})

def echart_sample(request):
    PCRcount=models.BingYuan.objects.all().count()

    kangti_count=models.kangti.objects.all().count()

    last_month_pcrcount=models.BingYuan.objects.filter(日期__gte=start).count()

    last_month_positive_count=models.BingYuan.objects.filter(Q(日期__gte=start) & Q(结果='+')).count()

    allcount=str(PCRcount+kangti_count)
    if len(allcount)==5:
        allcount=str('00')+allcount
    elif len(allcount)==6:
        allcount = str('0') + allcount
    else:
        allcount = allcount
    allcount_list=[]
    for i in allcount:
        allcount_list.append(i)

    data={
        'pcrcount':PCRcount,
        'last_month_pcrcount':last_month_pcrcount,
        'kangti_count':kangti_count,
        'last_month_positive_count':last_month_positive_count,
        'all_count':allcount
    }

    return render(request,'index.html',data)



def echart_list(request):

    return render(request,'echart_list.html')




# def echart_bar(request):
#
#     start = datetime.datetime.now()
#     #本月查询
#     table_list = models.BingYuan.objects.filter(Q(日期__month=start.month-1)&Q(日期__year=start.year))
#     #转为pandas
#     df = read_frame(qs=table_list)
#
#     #不同公司的操作
#     gongsi_count = df['公司'].value_counts()
#     gongsi_list = gongsi_count.to_dict()
#     # print(gongsi_count)
#     gongsi_name = list(gongsi_list.keys())
#     gongsi_data = []
#     for key, value in gongsi_list.items():
#         gongsi_data.append({'value': value, 'name': key})
#
#      #前5的部门操作
#     bumen_count=df['部门'].value_counts()
#     bumen_list=bumen_count.to_dict()
#     bumen_name=list(bumen_list.keys())
#     bumen_name_count=list(bumen_list.values())
#
#     #不同样品操作
#     yangpin_type=df['样本类型'].value_counts()
#
#     yangpin_type_list=yangpin_type.to_dict()
#
#     yangpin_type_name=list(yangpin_type_list.keys())
#
#     yangpin_type_data=[]
#     for key, value in yangpin_type_list.items():
#         yangpin_type_data.append({'value': value, 'name': key})
#     # print(yangpin_type_data)
#
#     #不同检测类型操作
#     jiance_type=df['检测类型'].value_counts()
#
#     jiance_type_list=jiance_type.to_dict()
#
#     jiance_type_name=list(jiance_type_list.keys())
#
#     jiance_type_data=[]
#     for key, value in jiance_type_list.items():
#         jiance_type_data.append({'value': value, 'name': key})
#
#     #阳性数量操作
#     positive_type_count={}
#     negative_type_count={}
#     for i in jiance_type_name:
#         positive_count = models.BingYuan.objects.filter(Q(日期__month=start.month - 1) & Q(日期__year=start.year)&Q(检测类型=i)&Q(结果='+')).count()
#
#         positive_type_count[i]=positive_count
#
#         negative_count = models.BingYuan.objects.filter(Q(日期__month=start.month - 1) & Q(日期__year=start.year)&Q(检测类型=i)&Q(结果='-')).count()
#
#         negative_type_count[i] = negative_count
#
#     positive_count_list=[-x for x in list(positive_type_count.values())]
#
#     negative_count_list=list(negative_type_count.values())
#
#     # 阳性场区
#     positive_month=models.BingYuan.objects.filter(Q(日期__month=start.month-1)&Q(日期__year=start.year)&Q(结果='+'))
#
#     positive_month=read_frame(qs=positive_month)
#
#     positive_changqu=positive_month['部门'].value_counts().to_dict()
#     positive_changqu=list(positive_changqu.keys())
#
#     positive_jiance_type=positive_month['检测类型'].value_counts().to_dict()
#     positive_jiance_type=list(positive_jiance_type.keys())
#
#     positive_changqu_dic={}
#     for i in positive_changqu:
#         positive_changqu_dic_type={}
#         for j in positive_jiance_type:
#             count=models.BingYuan.objects.filter(Q(日期__month=start.month - 1) & Q(日期__year=start.year) & Q(结果='+')&Q(检测类型=j)&Q(部门=i)).count()
#             positive_changqu_dic_type[j]=count
#         positive_changqu_dic[i]=positive_changqu_dic_type
#
#     print(positive_changqu_dic)
#
#     positive_changqu_list=positive_changqu_dic.values()
#
#     positive_changqu_type_count=[]
#     for i in positive_changqu_list:
#         positive_changqu_type_count.append(list(i.values()))
#     print(positive_changqu_type_count)
#
#     positive_type_changqu_list=[['检测类型']+list(positive_jiance_type)]
#     for i in range(len(list(positive_changqu))):
#         positive_type_changqu_list.append([positive_changqu[i]]+positive_changqu_type_count[i])  #这是把阳性的场区和类型加上
#
#     print(positive_type_changqu_list)
#
#
#     #检测数量操作
#     now_time=datetime.datetime.now()
#
#     jiance_count_month={}
#     for i in range(1,13):
#         start_month=datetime.datetime(year=now_time.year,month=i,day=1)
#         month_jiance=models.BingYuan.objects.filter(Q(日期__month=start_month.month)&Q(日期__year=start_month.year))
#         df_month = read_frame(qs=month_jiance)
#         gongsi_count_month = df_month['公司'].value_counts()
#         gongsi_list_month = gongsi_count_month.to_dict()
#         # print(gongsi_list_month)
#         gongsi_name_month = list(gongsi_list_month.keys())
#         jiance_count_month[str(i)+'月']=gongsi_list_month
#
#     jiance_count_month_pd=pd.DataFrame(jiance_count_month)
#
#     for i in jiance_count_month_pd.columns:
#         if jiance_count_month_pd[i].count()==0:
#             jiance_count_month_pd.drop(labels=i,axis=1,inplace=True)
#
#     # print(jiance_count_month_pd)
#     #行列转换
#     jiance_count_month_pd=pd.DataFrame(jiance_count_month_pd.values.T,index=jiance_count_month_pd.columns,columns=jiance_count_month_pd.index)
#     # print(jiance_count_month_pd)
#     jiance_count_month_pd=jiance_count_month_pd.fillna(0)
#     one_list=['月份']
#     for i in jiance_count_month_pd.index:
#         one_list.append(i)
#
#     #怎么样把需要的数据添加上
#     all_columns={}
#     for j in jiance_count_month_pd.columns:
#         all_columns[j]=[j]+list(jiance_count_month_pd[j])
#
#     # print(all_columns)
#     #前5的检测数量场区
#
#
#
#
#     #图表内容数据
#     series_bar=[
#         {
#             "name": 'Funnel',
#             "type": 'funnel',
#             "left": '20%',
#             "top": 60,
#             "bottom":60,
#             "width": '80%',
#             "min": 0,
#             "max": 500,
#             "minSize": '0%',
#             "maxSize":'100%',
#             "sort":'ascending',
#             "gap":2,
#             "label": {
#                 "show": "true",
#                 "position": 'inside'
#             },
#             "labelLine": {
#                 "length": 10,
#                 "lineStyle": {
#                     "width": 1,
#                     'type':'solid'
#                 }
#             },
#             "itemStyle": {
#                "borderColor": '#fff',
#                 "borderWidth": 1
#             },
#             "emphasis": {
#                 "label": {
#                     'fontSize': 20
#                 }
#             },
#             'data': gongsi_data
#         }
#     ]
#     series_yangpinType = [
#         {
#               'name': '样品数量',
#               'type': 'pie',
#               'radius': ['40%', '70%'],
#               'center':['45%','50%'],
#               'avoidLabelOverlap': 'true',
#               'label': {
#                 'formatter': '{d}%',
#                  'position':'inner',
#                   'color':'#fff',
#             },
#
#             'emphasis': {
#                 'label': {
#                     'show': 'true',
#                     'fontSize': '40',
#                     'fontWeight': 'bold',
#                     'textStyle': {'color': '#FFFFFF'}
#                 }
#             },
#
#
#             'labelLine': {
#                 'show': 'false',
#             },
#             'data':yangpin_type_data
#
#         }
#     ]
#
#     jiance_type_radiusAxis= {
#        'type': 'category',
#        'data': jiance_type_name,
#         'axisLabel':{
#             'textStyle':{
#                 'color':'#7edae8',
#                 'fontSize': 10,
#             }
#         }
#     }
#     jiance_type_series={
#         'type': 'bar',
#         'data': jiance_type_data,
#         'label': {
#             'show': 'true',
#            ' position': 'left',
#          },
#
#
#
#     }
#
#     jiance_count=[one_list]
#
#     for i in all_columns.values():
#         jiance_count.append(i)
#     # print(jiance_count)
#     #上月不同类型检测数量
#     positive_jiance_type={
#         'yAxis': [
#             {
#                 'type': 'category',
#                 'axisTick': {
#                     'show': 'false'
#                 },
#                 'data': jiance_type_name
#             }
#         ],
#         'series': [
#             {
#                 'name': '阴性',
#                 'type': 'bar',
#                 'stack': 'Total',
#                'label': {
#                     'show': 'true'
#                 },
#                 'emphasis': {
#                     'focus': 'series'
#                 },
#                 'data': negative_count_list
#             },
#             {
#                 'name': '阳性',
#                 'type': 'bar',
#                 'stack': 'Total',
#                 'label': {
#                     'show': 'true',
#                     'position': 'left'
#                 },
#                 'emphasis': {
#                     'focus': 'series'
#                 },
#                 'data': positive_count_list
#             }
#         ]
#     }
#
#
#
#
#
#
#     data = {
#         'legend': gongsi_name,
#         'series': series_bar,
#         'series_yangpinType':series_yangpinType,
#         'jiance_type_radiusAxis':jiance_type_radiusAxis,
#         'jiance_type_series':jiance_type_series,
#         'jiance_count_source':jiance_count,
#         'positive_jiance_type':positive_jiance_type,
#         'positive_type_changqu_list':positive_type_changqu_list,
#         'bumen_name':bumen_name[:5],
#         'bumen_name_count':bumen_name_count[:5]
#
#     }
#
#
#
#
#
#
#
#
#     return JsonResponse(data)

def echart_one(request):
    now_time = datetime.datetime.now()
    # 上月查询

    last_month_all_counts = models.BingYuan.objects.filter(日期__gte=start)
    # 转为pandas
    df = read_frame(qs=last_month_all_counts)

    yangpin_type = df['样本类型'].value_counts()

    yangpin_type_list = yangpin_type.to_dict()

    yangpin_type_name = list(yangpin_type_list.keys())

    yangpin_type_data = []
    for key, value in yangpin_type_list.items():
        yangpin_type_data.append({'value': value, 'name': key})

    series_yangpinType = [
        {
            'name': '样品数量',
            'type': 'pie',
            'radius': ['40%', '70%'],
            'center': ['45%', '50%'],
            'avoidLabelOverlap': 'true',
            'label': {
                'formatter': '{d}%',
                'position': 'inner',
                'color': '#fff',
            },

            'emphasis': {
                'label': {
                    'show': 'true',
                    'fontSize': '40',
                    'fontWeight': 'bold',
                    'textStyle': {'color': '#FFFFFF'}
                }
            },

            'labelLine': {
                'show': 'false',
            },
            'data': yangpin_type_data

        }
    ]
    data={
        'series_yangpinType': series_yangpinType,
    }
    return JsonResponse(data)


def echart_two(request):
    now_time = datetime.datetime.now()
    # 上月查询
    last_month_all_counts = models.BingYuan.objects.filter(Q(日期__gte=start))
    # 转为pandas
    df = read_frame(qs=last_month_all_counts)


    jiance_type = df['检测类型'].value_counts()

    jiance_type_list = jiance_type.to_dict()

    jiance_type_name = list(jiance_type_list.keys())

    jiance_type_data = []
    for key, value in jiance_type_list.items():
        jiance_type_data.append({'value': value, 'name': key})

    jiance_type_radiusAxis = {
        'type': 'category',
        'data': jiance_type_name,
        'axisLabel': {
            'textStyle': {
                'color': '#7edae8',
                'fontSize': 10,
            }
        }
    }
    jiance_type_series = {
        'type': 'bar',
        'data': jiance_type_data,
        'label': {
            'show': 'true',
            ' position': 'left',
        },

    }


    data={
        'jiance_type_radiusAxis': jiance_type_radiusAxis,
        'jiance_type_series': jiance_type_series,
    }
    return JsonResponse(data)

def echart_three(request):
    now_time = datetime.datetime.now()

    jiance_count_month = {}
    for i in range(1, 13):
        start_month = datetime.datetime(year=now_time.year, month=i, day=1)
        month_jiance = models.BingYuan.objects.filter(Q(日期__month=start_month.month) & Q(日期__year=start_month.year))
        df_month = read_frame(qs=month_jiance)
        gongsi_count_month = df_month['公司'].value_counts()
        gongsi_list_month = gongsi_count_month.to_dict()
        # print(gongsi_list_month)
        gongsi_name_month = list(gongsi_list_month.keys())
        jiance_count_month[str(i) + '月'] = gongsi_list_month

    jiance_count_month_pd = pd.DataFrame(jiance_count_month)

    for i in jiance_count_month_pd.columns:
        if jiance_count_month_pd[i].count() == 0:
            jiance_count_month_pd.drop(labels=i, axis=1, inplace=True)

    # print(jiance_count_month_pd)
    # 行列转换
    jiance_count_month_pd = pd.DataFrame(jiance_count_month_pd.values.T, index=jiance_count_month_pd.columns,
                                         columns=jiance_count_month_pd.index)
    # print(jiance_count_month_pd)
    jiance_count_month_pd = jiance_count_month_pd.fillna(0)
    one_list = ['月份']
    for i in jiance_count_month_pd.index:
        one_list.append(i)
    jiance_count = [one_list]

    all_columns = {}
    for j in jiance_count_month_pd.columns:
        all_columns[j] = [j] + list(jiance_count_month_pd[j])

    for i in all_columns.values():
        jiance_count.append(i)

    data={
        'jiance_count_source': jiance_count,
    }
    return JsonResponse(data)


def echart_four(request):

    # 上月查询
    last_month_all_counts = models.BingYuan.objects.filter(日期__gte=start)
    # 转为pandas
    df = read_frame(qs=last_month_all_counts)

    jiance_type = df['检测类型'].value_counts()

    jiance_type_list = jiance_type.to_dict()

    jiance_type_name = list(jiance_type_list.keys())

    jiance_type_data = []
    for key, value in jiance_type_list.items():
        jiance_type_data.append({'value': value, 'name': key})

    positive_type_count = {}
    negative_type_count = {}
    for i in jiance_type_name:
        positive_count = models.BingYuan.objects.filter(
            Q(日期__gte=start) & Q(检测类型=i) & Q(结果='+')).count()

        positive_type_count[i] = positive_count

        negative_count = models.BingYuan.objects.filter(
            Q(日期__gte=start) & Q(检测类型=i) & Q(结果='-')).count()

        negative_type_count[i] = negative_count

    positive_count_list = [-x for x in list(positive_type_count.values())]

    negative_count_list = list(negative_type_count.values())



    now_time = datetime.datetime.now()
    positive_month = models.BingYuan.objects.filter(Q(日期__gte=start) & Q(结果='+'))

    positive_month = read_frame(qs=positive_month)

    positive_changqu = positive_month['部门'].value_counts().to_dict()
    positive_changqu = list(positive_changqu.keys())

    positive_jiance_type = positive_month['检测类型'].value_counts().to_dict()
    positive_jiance_type = list(positive_jiance_type.keys())

    positive_changqu_dic = {}
    for i in positive_changqu:
        positive_changqu_dic_type = {}
        for j in positive_jiance_type:
            count = models.BingYuan.objects.filter(
                Q(日期__gte=start) & Q(结果='+') & Q(检测类型=j) & Q(部门=i)).count()
            positive_changqu_dic_type[j] = count
        positive_changqu_dic[i] = positive_changqu_dic_type

    print(positive_changqu_dic)

    positive_changqu_list = positive_changqu_dic.values()

    positive_changqu_type_count = []
    for i in positive_changqu_list:
        positive_changqu_type_count.append(list(i.values()))
    print(positive_changqu_type_count)

    positive_type_changqu_list = [['检测类型'] + list(positive_jiance_type)]
    for i in range(len(list(positive_changqu))):
        positive_type_changqu_list.append([positive_changqu[i]] + positive_changqu_type_count[i])  # 这是把阳性的场区和类型加上

    print(positive_type_changqu_list)

    jiance_type_name = list(jiance_type_list.keys())

    positive_jiance_type = {
        'yAxis': [
            {
                'type': 'category',
                'axisTick': {
                    'show': 'false'
                },
                'data': jiance_type_name
            }
        ],
        'series': [
            {
                'name': '阴性',
                'type': 'bar',
                'stack': 'Total',
                'label': {
                    'show': 'true'
                },
                'emphasis': {
                    'focus': 'series'
                },
                'data': negative_count_list
            },
            {
                'name': '阳性',
                'type': 'bar',
                'stack': 'Total',
                'label': {
                    'show': 'true',
                    'position': 'left'
                },
                'emphasis': {
                    'focus': 'series'
                },
                'data': positive_count_list
            }
        ]
    }

    data={
       'positive_jiance_type': positive_jiance_type,
       'positive_type_changqu_list': positive_type_changqu_list,
    }

    return JsonResponse(data)


def echart_five(request):

    positive_month = models.BingYuan.objects.filter(Q(日期__gte=start) & Q(结果='+'))

    positive_month = read_frame(qs=positive_month)

    positive_changqu = positive_month['部门'].value_counts().to_dict()
    positive_changqu = list(positive_changqu.keys())

    positive_jiance_type = positive_month['检测类型'].value_counts().to_dict()
    positive_jiance_type = list(positive_jiance_type.keys())

    positive_changqu_dic = {}
    for i in positive_changqu:
        positive_changqu_dic_type = {}
        for j in positive_jiance_type:
            count = models.BingYuan.objects.filter(
                Q(日期__gte=start) & Q(结果='+') & Q(检测类型=j) & Q(部门=i)).count()
            positive_changqu_dic_type[j] = count
        positive_changqu_dic[i] = positive_changqu_dic_type

    print(positive_changqu_dic)

    positive_changqu_list = positive_changqu_dic.values()

    positive_changqu_type_count = []
    for i in positive_changqu_list:
        positive_changqu_type_count.append(list(i.values()))
    print(positive_changqu_type_count)

    positive_type_changqu_list = [['检测类型'] + list(positive_jiance_type)]
    for i in range(len(list(positive_changqu))):
        positive_type_changqu_list.append([positive_changqu[i]] + positive_changqu_type_count[i])  # 这是把阳性的场区和类型加上

    data={
        'positive_type_changqu_list': positive_type_changqu_list,
    }
    return JsonResponse(data)

def echart_six(request):

    # 本月查询
    table_list = models.BingYuan.objects.filter(Q(日期__gte=start))
    # 转为pandas
    df = read_frame(qs=table_list)
    # 前5的部门操作
    bumen_count = df['部门'].value_counts()
    bumen_list = bumen_count.to_dict()
    bumen_name = list(bumen_list.keys())
    bumen_name_count = list(bumen_list.values())

    data={
        'bumen_name': bumen_name[:5],
        'bumen_name_count': bumen_name_count[:5]
    }
    return JsonResponse(data)


'''抗体可分析可视化'''

def kangti_echart(request):

    kangti_counts=models.kangti.objects.filter(日期__gte=start).count()
    now_year=models.kangti.objects.filter(日期__year=start.year).count()
    data={
        'now_year':now_year,
        'kangti_counts':kangti_counts

    }

    return render(request,'kangti.html',data)

def kangti_echart_one(request):
    #上月抗体类型及数量
    last_month_kangti=models.kangti.objects.filter(日期__gte=start)
    #转成pandas
    df_last_month_kangti=read_frame(last_month_kangti)
    jianceType=df_last_month_kangti['检测类型'].value_counts().to_dict()
    print(jianceType)
    data_last_kangti=[]
    for key,value in jianceType.items():
        data_last_kangti.append({'value':value,'name':key})
    data={
        'data_last_kangti':data_last_kangti
    }
    return JsonResponse(data)


def kangti_echart_two(request):
    now_time=datetime.datetime.now()
    '''今年抗体'''
    now_year_kangti=models.kangti.objects.filter(日期__year=now_time.year)
    now_year_kangti=read_frame(now_year_kangti)
    '''公司名称'''
    gongsi_name=now_year_kangti['公司'].value_counts().to_dict()

    gongsi_name=[x for x in gongsi_name]


    jiance_type=now_year_kangti['检测类型'].value_counts().to_dict()

    jiance_type=['伪狂犬gE抗体', '猪瘟抗体', '伪狂犬gB抗体', '非洲猪瘟抗体', '蓝耳抗体', '口蹄疫A型抗体', '圆环抗体', '口蹄疫O型抗体']
    print(jiance_type)
    '''截止到上个月'''
    all_month=[str(x)+str('月') for x in range(1,int(now_time.month))]





    series=[]
    for gongsi in gongsi_name:
        month_list=[]
        month_dic={}
        for month in range(1, int(now_time.month)):
            jiance_type_count=models.kangti.objects.filter(Q(日期__year=now_time.year) & Q(日期__month=month) &Q(公司=gongsi)).count()
            month_list.append(jiance_type_count)
        month_dic['name']=gongsi
        month_dic['data']=month_list
        month_dic['type']='line'
        month_dic['smooth']=True,
        series.append(month_dic)



    print(series)


    data={
        'all_month':all_month,
        'series':series,
        'gongsi_name':gongsi_name
    }
    return JsonResponse(data)


def kangti_echart_three(request):
    #场区样品达标情况
    muzhuchang=models.BingYuan.objects.filter(Q(日期__gte=start)&
                                              Q(公司__in=
                                                ['安徽禾丰浩翔农业发展有限公司','利辛宏丰农牧有限公司','阜阳禾丰农牧科技有限公司','利辛翔丰农牧有限公司',
                                                 '利辛荣丰农牧有限公司'])).all()
    muzhuchang=muzhuchang.exclude(部门__in=['阜阳生物安全部','利辛翔丰','马店外围','荣丰','阜阳服务部']).all()

    gongsi=['安徽禾丰浩翔农业发展有限公司','利辛宏丰农牧有限公司','阜阳禾丰农牧科技有限公司','利辛翔丰农牧有限公司','利辛荣丰农牧有限公司']

    # 统计每个公司下面有哪几个部门
    gongsi_dic={}
    for i in gongsi:
        bumen=muzhuchang.filter(公司=i)
        bumen=read_frame(bumen)['部门'].value_counts().to_dict().keys()
        bumen=list(bumen)
        gongsi_dic[i]=bumen
    print(gongsi_dic)
    #浩翔、翔丰、宏丰 环境1周 猪群15天
    # 阜阳禾丰 环境15天 猪群15天
    start_time=start
    fivetheen_time=datetime.datetime(year=start.year,month=start.month+1,day=13)
    #第一周开始结束
    week_one=datetime.datetime(year=start.year,month=start.month+1,day=5)
    week_one_start=datetime.datetime(year=start.year,month=start.month+1,day=5)
    # 第二周开始结束
    week_two=datetime.datetime(year=start.year,month=start.month+1,day=12)
    week_two_start=datetime.datetime(year=start.year,month=start.month+1,day=12)
    # 第三周开始结束
    week_three=datetime.datetime(year=start.year,month=start.month+1,day=20)
    week_three_start=datetime.datetime(year=start.year,month=start.month+1,day=20)

    #前十天
    one_therteen=datetime.datetime(year=start_time.year,month=start.month+1,day=8)
    two_therteen_start=datetime.datetime(year=start_time.year,month=start.month+1,day=8)
    #中间10天
    two_therteen=datetime.datetime(year=start_time.year,month=start.month+1,day=18)
    #后十天
    three_therteen_start=datetime.datetime(year=start_time.year,month=start.month+1,day=18)


    yangpin_count=[]
    for i in gongsi:
        yangpin_count_dic={}
        yangpin_count_list=[]
        for j in gongsi_dic[i]:
            bumen_dic = {}
            if i == '阜阳禾丰农牧科技有限公司':
                #判断阜阳禾丰有哪几个公司
    #           统计环境前15天有多少，后15天有多少个 义13号为15天 统计13号之前和之后的数据
                qian_15tian_zhu_yangpin=muzhuchang.filter(Q(公司=i)&Q(样本类型='猪源样本')&Q(部门=j)&Q(日期__range=(start_time,fivetheen_time))).count()
                qian_15tian_huanjin_yangpin=muzhuchang.filter(Q(公司=i)&Q(样本类型='环境样本')&Q(部门=j)&Q(日期__range=(start_time,fivetheen_time))).count()
                hou_15tian_zhu_yangpin=muzhuchang.filter(Q(公司=i)&Q(样本类型='猪源样本')&Q(部门=j)&Q(日期__gt=fivetheen_time)).count()
                hou_15tian_huanjin_yangpin=muzhuchang.filter(Q(公司=i)&Q(样本类型='环境样本')&Q(部门=j)&Q(日期__gt=fivetheen_time)).count()

                qian_15tian_zhu_yangpin={'28-13猪源样本':qian_15tian_zhu_yangpin}
                hou_15tian_zhu_yangpin={'14-27猪源样本':hou_15tian_zhu_yangpin}

                qian_15tian_huanjin_yangpin = {'28-13环境样本': qian_15tian_huanjin_yangpin}
                hou_15tian_huanjin_yangpin={'14-27环境样本':hou_15tian_huanjin_yangpin}

                yangpin_list =[qian_15tian_zhu_yangpin,qian_15tian_huanjin_yangpin,hou_15tian_zhu_yangpin,hou_15tian_huanjin_yangpin]
                bumen_dic[j]=yangpin_list
            elif i=='利辛荣丰农牧有限公司':
                one_therteen_zhu_yangpin=muzhuchang.filter(Q(公司=i)&Q(样本类型='猪源样本')&Q(部门=j)&Q(日期__range=(start_time,one_therteen))).count()
                two_therteen_zhu_yangpin=muzhuchang.filter(Q(公司=i)&Q(样本类型='猪源样本')&Q(部门=j)&Q(日期__range=(two_therteen_start,two_therteen))).count()
                three_therteen_zhu_yangpin=muzhuchang.filter(Q(公司=i)&Q(样本类型='猪源样本')&Q(部门=j)&Q(日期__gt=three_therteen_start)).count()

                one_therteen_huanjin_yangpin = muzhuchang.filter(
                    Q(公司=i) & Q(样本类型='环境样本') & Q(部门=j) & Q(日期__range=(start_time, one_therteen))).count()
                two_therteen_huanjing_yangpin = muzhuchang.filter(
                    Q(公司=i) & Q(样本类型='环境样本') & Q(部门=j) & Q(日期__range=(two_therteen_start, two_therteen))).count()
                three_therteen_huanjing_yangpin = muzhuchang.filter(
                    Q(公司=i) & Q(样本类型='环境样本') & Q(部门=j) & Q(日期__gt=three_therteen_start)).count()

                one_therteen_zhu_yangpin={'28-7猪源样本':one_therteen_zhu_yangpin}
                two_therteen_zhu_yangpin={'8-17猪源样本':two_therteen_zhu_yangpin}
                three_therteen_zhu_yangpin={'18-27猪源样本':three_therteen_zhu_yangpin}

                one_therteen_huanjin_yangpin={'28-7环境样本':one_therteen_huanjin_yangpin}
                two_therteen_huanjing_yangpin={'8-17环境样本':two_therteen_huanjing_yangpin}
                three_therteen_huanjing_yangpin={'18-27环境样本':three_therteen_huanjing_yangpin}



                yangpin_list =[one_therteen_zhu_yangpin,two_therteen_zhu_yangpin,three_therteen_zhu_yangpin,one_therteen_huanjin_yangpin,
                               two_therteen_huanjing_yangpin,three_therteen_huanjing_yangpin]
                bumen_dic[j] = yangpin_list

            else:
                qian_15tian_zhu_yangpin = muzhuchang.filter(
                    Q(公司=i) & Q(样本类型='猪源样本') & Q(部门=j) & Q(日期__range=(start_time,fivetheen_time))).count()

                hou_15tian_zhu_yangpin = muzhuchang.filter(
                    Q(公司=i) & Q(样本类型='猪源样本') & Q(部门=j) & Q(日期__gt=fivetheen_time)).count()
                #4周环境样品
                qian_one_week_huanjin_yangpin = muzhuchang.filter(
                    Q(公司=i) & Q(样本类型='环境样本') & Q(部门=j) & Q(日期__range=(start_time, week_one))).count()
                qian_two_week_huanjin_yangpin = muzhuchang.filter(
                    Q(公司=i) & Q(样本类型='环境样本') & Q(部门=j) & Q(日期__range=(week_one_start, week_two))).count()
                qian_three_week_huanjin_yangpin = muzhuchang.filter(
                    Q(公司=i) & Q(样本类型='环境样本') & Q(部门=j) & Q(日期__range=(week_two_start, week_three))).count()
                qian_four_week_huanjin_yangpin = muzhuchang.filter(
                    Q(公司=i) & Q(样本类型='环境样本') & Q(部门=j) & Q(日期__gt=week_three_start)).count()



                qian_15tian_zhu_yangpin = {'28-13猪源样本': qian_15tian_zhu_yangpin}

                hou_15tian_zhu_yangpin = {'14-27猪源样本': hou_15tian_zhu_yangpin}

                qian_one_week_huanjin_yangpin={'第一周环境样本':qian_one_week_huanjin_yangpin}
                qian_two_week_huanjin_yangpin={'第二周环境样本':qian_two_week_huanjin_yangpin}
                qian_three_week_huanjin_yangpin={'第三周环境样本':qian_three_week_huanjin_yangpin}
                qian_four_week_huanjin_yangpin={'第四周环境样本':qian_four_week_huanjin_yangpin}


                yangpin_list = [qian_15tian_zhu_yangpin, hou_15tian_zhu_yangpin,
                                qian_one_week_huanjin_yangpin,qian_two_week_huanjin_yangpin,
                                qian_three_week_huanjin_yangpin,qian_four_week_huanjin_yangpin]
                bumen_dic[j] = yangpin_list
            yangpin_count_list.append(bumen_dic)
        yangpin_count_dic[i]=yangpin_count_list
        yangpin_count.append(yangpin_count_dic)
    # print(yangpin_count)


    data = {}

    children5=[]
    dic_four = {}
    for i in yangpin_count:

        children4 = []

        for j in i.values():
            dic_three = {}
            children3=[]

            for z in j:

                children1 = []
                for m in z.values():
                    dic_two = {}
                    children = []
                    for n in m:
                        dic={}
                        dic['name']=list(n.keys())[0]
                        dic['value']=list(n.values())[0]
                        children.append(dic)


                    dic_two['name']=list(z.keys())[0]
                    dic_two['children']=children

                    children3.append(dic_two)
                # children3.append(children1)
            # print(children3)
            dic_three['name']=list(i.keys())[0]
            dic_three['children']=children3
            children4.append(dic_three)


        children5.append(children4)

    print(children5)
    dic_four['name']='公司'
    dic_four['children']=children5[0]+children5[1]+children5[2]+children5[3]



    data={
        'data':[dic_four],
        'rongfeng':children5[4]
    }
    return JsonResponse(data)



