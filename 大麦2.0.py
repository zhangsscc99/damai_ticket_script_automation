# coding: utf-8
from json import loads
from time import sleep, time
from pickle import dump, load
from os.path import exists
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import threading
from json import loads
class Concert(object):

    def __init__(self,sess, price, ticket_num, viewer_person, damai_url, target_url, driver_path, chrome_path,port,switch):
        self.sess = sess  # 场次序号优先级
        self.price = price  # 票价序号优先级
        self.status = 0  # 状态标记
        self.num = 0  # 尝试次数
        self.switch = switch # 开关
        self.chrome_path = chrome_path  # 浏览器地址
        self.ticket_num = ticket_num  # 购买票数
        self.viewer_person = viewer_person  # 观影人序号优先级
        self.damai_url = damai_url  # 大麦网官网网址
        self.target_url = target_url  # 目标购票网址
        self.driver_path = driver_path  # 浏览器驱动地址
        self.port = port  # 端口
        self.options = webdriver.ChromeOptions()  # 调试
        self.options.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.port}")
        service = webdriver.chrome.service.Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=self.options)

        # 获取cookie
    def get_cookie(self):
        # 打开大麦网
        self.driver.get(self.damai_url)
        print('---请点击登录---')
        while self.driver.title.find('大麦网-全球演出赛事官方购票平台') != -1:
            sleep(1)
        # 点击扫码登录
        print(u"---请扫码登录---")
        while self.driver.title == '大麦登录':  # 等待扫码完成
            sleep(1)
        # 下载cookie
        dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
        print(u"---Cookie保存成功---")

    # 设置cookie
    def set_cookie(self):
        try:
            cookies = load(open("cookies.pkl", "rb"))  # 载入cookie
            for cookie in cookies:
                cookie_dict = {
                    'domain': '.damai.cn',  # 必须有，不然就是假登录
                    'name': cookie.get('name'),
                    'value': cookie.get('value'),
                    "expires": "",
                    'path': '/',
                    'httpOnly': False,
                    'HostOnly': False,
                    'Secure': False}
                self.driver.add_cookie(cookie_dict)
            print(u'---载入Cookie---')
        except Exception as e:
            print(e)

    # 使用cookie登录，跳转到抢票页面
    def login(self):
        print(u'---开始登录---')
        self.driver.get(self.target_url)
        WebDriverWait(self.driver, 10, 0.1).until(EC.title_contains('商品详情'))
        self.set_cookie()

    # 最后面，查找是否有cookie
    def enter_concert(self):
        print(u'---打开浏览器，进入大麦网---')
        if not exists('cookies.pkl'):  # 查看是否有cookie
            # self.driver = webdriver.Chrome(executable_path=self.driver_path,options=self.options)
            self.get_cookie()
            print(u'---成功获取Cookie，重启浏览器---')
        self.login()  #包含载入cookie
        # self.driver.refresh()

    # 进入第一个页面-抢票
    def choose_ticket(self):
        print(u"---进入抢票界面---")
            # 查看这一步是否成功，不成功一直循环
        while True:
            # 查看页面是否刷新成功，找到box
            try:
                box = WebDriverWait(self.driver, 4, 0.1).until(
                    EC.presence_of_element_located((By.ID, 'root')))
                # return box
            except:
                self.driver.refresh()
                print(u"---Error: 页面刷新出错---")
                continue

            # 查看立即预订、即将开抢、缺货
            try:
                buybutton = WebDriverWait(self.driver,4,0.1).until(EC.presence_of_element_located((
                    By.CLASS_NAME,'button'
                )))
                # buybutton = box.find_element(by=By.CLASS_NAME, value='button')
                # 当前状态储存
                buybutton_text = buybutton.text
            except:
                self.driver.refresh()
                print("---Error: buybutton 位置找不到---")
                continue

            # 等待预约
            # if "预约抢票" in buybutton_text:
            while True:
                buybutton = WebDriverWait(self.driver, 4, 0.1).until(EC.presence_of_element_located((
                    By.CLASS_NAME, 'button')))
                if '预约抢票' in buybutton.text:
                    print(u"---未开售，等待中---")
                else:
                    break

            # 缺货刷新
            # if "缺货" in buybutton_text:
            #     self.driver.refresh()
            #     raise Exception("---已经缺货了---")
            # 点击
            print('点击立即预订')
            self.driver.execute_script("arguments[0].click();", buybutton)
            # 是否有验证
            while True:
                try:
                    WebDriverWait(self.driver, 0.3, 0.1).until(
                        EC.presence_of_element_located((By.ID, 'baxia-dialog-content')))
                    sleep(0.5)
                except:
                    break

            # 更新box为弹窗
            box = WebDriverWait(self.driver, 3, 0.1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sku-pop-wrapper')))

            # 进入选票页面
            try:
                # 选场次
                session = WebDriverWait(self.driver, 2, 0.1).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'sku-content')))  # 日期、场次和票档进行定位
                session_list = session.find_elements(
                    by=By.CLASS_NAME, value='bui-dm-sku-card-item')
                # 判断是否为单场
                if len(session_list) == 1:
                    self.status = 1
                else:
                    self.status = 2
                # 单场
                if self.status != 1:
                    self.driver.execute_script("arguments[0].click();", session_list[self.sess - 1])
            except:
                print('选择场次出错')
                self.driver.refresh()
                continue
            try:
                all = True
                price = WebDriverWait(self.driver, 2, 0.1).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'sku-tickets-card')))  # 日期、场次和票档进行定位
                price_list = price.find_elements(
                    by=By.CLASS_NAME, value='bui-dm-sku-card-item')  # 选定票档
                for i in self.price:
                    j = price_list[i - 1]
                    if '缺货登记' not in j.text:
                        all = False
                        # j.click()
                        self.driver.execute_script("arguments[0].click();", j)
                if all:
                    self.driver.refresh()
                    print('缺货刷新')
                    continue
            except:
                self.driver.refresh()
                print('选择票价出错')
                continue
                # 加票
            try:
                ticket_num_up = box.find_element(
                    by=By.CLASS_NAME, value='plus-enable')
                for i in range(self.ticket_num - 1):  # 设置增加票数
                    ticket_num_up.click()
                    # self.driver.execute_script("arguments[0].click();", ticket_num_up)
            except:
                self.driver.refresh()
                print('加票错误')
                continue
            try:
                # 点买票
                buy = self.driver.find_element(By.CLASS_NAME,'bui-btn-default')
                # buy.click()
                self.driver.execute_script("arguments[0].click();", buy)
                break

            except:
                raise Exception('确定按钮错误')

        # 跳到第三个页面
    def check_order(self):
        try:
            # 选择观影人  找到人那一行
            people = WebDriverWait(self.driver,1).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.iconfont.icondanxuan-weixuan_')))
            for i in self.viewer_person:
                i -= 1
                self.driver.execute_script("arguments[0].click();", people[i])

            comfirmBtn = WebDriverWait(self.driver, 5, 0.1).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="dmOrderSubmitBlock_DmOrderSubmitBlock"]/div[2]/div/div[2]/div[2]/div[2]')))
            if self.switch == 'T':
                comfirmBtn.click()
            # 判断title是不是支付宝
            print(u"---等待跳转到--付款界面--，可自行刷新，若长期不跳转可选择-- CRTL+C --重新抢票---")
        except:
            self.driver.refresh()
        while True:
            try:
                WebDriverWait(self.driver, 4, 0.1).until(
                    EC.title_contains('支付宝'))
                break
            except:
                sleep(1)
def run_concert(port):
    try:
        with open('./config.json', 'r', encoding='utf-8') as f:
            config = loads(f.read())
            # params: 场次优先级，票价优先级，实名者序号, 用户昵称， 购买票数， 官网网址， 目标网址, 浏览器驱动地址
        con = Concert(config['sess'], config['price'], config['ticket_num'], config['viewer_person'], config['damai_url'], config['target_url'], config['driver_path'], config['chrome_path'], port,config['switch'])
        con.enter_concert()  # 检查是否有cookie，包含载入cookie和跳转到页面
    except Exception as e:
        print(e)

    while True:
        try:
            con.choose_ticket()
            con.check_order()
            break
        except Exception as e:
            print(e)





if __name__ == '__main__':
    # 读取配置文件并创建线程
    try:
        with open('./config.json', 'r', encoding='utf-8') as f:
            config = loads(f.read())
            threads = []
            for port in config['ports']:
                thread = threading.Thread(target=run_concert, args=(port,))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()  # 等待所有线程完成
    except Exception as e:
        print(e)


