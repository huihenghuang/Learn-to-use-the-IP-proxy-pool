#学习使用selenium(自动化测试)
from selenium import webdriver
import time

#加载浏览器驱动
driver = webdriver.Chrome('chromedriver.exe')

#模拟谷歌浏览器访问百度页面
driver.get('http://www.baidu.com')
time.sleep(1)

#找到输入框，向输入框输入‘美女’关键字
input_tag = driver.find_element_by_id('kw')
input_tag.send_keys('美女')
time.sleep(2)

#点击回车
btn_tag = driver.find_element_by_id('su')
btn_tag.click()
time.sleep(2)
'''
#离开浏览器
driver.quit()
'''