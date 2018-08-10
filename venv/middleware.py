#!/usr/bin/python
# -*- coding: UTF-8 -*-
#coding:utf-8
import sys
import urllib2
import time
import urllib
import json
import hashlib
import base64
import json
import sqlite3
conn = sqlite3.connect('fillinblank.db')
c = conn.cursor()

reload(sys)
sys.setdefaultencoding( "utf-8" )
text_factory = str

def getData(path):
    f = open(path, 'rb')
    file_content = f.read()
    base64_audio = base64.b64encode(file_content)
    body = urllib.urlencode({'audio': base64_audio})

    url = 'http://api.xfyun.cn/v1/service/v1/iat'
    # 此处填写讯飞控制台提供的apiKey
    api_key = '463293f4cb68800c9aecdccd7224d324'
    # 更改上传的声音格式
    param = {"engine_type": "sms8k", "aue": "raw"}
    # 此处填写讯飞控制台提供的apiId
    x_appid = '5b6a5dab'
    x_param = base64.b64encode(json.dumps(param).replace(' ', ''))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum = hashlib.md5(api_key + str(x_time) + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib2.Request(url, body, x_header)
    result = urllib2.urlopen(req)
    result = result.read()
    dict = json.loads(result)
    print(result)
    if(dict["code"]=="0"):
        return dict["data"]
    else:
        return dict["code"]

def aduioFormat(audio):
    city = "empty"
    province = "empty"
    list1 = c.execute('select provincename from province')
    for element in list1:
        temp = element[0]
        if audio.find(temp[0:-1]) != -1:  # 包含'省'
            province = element[0]
            break
    if (province != "empty"):
        list2 = c.execute('select cityname from city where provincename=?', (province,))
        for element in list2:
            temp = element[0]
            if audio.find(temp[0:-1]) != -1:  # 包含'省'
                city = element[0]
    else:
        list2 = c.execute('select cityname,provincename from city')
        for element in list2:
            temp = element[0]
            if audio.find(temp[0:-1]) != -1:  # 包含'省'
                city = element[0]
                province = element[1]
    retjson = "{\"province\":\""+province+"\",\"city\":\""+city+"\"}"
    return retjson
    c.close()
    conn.close()

def createDB():
    f = open(r"D:\code\fillinBlank\json3.txt", "r")
    count = len(open(r"D:\code\fillinBlank\json3.txt", 'rU').readlines())
    dict={}
    for i in range(count):
        if (i % 2 == 0):
            provincetemp = f.next()
            tmp=provincetemp.decode("gbk")
            province=tmp.split("\n")
            print province[0]
            print "11111"
            dict[province[0]] = ""
            strr='INSERT INTO province (provincename)  VALUES (:cas)'
            print strr
            c.execute(strr,{'cas':province[0]})
            conn.commit()
        if (i % 2 == 1):
            citytemp = f.next()
            list=str(citytemp).split("a")
            for j in list:
                if(j == "\n"):
                    break
                strrr='INSERT INTO city (cityname,provincename)  VALUES (:a,:b);'
                c.execute(strrr, {'a': unicode(j),'b':unicode(province[0])})
            dict[province[0]]=list
    return dict


if __name__ == '__main__':
    # audio="我住在北京市朝阳区"
    # 下面path应传入一个wav文件的位置
    audio=getData("path")
    print aduioFormat(audio)