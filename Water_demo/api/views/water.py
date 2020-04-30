from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

from api import models
from api.serializers import SiteForm


class Water(APIView):
    """
    大屏页面展示
    """

    authentication_classes = []

    def get(self, request):
        return render(request, "index.html")


# class WaterForm(APIView):
#     authentication_classes = []
#
#     queryset = models.Site.objects.all()
#
#     def get(self, request):
#         queryset = models.Site.objects.all()
#         form = SiteForm(instance=queryset)
#         return render(request, 'water_f.html', {'form': form})


def water_form(request):
    if request.method == "GET":
        form_obj = SiteForm()

        return render(request, 'water_f.html', {"form_obj": form_obj})

    else:
        data = request.POST
        form_obj = SiteForm(data)
        if form_obj.is_valid():
            data = form_obj.cleaned_data
            print(data)
            create_time = timezone.now() + timedelta(hours=8)
            site_all = data.get("siteAll")
            site_all_1 = site_all[0]
            site_all_2 = site_all[1]
            site_on = data.get("siteON")
            site_off = data.get("siteOFF")
            site_exp = data.get("siteExcept")
            # models.Site.objects.create(**data)
            return render(request, 'index.html',
                          {"siteAllONE": site_all_1, "siteAllTWO": site_all_2, "siteON": site_on, "siteOFF": site_off,
                           "siteExcept": site_exp})
        else:
            return render(request, 'water_f.html', {'form_obj': form_obj})


# 折线图
class Aliyun(APIView):
    """
    water信息展示
    """

    def get(self, request):
        print(1111111)

        res = models.WaterSite.objects.values().first()
        print(res.get("cTime"),type(res.get("cTime")))

        return Response(res)


def water_test(request):
    if request.method == "GET":
        return render(request, "test.html")
