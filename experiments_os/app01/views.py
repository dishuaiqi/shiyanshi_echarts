from django.shortcuts import render
import datetime
from django import forms
from app01 import models
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
from django_pandas.io import read_frame
import pandas as pd
import numpy as np
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
    print(request.POST)
    form=pcrModleform(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status':True})

def echart_sample(request):
    PCRcount=models.BingYuan.objects.all().count()

    kangti_count=models.kangti.objects.all().count()
    start = datetime.datetime(year=2022, month=8, day=28)
    last_month_pcrcount=models.BingYuan.objects.filter(日期__gt=start).count()

    last_month_positive_count=models.BingYuan.objects.filter(Q(日期__gt=start) & Q(结果='+')).count()

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
def echart_bar(request):

    start = datetime.datetime.now()
    #本月查询
    table_list = models.BingYuan.objects.filter(Q(日期__month=start.month-1)&Q(日期__year=start.year))
    #转为pandas
    df = read_frame(qs=table_list)

    #不同公司的操作
    gongsi_count = df['公司'].value_counts()
    gongsi_list = gongsi_count.to_dict()
    # print(gongsi_count)
    gongsi_name = list(gongsi_list.keys())
    gongsi_data = []
    for key, value in gongsi_list.items():
        gongsi_data.append({'value': value, 'name': key})

     #前5的部门操作
    bumen_count=df['部门'].value_counts()
    bumen_list=bumen_count.to_dict()
    bumen_name=list(bumen_list.keys())
    bumen_name_count=list(bumen_list.values())

    #不同样品操作
    yangpin_type=df['样本类型'].value_counts()

    yangpin_type_list=yangpin_type.to_dict()

    yangpin_type_name=list(yangpin_type_list.keys())

    yangpin_type_data=[]
    for key, value in yangpin_type_list.items():
        yangpin_type_data.append({'value': value, 'name': key})
    # print(yangpin_type_data)

    #不同检测类型操作
    jiance_type=df['检测类型'].value_counts()

    jiance_type_list=jiance_type.to_dict()

    jiance_type_name=list(jiance_type_list.keys())

    jiance_type_data=[]
    for key, value in jiance_type_list.items():
        jiance_type_data.append({'value': value, 'name': key})

    #阳性数量操作
    positive_type_count={}
    negative_type_count={}
    for i in jiance_type_name:
        positive_count = models.BingYuan.objects.filter(Q(日期__month=start.month - 1) & Q(日期__year=start.year)&Q(检测类型=i)&Q(结果='+')).count()

        positive_type_count[i]=positive_count

        negative_count = models.BingYuan.objects.filter(Q(日期__month=start.month - 1) & Q(日期__year=start.year)&Q(检测类型=i)&Q(结果='-')).count()

        negative_type_count[i] = negative_count

    positive_count_list=[-x for x in list(positive_type_count.values())]

    negative_count_list=list(negative_type_count.values())

    # 阳性场区
    positive_month=models.BingYuan.objects.filter(Q(日期__month=start.month-1)&Q(日期__year=start.year)&Q(结果='+'))

    positive_month=read_frame(qs=positive_month)

    positive_changqu=positive_month['部门'].value_counts().to_dict()
    positive_changqu=list(positive_changqu.keys())

    positive_jiance_type=positive_month['检测类型'].value_counts().to_dict()
    positive_jiance_type=list(positive_jiance_type.keys())

    positive_changqu_dic={}
    for i in positive_changqu:
        positive_changqu_dic_type={}
        for j in positive_jiance_type:
            count=models.BingYuan.objects.filter(Q(日期__month=start.month - 1) & Q(日期__year=start.year) & Q(结果='+')&Q(检测类型=j)&Q(部门=i)).count()
            positive_changqu_dic_type[j]=count
        positive_changqu_dic[i]=positive_changqu_dic_type

    print(positive_changqu_dic)

    positive_changqu_list=positive_changqu_dic.values()

    positive_changqu_type_count=[]
    for i in positive_changqu_list:
        positive_changqu_type_count.append(list(i.values()))
    print(positive_changqu_type_count)

    positive_type_changqu_list=[['检测类型']+list(positive_jiance_type)]
    for i in range(len(list(positive_changqu))):
        positive_type_changqu_list.append([positive_changqu[i]]+positive_changqu_type_count[i])  #这是把阳性的场区和类型加上

    print(positive_type_changqu_list)


    #检测数量操作
    now_time=datetime.datetime.now()

    jiance_count_month={}
    for i in range(1,13):
        start_month=datetime.datetime(year=now_time.year,month=i,day=1)
        month_jiance=models.BingYuan.objects.filter(Q(日期__month=start_month.month)&Q(日期__year=start_month.year))
        df_month = read_frame(qs=month_jiance)
        gongsi_count_month = df_month['公司'].value_counts()
        gongsi_list_month = gongsi_count_month.to_dict()
        # print(gongsi_list_month)
        gongsi_name_month = list(gongsi_list_month.keys())
        jiance_count_month[str(i)+'月']=gongsi_list_month

    jiance_count_month_pd=pd.DataFrame(jiance_count_month)

    for i in jiance_count_month_pd.columns:
        if jiance_count_month_pd[i].count()==0:
            jiance_count_month_pd.drop(labels=i,axis=1,inplace=True)

    # print(jiance_count_month_pd)
    #行列转换
    jiance_count_month_pd=pd.DataFrame(jiance_count_month_pd.values.T,index=jiance_count_month_pd.columns,columns=jiance_count_month_pd.index)
    # print(jiance_count_month_pd)
    jiance_count_month_pd=jiance_count_month_pd.fillna(0)
    one_list=['月份']
    for i in jiance_count_month_pd.index:
        one_list.append(i)

    #怎么样把需要的数据添加上
    all_columns={}
    for j in jiance_count_month_pd.columns:
        all_columns[j]=[j]+list(jiance_count_month_pd[j])

    # print(all_columns)
    #前5的检测数量场区




    #图表内容数据
    series_bar=[
        {
            "name": 'Funnel',
            "type": 'funnel',
            "left": '20%',
            "top": 60,
            "bottom":60,
            "width": '80%',
            "min": 0,
            "max": 500,
            "minSize": '0%',
            "maxSize":'100%',
            "sort":'ascending',
            "gap":2,
            "label": {
                "show": "true",
                "position": 'inside'
            },
            "labelLine": {
                "length": 10,
                "lineStyle": {
                    "width": 1,
                    'type':'solid'
                }
            },
            "itemStyle": {
               "borderColor": '#fff',
                "borderWidth": 1
            },
            "emphasis": {
                "label": {
                    'fontSize': 20
                }
            },
            'data': gongsi_data
        }
    ]
    series_yangpinType = [
        {
              'name': '样品数量',
              'type': 'pie',
              'radius': ['40%', '70%'],
              'center':['45%','50%'],
              'avoidLabelOverlap': 'true',
              'label': {
                'formatter': '{d}%',
                 'position':'inner',
                  'color':'#fff',
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
            'data':yangpin_type_data

        }
    ]

    jiance_type_radiusAxis= {
       'type': 'category',
       'data': jiance_type_name,
        'axisLabel':{
            'textStyle':{
                'color':'#7edae8',
                'fontSize': 10,
            }
        }
    }
    jiance_type_series={
        'type': 'bar',
        'data': jiance_type_data,
        'label': {
            'show': 'true',
           ' position': 'left',
         },



    }

    jiance_count=[one_list]

    for i in all_columns.values():
        jiance_count.append(i)
    # print(jiance_count)
    #上月不同类型检测数量
    positive_jiance_type={
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






    data = {
        'legend': gongsi_name,
        'series': series_bar,
        'series_yangpinType':series_yangpinType,
        'jiance_type_radiusAxis':jiance_type_radiusAxis,
        'jiance_type_series':jiance_type_series,
        'jiance_count_source':jiance_count,
        'positive_jiance_type':positive_jiance_type,
        'positive_type_changqu_list':positive_type_changqu_list,
        'bumen_name':bumen_name[:5],
        'bumen_name_count':bumen_name_count[:5]

    }








    return JsonResponse(data)

