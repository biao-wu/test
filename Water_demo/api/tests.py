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

# from django.utils import timezone
# import datetime
# import pytz
#
# now = timezone.now()
# print(now)
# new = timezone.localtime(now)
# print(new)
import json
import re

s1 = "['1230000', ' 4560000']"
l1 = [1230000, 4560000]

# s2 = str(s1.split(","))
# print(s2)
#
# num = re.sub(r'\D', "", s1)
# print(num)

s1 = s1.replace("'",'"')

print([int(item) for item in json.loads(s1)])
# print(print([int(item.strip()) for item in json.loads(s1)]))