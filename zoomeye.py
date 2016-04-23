#!/usr/bin/env python
# coding:utf-8

import requests
from json import loads , dumps

base_url = "http://api.zoomeye.org"

def get_search_results(token , dork , search_type = "host" , page = 1):
    '''
    获取json格式的原始数据。
    '''
    header = {"Authorization": "JWT %s" % token}
    response = requests.get(base_url + "/" + search_type + "/search?query=" + dork + "&page=" + str(page),  headers = header)
    result = loads(response.content)
    if response.status_code != 200:
        error_handler(result)
        return "error"
    else:
        return result


def classify_results(result , para = ['banner']):
    '''
    对来自get_search_result函数的数据进行处理————直接显示(print)一份,供使用者阅读；以重叠列表形式返回(return)一份,供poc等程序使用。
    '''
    geoinfo = {"asn" , "city" , "continent" , "country" , "location" , "isp" , "names" , "subdivisions" , "organization" , "aso"}
    portinfo = {"product" ,  "banner" , "device" , "extrainfo" , "hostname" , "os" , "port" ,  "service" , "version"}
    tmp_result_list = []
    result_list = []
    if result["total"] % 10 == 0:
        print "Total pages:" , result["total"] / 10 , "\n"
    else:
        print "Total pages:" , result["total"] / 10 + 1, "\n"

    #default print:ip , port

    for result_num in range(len(result["matches"])):    #获取总结果数。
        print "ip:" , result["matches"][result_num]["ip"] , "\n" , "port:" , result["matches"][result_num]["portinfo"]["port"]    #打印IP地址,端口。
        tmp_result_list.append(result["matches"][result_num]["ip"])    #将IP放入临时列表中。
        tmp_result_list.append(result["matches"][result_num]["portinfo"]["port"])    #将端口信息放入临时列表中。
        for para_num in range(len(para)):    #获取形参para列表的元素个数,并打印对应信息，添加至临时列表。
            if para[para_num] in geoinfo:
                print para[para_num] , ":" , result["matches"][result_num]["geoinfo"][para[para_num]]
                tmp_result_list.append(result["matches"][result_num]["geoinfo"][para[para_num]])
            elif para[para_num] in portinfo:
                print para[para_num] , ":" , result["matches"][result_num]["portinfo"][para[para_num]]
                tmp_result_list.append(result["matches"][result_num]["portinfo"][para[para_num]])
            else:
                print para[para_num], ":" , result["matches"][result_num][para[para_num]]
                tmp_result_list.append(result["matches"][result_num][para[para_num]])

            #creates a list.

        result_list.append(tmp_result_list)    #将临时列表作为一个元素放入正式列表中。
        tmp_result_list = []
        print "\n"
    return result_list    #返回正式列表。


def get_token(email , password):
    '''
    获取token。
    '''
    data = dumps({"username": email , "password": password})
    response = requests.post(base_url + "/user/login" , data = data)
    result = loads(response.content)
    if response.status_code != 200:
        error_handler(result)
        return "error"
    else:
        return result["access_token"]


def remain_of_resources(token):
    '''
    检查token的剩余可用的资源数。
    '''
    header = {"Authorization": "JWT %s" % token}
    response = requests.get(base_url + "/resources-info" ,  headers = header)
    result = loads(response.content)
    if response.status_code != 200:
        error_handler(result)
        return "error"
    else:
        print "plan:" + result["plan"] , "\n" , "host-search:" , result["resources"]["host-search"] , "\n" , "web-search:" , result["resources"]["web-search"]


def error_handler(result):
    '''
    处理错误。
    '''
    print "error: " + result["error"] , "message: " + result["message"] , "url: " + result["url"]
