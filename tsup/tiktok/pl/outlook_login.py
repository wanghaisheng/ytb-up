import json
import re
import time


import os
from loguru import logger
from tsup.utils.webdriver import DPhelper


class OutlookMailLogin:
    def __init__(self):
        super().__init__()
        self.base_url = 'https://www.outlook.com'
        self.email_url = 'https://outlook.live.com/mail/0/'
        self.login_url = 'https://www.outlook.com/login'
        self.email = None
        self.broswer_dir = os.path.join(os.getcwd(), 'Browser')

        self.browser = DPhelper()

    def is_exist(self, xpath_pattern):
        """
        driver.find_element(*locator)
        :param xpath_pattern:
        :return False or the Element:
        """
        try:
            self.wait.ele_displayed(xpath_pattern)
            element = self.browser.ele( xpath_pattern)
            return element
        except:
            return False

    def input_email(self, this_email: str):
        # 页面等待加载
        self.wait.ele_displayed('.//input[@type="email"]')
        # 邮箱名称
        self.ele('.//input[@type="email"]').input( this_email)  # 填写邮箱
        self.email = this_email
        # 提交按钮
        self.ele('.//input[@type="submit"]').click()

    def input_password(self, _password: str):
        # 页面加载
        self.wait.ele_displayed('.//input[@type="password"]')
        # 输入密码
        self.ele('.//input[@type="password"]').input( _password)  # 填写邮箱
        # input('输入密码')
        # 提交按钮
        self.ele('.//input[@type="submit"]').click()

    def skip_the_back_email(self):
        time.sleep(5)
        skip_email = self.ele('.//a[@id="iShowSkip"]')
        if skip_email:
            self.browser.run_js("arguments[0].click();", skip_email)

    def login(self, email: str, password: str):
        # 登录页面
        self.browser.get(self.login_url)
        # 邮箱
        self.input_email(email)
        # 密码
        self.input_password(password)
        # 如果有back_email就跳过
        self.skip_the_back_email()
        # 拒绝持久登录
        self.reject_long_session()
        # 拒绝了解更多内容
        self.shutdown_learn_more()
        # 拒绝特色登录
        self.refuse_special_login()
        logger.info('success to login the email:{}'.format(email))

    # 拒绝持久登录协议
    def reject_long_session(self):
        try:
            time.sleep(5)
            id_btn_back = self.browser.ele( './/input[@id="idBtn_Back"]')  # 否
            self.browser.run_js("arguments[0].click();", id_btn_back)
        except:
            pass

    # 拒绝特色登录
    def refuse_special_login(self):
        refuse_login = self.is_exist('.//a[@id="iCancel"]')
        if refuse_login:
            self.browser.run_js("arguments[0].click();", refuse_login)

    # 关闭了解更多内容
    def shutdown_learn_more(self):
        try:
            time.sleep(5)
            self.wait.ele_displayed('.//a[@href="#/LearnMore"]')
            self.ele('.//input[@type="submit"]').click()
        except:
            pass

    def get_email_content(self, xpath_pattern):
        self.wait.ele_displayed(xpath_pattern)
        email_datas = self.browser.ele( xpath_pattern)
        # 从 the_last_email_data 元素的 aria-label 属性中提取验证码
        for email_data in email_datas:
            try:
                aria_label = email_data.attr('aria-label')
                if aria_label and 'TikTok' in aria_label:
                    result = re.search(r'\b(\d{6})\b', aria_label)
                    if result:
                        code = result.group(1)
                        logger.info('the tiktok code is: {}'.format(code))
                        return code
            except Exception as e:
                ...
        return False

    def find_the_tk_email(self):
        try:
            # 访问邮箱页面
            current_url = self.browser.url
            self.browser.get('https://outlook.live.com/mail/0/')
            if current_url == self.browser.url: self.browser.refresh()  # 刷新页面
            self.browser.wait(5)
            # 获取最新的email  './/select[contains(@class,"datepart1")]/option[%s]'
            the_last_email_pattern = './/div[contains(@class,"zXLz3")]/div'
            # 重点的email内容
            email_content = self.get_email_content(the_last_email_pattern)
            if email_content is not False:
                return email_content
            # 其它的email内容
            self.check_others_box()
            email_content = self.get_email_content(the_last_email_pattern)
            return email_content
        except Exception as e:
            logger.error(e)
            html = self.browser.html
            with open(os.path.join(os.getcwd(), '%s.html' % self.email), 'w', encoding='utf-8') as f:  # 保存此时的页面
                f.write(html)
            return False

    def check_others_box(self):
        self.wait.ele_displayed('.//button[@name="其他"]')
        button_other = self.browser.ele('.//button[@name="其他"]')
        self.browser.run_js("arguments[0].click();", button_other)
        self.browser.wait(10)


    def sumbit_button_click(self, xpath_pattern):
        self.wait.ele_displayed(xpath_pattern)  # 等待按钮加载完毕
        submit_button = self.browser.ele(xpath_pattern)  # 按钮
        self.browser.run_js("arguments[0].click();", submit_button)

    # 等待知道页面成功加载
    def succeed_to_register(self):
        self.wait.ele_displayed('.//div[@class="zXLz3 EbLVy"]')

    def debug_stop(self):
        while 1:
            pass