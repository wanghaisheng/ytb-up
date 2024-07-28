# Lenovo-"Xie Yan"
import json
import pickle
import random
import time
from time import sleep
import pyperclip, pyautogui
from lxml import etree
from tsup.utils.webdriver import DPhelper
from DrissionPage.common import Actions
from DrissionPage.common import Actions

import os

# from PIL import Image
import requests
# from lxml import etree
import re
import os


from tsup.utils.webdriver import DPhelper

from loguru import logger
from loguru import logger


class TkLogin:
    def __init__(self):
        super().__init__()
        self.base_url = 'https://www.tiktok.com/'
        self.login_url = 'https://www.tiktok.com/login/phone-or-email/email'
        self.broswer_dir = os.path.join(os.getcwd(), 'Browser')
        # user agent


        # option.add_argument(
        #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        # self.browser = uc.Chrome(options=option)
        self.browser = DPhelper()
        # path = os.path.join(self.broswer_dir, "MicrosoftWebDriver.exe")
        # self.browser = webdriver.Edge(path)

        # with open(os.path.join(Working_ExePath, 'Browser', 'storage', 'stealth.min.js')) as f:
        #     js = f.read()
        # self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #     "source": js
        # })
        # self.wait = WebDriverWait(self.browser, 10)
        self.verication_success = False

    # 启动 clean 插件
    def click_clean_button_crt(self):
        time.sleep(5)
        self.wait.ele_displayed('.//img[@class="inserted-btn mtz"]')
        clean_button = self.browser.ele('.//img[@class="inserted-btn mtz"]')
        clean_button.click()

    def click_cookie_button(self):
        try:
            accept_all_btn = self.browser.run_js(
                '''return document.querySelector('tiktok-cookie-banner').shadowRoot.querySelector('button:nth-child(2)')''')
            if accept_all_btn:
                accept_all_btn.click()
        except:...

    # 打开浏览器首次请求，清理缓存，接受cookie
    def first_get_deal(self, url: str):
        # 请求网页
        self.browser.get(url)
        self.browser.set.window.max()
        # 清理缓存
        self.click_clean_button_crt()


        # 接受cookie协议
        cookie_button = self.is_exist('.//tiktok-cookie-banner')
        if cookie_button:
            self.click_cookie_button()

    def deal_img_verication(self):
        time.sleep(random.random() * 2 + 3)
        vericaiton_state = self.deal_verication_pic()  # 0 无验证       1  环形   2 图片拖动  3 图片相同元素验证
        if vericaiton_state != 0:
            self.deal_the_img(vericaiton_state)

    # 点击登录按钮
    def click_login_button_foryou(self):
        time.sleep(5)
        self.wait.ele_displayed('.//button[@id="header-login-button"]')
        self.click_element_based_father('.//button[@id="header-login-button"]')
        time.sleep(3)
        # 点击 密码邮箱登录
        self.wait.ele_displayed(
            './/div[contains(@class,"DivLoginContainer")]/div[contains(@class,"DivHomeContainer")]/a[2]')  # 验证码块 DivHomeContainer
        self.click_element_based_father(
            './/div[contains(@class,"DivLoginContainer")]/div[contains(@class,"DivHomeContainer")]/a[2]')  # 验证码块 DivHomeContainer
        # 使用邮箱
        time.sleep(3)
        self.wait.ele_displayed('.//a[@href="/login/phone-or-email/email"]')
        self.click_element_based_father('.//a[@href="/login/phone-or-email/email"]')

    def get_login_website(self, email, password: str):
        '''
        :param email password
        :return:
        '''
        logger.info('ready to use selenium to get login website')
        # input('fdfsdfsdfds')
        self.first_get_deal(self.login_url)  # ('https://www.tiktok.com/foryou')

        # 点击登录按钮
        time.sleep(3)
        self.add_email_passwd(email, password)
        self.deal_img_verication()  # 等待一段时间，判断是否需要验证处理，如果需要，就点击
        time.sleep(5)
        if self.is_exist('.//input[@name="username"]'):
            logger.error('An error in the login')
        try:
            # # 填写邮箱和密码
            # self.click_login_button_foryou()
            self.add_email_passwd(email, password)
            self.deal_img_verication()  # 等待一段时间，判断是否需要验证处理，如果需要，就点击
            time.sleep(5)
            if self.is_exist('.//input[@name="username"]'):
                logger.error('An error in the login')
            else:
                self.write_cookies(email)
        except Exception as e:
            logger.error(e)
            error = input('this is an error in login in')
            self.write_cookies(email)
            # self.write_cookies(outlook.email)
            # update_the_tb(email, 'LAST_LOGIN', get_today())

    # 根据xpath点击子元素
    def click_element_based_father(self, xpath_pattern, father_dot=None):
        if father_dot:
            birth_year = father_dot.ele(xpath_pattern)
        else:
            birth_year = self.browser.ele(xpath_pattern)
        Actions(self.browser).move_to(birth_year).perform()
        Actions(self.browser).click(birth_year).perform()
        return birth_year

    # 根据xpath点击子元素
    def click_element_mouce_anti_defection(self, xpath_pattern, father_dot=None):
        if father_dot:
            birth_year = father_dot.ele(xpath_pattern)
        else:
            birth_year = self.browser.ele(xpath_pattern)

        move_mouse(self.browser, birth_year, 2)
        return birth_year

    def get_element_location(self, targe_element, this_offset_x=None, this_offset_y=None):  # 移动到目标位置，同时返回具体目标位置
        if this_offset_x is None and this_offset_y is None:
            this_offset_x, this_offset_y = random.randint(-3, 3), random.randint(-3, 3)
        element_center_x = targe_element.location['x'] + targe_element.size['width'] / 2
        element_center_y = targe_element.location['y'] + targe_element.size['height'] / 2
        return element_center_x + this_offset_x, element_center_y + this_offset_y

    def mouse_modulation(self, start_element_location: list,
                         xpath_pattern,
                         numberList=30
                         ):
        passwd_element = self.browser.ele(xpath_pattern)  # 找到元素
        passwd_element_x, passwd_element_y = self.get_element_location(passwd_element)  # 这个元素的目标点击offset
        s = bezierTrajectory()  # 实例化贝塞尔曲线
        mouse_tracks = s.return_offset_cbezier(start_element_location, [passwd_element_x, passwd_element_y],
                                               numberList=numberList)  # 鼠标的移动轨迹
        # 鼠标的移动
        for mouse_track in mouse_tracks:
            try:
                Actions(self.browser).move(mouse_track[0], mouse_track[1]).perform()
            except Exception as e:
                print(mouse_track[0], mouse_track[1])
                raise e
        return passwd_element, passwd_element_x, passwd_element_y

        # 填写邮箱和密码

    def add_email_passwd(self, email, password):
        self.wait.ele_displayed('.//input[@type="password"]')
        tk_logo = self.is_exist('.//a[@data-e2e="tiktok-logo"]')
        tk_logo_x, tk_logo_y = 0, 0
        if tk_logo is not False:
            this_offset_x, this_offset_y = random.randint(-3, 3), random.randint(-3, 3)
            tk_logo_x, tk_logo_y = self.get_element_location(tk_logo, this_offset_x, this_offset_y)
            Actions(self.browser).move(tk_logo, this_offset_x,
                                                                             this_offset_y).perform()

        # passwd
        time.sleep(random.random() + 1)
        passwd_element, passwd_element_x, passwd_element_y = self.mouse_modulation([tk_logo_x, tk_logo_y],
                                                                                   xpath_pattern='.//input[@type="password"]',
                                                                                   numberList=51)
        self.browser.run_js("arguments[0].click();", passwd_element)
        time.sleep(random.random() + 2)
        passwd_element.input(password)
        # email
        time.sleep(random.random() * 2 + 1)
        email_element, email_element_x, email_element_y = self.mouse_modulation([passwd_element_x, passwd_element_y],
                                                                                xpath_pattern='.//input[@name="username"]',
                                                                                numberList=11)
        self.browser.run_js("arguments[0].click();", email_element)
        time.sleep(random.random() * 2 + 2)
        email_element.input(email)
        # submit
        time.sleep(random.random() + 2)
        submit_button, submit_button_x, submit_button_y = self.mouse_modulation([email_element_x, email_element_y],
                                                                                xpath_pattern='.//form//button[@type="submit"]',
                                                                                numberList=31)
        # self.browser.run_js("arguments[0].click();", submit_button)

        # submit_button.click()
        # time.sleep(random.random())
        # self.browser.run_js("arguments[0].click();", submit_button)

    # 保存cookie,携带 email 地址
    def write_cookies(self, email):
        with open(os.path.join(User_Cookie_Dir, "%s.json" % email), 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.browser.get_cookies(), ensure_ascii=False))  # 将cookies保存为json格式
            logger.info('write  cookies info to the json')

    def debug_stop(self):
        while 1:
            pass



    # 如果点击发送邮件出现图片验证，需要进行
    def deal_verication_code(self):
        # 发送验证码
        send_email_button = self.browser.ele('.//button[@data-e2e="send-code-button"]')
        send_email_button.click()
        self.browser.run_js("arguments[0].click();", send_email_button)
        self.browser.implicitly_wait(10)
        vericaiton_state = self.deal_verication_pic()  # 0 无验证       1  环形   2 图片拖动  3 
        
        if vericaiton_state != 0:

            self.deal_the_img(vericaiton_state)
            time.sleep(3)
            return True
        else:  # 无验证
            vericaiton_over = self.judge_button_clickable('.//button[@data-e2e="send-code-button"]')
            if vericaiton_over:
                return True
        logger.error('An error in the verication code receive')
        return False

    def deal_the_img(self, vericaiton_type):
        '''
        :param vericaiton_type:  1 双环    2 图片拖动 3  图片 同样元素
        :return:
        '''
        from .ocr import ddddOcr_tk
        from .solver import tk_circle_discern
        # img 外部容器
        img_outer_container = None
        this_xpath_pattern = None  # 图片 二维码 pattern
        if vericaiton_type == 1:  # 外环
            this_xpath_pattern = './/div[@class="sc-jTzLTM kuTGKN"]'
            img_outer_container = self.browser.ele(this_xpath_pattern)
        elif vericaiton_type == 2:  # 图片
            this_xpath_pattern = './/div[contains(@class,"captcha_verify_img--wrapper")]'
            img_outer_container = self.browser.ele(this_xpath_pattern)
        elif vericaiton_type == 3:
            this_xpath_pattern = './/img[@id="captcha-verify-image"]'
            logger.error('this is the picture choose img???')
            input('please deal the problem by hand,input waiting...')
            return
        # 外圈图片   背景图片
        outer_pic = img_outer_container.ele('./img[1]')
        outer_pic = outer_pic.attr('src')
        self.browser.download(outer_pic, 'outer.png')  # 下载图片
        # 内圈图片   目标小图片
        inner_pic = img_outer_container.ele('./img[2]')
        inner_pic = inner_pic.attr('src')
        # 下载到本地
        self.browser.download(inner_pic, 'inner.png')  # 下载图片
        print('have download the two picture')
        # 验证码本地识别
        distance = None  # 需要拖动的距离
        if vericaiton_type:
            angle = tk_circle_discern('inner.png', 'outer.png')
            distance = angle / 180 * (340 - 64)
        else:
            distance = ddddOcr_tk('inner.png', 'outer.png')
            distance = distance * 0.62
        this_track = [int(distance // 4), int(distance // 4), int(distance * 0.3), int(distance * 0.2) + 5,
                      -8]  # 模拟鼠标拖动的点移
        this_track.append(int(distance) - sum(this_track))
        self.hold_on_slide(this_track)  # 拖动滑块 模拟移动
        self.judge_the_img_src_change(this_xpath_pattern + '/img[2]/@src', inner_pic, vericaiton_type)

    # 判断验证码是否改变， 验证成功后验证码消失，或者失败验证码refresh
    def judge_the_img_src_change(self, this_xpath_pattern, last_inner_img_url: str, circle):
        html = this_xpath_pattern  # inner_img_url pattern
        response = self.browser.html
        verication = html.xpath('.//div[contains(@class,"captcha_verify_container")]')  # 验证码块
        import time
        if verication:
            img_src = html.xpath(this_xpath_pattern)  # 验证码图片
            if len(img_src) == 1 and img_src[0] != last_inner_img_url:  # 验证码已经改变
                # self.browser.implicitly_wait(5)
                print("img_src%s" % img_src)
                a = input('there is img need to deal')
                if a == 'a':
                    return False
                time.sleep(5)  # 等待 5s
                self.deal_the_img(circle)
            # 验证码没有改变 或者加载错误
            else:
                time.sleep(10)
                self.judge_the_img_src_change(this_xpath_pattern, last_inner_img_url, circle)
        else:
            print('Success to over the picture')
            self.verication_success = True  # 成功
            return True

    # 模拟滑动验证
    def hold_on_slide(self, tracks):
        import time, random
        try:
            slider = self.browser.ele('.//div[contains(@class,"secsdk-captcha-drag-icon")]')
            # 鼠标点击并按住不松
            Actions(self.browser).move_to(slider).hold()
            # 让鼠标随机往下移动一段距离
            Actions(self.browser).move(xoffset=0, yoffset=100)
            time.sleep(0.15)
            for item in tracks:
                Actions(self.browser).move(xoffset=item,
                                                                    yoffset=random.randint(-1, 1)).perform()
                time.sleep(random.uniform(0.02, 0.15))
            # 稳定一秒再松开
            time.sleep(1)
            # Actions(self.browser).release().perform()
            time.sleep(1)
        except Exception as e:
            print(e)

    def deal_verication_pic(self):
        res = self.is_exist('.//div[@class="sc-jTzLTM kuTGKN"]/img[2]')
        if res:
            return 1
        res = self.is_exist('.//div[contains(@class,"captcha_verify_img--wrapper")]/img[2]')
        if res:
            return 2
        res = self.is_exist('.//img[@id="captcha-verify-image"]')
        if res:
            return 3
        return 0

    def is_exist(self, xpath_pattern):
        """
        driver.ele(*locator)
        :param xpath_pattern:
        :return False or the Element:
        """
        try:
            self.wait.ele_displayed(xpath_pattern)
            element = self.browser.ele(xpath_pattern)
            return element
        except:
            return False

    # 随机生成名称
    def random_user_name(self):
        _name = ''
        from random_word import RandomWords
        r = RandomWords()
        # Return a single random word
        _name += r.get_random_word()
        self.wait.ele_displayed('.//input[@name="new-username"]')

        def test_name_input(input_name):
            user_name = self.browser.ele('.//input[@name="new-username"]')
            user_name.input(input_name)

        # 注册按钮
        button_pattern = input('.//button[1]')
        if self.judge_button_clickable(button_pattern):
            _name += r.get_random_word()
            test_name_input(_name)
        button = self.browser.ele(button_pattern)
        self.browser.run_js("arguments[0].click();", button)

    def judge_button_clickable(self, xpath_pattern):
        button = self.browser.ele(xpath_pattern)
        button_class = button.attr('class')
        logger.info('button_class_for_verication_code is {}'.format(button_class))
        return 'disable' in button_class

    def get_setting_button(self):
        time.sleep(5)
        # 点击设置
        self.wait.ele_displayed('.//div[@id="header-more-menu-icon"]')
        self.click_element_based_father('.//div[@id="header-more-menu-icon"]')