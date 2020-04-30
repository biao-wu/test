# from __future__ import unicode_literals
from django.db import models

from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserInfo(AbstractUser):
    """
    用户
    """
    phone = models.CharField(max_length=11, verbose_name="电话")
    nickname = models.CharField(max_length=32, null=True, blank=True, verbose_name="昵称")
    des = models.CharField(max_length=300, null=True, blank=True, verbose_name="个性签名")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Dev(models.Model):
    """
    设备
    """
    devName = models.CharField(max_length=32, verbose_name="设备名称")
    devNum = models.CharField(max_length=32, verbose_name="设备编号")
    devDate = models.DateTimeField(max_length=32, verbose_name="设备日期")
    devSIM = models.CharField(max_length=100, verbose_name="SIM卡号")
    devUse = models.BooleanField(verbose_name="是否正在使用")
    devLocation = models.CharField(max_length=100, verbose_name="位置")
    devAdmin = models.CharField(max_length=32, null=True, blank=True, verbose_name="维护人员")
    cTime = models.DateTimeField(max_length=100, null=True, blank=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "设备"
        verbose_name_plural = verbose_name
        ordering = ["devNum"]

    def __str__(self):
        return self.devName


class Log(models.Model):
    """
    日志
    """
    username = models.CharField(max_length=32, blank=True, null=True, verbose_name="用户名")
    lastLoginTime = models.DateTimeField(max_length=100, blank=True, null=True, verbose_name="上次登录时间")
    lastLoginIp = models.CharField(max_length=32, blank=True, null=True, verbose_name="上次登录IP")
    nowLoginTime = models.DateTimeField(max_length=100, blank=True, null=True, verbose_name="本次登录时间")
    nowLoginIp = models.CharField(max_length=32, blank=True, null=True, verbose_name="本次登录IP")

    class Meta:
        verbose_name = "日志"
        verbose_name_plural = verbose_name
        ordering = ["username"]

    def __str__(self):
        return self.username


class OperationLogs(models.Model):
    """
    管理员操作日志
    """
    admin = models.CharField(max_length=64, verbose_name="管理员")
    opa = models.CharField(max_length=100, null=True, verbose_name="操作记录")
    cTime = models.DateTimeField(max_length=100, blank=True, null=True, verbose_name="操作时间")

    class Meta:
        verbose_name = "操作日志"
        verbose_name_plural = verbose_name
        ordering = ["admin"]

    def __str__(self):
        return self.admin


class InfoShares(models.Model):
    """
    信息分享
    """
    shareName = models.CharField(max_length=32, verbose_name="发布人员")
    contents = models.CharField(max_length=200, verbose_name="内容")
    cTime = models.DateTimeField(max_length=100, null=True, blank=True, verbose_name="创建时间")
    imgSrc = models.ImageField(upload_to='img', null=True, blank=True)

    class Meta:
        verbose_name = "信息分享"
        verbose_name_plural = verbose_name
        ordering = ["shareName"]

    def __str__(self):
        return self.shareName


"""
大屏的model分析

- 饮水水质监测模块
站点（site）
站点总数  int
正常站点数  int
离线站点数  int
异常站点数  int

地图中的信息
余氯警戒点  int
PH警戒点  int
浊度警戒点  int
上报时间  datetime

- 对比数据分析模块
余氯实时数据监控（A、B站点折线图）
PH数据对比（A、B站点折线图）
余氯实时数据监控（A、B站点折线图）

- 视频监控
小区。。。

- 站点水质质量分析
选择月份
表格展示
数轴（站点名称）
横轴（余氯（mg/L）合格率、PH合格率、浊度（NTU）合格率、质量分析）


"""


# class Site(models.Model):
#     """
#     站点数据统计
#     """
#     siteAll = models.CharField(max_length=32, verbose_name="站点总数")
#     siteON = models.CharField(max_length=32, verbose_name="正常站点数")
#     siteOFF = models.CharField(max_length=32, verbose_name="离线站点数")
#     siteExcept = models.CharField(max_length=32, verbose_name="异常站点数")
#
#     class Meta:
#         verbose_name = "站点数据统计"
#         verbose_name_plural = verbose_name
#
#
# class Water(models.Model):
#     """
#     水质信息
#     """
#     # chlorine = models.CharField(max_length=32, verbose_name="余氯")
#     pH = models.CharField(max_length=32, verbose_name="PH")
#     NTU = models.CharField(max_length=32, verbose_name="浑浊度")
#     oxygen = models.CharField(max_length=32, verbose_name="溶解氧")
#     tem = models.CharField(max_length=32, verbose_name="水温")
#     ele = models.CharField(max_length=32, verbose_name="电导率")
#     time = models.DateTimeField(max_length=64, null=True, blank=True, verbose_name="上报日期")
#
#     class Meta:
#         verbose_name = "水质信息"
#         verbose_name_plural = verbose_name


class WaterSite(models.Model):
    """
    站点信息
    """
    site_status = (
        (1, "正常"),
        (2, "异常"),
        (0, "离线")
    )

    siteName = models.CharField(max_length=32, verbose_name="站点名称")
    PH = models.CharField(max_length=32, verbose_name="PH")
    NTU = models.CharField(max_length=32, verbose_name="浑浊度")
    oxygen = models.CharField(max_length=32, verbose_name="溶解氧")
    tem = models.CharField(max_length=32, verbose_name="水温")
    ele = models.CharField(max_length=32, verbose_name="电导率")
    chlorine = models.CharField(max_length=32, verbose_name="余氯")
    site = models.IntegerField(choices=site_status, verbose_name="站点状态")
    cTime = models.DateTimeField(max_length=100, blank=True, null=True, verbose_name="上报日期")

    class Meta:
        verbose_name = "水质站点信息"
        verbose_name_plural = verbose_name
