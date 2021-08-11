from selenium import webdriver
import numpy as np
import time

browser = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

url = 'http://36.112.130.153:7777/DSSPlatform/shirologin.html###'
browser.get(url)

browser.find_element_by_id('username').send_keys('Maxiaofeng')
browser.find_element_by_id('password').send_keys('076476')
key_code = input("Wait:")
print(browser.current_url)
print(browser.title)
datas = browser.find_elements_by_partial_link_text("WFV 地址2")
datas = [x.get_attribute("href") for x in datas]
datas = np.array(datas)

# time_str = time.strftime('%Y%m%d')
time_str = '20210115'
np.savetxt(f'{time_str}.txt', datas, fmt='%s')
# all_windows = dr.window_handles#获取当前打开的所有页面句柄,以列表类型返回。当前有两个页面，对应两个句柄
# dr.switch_to.window(all_windows[1])#切换到第二个页面对应的句柄，即下标为1的对象。如果不加该行，最终只会关闭百度首页
# alert = dr.switch_to.alert#切换alert相关窗口
# message = alert.text#获取弹窗提示信息，多用于判断
input("Wait:")

