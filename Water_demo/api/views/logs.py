from django.core.paginator import Paginator

from rest_framework.views import APIView
from rest_framework.response import Response

from api import models


class GetLogs(APIView):
    """
    获取单个管理员登录日志
    """

    def get(self, request):
        name = request.GET.get("name")
        page = request.GET.get("page", 1)
        log_query = models.Log.objects.filter(username=name)
        news = Paginator(log_query, 10)
        queryset = news.page(page)
        # 判断该用户之前是否有日志记录
        if queryset:
            data = []
            for i in queryset:
                last_login_ip = i.lastLoginIp
                last_login_time = i.lastLoginTime.strftime("%Y/%m/%d %H:%M:%S")
                now_login_time = i.nowLoginTime.strftime("%Y/%m/%d %H:%M:%S")
                now_login_ip = i.nowLoginIp
                # 通过UserInfo表查询id构建对应的数据结构
                user = models.UserInfo.objects.filter(username=name)
                for j in user:
                    id = j.id
                    ret = {}
                    last_login = {}
                    now_login = {}
                    last_login["loginTime"] = last_login_time
                    last_login["ip"] = last_login_ip
                    now_login["loginTime"] = now_login_time
                    now_login["ip"] = now_login_ip
                    ret["_id"] = id
                    ret["username"] = name
                    ret["lastLogin"] = last_login
                    ret["nowLogin"] = now_login
                    data.append(ret)
            return Response({
                "status": 200,
                "state": True,
                "msg": "success",
                "data": data,
                "__v": 0
            })

        return Response({
            "status": 0,
            "state": False,
            "msg": "false",
        })


class GetLogsAll(APIView):
    """
    获取所有登录日志
    """

    def get(self, request):
        page = request.GET.get("page", 1)
        logs = models.Log.objects.all()
        news = Paginator(logs, 10)
        queryset = news.page(page)
        data = []
        for i in queryset:
            name = i.username
            last_login_ip = i.lastLoginIp
            last_login_time = i.lastLoginTime.strftime("%Y/%m/%d %H:%M:%S")
            now_login_time = i.nowLoginTime.strftime("%Y/%m/%d %H:%M:%S")
            now_login_ip = i.nowLoginIp
            user = models.UserInfo.objects.filter(username=name)
            for j in user:
                id = j.id
                ret = {}
                last_login = {}
                now_login = {}
                last_login["loginTime"] = last_login_time
                last_login["ip"] = last_login_ip
                now_login["loginTime"] = now_login_time
                now_login["ip"] = now_login_ip
                ret["_id"] = id
                ret["username"] = name
                ret["lastLogin"] = last_login
                ret["nowLogin"] = now_login
                data.append(ret)
        return Response(
            {
                "status": 200,
                "state": True,
                "msg": "success",
                "data": data,
                "__v": 0
            }
        )
