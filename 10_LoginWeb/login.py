from selenium import webdriver
import time
import sched


def login():
    user_name = 'sy1915213'
    pwd = '19961012'

    driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

    # 设置浏览器窗口的位置和大小
    driver.set_window_position(20, 40)
    driver.set_window_size(1100, 700)

    driver.get("https://gw.buaa.edu.cn:804/beihanglogin.php?ac_id=20&url=http://gw.buaa.edu.cn:804/beihangview.php")
    try:
        driver.find_element_by_id('loginname').send_keys(user_name)
        driver.find_element_by_id('password').send_keys(pwd)
        driver.find_element_by_id('button').click()

    except:
        pass
    finally:
        time.sleep(20)
        driver.close()


s = sched.scheduler(time.time, time.sleep)
while True:
    s.enter(60*60, 0, login)
    s.run()


