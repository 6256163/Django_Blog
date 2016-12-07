# coding=utf-8
import os
from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase

# Create your tests here.
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import *




class RegisterTests(StaticLiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super(RegisterTests, cls).setUpClass()
        path =os.getcwd()
        chromedriver = path+"/selenium_test/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        cls.selenium = WebDriver(chromedriver)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(RegisterTests, cls).tearDownClass()

    def logout(self):
        setting = self.selenium.find_element_by_link_text(u'设置')
        chain = ActionChains(self.selenium)
        chain.move_to_element(setting).perform()
        sleep(1)
        logout = self.selenium.find_element_by_id("logout")
        logout.click()

    def regsiter(self,username,email,password,password_confirm,first_name,last_name, ifm=True, submit=True):
        register = self.selenium.find_element_by_id("text_register")
        register.click()
        if ifm:
            self.selenium.switch_to.frame('ifm_image')
        username_input = self.selenium.find_element_by_id("reg_username")
        chain = ActionChains(self.selenium)
        chain.click(username_input).perform()
        username_input.send_keys(username)
        email_input = self.selenium.find_element_by_id("reg_email")
        chain.click(email_input).perform()
        email_input.send_keys(email)
        password_input = self.selenium.find_element_by_id("reg_password")
        chain.click(password_input).perform()
        password_input.send_keys(password)
        password_confirm_input = self.selenium.find_element_by_id("reg_password_confirm")
        chain.click(password_confirm_input).perform()
        password_confirm_input.send_keys(password_confirm)
        first_name_input = self.selenium.find_element_by_id("id_first_name")
        chain.click(first_name_input).perform()
        first_name_input.send_keys(first_name)
        last_name_input = self.selenium.find_element_by_id("id_last_name")
        chain.click(last_name_input).perform()
        last_name_input.send_keys(last_name)
        if submit:
            self.selenium.find_element_by_id('register_form').submit()
        if ifm:
            self.selenium.switch_to.default_content()


    def login(self):
        login = self.selenium.find_element_by_id("text_login")
        login.click()
        username_input = self.selenium.find_element_by_id("id_username")
        username_input.send_keys('admin')
        password_input = self.selenium.find_element_by_id("id_password")
        password_input.send_keys('adminadmin')
        self.selenium.find_element_by_id('login_form').submit()

    def test_1_register(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/blog/'))
        self.regsiter(username='admin',
                      password='adminadmin',
                      password_confirm='adminadmin',
                      email='admin@dahsk.com',
                      first_name='asdasda',
                      last_name='dasasd')
        self.selenium.switch_to.frame('ifm_image')
        self.assertEqual( u'登录成功' in self.selenium.switch_to.active_element.text, True)
        sleep(6)
        #检查登陆名称的正确
        self.assertEqual(self.selenium.find_element_by_xpath('//*[@id="nva"]/div/div[1]/li[1]/div/p/a').text, 'admin')
        self.logout()

    def test_2_register(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/blog/'))
        self.regsiter(username='abcdefghijkl@',
                      password='adminadmin',
                      password_confirm='adminadmin',
                      email='admin@dahsk.com',
                      first_name='asdasda',
                      last_name='dasasd',
                      submit=False)
        ifm = self.selenium.find_element_by_id('ifm_image')
        self.selenium.switch_to.frame(ifm)
        self.assertEqual(self.selenium.find_element_by_id("username_error").text, u'× 用户名包含特殊字符或长度不符')
        self.assertEqual(self.selenium.find_element_by_id("email_succe").text, u'√')
        self.assertEqual(self.selenium.find_element_by_id("password_succe").text, u'√')
        self.assertEqual(self.selenium.find_element_by_id("password_confirm_succe").text, u'√')
        self.selenium.find_element_by_id('register_form').submit()
        self.assertEqual(self.selenium.find_element_by_id("register_error").text, u'用户名不正确')
        chain = ActionChains(self.selenium)
        chain.click(self.selenium.find_element_by_id('x_register'))


    def test_3_register(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/blog/'))
        self.regsiter(username='abcdefghijkl',
                      password='adminadmin',
                      password_confirm='adminadmin',
                      email='admin.dahsk.com',
                      first_name='asdasda',
                      last_name='dasasd',
                      submit=False)
        ifm = self.selenium.find_element_by_id('ifm_image')
        self.selenium.switch_to.frame(ifm)
        self.assertEqual(self.selenium.find_element_by_id("username_succe").text, u'√')
        self.assertEqual(self.selenium.find_element_by_id("email_error").text, u'× 邮箱地址有误')
        self.assertEqual(self.selenium.find_element_by_id("password_succe").text, u'√')
        self.assertEqual(self.selenium.find_element_by_id("password_confirm_succe").text, u'√')
        self.selenium.find_element_by_id('register_form').submit()
        self.assertEqual(self.selenium.find_element_by_id("register_error").text, u'邮箱格式不正确')
        self.assertEqual(self.selenium.find_elements_by_css_selector('.errorlist li')[0].text, u'请输入合法的邮件地址。')
        chain = ActionChains(self.selenium)
        chain.click(self.selenium.find_element_by_id('x_register'))

"""
    def test_2_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/blog/'))
        self.regsiter()
        sleep(6)
        self.logout()
        self.login()
        #检查登陆名称的正确
        self.assertEqual(self.selenium.find_element_by_xpath('//*[@id="nva"]/div/div[1]/li[1]/div/p/a').text, 'admin')

    def test_21_post_blog(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/blog/'))
        self.regsiter()
        sleep(6)


    def test_3_logout(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/blog/'))
        self.regsiter()
        self.logout()
        #检查登录链接的显示正确
        self.assertEqual(self.selenium.find_element_by_id("text_login").text, u'登录')
"""

