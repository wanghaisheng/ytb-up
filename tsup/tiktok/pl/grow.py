import json
import pickle
import random
import time
from time import sleep
import pyautogui
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from PIL import Image
import requests
from selenium.webdriver.support.select import Select
# from lxml import etree
import re
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium.webdriver.support.select import Select
from decouple import config
from selenium.webdriver.common.by import By

from Source.chrome.Chrome import run_chrome_thread
from tiktok_config import Data_Storage_storage_Dir, Working_Exe_Path, Chrome_Extension_Dir, Error_Html_Dir, \
    User_Avter_Dir
from utils.common import common_download_image
from selenium.webdriver.chrome.options import Options

from utils.verication.powerddddocr import ddddOcr_tk
from utils.verication.rotate_captcha import tk_circle_discern
import undetected_chromedriver as uc
from loguru import logger


class TkIntroduction(object):
    def __init__(self):
        self.base_url = 'https://www.tiktok.com/'
        self.url = 'https://www.tiktok.com/foryou'
        self.broswer_dir = os.path.join(os.getcwd(), 'Browser')
        self.verication_success = False
        self.browser_port = 9222
        run_chrome_thread(self.browser_port)
        time.sleep(5)
        # 启用带插件的浏览器
        option = webdriver.ChromeOptions()
        option.add_experimental_option("debuggerAddress", "127.0.0.1:%s" % self.browser_port)
        chrome_driver_path = os.path.join(self.broswer_dir, "chromedriver.exe")
        self.browser = webdriver.Chrome(executable_path=chrome_driver_path, options=option)

        with open(os.path.join(Working_Exe_Path, 'Browser', 'storage', 'stealth.min.js')) as f:
            js = f.read()
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })
        self.wait = WebDriverWait(self.browser, 25)
        self.last_data_num = 0  # 上一次数据的数量
        self.this_video_process = {'play_time_ratio': 0.0, 'show_times': 0, 'process_over': False}  # 存储此次视频的操作

    # 从页面产出clean图标
    def delete_clean_img(self):
        clean_img = self.is_exist('.//img[@class="inserted-btn mtz"]')
        if clean_img:
            self.browser.execute_script('arguments[0].remove();', clean_img)

    # 利用 smart clean 清除 缓存等信息
    def click_clean_button_crt(self):
        time.sleep(5)
        self.wait_xpath('.//img[@class="inserted-btn mtz"]')
        clean_button = self.browser.find_element(By.XPATH, './/img[@class="inserted-btn mtz"]')
        clean_button.click()

    def wait_xpath(self, xpath_pattern, ):
        element = (By.XPATH, xpath_pattern)
        self.wait.until(EC.presence_of_element_located(element))

    def is_exist(self, xpath_pattern):
        """
        driver.find_element(*locator)
        :param xpath_pattern:
        :return False or the Element:
        """
        try:
            self.wait_xpath(xpath_pattern)
            element = self.browser.find_element(By.XPATH, xpath_pattern)
            return element
        except:
            return False

    def is_exist_elements(self, xpath_pattern):
        """
        driver.find_element(*locator)
        :param xpath_pattern:
        :return False or the Element:
        """
        try:
            self.wait_xpath(xpath_pattern)
            elements = self.browser.find_elements(By.XPATH, xpath_pattern)
            return elements
        except:
            return False

    def read_cookies(self):  # 读取 cookies
        self.browser.delete_all_cookies()
        if os.path.exists(os.path.join(self.broswer_dir, 'cookies.txt')):
            with open(os.path.join(self.broswer_dir, 'cookies.txt'),
                      'r') as f:  # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
                cookies_list = json.load(f)
                for cookie in cookies_list:
                    self.browser.add_cookie(cookie)

    # 判断是登录或者使用cookie
    def add_user_session(self):
        self.browser.get('https://www.tiktok.com/signup')
        self.click_clean_button_crt()
        time.sleep(5)
        self.read_cookies()
        # self.browser.maximize_window()
        username = self.get_name_tiktok()
        if username is False:  # cookie 没有 或者 cookie失效
            # self.login()
            logger.error('You should login in the website:tiktok')
        else:
            logger.info('Succeed to login in with session')

    # 第一次请求 某个url
    def get_first_url(self):
        self.browser.get(self.url)  # 浏览器请求url~
        # self.browser.get('https://www.tiktok.com/@holiveira372/video/7231222427471121707')
        time.sleep(5)
        video_container = self.browser.find_element(By.XPATH,
                                                    './/video/ancestor::*[contains(@class, "DivItemContainer")]')
        self.click_the_video_comment_button(video_container)
        logger.info('click the foryou page video and enter the single video page')
        time.sleep(5)

    # 每个视频开始前更新参数
    def clean_video_params(self):
        self.this_video_process = {'play_time_ratio': 0.0, 'show_times': 0, 'process_over': False}  # 存储此次视频的操作

    # 处理一个视频
    def deal_one_video(self):
        video_deal = random_generate_deals()
        self.clean_video_params()  # 重置单个视频的处理情况信息（上一次的）
        ############# 测试 each funciton 的 video deal #########
        video_deal['love'] = True
        video_deal['love_comment'] = False
        video_deal['reply'] = False
        video_deal['follow'] = False
        video_deal['show_times'] = 1
        ############# 测试 each function end ##########
        logger.info(video_deal)
        time.sleep(3)  # 等待3s
        while True:  # 浏览的主循环
            # 验证码处理
            vericaiton_state = self.deal_verication_pic()  # 0 无验证       1  环形      2 图片拖动
            if vericaiton_state != 0:
                self.deal_the_img(vericaiton_state == 1)
            if video_deal['show_times'] == 0:
                time.sleep(random.random() * 5 + 4)
                return
                ########### 视频处理逻辑 ##############
            # try:
            # 更新视频的状态
            self.update_the_video_state()
            # 下一个视频
            next_video = self.comments_pass_next_video(video_deal['show_times'])
            if next_video:
                logger.info('next video...')
                self.next_video()
                break
            if not self.this_video_process['process_over']:
                # 获取评论
                # self.comments_get_comments()
                # 点赞
                if video_deal['love']:
                    self.comments_love_the_video()
                    video_deal['love'] = False
                # 关注
                if video_deal['follow']:
                    self.comments_click_the_follow()
                    video_deal['follow'] = False
                # 评论
                if video_deal['reply']:
                    self.comments_reply_the_video()
                    video_deal['reply'] = False
                # 喜欢某个评论
                if video_deal['love_comment']:
                    self.comments_click_love_comment()
                    video_deal['love_comment'] = False
            else:
                # 滑动评论
                if random.random() < 0.5:
                    self.scoll_down_comments()
            time.sleep(3)
            # except Exception as e:
            #     logger.info(e)

    # 单次播放完成
    def update_the_video_state(self):
        # 播放率
        _play_time_ratio = self.comments_get_the_video_timebar()  # 视频播放完成度
        saved_time_ratio = self.this_video_process['play_time_ratio']
        if _play_time_ratio < float(saved_time_ratio):
            self.this_video_process['show_times'] += 1
        # 播放完成一遍
        else:
            ...  # 没能播放完成
        self.this_video_process['play_time_ratio'] = _play_time_ratio  # update the value

        # 操作完成了吗
        video_deal = random_generate_deals()
        if video_deal['love'] or video_deal['love_comment'] or video_deal['reply'] or video_deal['follow']:
            self.this_video_process['process_over'] = False
        else:
            self.this_video_process['process_over'] = True

    # 判断是否需要下一个
    def comments_pass_next_video(self, _show_times) -> False:
        if self.this_video_process["show_times"] >= _show_times:
            # 这个视频播放完成

            return True
        # 视频没播放完成
        return False

    def get_tk_website(self):
        '''
        :return:
        '''
        self.add_user_session()  # 登录
        self.get_first_url()  # 前面模拟视频
        # self.debug_stop()It is great
        while True:
            self.deal_one_video()
            # self.get_target_url('https://www.tiktok.com/@wandi_cianjur/video/7203640240408448282')

    # 对指定视频进行关注性的播放，love reply and so on
    def get_target_url(self, target_url, comments_content: None):
        self.browser.get(target_url)
        time.sleep(5)
        video_dict = {
            'this_time': 0,  # 这是第几次
            'love': False,
            'reply': False,
            'love_comment': False,
            'watch_times': random.randint(5, 8)  # 本视频的总观看次数
        }
        video_dict['deal_indexs'] = [random.randint(2, video_dict['watch_times'] - 1),
                                     random.randint(2, video_dict['watch_times'] - 1),
                                     random.randint(2, video_dict['watch_times'] - 1)]  # love , reply love_comment
        while True:
            # 验证码处理
            vericaiton_state = self.deal_verication_pic()  # 0 无验证       1  环形      2 图片拖动
            if vericaiton_state != 0:
                self.deal_the_img(vericaiton_state == 1)
            try:
                if self.get_the_video_over_or_not_based_on_timebar():  # 视频播放完毕，就重新refresh
                    self.click_refresh_video()
                    video_dict['this_time'] += 1
                # love_the_video
                if video_dict['this_time'] == video_dict['deal_indexs'][0] and not video_dict['love']:
                    self.love_the_video()
                    video_dict['love'] = True
                # reply_the_video
                if video_dict['this_time'] == video_dict['deal_indexs'][1] and not video_dict['reply']:
                    self.reply_the_video(comments_content)
                    video_dict['reply'] = True
                # click_love_comment
                if video_dict['this_time'] == video_dict['deal_indexs'][2] and not video_dict['love_comment']:
                    self.click_love_comment()
                    video_dict['love_comment'] = True
                # 关注
                #     self.comments_click_the_follow()
                if video_dict['this_time'] == video_dict['watch_times']:
                    if not video_dict['love']:
                        self.love_the_video()
                    if not video_dict['reply']:
                        self.reply_the_video()
                    if not video_dict['love_comment']:
                        self.click_love_comment()
                        break
                if video_dict['love_comment']:
                    self.scoll_down_comments()
                time.sleep(3)
            except Exception as e:
                logger.info(e)
        logger.success('Over the video')

    # FORYOU PAGE
    def get_the_video_show_attr(self):
        video_show_element = self.browser.find_element(By.XPATH, './/div[contains(@id, "xgwrapper-")]')
        video_show_attr = video_show_element.get_attribute('class')
        if 'xgplayer-inactive' in video_show_attr:  # 观看视频超过3秒，返回
            return 1
        if 'xgplayer-pause' in video_show_attr:  # 暂停
            return 3
        return 2  # 距离视频开头不到3s或者暂定后开始不到3s

    # 根据xpath点击子元素
    def click_element_based_father(self, xpath_pattern, father_dot=None):
        if father_dot:
            birth_year = father_dot.find_element(By.XPATH, xpath_pattern)
        else:
            birth_year = self.browser.find_element(By.XPATH, xpath_pattern)
        webdriver.ActionChains(self.browser).move_to_element(birth_year).perform()
        webdriver.ActionChains(self.browser).click(birth_year).perform()
        return birth_year

    def scoll_to_bottom(self):
        pass

    # def scoll_to_bottom(self):
    #     js = "window.scrollBy(0, 1000)"
    #     self.browser.execute_script(js)  # 模拟鼠标滚轮，滑动页面至底部
    #     response = self.browser.page_source
    #     # with open('test.html', 'w', encoding='utf-8') as f:
    #     #     f.write(response)
    #     # 解析响应
    #     html = etree.HTML(response)
    #     this_data_num = self.parse_html_page(html)
    #     print('the last_data is {}; this data is{}'.format(self.last_data_num, this_data_num))
    #     if this_data_num == self.last_data_num:
    #         if self.deal_verication_pic(html) != 0:
    #             h1 = input('verication is need')
    #             self.scoll_to_bottom()
    #         print('scoll to the bottom')
    #         ht = input('input over')
    #         with open('test.html', 'w', encoding='utf-8') as f:  # 保存此时的页面
    #             f.write(response)
    #         print(this_data_num)
    #     else:
    #         self.last_data_num = this_data_num  # 保存此次的值
    #         self.scoll_to_bottom()

    # 抓取评论

    ################ COMMENTS PAGE ###############
    def comments_love_the_video(self):
        self.wait_xpath('.//div[contains(@class, "DivFlexCenterRow")]')
        comment_love_element = self.browser.find_element(By.XPATH,
                                                         './/div[contains(@class, "DivFlexCenterRow")]/button[1]')
        webdriver.ActionChains(self.browser).move_to_element(comment_love_element).perform()
        logger.info('Click the love in the comments page')

    # 评论页面 返回foryou 页面
    def return_foryou(self):
        return_button_xpath = './/button[@data-e2e="browse-close"]'
        self.wait_xpath(return_button_xpath)
        return_button = self.browser.find_element(By.XPATH, return_button_xpath)
        self.browser.execute_script("arguments[0].click();", return_button)

    # replay
    def comments_reply_the_video(self, comments_content=None):
        send_out_button = self.is_exist('.//div[@data-e2e="comment-post"]')
        if send_out_button == False:
            return
        self.wait_xpath('.//div[@data-e2e="comment-input"]')
        repley_area = self.browser.find_element(By.XPATH, './/div[@data-e2e="comment-input"]')
        # 等待元素加载完成，然后进行交互

        webdriver.ActionChains(self.browser).click(repley_area).perform()
        self.browser.execute_script("arguments[0].click();", repley_area)
        # 通过模拟键盘打字
        this_comment = comments_content if comments_content is not None else generate_comments()  # 生成评论
        type_write_sentence(this_comment)  # pyautogui 来输入文字
        # # 发布
        self.delete_clean_img()
        webdriver.ActionChains(self.browser).click(send_out_button).perform()
        self.browser.execute_script("arguments[0].click();", send_out_button)
        logger.success('succeed to send one comment: {}'.format(this_comment))

    # next button
    def comments_click_next_button(self):
        self.wait_xpath('.//button[@data-e2e="arrow-right"]')
        self.click_element_based_father('.//button[@data-e2e="arrow-right"]')
        logger.success('succeed to click the next button')

    # 主页视频页面
    def comments_get_comments(self) -> list:
        # 获取前 n 条评论
        comments_list = []
        self.wait_xpath('.//div[contains(@class,"DivCommentListContainer")]')
        response = self.browser.page_source
        html = etree.HTML(response)
        comments_texts = html.xpath('.//div[contains(@class,"DivCommentListContainer")]//p['
                                    '@data-e2e="comment-level-1"]/span/text()')  # ('.//p[contains(@class,
        # "PCommentText")]/span/text()')
        if len(comments_texts) > 1:
            for comment in comments_texts:
                comments_list.append(comment)
        logger.info('succeed to grap the comments!!!')
        logger.info('comments_list is {}'.format(comments_list[0]))
        return comments_list

    def error_page_save(self):
        html = self.browser.page_source
        with open(os.path.join(Error_Html_Dir, 'time.html'), 'w', encoding='utf-8') as f:  # 保存此时的页面
            f.write(html)

    # 获取视频的时间轴
    def comments_get_the_video_timebar(self) -> float:
        # 视频是否结束DivSeekBarTimeContainer
        html = self.browser.page_source
        from lxml import etree
        html = etree.HTML(html)
        patter = './/*[contains(@class,"DivSeekBarTimeContainer")]/text()'
        res = html.xpath(patter)
        if len(res) == 0:
            return 0
        bartime_video = res[0]
        logger.info('this video time is: %s' % bartime_video)
        if '/' not in bartime_video:
            self.error_page_save()
            return 0
        current_time, whole_time = bartime_video.split('/')
        current_time = current_time.strip()
        whole_time = whole_time.strip()
        # 总时长 和 部分时长的转换 单位 s
        current_time = string_2_time(current_time)
        whole_time = string_2_time(whole_time)
        return float(current_time / whole_time)

    # follow the creator
    def comments_click_the_follow(self):
        follow_button = self.browser.find_element(By.XPATH, './/button[@data-e2e="browse-follow"]')
        if follow_button.text == "关注":
            self.browser.execute_script("arguments[0].scrollIntoView();", follow_button)
            self.browser.implicitly_wait(random.randint(1, 2))
            self.browser.execute_script("arguments[0].click();", follow_button)
            logger.success("succeed to follow the creator")

    # 喜欢某个评论
    def comments_click_love_comment(self):
        # 点击喜欢
        comments_containers = self.is_exist_elements('.//div[contains(@class,"DivCommentItemContainer")]')
        if comments_containers == False or len(comments_containers) == 0:
            return
        range_biggest = 10 if len(comments_containers) > 11 else len(comments_containers) - 1
        # which comments
        comments_container = comments_containers[random.randint(0, range_biggest)]
        comments_svg = comments_container.find_element(By.XPATH, './/div[@data-e2e="comment-like-icon"]')  #

        self.mouth_move_element_center()
        run_result = False
        while not run_result:
            try:
                webdriver.ActionChains(self.browser).click(comments_svg).perform()
                run_result = True
            except:
                pyautogui.scroll(-200 + random.randint(0, 10))
                time.sleep(random.random() + 0.3)
        self.browser.implicitly_wait(random.random() * 3 + 2)

        logger.info('click the love for which comment')

    # 评论区 下滑
    def scoll_down_comments(self):
        screen_width, screen_height = pyautogui.size()
        pyautogui.moveTo(int(0.8 * screen_width), 0.7 * screen_height)
        pyautogui.scroll(-300 + random.randint(0, 15))
        time.sleep(random.random() + 1)
        if random.random() < 0.4:
            pyautogui.scroll(40 - random.randint(0, 5))
            time.sleep(random.random() + 1)
        if random.random() < 0.85:
            pyautogui.scroll(-200 + random.randint(0, 10))
            time.sleep(random.random() + 1)
        logger.info('scoll down the comments')

    # 主页视频页面
    def get_comments(self) -> list:
        # 获取前 n 条评论
        comments_list = []
        self.smooth_move_mource(1000)
        self.browser.implicitly_wait(10)
        self.wait_xpath('.//p[contains(@class,"PCommentText")]')
        response = self.browser.page_source
        html = etree.HTML(response)
        comments_texts = html.xpath('.//p[contains(@class,"PCommentText")]/span/text()')
        if len(comments_texts) > 1:
            for comment in comments_texts:
                comments_list.append(comment)
        logger.info('succeed to grap the comments!!!')
        return comments_list

    def next_video(self):
        pyautogui.press('pgdn')  # 按下down
        self.comments_click_next_button()

    # 获取视频的时间轴
    def get_the_video_over_or_not_based_on_timebar(self):
        # 视频是否结束
        html = self.browser.page_source
        from lxml import etree
        html = etree.HTML(html)
        patter = './/*[contains(@class,"DivSeekBarTimeContainer")]/text()'
        res = html.xpath(patter)
        if len(res) == 0:
            return
        bartime_video = res[0]
        logger.info('this video time is: %s' % bartime_video)
        if '/' not in bartime_video:
            self.error_page_save()
            return
        current_time, whole_time = bartime_video.split('/')
        current_time = current_time.strip()
        whole_time = whole_time.strip()
        return whole_time == current_time

    # replay
    def reply_the_video(self, comments_content=None):
        send_out_button = self.is_exist('.//div[@data-e2e="comment-post"]')
        if send_out_button == False:
            return
        self.wait_xpath('.//div[contains(@class,"public-DraftEditorPlaceholder-root")]')
        repley_area = self.browser.find_element(By.XPATH,
                                                './/div[contains(@class,"public-DraftEditorPlaceholder-root")]')
        # 等待元素加载完成，然后进行交互
        self.move_to_top_page()
        self.browser.execute_script("arguments[0].scrollIntoView();", repley_area)
        self.browser.execute_script("arguments[0].click();", repley_area)
        # 通过模拟键盘打字
        this_comment = comments_content if comments_content is not None else generate_comments()  # 生成评论
        type_write_sentence(this_comment)  # pyautogui 来输入文字
        # # 发布
        webdriver.ActionChains(self.browser).click(send_out_button).perform()
        self.browser.execute_script("arguments[0].click();", send_out_button)
        logger.success('succeed to send one comment: {}'.format(this_comment))

    # 鼠标移动到元素中心
    def mouth_move_element_center(self):
        '''
        :param containers: # 获取元素
        :return:
        '''
        # 获取元素中心的x和y坐标
        # center_x = containers.location['x'] + containers.size['width'] / 2
        # center_y = containers.location['y'] + containers.size['height'] / 2
        # 创建ActionChains对象
        # webdriver.ActionChains(self.browser).move_to_element(containers).perform()
        screen_width, screen_height = pyautogui.size()
        pyautogui.moveTo(int(0.8 * screen_width), 0.7 * screen_height)

    # 喜欢某个评论
    def click_love_comment(self):
        # 点击喜欢
        comments_containers = self.is_exist_elements('.//div[contains(@class,"DivCommentItemContainer")]')
        if comments_containers == False or len(comments_containers) == 0:
            return
        range_biggest = 10 if len(comments_containers) > 11 else len(comments_containers) - 1
        # which comments
        comments_container = comments_containers[random.randint(0, range_biggest)]
        comments_svg = comments_container.find_element(By.XPATH, ".//*[name()='svg']")  #
        self.mouth_move_element_center()
        run_result = False
        while not run_result:
            try:
                webdriver.ActionChains(self.browser).click(comments_svg).perform()
                run_result = True
            except:
                pyautogui.scroll(-200 + random.randint(0, 10))
                time.sleep(random.random() + 0.3)
        self.browser.implicitly_wait(random.random() * 3 + 2)

        logger.info('click the love for which comment')

    # 点击视频的refresh
    def click_refresh_video(self):
        res = self.is_exist('.//div[contains(@class,"DivPlayIconContainer")]')
        if res:
            refresh_button = self.browser.find_element(By.XPATH, './/div[contains(@class,"DivPlayIconContainer")]')
            self.browser.execute_script("arguments[0].click();", refresh_button)
            return True
        return False

    def move_to_top_page(self):
        # 获取页面顶部元素
        top_element = self.browser.find_element(By.TAG_NAME, 'body')
        # 滑动到页面顶部
        self.browser.execute_script("arguments[0].scrollIntoView();", top_element)
        time.sleep(2)

    def love_the_video(self):
        self.move_to_top_page()
        actionbar_container = self.browser.find_element(By.XPATH, './/div[contains(@class,"DivActionItemContainer")]')
        loving_video_button = actionbar_container.find_element(By.XPATH, './/button')
        self.browser.implicitly_wait(random.randint(1, 3))
        webdriver.ActionChains(self.browser).move_to_element(loving_video_button).perform()
        webdriver.ActionChains(self.browser).click(loving_video_button).perform()
        logger.success('succeed to love this video')

    def click_the_video_comment_button(self, father_node=None):
        if father_node is None:
            father_node = self.browser
        self.smooth_move_mource(0)
        self.wait_xpath('.//div[contains(@class,"DivActionItemContainer")]')
        actionbar_container = father_node.find_element(By.XPATH, './/div[contains(@class,"DivActionItemContainer")]')
        self.browser.execute_script("arguments[0].scrollIntoView();", actionbar_container)
        video_comment_button = actionbar_container.find_element(By.XPATH, './/button[2]')
        self.browser.implicitly_wait(random.random() * 3 + 1)
        # webdriver.ActionChains(self.browser).move_to_element(loving_video_button).perform()
        webdriver.ActionChains(self.browser).click(video_comment_button).perform()
        logger.success('succeed to click the video comment button, then enter the main page')

    def deal_verication_pic(self):
        response = self.browser.page_source
        html = etree.HTML(response)
        # this_data_num = self.parse_html_page(html)
        verication = html.xpath('.//div[contains(@class,"captcha_verify_container")]')  # 验证码块
        if verication:
            cirlce_element = html.xpath('.//div[@class="sc-jTzLTM kuTGKN"]/img[2]/@src')  # 环形
            if cirlce_element:
                return 1
            else:
                picture_element = html.xpath('.//div[contains(@class,"captcha_verify_img--wrapper")]/img[2]/@src')  # 图片
                if picture_element:
                    return 2
        return 0

    # 模拟滚轮滑动页面
    def smooth_move_mource(self, distance=0):
        js = "window.scrollBy(0, %s)" % distance
        self.browser.execute_script(js)  # 模拟鼠标滚轮，滑动页面

    def click_refresh_verication_img(self):
        refresh_a = self.browser.find_element(By.XPATH, './/a[contains(@class,"secsdk_captcha_refresh")]')
        self.browser.execute_script("arguments[0].click();", refresh_a)

    def parse_html_page(self, html):  # 解析 html页面
        video_url = html.xpath('.//div[@data-e2e="user-post-item"]//a/@href')
        return len(video_url)

    def debug_stop(self):
        while 1:
            pass

    def deal_the_img(self, circle=True):
        # img 外部容器
        img_outer_container = None
        this_xpath_pattern = None  # 图片 二维码 pattern
        if circle:  # 外环
            this_xpath_pattern = './/div[@class="sc-jTzLTM kuTGKN"]'
            img_outer_container = self.browser.find_element(By.XPATH, this_xpath_pattern)
        else:  # 图片
            this_xpath_pattern = './/div[contains(@class,"captcha_verify_img--wrapper")]'
            img_outer_container = self.browser.find_element(By.XPATH, this_xpath_pattern)
        # 外圈图片   背景图片
        outer_pic = img_outer_container.find_element(By.XPATH, './img[1]')
        outer_pic = outer_pic.get_attribute('src')
        common_download_image(outer_pic, 'outer.png')  # 下载图片
        # 内圈图片   目标小图片
        inner_pic = img_outer_container.find_element(By.XPATH, './img[2]')
        inner_pic = inner_pic.get_attribute('src')
        # 下载到本地
        common_download_image(inner_pic, 'inner.png')  # 下载图片
        print('have download the two picture')
        # 验证码本地识别
        distance = None  # 需要拖动的距离
        if circle:
            angle = tk_circle_discern('inner.png', 'outer.png')
            distance = angle / 180 * (344 - 60)
        else:
            distance = ddddOcr_tk('inner.png', 'outer.png')
            distance = distance * 0.62
        this_track = [int(distance // 4), int(distance // 4), -5, -2, int(distance * 0.3), int(distance * 0.2) + 5,
                      -8]  # 模拟鼠标拖动的点移
        this_track.append(int(distance) - sum(this_track))
        self.hold_on_slide(this_track)  # 拖动滑块 模拟移动
        self.judge_the_img_src_change(this_xpath_pattern + '/img[2]/@src', inner_pic, circle)

    # 判断验证码是否改变， 验证成功后验证码消失，或者失败验证码refresh
    def judge_the_img_src_change(self, this_xpath_pattern, last_inner_img_url: str, circle):
        this_xpath_pattern = this_xpath_pattern  # inner_img_url pattern
        response = self.browser.page_source
        html = etree.HTML(response)
        verication = html.xpath('.//div[contains(@class,"captcha_verify_container")]')  # 验证码块
        import time
        if verication:
            img_src = html.xpath(this_xpath_pattern)  # 验证码图片
            if len(img_src) == 1 and img_src[0] != last_inner_img_url:  # 验证码已经改变
                # self.browser.implicitly_wait(5)
                print("img_src%s" % img_src)
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
            slider = self.browser.find_element(By.XPATH, './/div[contains(@class,"secsdk-captcha-drag-icon")]')
            # 鼠标点击并按住不松
            webdriver.ActionChains(self.browser).click_and_hold(slider).perform()
            # 让鼠标随机往下移动一段距离
            webdriver.ActionChains(self.browser).move_by_offset(xoffset=0, yoffset=100).perform()
            time.sleep(0.15)
            for item in tracks:
                webdriver.ActionChains(self.browser).move_by_offset(xoffset=item,
                                                                    yoffset=random.randint(-1, 1)).perform()
                time.sleep(random.uniform(0.02, 0.15))
            # 稳定一秒再松开
            time.sleep(1)
            webdriver.ActionChains(self.browser).release().perform()
            time.sleep(1)
        except Exception as e:
            print(e)

    def update_user_avatar(self):
        '''
        :return:
        '''
        self.browser.get('https://www.tiktok.com/signup')
        self.read_cookies()
        self.browser.get('https://www.tiktok.com/foryou')
        # self.browser.maximize_window()
        # tjs = input('wating')
        time.sleep(5)
        tiktok_name = self.get_name_tiktok()
        self.browser.get('https://www.tiktok.com/@%s' % tiktok_name)  # 个人主页
        time.sleep(10)

        vericaiton_state = self.deal_verication_pic()  # 0 无验证       1  环形      2 图片拖动
        if vericaiton_state != 0:
            self.deal_the_img(vericaiton_state == 1)

        # 主页编辑按钮
        self.wait_xpath('.//button[contains(@class,"StyledEditButton")]')
        self.click_element_based_father('.//button[contains(@class,"StyledEditButton")]')
        # 个人avatar 点击
        time.sleep(3)
        self.wait_xpath('.//div[contains(@class,"DivAvatarEditIcon")]')
        self.click_element_based_father('.//div[contains(@class,"DivAvatarEditIcon")]')
        # upload img
        time.sleep(3)
        self.uploadWinFile()
        # 确定图片改变
        time.sleep(2)
        self.wait_xpath('.//div[contains(@class,"DivFooterContainer")]/button[2]')
        self.click_element_based_father('.//div[contains(@class,"DivFooterContainer")]/button[2]')
        time.sleep(4)
        # 保存图片
        self.wait_xpath('.//button[@data-e2e="edit-profile-save"]')
        self.click_element_based_father('.//button[@data-e2e="edit-profile-save"]')
        time.sleep(10)

    def uploadWinFile(self):
        '''
        通过Windows系统上传文件
        '''
        import glob
        user_avter_files = glob.glob(os.path.join(User_Avter_Dir, '*.jpg')) + \
                           glob.glob(os.path.join(User_Avter_Dir, '*.png'))
        if len(user_avter_files) == 0:
            logger.error('The avter is over')
        user_avter_files = sorted(user_avter_files, key=lambda name: int(name.split('\\')[-1][:-4]))
        filepath = user_avter_files[0]  # 选取第一个
        try:
            time.sleep(1)
            pyautogui.write(filepath)  # 输入文件绝对路径
            time.sleep(1)
            pyautogui.press('enter', 2)  # 按2次回车键（按2次是为了防止出错）
            time.sleep(1)
            os.remove(filepath)
        except Exception as e:
            logger.error('Upload picture failed!!!')
        return filepath

    # 获取tiktok的用户名,用于判断是否登录成功，同时获取uesr主页地址
    def get_name_tiktok(self):
        if 'foryou' not in self.browser.current_url:
            self.browser.get('https://www.tiktok.com/foryou')
            time.sleep(5)
        html = self.browser.page_source
        html = etree.HTML(html)
        patter = './/script[@id="SIGI_STATE"]/text()'  #::*[contains(@class, "xgwrapper")]
        res = html.xpath(patter)
        if res:
            text = res[0]
            pattern = r'"nickName":"([^"]+)"'
            # 使用 re.search() 函数进行匹配，返回一个 Match 对象
            match_obj = re.search(pattern, text)
            # 如果匹配成功，可以使用 group() 方法获取捕获的部分
            if match_obj:
                nickname = match_obj.group(1)
                return nickname
        return False


# 生成评论
def generate_comments():
    comments = [
        'loving',
        'I like it',
        'I love it',
        "It is great",
        "It is wonderful",
        "It is fantastic",
        "I enjoy it",
        "It is awesome",
        "It is amazing",
        "I am fond of it",
        "I am into it",
        "It is my favorite"
    ]
    random_index = random.randint(0, len(comments) - 1)
    return comments[random_index]


# 时间格式转换
def string_2_time(string: str):
    '''
    :param string: '00:15'
    :return:
    '''
    return int(string.split(":")[0]) * 60 + int(string.split(":")[1])


# 文本键入到框内
def type_write_sentence(text):
    import pyperclip
    import time
    # 复制文本到剪切板
    pyperclip.copy(text)
    # 模拟Ctrl+V键盘快捷键粘贴文本
    pyautogui.hotkey('ctrl', 'v')
    # 等待0.1秒以确保文本已被键入


# 随机生成 视频的操作
def random_generate_deals():
    video_deal = {}
    # follow
    video_deal['follow'] = True if random.random() < 0.1 else False
    # love
    love_actor = 0.2
    if video_deal['follow']:
        love_actor = 0.68
    video_deal['love'] = True if random.random() < love_actor else False
    # reply
    reply_actor = 0.4
    if video_deal['love']:
        reply_actor = 0.7
    video_deal['reply'] = True if random.random() < reply_actor else False
    # love comment
    video_deal['love_comment'] = True if random.random() < 0.3 else False
    # show time
    video_deal['show_times'] = 1 if random.random() < 0.85 else 0

    if video_deal['follow'] or video_deal['love']:
        video_deal['show_times'] = random.randint(1, 3)
    elif video_deal['reply'] or video_deal['love_comment']:
        video_deal['show_times'] = 1
    return video_deal