import http.cookiejar
import tkinter
import urllib.request
import hashlib
import tkinter.messagebox
from urllib import parse

from PIL import ImageTk
from PIL import Image

from config import Config
from downloader import DownLoader
from resource import Resource
from stu_parser import StuParser


# 产生MD5，用来给密码加密
def get_md5(data):
    md5 = hashlib.md5()
    md5.update(data.encode('utf-8'))
    return md5.hexdigest()


# 注意要传一个Frame/Tk参数给ReCalendar类，并调用父类的初始化函数，否则在Tk类生成之前有些事情无法干，比如预设值什么的
class ReCalendar(tkinter.Tk):
    id = None  # 学号
    pwd = None  # 密码是MD5加密之后的
    img = None  # 验证码的图片
    xdvfb = None  # 验证码
    csrftoken = None  # 查询页面的令牌
    opener = None  # 保存cookie的opener，每次登录用这个opener打开

    def __init__(self, **kw):
        super().__init__(**kw)  # 父类的初始化工作
        id_c, pwd_c = Config.get_configs()
        self.title('ReCalendar')
        self.lab_id = tkinter.Label(text='学号')
        self.lab_pwd = tkinter.Label(text='密码')
        self.che_rem = tkinter.Checkbutton(text='记住密码')
        self.ent_id = tkinter.Entry(textvariable=tkinter.StringVar(value=id_c))  # 预设值
        self.ent_pwd = tkinter.Entry(textvariable=tkinter.StringVar(value=pwd_c))  # 预设值
        self.lab_img = tkinter.Label(image=self.ret_img())
        self.ent_verify_code = tkinter.Entry()
        self.but_login = tkinter.Button(text="登录", command=self.login)
        self.but_get_img = tkinter.Button(text="获取验证码", command=self.change_image)
        self.but_get_scores = tkinter.Button(text='获取总体成绩', command=self.get_gpa_page)
        self.but_QueryStuScore = tkinter.Button(text='获取成绩单', command=self.get_scores_page)
        self.but_get_lesson = tkinter.Button(text='获取课表', command=self.get_lessons_page)
        self.but_create_ics = tkinter.Button(text='生成日历文件', command=self.create_ics)
        self.lab_id.grid(row=0, column=0)
        self.ent_id.grid(row=0, column=1)
        self.lab_pwd.grid(row=1, column=0)
        self.ent_pwd.grid(row=1, column=1)
        self.lab_img.grid(row=2, column=0)
        self.ent_verify_code.grid(row=2, column=1)
        self.but_get_img.grid(row=3, column=0)
        self.che_rem.grid(row=3, column=1)
        self.but_login.grid(row=4, column=1)
        self.but_get_scores.grid(row=5, column=1)
        self.but_QueryStuScore.grid(row=6, column=1)
        self.but_get_lesson.grid(row=7, column=1)
        self.but_create_ics.grid(row=8, column=1)
        self.mainloop()  # 进入消息循环

    # 获取验证码
    def ret_img(self):
        self.get_server_img()
        return self.img

    # 变换验证码，并且让验证码图片变换
    def change_image(self):
        self.get_server_img()
        # 设置图片变化
        self.lab_img.configure(image=self.img)

    # 获取验证码
    def get_server_img(self):
        # 获取验证码//并且要注意一点，每次获取验证码之后，cookie都会随之改变。所以cookie和验证码的获取是绑定的
        # 创建管理cookie的opener
        cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        # 下载验证码
        DownLoader.download_html(self.opener, Resource.img_url, 'img.jpg', None)
        # 显示验证码
        self.img = ImageTk.PhotoImage(Image.open(r'outputs\img.jpg'))

    # 登录时的操作，要获取主页面和一些其他页面
    def login(self):
        self.id = self.ent_id.get()  # 获取填入的id
        self.pwd = self.ent_pwd.get()  # pwd
        id_c, pwd_c = Config.get_configs()
        # 更新配置文件
        if id_c != self.id or id_c == '':  # 如果学号变了则记住学号
            Config.set_id_c(self.id)
        # 如果记住密码的话
        if self.che_rem.getboolean(1):
            Config.set_pwd_c(self.pwd)
        self.xdvfb = self.ent_verify_code.get()
        req = urllib.request.Request(Resource.login_url)
        req = self.packing_header(req)
        # 下面要单独pack
        req.add_header("Referer", "http://210.42.121.241/servlet/Login")
        post_data = parse.urlencode([("id", self.id), ("pwd", get_md5(self.pwd)), ("xdvfb", self.xdvfb)])
        # 登录
        resp = self.opener.open(req, data=post_data.encode("utf-8"))
        if resp != 200:
            tkinter.messagebox.askokcancel('提示', '登录失败，请检查验证码！(或者学号和密码？)')
        # 获取首页面
        self.get_index_page()

    # 给页面包装一些头，让自己看起来不那么像爬虫
    @staticmethod
    def packing_header(request):
        request.add_header("Accept", r"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
        request.add_header("Accept-Language", "zh-CN,zh;q=0.8")
        request.add_header("Cache-Control", "max-age=0")
        request.add_header("Connection", "keep-alive")
        request.add_header("Content-Type", "application/x-www-form-urlencoded")
        request.add_header("Host", "210.42.121.132")
        request.add_header("Origin", "http://210.42.121.132")
        request.add_header("Upgrade-Insecure-Requests", "1")
        request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                         "like Gecko) Chrome/56.0.2924.87 Safari/537.36")
        return request

    def get_index_page(self):
        data_index_page = DownLoader.download_html(self.opener, Resource.index_url, 'index_page.html', None)
        # 查找令牌
        self.csrftoken = StuParser.find_csrftoken(data_index_page)

    def get_lessons_page(self):
        params = urllib.parse.urlencode({'action': 'queryStuLsn', 'csrftoken': self.csrftoken})
        DownLoader.download_html(self.opener, Resource.lessons_url, 'lessons_page.html', params)

    # 从教务系统中获取成绩的页面
    def get_scores_page(self):
        params = urllib.parse.urlencode(
            {'csrftoken': self.csrftoken, 'year': 0, 'term': "", "learnType": "",
             "scoreFlag": 0, "t": ""})
        data_scores_page = DownLoader.download_html(self.opener, Resource.scores_url, 'scores_page.html', params)
        # 获取所有成绩
        StuParser.get_all_scores(data_scores_page)

    def get_gpa_page(self):
        data_gpa_page = DownLoader.download_html(self.opener, Resource.gpa_url, 'gpa_page.html', None)
        StuParser.parse_gpa_page(data_gpa_page)

    @staticmethod
    def create_ics():
        f = open(r'outputs\lessons_page.html', 'r')
        data = f.read()
        f.close()
        schedule = StuParser.generate_schedule(data)
        print(schedule)
        from schedule_to_ics import generate_ics
        generate_ics(schedule)


if __name__ == '__main__':
    re_calendar = ReCalendar()
