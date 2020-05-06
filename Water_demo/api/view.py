import json
import socket
from datetime import timedelta

from django.contrib import auth
from django.utils import timezone
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_decode_handler

from api import models
from .form import SiteSerializer
from api.utils.jwt_auth import create_token


def get_name(request):
    """
    通过登录用户的token获取当前用户名
    :param request:
    :return: 用户名
    """
    if request.query_params.get("token"):
        # 通过get请求的方式获取token
        token = request.query_params.get('token')
    else:
        # 获取headers中的token
        token = request.META.get('HTTP_AUTHORIZATION')
    # token解析后的值
    toke_user = jwt_decode_handler(token)
    # 获得user_id
    user_id = toke_user["user_id"]
    # 通过user_id查询用户信息
    name = models.UserInfo.objects.get(id=user_id).username
    return name


class Water(APIView):
    """
    大屏页面展示
    """

    authentication_classes = []

    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        pass


from django.shortcuts import HttpResponse, redirect
from django import forms


class WaterForm(APIView):
    authentication_classes = []

    def get(self, request):
        queryset = models.Site.objects.all()
        serializer_class = SiteSerializer


class RegisterView(APIView):
    """
    注册
    """

    def post(self, request):
        username = request.data.get("name")
        password = request.data.get("pwd")
        # 查询用户名密码是否传入
        if username and password:
            # 查询数据库是否有相同的用户名
            user = models.UserInfo.objects.filter(username=username)
            if user:
                return Response({
                    "state": False,
                    "status": 0,
                    "msg": "用户名已注册"
                })
            # 用户未注册情况
            # 加密密码
            name = request.data.get("name")
            new_pwd = make_password(password)
            models.UserInfo.objects.create(username=name, password=new_pwd)
            return Response({
                "state": True,
                "status": 1,
                "msg": "注册成功"
            })

        return Response({
            "state": False,
            "status": 0,
            "msg": "name||pwd必填"
        })


class LoginView(APIView):
    """
    用户登录
    """
    authentication_classes = []

    def post(self, request):
        name = request.data.get('name')
        pwd = request.data.get('pwd')

        user_info = models.UserInfo.objects.filter(username=name)
        if user_info.exists():
            user = auth.authenticate(username=name, password=pwd)
            if not user:
                return Response({
                    "state": False,
                    "status": 0,
                    "msg": "账号或者密码错误"
                })
            # jwt生成token
            token = create_token({"user_id": user.id, "username": user.username})
            # 登录成功，记录登录日志
            lastLoginQuery = models.Log.objects.filter(username=name)
            if lastLoginQuery:
                lastLoginTimeList = []
                lastLoginIpList = []
                for i in lastLoginQuery:
                    lastLoginTime = i.nowLoginTime
                    lastLoginTimeList.append(lastLoginTime)
                    lastLoginIp = i.nowLoginIp
                    lastLoginIpList.append(lastLoginIp)
                create_time = timezone.now() + timedelta(hours=8)
                now_name = socket.getfqdn(socket.gethostname())
                now_ip = socket.gethostbyname(now_name)
                models.Log.objects.create(username=name,
                                          lastLoginTime=lastLoginTimeList[-1],
                                          lastLoginIp=lastLoginIpList[-1],
                                          nowLoginTime=create_time,
                                          nowLoginIp=now_ip)
            else:
                create_time = timezone.now() + timedelta(hours=8)
                now_name = socket.getfqdn(socket.gethostname())
                now_ip = socket.gethostbyname(now_name)
                models.Log.objects.create(username=name,
                                          lastLoginTime="1970-01-01 08:00",
                                          lastLoginIp="127.0.0.1",
                                          nowLoginTime=create_time,
                                          nowLoginIp=now_ip)
            return Response({
                "state": True,
                "status": 1,
                "msg": "登录成功",
                "_id": user.id,
                "token": token
            })
        else:
            return Response({
                "state": False,
                "status": 0,
                "msg": "没有该账户"
            })


class UsersView(APIView):
    """
    查找管理员列表
    """

    def get(self, request):
        name = request.GET.get("name")
        find_result = []
        user_obj = models.UserInfo.objects.filter(username=name)
        dic = {}
        for i in user_obj:
            dic["_id"] = i.id
            dic["name"] = i.username
            dic["phone"] = i.phone
            dic["email"] = i.email
            dic["nickname"] = i.nickname
            dic["des"] = i.des
        find_result.append(dic)
        return Response({
            "state": True,
            "status": 1,
            "findResult": find_result
        })


class UsersUpdateView(APIView):
    """
    更新管理员基本信息,不包括密码
    """

    def post(self, request):
        # 获取_id作为更新条件
        _id = request.data.get("_id")
        query = models.UserInfo.objects.filter(id=_id)
        if query.exists():
            name = request.data.get("name")
            phone = request.data.get("phone")
            email = request.data.get("email")
            nickname = request.data.get("nickname")
            des = request.data.get("des")
            if name: models.UserInfo.objects.filter(id=_id).update(username=name)
            if phone: models.UserInfo.objects.filter(id=_id).update(phone=phone)
            if email: models.UserInfo.objects.filter(id=_id).update(email=email)
            if nickname: models.UserInfo.objects.filter(id=_id).update(nickname=nickname)
            if des: models.UserInfo.objects.filter(id=_id).update(des=des)
            return Response({
                "state": True,
                "status": 1,
                "msg": "基本信息更新成功"
            })
        return Response(
            {
                "state": False,
                "status": "0",
                "msg": "没有该账户"
            }
        )


class UsersUppwd(APIView):
    """
    修改管理员账号密码
    """

    def post(self, request):
        # 查看用户名、密码、新密码是否传入
        id = request.data.get("_id")
        pwd = request.data.get("pwd")
        new_pwd = request.data.get("newpwd")
        if (id and pwd and new_pwd):
            # 获取请求用户
            query = models.UserInfo.objects.filter(id=id)
            for user in query:
                # 检查原始密码是否正确
                if user.check_password(pwd):
                    # 修改密码为新密码
                    user.set_password(new_pwd)
                    user.save()
                    return Response({
                        "state": True,
                        "status": 1,
                        "msg": "密码修改成功"
                    })
                return Response({
                    "state": False,
                    "status": 0,
                    "msg": "密码错误"
                })
            return Response({
                "state": False,
                "status": 0,
                "msg": "数据库查询失败"
            })
        return Response({
            "state": False,
            "status": 0,
            "msg": "新密码和旧密码必填"
        })


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
                last_login_time = i.lastLoginTime
                now_login_time = i.nowLoginTime
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
        # page = request.GET.get("page", 1)
        logs = models.Log.objects.all()
        # news = Paginator(logs, 10)
        # queryset = news.page(page)
        data = []
        for i in logs:
            name = i.username
            last_login_ip = i.lastLoginIp
            last_login_time = i.lastLoginTime
            now_login_time = i.nowLoginTime
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


class AddDev(APIView):
    """
    添加设备
    """

    def post(self, request):
        dev_name = request.data.get("devName")
        dev_num = request.data.get("devNum")
        dev_date = request.data.get("devDate")
        # 查看devName,devNum,devDate否传入
        if dev_name and dev_num and dev_date:
            if dev_num:
                # 先查询数据库是否有相同的设备编号
                dev_obj = models.Dev.objects.filter(devNum=dev_num)
                if dev_obj:
                    return Response({
                        "state": False,
                        "status": 0,
                        "msg": "设备已注册"
                    })
                else:
                    # 设备信息写入到数据库

                    now_time = timezone.now() + timedelta(hours=8)
                    request.data["cTime"] = now_time
                    models.Dev.objects.create(**request.data)
                    # 记录日志
                    dev_admin = get_name(request)
                    # dev_admin = request.data.get("devAdmin")
                    opa = "添加一个新设备:" + dev_num

                    try:
                        models.OperationLogs.objects.create(admin=dev_admin, opa=opa, cTime=now_time)
                        return Response({
                            "state": True,
                            "status": 1,
                            "logs": 1,
                            "msg": "设备添加成功,日志添加成功"
                        })
                    except Exception as e:
                        return Response({
                            "state": True,
                            "status": 1,
                            "logs": 0,
                            "msg": "设备添加成功,日志添加失败"
                        })
            return Response({
                "state": False,
                "status": 0,
                "msg": "查询失败"
            })
        return Response({
            "state": False,
            "status": 0,
            "msg": "devName||devDate||devNum必填"
        })


class UpdateDev(APIView):
    """
    修改设备基本信息（devName,devNum,devDate不可更改） 通过devNum进行查找修改
    """

    def post(self, request):
        dev_num = request.data.get("devNum")
        queryset = models.Dev.objects.filter(devNum=dev_num)
        for i in queryset:
            dev_sim = i.devSIM
            dev_use = str(i.devUse)
            dev_location = i.devLocation
            print(dev_location)
            dev_admin = i.devAdmin
            if request.data.get("devSIM") == dev_sim and \
                    request.data.get("devUse") == dev_use and \
                    request.data.get("devLocation") == dev_location and \
                    request.data.get("devAdmin") == dev_admin:
                return Response({
                    "state": False,
                    "status": 0,
                    "msg": "设备信息一致,更新失败"
                })
            # 更新信息到数据库
            print(request.data)
            models.Dev.objects.filter(devNum=dev_num).update(**request.data)
            # 添加日志到数据库
            l_admin = get_name(request)
            opa = "修改了设备信息:" + json.dumps(request.data)
            ctime = timezone.now() + timedelta(hours=8)
            models.OperationLogs.objects.create(admin=l_admin, opa=opa, cTime=ctime)
            return Response({
                "state": True,
                "status": 1,
                "logs": 1,
                "msg": "设备信息更新成功,日志添加成功"
            })
        return Response({
            "state": False,
            "status": 0,
            "msg": "查询失败"
        })


class DevFind(APIView):
    """
    查询设备信息
    """

    def post(self, request):
        receive_data = request.data
        # 获得了post请求传过来的数据，字典形式{'devName': '2112', 'devNum': '123456'}
        if receive_data:
            dev_num = receive_data.get("devNum")
            if dev_num:
                page = request.GET.get("page", 1)
                dev_obj = models.Dev.objects.filter(devNum=dev_num)
                news = Paginator(dev_obj, 5)
                queryset = news.page(page)
                if queryset:
                    find_result = []
                    res = {}
                    for i in queryset:
                        s1 = i.devLocation.replace("'", '"')
                        dev_location = [float(item) for item in json.loads(s1)]
                        res["devLocation"] = dev_location
                        res["_id"] = i.id
                        res["devName"] = i.devName
                        res["devNum"] = i.devNum
                        res["devDate"] = i.devDate
                        res["devSIM"] = i.devSIM
                        res["devUse"] = i.devUse
                        res["devAdmin"] = i.devAdmin
                        res["cTime"] = i.cTime
                        res["__v"] = 0
                    find_result.append(res)
                    return Response({
                        "state": True,
                        "status": 1,
                        "findResult": find_result
                    })
                return Response({
                    "state": True,
                    "status": 1,
                    "findResult": []
                })
            return Response({
                "state": False,
                "status": 0,
                "msg": "查询失败"
            })
        else:
            query = models.Dev.objects.all()
            find_result = []

            for i in query:
                res = {}
                s1 = i.devLocation.replace("'", '"')
                dev_location = [float(item) for item in json.loads(s1)]
                res["devLocation"] = dev_location
                res["_id"] = i.id
                res["devName"] = i.devName
                res["devNum"] = i.devNum
                res["devDate"] = i.devDate
                res["devSIM"] = i.devSIM
                res["devUse"] = i.devUse
                res["devAdmin"] = i.devAdmin
                res["cTime"] = i.cTime
                res["__v"] = 0

                find_result.append(res)
            return Response({
                "state": True,
                "status": 1,
                "findResult": find_result
            })


class DevFindAll(APIView):
    """
    查询所有设备信息
    """

    def post(self, request):
        query = models.Dev.objects.all()
        page = request.data.get("page", 1)
        count = Paginator(query, 5)
        queryset = count.page(page)
        find_result = []

        for i in queryset:
            res = {}
            s1 = i.devLocation.replace("'", '"')
            dev_location = [float(item) for item in json.loads(s1)]
            res["devLocation"] = dev_location
            res["_id"] = i.id
            res["devName"] = i.devName
            res["devNum"] = i.devNum
            res["devDate"] = i.devDate
            res["devSIM"] = i.devSIM
            res["devUse"] = i.devUse
            res["devAdmin"] = i.devAdmin
            res["cTime"] = i.cTime
            res["__v"] = 0

            find_result.append(res)
        return Response({
            "state": True,
            "status": 1,
            "findResult": find_result
        })


class DeleteDev(APIView):
    """
    删除设备
    """

    def post(self, request):
        dev_num = request.data.get("devNum")
        if dev_num:
            dev_obj = models.Dev.objects.filter(devNum=dev_num)

            if dev_obj:
                # 数据库中删除该条数据
                dev_obj.delete()
                # 记录日志到数据库
                admin = get_name(request)
                opa = "删除设备:" + dev_num
                c_time = timezone.now() + timedelta(hours=8)
                models.OperationLogs.objects.create(admin=admin, opa=opa, cTime=c_time)
                return Response({
                    "state": True,
                    "status": 1,
                    "logs": 1,
                    "msg": "设备删除成功,日志添加成功"
                })
            return Response({
                "state": False,
                "status": 0,
                "msg": "查询失败"
            })
        return Response({
            "state": False,
            "status": 0,
            "msg": "设备编号必传"
        })


class AdminLogs(APIView):
    """
    查看操作日志
    """

    def get(self, request):
        name = request.GET.get("name")
        if name:
            query = models.OperationLogs.objects.filter(admin=name)
            page = request.data.get("page", 1)
            count = Paginator(query, 10)
            queryset = count.page(page)
            data = []
            for i in queryset:
                res = {}
                res["_id"] = i.id
                res["admin"] = i.admin
                res["opa"] = i.opa
                res["cTime"] = i.cTime
                res["__v"] = 0
                data.append(res)
            return Response({
                "status": 1,
                "state": True,
                "msg": "success",
                "data": data
            })
        query = models.OperationLogs.objects.all()
        page = request.data.get("page", 1)
        count = Paginator(query, 10)
        queryset = count.page(page)
        data = []
        for i in queryset:
            res = {}
            res["_id"] = i.id
            res["admin"] = i.admin
            res["opa"] = i.opa
            res["cTime"] = i.cTime
            res["__v"] = 0
            data.append(res)
        return Response({
            "status": 1,
            "state": True,
            "msg": "success",
            "data": data
        })

    # def post(self, request):
    #     pass


class AdminLogsAll(APIView):
    """
    查看全部操作日志
    """

    def post(self, request):
        query = models.OperationLogs.objects.all()
        page = request.data.get("page", 1)
        count = Paginator(query, 10)
        queryset = count.page(page)
        data = []
        for i in queryset:
            res = {}
            res["_id"] = i.id
            res["admin"] = i.admin
            res["opa"] = i.opa
            res["cTime"] = i.cTime
            res["__v"] = 0
            data.append(res)
        return Response({
            "status": 1,
            "state": True,
            "msg": "全部操作日志获取成功",
            "data": data
        })


class ShareAdd(APIView):
    """
    添加信息
    """

    def post(self, request):
        content = request.data.get("contents")
        name = get_name(request)
        if content:
            c_time = timezone.now() + timedelta(hours=8)
            last_id = models.InfoShares.objects.order_by("-id")[0].id
            models.InfoShares.objects.filter(id=last_id).update(shareName=name, contents=content, cTime=c_time)
            return Response({
                "state": True,
                "status": 1,
                "msg": "内容添加成功"
            })
        return Response({
            "state": False,
            "status": 0,
            "msg": "请传入发布的内容"
        })


class ShareUpload(APIView):
    """
    上传文件接口
    """

    def post(self, request):
        file_obj = request.FILES.get('file')
        models.InfoShares.objects.create(imgSrc=file_obj)
        return Response({
            "status": 0,
            "path": "/media/img" + file_obj.name
        })


class ShareContentPage(APIView):
    """
    查询分享内容
    """

    def post(self, request):
        share_name = request.data.get("shareName")
        if share_name:
            data = []
            query = models.InfoShares.objects.filter(shareName=share_name)
            page = request.data.get("page", 1)
            news = Paginator(query, 5)
            queryset = news.page(page)
            for i in queryset:
                res = {}
                res["_id"] = i.id
                res["shareName"] = i.shareName
                res["contents"] = i.contents
                res["cTime"] = "" if i.cTime is None else i.cTime
                res["imgSrc"] = "" if i.imgSrc is None else str(i.imgSrc)
                res["__v"] = 0
                data.append(res)
            return Response({
                "status": 1,
                "state": True,
                "msg": "查询成功",
                "data": data
            })
        data = []
        query = models.InfoShares.objects.all()
        for i in query:
            res = {}
            res["_id"] = i.id
            res["shareName"] = i.shareName
            res["contents"] = i.contents
            res["cTime"] = "" if i.cTime is None else i.cTime
            res["imgSrc"] = "" if i.imgSrc is None else str(i.imgSrc)
            res["__v"] = 0
            data.append(res)
        return Response({
            "status": 1,
            "state": True,
            "msg": "查询成功",
            "data": data
        })


class ShareContentAll(APIView):
    """
    查看全部内容
    """

    def post(self, request):
        share_name = request.data.get("name")
        if share_name:
            data = []
            query = models.InfoShares.objects.filter(shareName=share_name)
            for i in query:
                res = {}
                res["_id"] = i.id
                res["shareName"] = i.shareName
                res["contents"] = i.contents
                res["cTime"] = "" if i.cTime is None else i.cTime
                res["imgSrc"] = "" if i.imgSrc is None else str(i.imgSrc)
                res["__v"] = 0
                data.append(res)
            return Response({
                "status": 1,
                "state": True,
                "msg": "查询成功",
                "data": data
            })
        data = []
        query = models.InfoShares.objects.all()
        for i in query:
            res = {}
            res["_id"] = i.id
            res["shareName"] = i.shareName
            res["contents"] = i.contents
            res["cTime"] = "" if i.cTime is None else i.cTime
            res["imgSrc"] = "" if i.imgSrc is None else str(i.imgSrc)
            res["__v"] = 0
            data.append(res)
        return Response({
            "status": 1,
            "state": True,
            "msg": "查询成功",
            "data": data
        })


class Test(APIView):
    """
    测试接口
    """

    def get(self, request):
        # 获取请求参数token的值
        token = request.GET.get("token")
        token1 = request.META.get('HTTP_AUTHORIZATION')
        # token解析后的值
        toke_user = jwt_decode_handler(token1)
        # 获得user_id
        user_id = toke_user["user_id"]
        # 通过user_id查询用户信息
        name = models.UserInfo.objects.get(id=user_id).username
        print(name, type(name))
        """
        # 更改下密码
        u = models.UserInfo.objects.get(username="wubiao")
        u.set_password("123456")
        u.save()
        """
        return Response({
            "state": True,
            "status": 1
        })


class Aliyun(APIView):
    """
    water信息展示
    """

    def get(self, request):
        res = models.Water.objects.values()

        return Response(res)
