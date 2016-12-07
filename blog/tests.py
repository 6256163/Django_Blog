# coding=utf-8
import datetime
from dateutil import parser
from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from blog.models import Blog, Reply
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver

class BlogViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'admin'
        self.password = 'admin'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.blog_title = u"新建blog测试——标题"
        self.blog_text = u"新建blog测试——内容"
        self.reply_text = "reply test blog"
        self.blog = Blog.objects.create(blog_title=self.blog_title, blog_text=self.blog_text,
                                        user=self.user, latest_reply_user=self.user)
        self.reply = Reply.objects.create(reply_text=self.reply_text, blog=self.blog, user=self.user)

    def prepare_data(self):
        pass

    # 测试 blog新建
    def test_create_blog(self):
        response = self.client.post('/blog/', {
            'blog_title': self.blog_title,
            'blog_text': self.blog_text,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.data['pub_date'][:19], response.data['latest_reply'][:19])
        self.assertEqual(response.data['latest_reply_user'], self.user.username)
        self.assertEqual(response.data['reply_counter'], 0)

    # 测试 blog查询
    def test_list_blog(self):
        response = self.client.get('/blog/', {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['blog']['results']), 1)
        self.assertEqual(response.data['blog']['results'][0]['blog_title'], self.blog_title)
        self.assertEqual(response.data['blog']['results'][0]['blog_text'], self.blog_text)
        self.assertEqual(response.data['blog']['results'][0]['latest_reply_user'], self.user.username)
        self.assertEqual(response.data['blog']['results'][0]['pub_date'][:19],
                         response.data['blog']['results'][0]['latest_reply'][:19])

    # 测试 blog详细内容查询
    def test_retrieve_blog(self):
        url = '/blog/' + str(self.blog.id) + '/'
        response = self.client.get(url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['blog']['blog_title'], self.blog_title)
        self.assertEqual(response.data['blog']['blog_title'], self.blog_title)
        self.assertEqual(response.data['blog']['blog_text'], self.blog_text)
        self.assertEqual(response.data['blog']['latest_reply_user'], self.user.username)
        self.assertEqual(response.data['blog']['pub_date'][:19],
                         response.data['blog']['latest_reply'][:19])
        self.assertEqual(len(response.data['replies']['results']), 1)
        self.assertEqual(response.data['replies']['results'][0]['reply_text'], self.reply_text)
        self.assertEqual(response.data['replies']['results'][0]['floor'], 2)


class ReplyViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'admin'
        self.password = 'admin'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.blog_title = u"新建blog测试——标题"
        self.blog_text = u"新建blog测试——内容"
        self.reply_text = "reply test blog"
        self.blog = Blog.objects.create(blog_title=self.blog_title, blog_text=self.blog_text,
                                        user=self.user, latest_reply_user=self.user)
        self.reply = Reply.objects.create(reply_text=self.reply_text, blog=self.blog, user=self.user)

    # test create reply test
    def test_create_reply(self):
        b = self.client.post('/blog/', {
            'blog_title': self.blog_title,
            'blog_text': self.blog_text,
        })
        response = self.client.post('/replies/', {
            'reply_text': self.reply_text,
            'blog': b.data['url']
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['blog'], b.data['url'])
        self.assertEqual(response.data['floor'], 2)
        self.assertEqual(response.data['reply_text'], self.reply_text)
        self.assertEqual(response.data['user'], self.user.username)
        self.assertEqual(response.data['reply_counter'], 0)


class ReplyInReplyViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'admin'
        self.password = 'admin'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.blog_title = u"新建blog测试——标题"
        self.blog_text = u"新建blog测试——内容"
        self.reply_text = "reply test blog"
        self.blog = Blog.objects.create(blog_title=self.blog_title, blog_text=self.blog_text,
                                        user=self.user, latest_reply_user=self.user)
        self.reply = Reply.objects.create(reply_text=self.reply_text, blog=self.blog, user=self.user)


    #test: create lzl test
    def test_create_lzl(self):
        b = self.client.post('/blog/', {
            'blog_title': self.blog_title,
            'blog_text': self.blog_text,
        })
        r = self.client.post('/replies/', {
            'reply_text': self.reply_text,
            'blog': b.data['url']
        })
        reply_url=r.data['url']
        reply_id = r.data['id']
        print(reply_id)
        response = self.client.post('/reply_in_reply/',{
            'reply_text':self.reply_text,
            'reply':reply_url
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['reply'], r.data['url'])
        self.assertEqual(response.data['reply_text'], self.reply_text)
        self.assertEqual(response.data['user'], self.user.username)
        self.assertEqual(parser.parse(response.data['pub_date']).date(),datetime.datetime.now().date())


