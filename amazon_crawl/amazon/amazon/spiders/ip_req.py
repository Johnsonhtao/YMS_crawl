import base64
import requests
import time
import random
import json

def base_code(username, password):
    str = '%s:%s' % (username, password)
    encodestr = base64.b64encode(str.encode('utf-8'))
    return '%s' % encodestr.decode()

def main():
    DEFAULT_REQUEST_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'cookie':'AGL_USER_ID=cd227b9b-e593-41d0-88cd-9a2d30366a7d',#cookie要自己更新一下！！！！！！
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.56",
    }
    username = 'cht123null' #这里填入用户名！！！！！
    password = 'Doupandaili123'# 这里填入密码！！！！！
    #
    base = base_code(username, password)
    print(base)
    DEFAULT_REQUEST_HEADERS['Proxy-Authorization'] = 'Basic '+base
    url = r'http://api.wandoudl.com/api/ip?app_key=5c4185f351ee2bda765c81343cde3859&pack=0&num=20&xy=1&type=2&lb=\r\n&mr=1&'
    # url = r'https://h.wandouip.com/get/ip-list?pack=%s&num=1&xy=1&type=2&lb=\r\n&mr=1&' % random.randint(100,1000)

    response = requests.get(url=url,headers=DEFAULT_REQUEST_HEADERS)

    text = json.loads(response.text)
    ip = text['data'][0]['ip']
    port = text['data'][0]['port']
    proxy = {'http': '%s:%s' % (ip, port)}

    # url_1 = 'http://www.baiduyunpan.org/thread-31333-1-1.html?x=328738'
    # url_1 = 'http://httpbin.org/ip'
    #
    # r1 = requests.get(url_1, headers=DEFAULT_REQUEST_HEADERS, proxies=proxy)
    # time.sleep(random.randint(1, 3))
    print(response.text)
    # print(r1.text)

if __name__ == '__main__':
    for i in range(20):
        main()
        print('成功获取IP数量: '+str(i+1))
