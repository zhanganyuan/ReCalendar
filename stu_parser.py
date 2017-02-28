import re
import logging
from bs4 import BeautifulSoup

weekDay = ("一", "二", "三", "四", "五", "六", "日")


def get_lesson_time(day, begin_time, end_time):
    time = '周' + weekDay[int(day) - 1] + '第'
    num = int(end_time) - int(begin_time) + 1
    for count in range(num):
        time += str(int(begin_time) + count)
        if count < num - 1:
            time += ','
    time += '节'
    return time


# 第10-10周|双周
def get_weeks(begin_week, end_week, week_inter_val):
    weeks = '第' + begin_week + '-' + end_week + '周'
    if week_inter_val == 2:  # 如果隔周一次课
        if begin_week % 2 != 0:  # 如果开始周数是奇数
            weeks += '|单周'
        else:
            weeks += '|双周'
    return weeks


# '第1实验楼B403-A'
def get_class_room(area_name, class_room):
    class_room += area_name
    return class_room


# '刘小洋(教授)'
def get_teacher_name(teacher_name, profession_name):
    teacher_name = teacher_name + '(' + profession_name + ')'
    return teacher_name


class StuParser(object):
    @staticmethod
    def parse_gpa_page(html_cont):
        soup = BeautifulSoup(html_cont, "html.parser", from_encoding="gb2312")
        data_table = soup.find("table", class_="listTable")
        print(data_table.get_text())
        data_table.find_all("tr")

    # noinspection PyBroadException
    @staticmethod
    def find_csrftoken(html_cont):
        soup = BeautifulSoup(html_cont, "html.parser", from_encoding="gb2312")
        data = soup.find("div", id="school")
        csrftoken = None
        try:
            csrftoken = re.search(re.compile("\w{8}-\w{4}-\w{4}-\w{4}-\w{12}"), str(data)).group()
        except Exception:
            # 输出错误日志
            logging.basicConfig(level=logging.WARNING,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                datefmt='%a, %d %b %Y %H:%M:%S',
                                filename='logging.conf',
                                filemode='a')
            logging.warning('未获取到令牌，可能没有登录成功！')
        return csrftoken

    @staticmethod
    def get_all_scores(html_cont):
        soup = BeautifulSoup(html_cont, "html.parser", from_encoding="gb2312")
        all_courses = soup.find_all('tr')
        f = open(r'outputs\scores.txt', 'w')
        for course in all_courses:
            f.write(course.get_text())
        f.close()

    @staticmethod
    def generate_schedule(data):
        """
            var lessonName = "虚拟现实技术";//课程名
            var day = "2";//
            var weekDay = new Array("一","二","三","四","五","六","日")
            var beginWeek = "1";//上课时间，从第几周开始
            var endWeek = "18";//上课时间，到第几周结束
            var classNote = "14卓工班";
            var beginTime = "11";//上课时间，从第几节课开始
            var endTime = "13";//上课时间，到第几节课结束
            var detail="1-18周,每1周;11-13节,3区,2-213";//课程的详细信息
            var classRoom = "2-213";//教室
            var weekInterVal= "1";//隔几周一次
            var teacherName = "宋成芳";//任课老师
            var professionName = "讲师";//教师职称
            var planType = "专业选修";
            var credit = "3.0";//课程学分
            var areaName = "3区";
            var weekInterVal = "1";
            var academicTeach = "计算机学院";
            var grade = "2014";
            var classNote = "14卓工班";
            var note = "";
            var state = "0";
        """
        # [课程名，上课时间，周，教室，老师]
        # ['汇编语言程序设计', '周二第7,8节', '第10-10周|双周', '第1实验楼B403-A', '刘小洋(刘小洋)']
        all_lesson_name = re.findall(re.compile(r'var lessonName = "(\S+)";'), data)
        all_day = re.findall(re.compile(r'var day = "(\S+)";'), data)
        all_begin_week = re.findall(re.compile(r'var beginWeek = "(\S+)";'), data)
        all_end_week = re.findall(re.compile(r'var endWeek = "(\S+)";'), data)
        all_begin_time = re.findall(re.compile(r'var beginTime = "(\S+)";'), data)
        all_end_time = re.findall(re.compile(r'var endTime = "(\S+)";'), data)
        all_area_name = re.findall(re.compile(r'var areaName = "(\S+)";'), data)
        all_class_room = re.findall(re.compile(r'var classRoom = "(\S+)";'), data)
        all_week_inter_val = re.findall(re.compile(r'var weekInterVal = "(\S+)";'), data)
        all_teacher_name = re.findall(re.compile(r'var teacherName = "(\S+)";'), data)
        all_profession_name = re.findall(re.compile(r'var professionName = "(\S+)";'), data)
        num = len(all_lesson_name)
        schedule = []
        for count in range(num):
            lesson = []
            # 课程名 汇编语言程序设计
            lesson_name = all_lesson_name[count]
            print(lesson_name)
            # 上课时间 周二第7,8节
            day = all_day[count]
            begin_time = all_begin_time[count]
            end_time = all_end_time[count]
            time = get_lesson_time(day, begin_time, end_time)
            print(time)
            # 周数 第10-10周|双周
            begin_week = all_begin_week[count]
            end_week = all_end_week[count]
            week_inter_val = all_week_inter_val[count]
            weeks = get_weeks(begin_week, end_week, week_inter_val)
            print(weeks)
            # 教室 '第1实验楼B403-A'
            area_name = all_area_name[count]
            class_room = all_class_room[count]
            class_room = get_class_room(area_name, class_room)
            print(class_room)
            # 教室 '刘小洋(刘小洋)'
            teacher_name = all_teacher_name[count]
            profession_name = all_profession_name[count]
            teacher_name = get_teacher_name(teacher_name, profession_name)
            print(teacher_name)
            lesson.append(lesson_name)
            lesson.append(time)
            lesson.append(weeks)
            lesson.append(class_room)
            lesson.append(teacher_name)
            schedule.append(lesson)
        return schedule
