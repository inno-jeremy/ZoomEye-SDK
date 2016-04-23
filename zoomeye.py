#!/usr/bin/env python
# coding:utf-8

import requests
from json import loads , dumps

base_url = "http://api.zoomeye.org"

def get_search_results(token , dork , search_type = "host" , page = 1):
    '''
    ��ȡjson��ʽ��ԭʼ���ݡ�
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
    ������get_search_result���������ݽ��д���������ֱ����ʾ(print)һ��,��ʹ�����Ķ������ص��б���ʽ����(return)һ��,��poc�ȳ���ʹ�á�
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

    for result_num in range(len(result["matches"])):    #��ȡ�ܽ������
        print "ip:" , result["matches"][result_num]["ip"] , "\n" , "port:" , result["matches"][result_num]["portinfo"]["port"]    #��ӡIP��ַ,�˿ڡ�
        tmp_result_list.append(result["matches"][result_num]["ip"])    #��IP������ʱ�б��С�
        tmp_result_list.append(result["matches"][result_num]["portinfo"]["port"])    #���˿���Ϣ������ʱ�б��С�
        for para_num in range(len(para)):    #��ȡ�β�para�б��Ԫ�ظ���,����ӡ��Ӧ��Ϣ���������ʱ�б�
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

        result_list.append(tmp_result_list)    #����ʱ�б���Ϊһ��Ԫ�ط�����ʽ�б��С�
        tmp_result_list = []
        print "\n"
    return result_list    #������ʽ�б�


def get_token(email , password):
    '''
    ��ȡtoken��
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
    ���token��ʣ����õ���Դ����
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
    �������
    '''
    print "error: " + result["error"] , "message: " + result["message"] , "url: " + result["url"]
