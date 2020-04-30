from django import forms
from rest_framework import serializers

from api import models


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        # model = models.Site
        fields = (
            "siteAll",
            "siteON",
            "siteOFF",
            "siteExcept",
        )


class SiteForm(forms.ModelForm):
    class Meta:
        model = models.WaterSite
        fields = "__all__"
        labels = {
            "siteAll": "站点总数",
            "siteON": "正常站点数",
            "siteOFF": "离线站点数",
            "siteExcept": "异常站点数",
        }
