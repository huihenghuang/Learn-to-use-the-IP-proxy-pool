import requests

import urllib
import urllib.request

from bs4 import BeautifulSoup

from http import  client

from threading import Thread

from threading import Lock

url = 'http://www.xicidaili.com/nn/%d'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
           'Host':'www.xicidaili.com'}

inFile = open('./proxy.txt',mode='r',encoding='utf-8')
outFile = open('./verifiedProxy.txt',mode='w',encoding='utf-8')
lock = Lock()

def getProxy(page):
    fp = open('./proxy.txt',mode='a',encoding='utf-8')
    num = 0
    for p in range(1,page+1):
        url_proxy = url%(p)
        response = requests.get(url=url_proxy,headers = headers)
        response.encoding = 'utf-8'
        html = response.text

        # with open('./xici.html',mode='w',encoding='utf-8') as fp:
        #     fp.write(html)

        soup = BeautifulSoup(html)

        proxies = soup.find('table', id='ip_list').find_all('tr')

        # print(len(proxies))

        '''<tr class="odd">
      <td class="country"><img src="http://fs.xicidaili.com/images/flag/cn.png" alt="Cn"></td>
      <td>125.121.122.126</td>
      <td>6666</td>
      <td>
        <a href="/2018-07-02/zhejiang">浙江杭州</a>
      </td>
      # 4
      <td class="country">高匿</td>
      # 5
      <td>HTTPS</td>
      # 6
      <td class="country">
        <div title="0.403秒" class="bar">
          <div class="bar_inner fast" style="width:89%">
            
          </div>
        </div>
      </td>
      # 7
      <td class="country">
        <div title="0.08秒" class="bar">
          <div class="bar_inner fast" style="width:97%">
            
          </div>
        </div>
      </td>
      
      # 8
      <td>6分钟</td>
      # 9
      <td>18-07-02 11:01</td>
    </tr>'''
        # 一页的数据爬取成功
        for p in proxies[1:]:
            tds = p.find_all('td')
            ip = tds[1].string
            port = tds[2].string

            # 位置有可能为kong
            try:
                a_ = tds[3].find('a')
                location = a_.get_text()
            except:
                location = '未知'
            protacol = tds[5].string
            speed = tds[6].div['title']
            time = tds[8].get_text()
            last_verified_time = tds[9].get_text()

            proxy = '%s,%s,%s,%s,%s,%s,%s\n'%(ip,port,location,protacol,speed,time,last_verified_time)

            fp.write(proxy)
            num+=1

    fp.close()
    return num


# 使用ip发起网络请求了
def verifyPorxy():
    verify_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
    verify_url = 'http://www.baidu.com/'
    num = 0
    while True:
        lock.acquire()
        line = inFile.readline().strip()
        lock.release()

        if line ==None :break

        try:
            l = line.split(',')
            ip = l[0]
            port = l[1]
        except Exception as e:
            break

        # 方式一
        # requests.get(verify_url,proxies = {'http':'%s:%s'%(ip,port)})
        # 方式二
        # handler = urllib.request.ProxyHandler({'http':'%s:%s'%(ip,port)})
        # opener = urllib.request.build_opener(handler)

        # 方式三
        conn = client.HTTPConnection(ip, port, timeout=5)

        try:
            # 网络请求
            conn.request('GET',verify_url,headers=verify_headers)

        #     如果不报异常，说明ip端口号可用
            print('+++Success+++%s'%(line))

            lock.acquire()
            outFile.write(line+'\n')
            lock.release()
            num+=1

        except:
            print('---Failure---%s'%(line))
    return num

if __name__ == '__main__':
    # page = int(input('请输入爬取的页码：'))

    # num = getProxy(page)
    # print('国内高匿代理获取了：%d'%(num))
    print('开始验证————————————')

    # inFile = open('./proxy.txt',mode='r',encoding='utf-8')
    #
    # outFile = open('./verifiedProxy.txt',mode='a',encoding='utf-8')

    # num = verifyPorxy(inFile,outFile)
    # print('可用ip数量是： %d'%(num))

    threads = []
    for i in range(30):
        th = Thread(target=verifyPorxy)
        th.start()
        threads.append(th)

    # 线程锁
    for th in threads:
        th.join()

    # 关闭文件流
    inFile.close()
    outFile.close()