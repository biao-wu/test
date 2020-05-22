"""
import socket
#获取本机电脑名
myname = socket.getfqdn(socket.gethostname(  ))
#获取本机ip
myaddr = socket.gethostbyname(myname)
print(myname)
print(myaddr)
"""

# li = [1,2,3,4]
# for i in li:
#     print(i)
# print(li[-1])
# import calendar
# import datetime
#
# import iso8601
#
# date_str = "2020-04-22 10:44:32.000000"
#
# d = iso8601.parse_date(date_str)
#
# print(d)
#
# datetime.datetime(2010, 10, 30, 17, 21, 12, tzinfo=None)
# datetime.datetime.fromtimestamp(calendar.timegm(d.timetuple()))
#
# print(d)

# from datetime import datetime
#
# now = datetime.now()
# print(now.strftime("%Y/%m/%d %H:%M:%S"))

import json
import re

# s1 = "['1230000', ' 4560000']"
# l1 = [1230000, 4560000]

# s2 = str(s1.split(","))
# print(s2)
#
# num = re.sub(r'\D', "", s1)
# print(num)

# s1 = s1.replace("'",'"')
#
# print([int(item) for item in json.loads(s1)])
# print(print([int(item.strip()) for item in json.loads(s1)]))


'''

var option = {
        grid: {
            top: 20,
            bottom: 30,
            right: 20
            // left: '10%'
        },
        xAxis: {
            type: "category",
            data: ["8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00"]
        },
        yAxis: {
            type: "value"
        },
        series: [
            {
                data: [400, 600, 300, 400, 900, 1330, 800],
                type: "line",
                showSymbol: false,
                smooth: true,
                lineStyle: {
                    color: "rgb(220, 205, 43)"
                },
                areaStyle: {
                    color: {
                        type: "linear",
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [
                            {
                                offset: 0,
                                color: "rgb(220, 205, 43,0.7)" // 0% 处的颜色
                            },
                            {
                                offset: 1,
                                color: "rgba(255, 255, 255,0)" // 100% 处的颜色
                            }
                        ]
                    }
                }
            },
            {
                data: [200, 300, 560, 170, 1200, 800, 320],
                type: "line",
                showSymbol: false,
                smooth: true,
                lineStyle: {
                    color: "rgb(151, 218, 245)"
                },
                areaStyle: {
                    color: {
                        type: "linear",
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [
                            {
                                offset: 0,
                                color: "rgba(151, 218, 245,0.7)" // 0% 处的颜色
                            },
                            {
                                offset: 1,
                                color: "rgba(255, 255, 255,0)" // 100% 处的颜色
                            }
                        ]
                    }
                }
            }
        ]
    };
    var option1 = {
        title: {
            text: '未来一周气温变化',
        },
        tooltip: {
            trigger: 'axis'
        },
        toolbox: {
            show: true,
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                dataView: {readOnly: false},
                magicType: {type: ['line', 'bar']},
                restore: {},
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: '{value} °C'
            }
        },
        series: [
            {
                name: '最高气温',
                type: 'line',
                data: [11, 11, 15, 13, 12, 13, 10],
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
            },
            {
                name: '最低气温',
                type: 'line',
                data: [1, -2, 2, 5, 3, 2, 0],
                markPoint: {
                    data: [
                        {name: '周最低', value: -2, xAxis: 1, yAxis: -1.5}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'},
                        [{
                            symbol: 'none',
                            x: '90%',
                            yAxis: 'max'
                        }, {
                            symbol: 'circle',
                            label: {
                                position: 'start',
                                formatter: '最大值'
                            },
                            type: 'max',
                            name: '最高点'
                        }]
                    ]
                }
            }
        ]
    };
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
'''
import datetime

l1 = [{'id': 1, 'siteName': '西乡站点', 'api_waterdata.id': 11, 'pH': '4.8', 'NTU': '0.61', 'oxygen': '7.3', 'tem': '38.8',
       'ele': '479', 'chlorine': '6.8', 'site_id': 1, 'time': datetime.datetime(2020, 5, 5, 14, 0), 'status': 1},
      {'id': 2, 'siteName': '龙华站点', 'api_waterdata.id': 12, 'pH': '5.9', 'NTU': '0.77', 'oxygen': '9.7', 'tem': '35.9',
       'ele': '593', 'chlorine': '8.3', 'site_id': 2, 'time': datetime.datetime(2020, 5, 5, 14, 0), 'status': 1},
      {'id': 3, 'siteName': '清湖站点', 'api_waterdata.id': 13, 'pH': '7.1', 'NTU': '0.79', 'oxygen': '7.2', 'tem': '36.7',
       'ele': '700', 'chlorine': '6.2', 'site_id': 3, 'time': datetime.datetime(2020, 5, 7, 9, 00),
       'status': 0}]
result = []

for i in l1:
    res = {}
    res["create_time"] = i.get("time")
    res["ph_data"] = str(format(float(i.get('pH')) / 7 * 100, '.1f')) + "%"
    res["chlorine_data"] = str(float(i.get('chlorine')) / 10 * 100) + "%"
    res["NTU_data"] = str(float(i.get('NTU')) / 1 * 100) + "%"
    res["site_id"] = i.get("site_id")
    result.append(res)
print(result)


    # print(format(float(i.get('pH')) / 7 * 100,'.2f'))
# x = 68.57142857142857
# print(format(x,'.2f'))


