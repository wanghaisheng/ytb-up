import json
import time


import os

import re
from tsup.utils.webdriver import DPhelper

from loguru import logger

class OutlookMailRegister():
    def __init__(self):
        super().__init__()
        self.base_url = 'https://www.outlook.com'
        self.url = 'https://www.outlook.com'
        self.login_url = 'https://login.live.com/'
        self.register_url = 'https://signup.live.com/'
        self.broswer_dir = os.path.join(os.getcwd(), 'Browser')

        self.browser_port = 9223
        time.sleep(5)
        # 启用带插件的浏览器

        self.browser = DPhelper()

        self.verication_success = False

    # 启动 clean 插件
    def click_clean_button_crt(self):
        pass
        time.sleep(5)
        self.wait.ele_displayed('.//img[@class="inserted-btn mtz"]')
        clean_button = self.browser.ele('.//img[@class="inserted-btn mtz"]')
        clean_button.click()

    def is_exist(self, xpath_pattern):
        """
        driver.find_element(*locator)
        :param xpath_pattern:
        :return False or the Element:
        """
        try:
            self.wait.ele_displayed(xpath_pattern)
            element = self.browser.ele(xpath_pattern)
            return element
        except:
            return False

    def judge_element_success_or_not(self, xpath_pattern, error_hander):
        """
        判断邮箱是否可用, 可用返回password输入元素，否则从新开始邮箱输入
        :return 密码输入定位元素:
        """
        password_input = self.is_exist(xpath_pattern)  # 密码输入框
        if not password_input:  # 没找到密码输入框
            print('can not find the the element: {}'.format(xpath_pattern))
            error_hander()  # 重新填写邮箱表单
        else:  # 找到密码输入框
            return password_input

    def input_email_in_register(self):
        # 获取邮箱和密码
        self.request_user_meta()
        # 邮箱名称
        self.browser.ele('.//input[@id="MemberName"]').input( self.email)  # 填写邮箱
        # 提交按钮
        self.ele('.//input[@type="submit"]').click()
        time.sleep(5)  # 隐式等待
        # 判断邮箱是否可用,可用返回password输入元素，否则重新获取meta中的邮箱
        password_input = self.judge_element_success_or_not('.//input[@id="PasswordInput"]',
                                                           self.input_email_in_register)
        # 输入 密码，并确认
        password_input.input(self.password)
        time.sleep(5)
        self.ele('.//input[@type="submit"]').click()

    def check_phone_number_need(self):
        res = self.is_exist('.//input[contains(@id,"PhoneInput")]')
        if res:
            res.input('17830373031')
            self.ele('.//a[@role="button"]').click()
            input('Phone number is needed!')
            self.save_user_data()
            logger.error('Outlook register need email, so give up')
            return True
        return False
    def save_user_data(self):
        print()
    # 注册 register
    def register(self):
        self.browser.get(self.register_url)  # 注册页面
        self.browser.set.window.max()
        self.click_clean_button_crt()
        self.browser.refresh()
        self.ele('.//input[@type="submit"]').click()  # 同意并退出
        time.sleep(5)
        self.input_email_in_register()
        # 输入姓名和出生信息
        self.add_user_infomation(self.firstname, self.lastname)
        # 是否需要处理手机号
        res = self.check_phone_number_need()
        if res:
            self.save_user_data()
            return False
        # 验证码 授权
        from loguru import logger
        logger.info(self.email, self.password)
        self.verication_right()

        # 储存用户数据
        self.save_user_data()
        self.browser.close()
        return True

    def send_key_to_element(self, xpath_pattern, keys):
        self.wait.ele_displayed(xpath_pattern)  # 等待元素加载
        member_name = self.browser.ele(xpath_pattern)  # 找到元素
        member_name.input(keys)

    def add_user_infomation(self, first_name: str, last_name: str):
        # 判断是否可以，输入姓名
        last_name_element = self.judge_element_success_or_not('.//input[@id="LastName"]',
                                                              self.input_email_in_register)
        last_name_element.input(first_name)  # 姓
        first_name_element = self.browser.ele('.//input[@id="FirstName"]')
        first_name_element.input(last_name)  # 名
        time.sleep(3)
        self.ele('.//input[@type="submit"]').click()
        time.sleep(3)
        # 输入出生地址
        # 输入 年 月 日
        # birth_month_pattern.
        time.sleep(1)
        # birth_day
        birth_data_pattern = './/select[contains(@class,"datepart2")]/option[%s]' % self.birth_month
        self.wait.ele_displayed(birth_data_pattern)
        self.browser.ele(birth_data_pattern).click()

        # birth_month
        birth_month_pattern = './/select[contains(@class,"datepart1")]/option[%s]' % self.birth_month
        self.wait.ele_displayed(birth_month_pattern)
        self.browser.ele(birth_month_pattern).click()

        # birth_year
        self.wait.ele_displayed('.//input[@type="number"]')
        birth_year_element = self.browser.ele('//input[@type="number"]')
        birth_year_element.input(self.birth_year)




        self.ele('.//input[@type="submit"]').click()  # 确定

    # verication_right 验证和授权
    def verication_right(self):
        # 下一步按钮
        # try:
        #     button_pattern = './/button[contains(@class,"button")]'
        #     button_element = (By.XPATH, button_pattern)
        #     WebDriverWait(self.browser, 60).until(EC.presence_of_element_located(button_element))
        #     self.browser.ele('.//button[contains(@class,"button")]').click()
        # except Exception as e:
        #     pass
        # 喇叭提示用户控制
        # horn_prompt()
        # 验证码
        self.deal_pic_verication()
        # 拒绝许可协议
        self.reject_long_session()
        # 等待知道成功加载,
        self.succeed_to_register()
        # 关闭页面
        # self.browser.close()

    # 等待知道页面成功加载
    def succeed_to_register(self):
        self.browser.wait(20)  # 隐式等待
        # EgoYiBQzuMD9@outlook.com q9ox@5jPmF7o5
        while 'login' in self.browser.url: pass

    def get_email_content(self, xpath_pattern):
        self.wait.ele_displayed(xpath_pattern)
        email_datas = self.browser.ele(xpath_pattern)
        # 从 the_last_email_data 元素的 aria-label 属性中提取验证码
        for email_data in email_datas:
            try:
                aria_label = email_data.attr('aria-label')
                print('aria_label is {}'.format(aria_label))
                if aria_label and 'TikTok' in aria_label:
                    result = re.search(r'\b(\d{6})\b', aria_label)
                    if result:
                        code = result.group(1)
                        return code
            except:
                ...
        return False

    def find_the_tk_email(self):
        # 访问邮箱页面
        current_url = self.browser.url
        self.browser.get('https://outlook.live.com/mail/0/')
        if current_url == self.browser.url: self.browser.refresh()  # 刷新页面
        self.browser.wait(5)
        # 获取最新的email
        the_last_email_pattern = './/div[@class="zXLz3 EbLVy"]/div'
        # 重点的email内容
        email_content = self.get_email_content(the_last_email_pattern)
        if email_content is not False:
            return email_content
        # 其它的email内容
        self.check_others_box()
        email_content = self.get_email_content(the_last_email_pattern)
        return email_content

    def check_others_box(self):
        self.wait.ele_displayed('.//button[@name="其他"]')
        button_other = self.browser.ele('.//button[@name="其他"]')
        self.browser.run_js("arguments[0].click();", button_other)
        self.browser.wait(10)

    # 处理 图片验证码
    def deal_pic_verication(self):
        try:
            self.deal_notice_page() # 等待 Btn Button 或者 登录
        except:
            self.deal_pic_verication()

    # 最新的问题是 隐私页面错误
    def deal_notice_page(self):
        if 'privacynotice' in self.browser.url:
            logger.info('the email and passwd is {}:{}'.format(self.email,self.password))
            login_url = "https://login.live.com/login.srf"
            self.browser.get(login_url)
            return True
        else:
            # 继续等待 idBtn
            self.wait.ele_displayed('.//input[@id="idBtn_Back"]')
            self.browser.ele('.//input[@id="idBtn_Back"]')

    # 拒绝持久登录协议
    def reject_long_session(self):
        id_btn_back = self.browser.ele('.//input[@id="idBtn_Back"]')  # 否
        self.browser.run_js("arguments[0].click();", id_btn_back)

    def get_outlook_website(self)->bool:
        # 测试ip
        self.check_ip_country()
        # if '北京' in self.country:
        #     raise "the ip is not right..."
        # 注册
        return self.register()

    def debug_stop(self):
        while 1:
            pass

    def check_ip_country(self):
        self.browser.get("http://myip.ipip.net/")
        html = self.browser.html
        match = re.search(r"来自于：(.*?)\s{2}", html)
        if match:
            country = match.group(1)
            self.country = country