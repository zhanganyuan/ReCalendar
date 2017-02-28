class Resource:
    # 各种需要用到的页面
    img_url = "http://210.42.121.241/servlet/GenImg"  # 获取验证码的页面
    login_url = "http://210.42.121.241/servlet/Login"  # 登录页面
    index_url = "http://210.42.121.241/stu/stu_index.jsp"  # 登录之后的主页面，在这里获取令牌
    gpa_url = "http://210.42.121.241/stu/stu_score_credit_statics.jsp"  # 带日历的总分和成绩
    lessons_url = "http://210.42.121.241/servlet/Svlt_QueryStuLsn?{}"  # 课程的页面
    scores_url = "http://210.42.121.241/servlet/Svlt_QueryStuScore?{}"  # 成绩的页面
