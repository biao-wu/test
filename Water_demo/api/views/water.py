import pymysql
from datetime import timedelta

from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

from api import models
from api.form import SiteForm


class Water(APIView):
    """
    大屏页面展示
    """

    authentication_classes = []

    def get(self, request):
        return render(request, "index.html")


def water_form(request):
    if request.method == "GET":
        form_obj = SiteForm()

        return render(request, 'water_f.html', {"form_obj": form_obj})

    else:
        data = request.POST
        form_obj = SiteForm(data)
        if form_obj.is_valid():
            data = form_obj.cleaned_data
            # 将表单数据写入数据库
            site_name = data.get("siteName")
            obj = models.Site.objects.update_or_create(siteName=site_name)

            site_id = obj[0].id
            create_time = timezone.now() + timedelta(hours=8)
            data.pop('siteName')
            data["time"] = create_time
            data["site_id"] = site_id
            # 写入数据库
            # models.WaterData.objects.create(**data)
            site_num = models.Site.objects.distinct().count()
            site_num = str(site_num)
            site_all_1 = 0 if len(site_num) == 1 else site_num[0]
            site_all_2 = site_num[0] if len(site_num) == 1 else site_num[1]
            # 正常站点数
            on_obj = models.WaterData.objects.filter(status=1)
            on_id_list = []
            for i in on_obj:
                on_id_list.append(i.site_id)
            site_on = len(set(on_id_list))
            # 离线站点数
            off_obj = models.WaterData.objects.filter(status=0)
            off_id_list = []
            for i in off_obj:
                off_id_list.append(i.site_id)
            site_off = len(set(off_id_list))
            # 异常站点数
            exp_obj = models.WaterData.objects.filter(status=2)
            exp_id_list = []
            for i in exp_obj:
                exp_id_list.append(i.site_id)
            site_exp = len(set(exp_id_list))
            # 站点信息
            site_obj = models.Site.objects.all()
            water_obj = models.WaterData.objects.all()
            return render(request, 'index.html',
                          {"siteAllONE": site_all_1, "siteAllTWO": site_all_2, "siteON": site_on, "siteOFF": site_off,
                           "siteExcept": site_exp, "site_obj": site_obj, "water_obj": water_obj})
        else:
            return render(request, 'water_f.html', {'form_obj': form_obj})


def echarts_data(request):
    db = pymysql.connect(host='localhost', user='root', password='root', database='water_demo')
    cur = db.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute('select chlorine,time,pH,NTU from api_waterdata where site_id = 1')
    ret = cur.fetchall()
    name_list = []
    site_name_1 = models.Site.objects.get(id=1)
    name_list.append(site_name_1.siteName)
    hours_1 = []
    chlorines_1 = []
    ph_list_1 = []
    ntu_list_one = []
    for i in ret:
        hours_1.append(i.get("time").strftime('%H:%M'))
        chlorines_1.append(i.get("chlorine"))
        ph_list_1.append(i.get("pH"))
        ntu_list_one.append(i.get("NTU"))
    cur.execute('select chlorine,time,pH,NTU from api_waterdata where site_id = 2')
    ret1 = cur.fetchall()
    site_name_2 = models.Site.objects.get(id=2)
    name_list.append(site_name_2.siteName)
    hours_2 = []
    chlorines_2 = []
    ph_list_2 = []
    ntu_list_two = []
    for i in ret1:
        hours_2.append(i.get("time").strftime('%H:%M'))
        chlorines_2.append(i.get("chlorine"))
        ph_list_2.append(i.get("pH"))
        ntu_list_two.append(i.get("NTU"))
    json_data = {
        "name": name_list,
        "key": hours_1,
        "value_c1": chlorines_1,
        "value_c2": chlorines_2,
        "val_ph1": ph_list_1,
        "val_ph2": ph_list_2,
        "val_ntu1": ntu_list_one,
        "val_ntu2": ntu_list_two,
    }

    return JsonResponse(json_data)


# 折线图
class Aliyun(APIView):
    """
    water信息展示
    """

    def get(self, request):
        res = models.WaterData.objects.values('pH', 'NTU', 'oxygen', 'tem', 'ele', 'time').filter(site=1)

        return Response(res)


def water_test(request):
    if request.method == "GET":
        return render(request, "test.html")
