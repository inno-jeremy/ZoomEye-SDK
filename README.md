# ZoomEye-SDK

基于ZoomEye api编写的SDK。主要函数及用法说明如下：
    token = get_token("email" , "password")：
        通过给定的邮箱地址及密码获取token。如返回错误信息，则返回“error”，并在屏幕上打印错误信息。
    
    remain_of_resources(token)：
        通过给定的token查询对应token剩余的可查询资源数。
    
    result = get_search_results(token , dork , type , page)：
        获取json格式的原始数据。
        参数说明如下：token为给定的token；dork为待搜索dork；type为搜索类型，可使用主机搜索（host）或Web结果搜索（web）；page为指定的页码。
    
    classify_results(result , para = ['banner'])：
        对来自get_search_result函数的数据进行筛选————直接显示(print)一份,供使用者阅读；以列表形式返回(return)一份,供poc等程序使用。
        参数说明如下：result为来自get_search_result的原始json数据；para为指定返回显示的的数据的key值，包括"ip" , "timestamp" , "asn" , "city" , "continent" , "country" , "location" , "isp" , "names" , "subdivisions" , "organization" , "aso" , "product" ,  "banner" , "device" , "extrainfo" , "hostname" , "os" , "port" ,  "service" , "version"。 
