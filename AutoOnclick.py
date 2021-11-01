# -*- coding: utf-8 -*-
# @Time : 2021/2/16 20:02
# @Author : TionKior
# @File : DaKa.py
# @Software : PyCharm

from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from selenium import webdriver
import time


# 开启浏览器
def openChrome():
    # 可视界面下运行浏览器(可视界面下请注释下面代码,return driver不要注释)
    driver = webdriver.Chrome(executable_path=r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")

    # 无界面化运行浏览器
    # options = webdriver.ChromeOptions()
    # options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    # options.add_argument('window-size=1600x900')  # 指定浏览器分辨率
    # options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    # options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    # options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    # options.add_argument('--headless')  # 浏览器不提供可视化页面.linux下如果系统不支持可视化不加这条会启动失败
    # options.add_argument('disable-infobars')  # 不显示正在受自动化软件控制

    # 前面的是配置,后面的是chromedriver.exe可执行路径

    # 无界面下运行请解开无界面化运行浏览器以及下面一行代码
    # driver = webdriver.Chrome(options=options, executable_path=r"/usr/bin/chromedriver")

    # 可视界面下浏览无界面运行请解开下面代码
    # driver = webdriver.Chrome(options=options,
    #                           executable_path=r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")

    return driver


def open_dk(driver):
    try:
        # 打开网页
        url = "http://ca.xzcit.cn/cas/login"
        driver.get(url)
        time.sleep(2)
        driver.set_page_load_timeout(5)  # 设置页面加载超时
    except:
        print("打开网页错误,请检查url是否正确")
        email("打卡失败,请手动打卡")
        driver.quit()
        quit()

    try:
        # 获取登录页面标签
        print("进入到登录网页")
        print(f"当前标签页标题:{driver.title}")

        # 封装账号密码
        driver.find_element_by_id("username").send_keys("")
        driver.find_element_by_id("ppassword").send_keys("")

        # 点击登录按钮
        dl = driver.find_element_by_xpath('//*[@id="dl"]')
        dl.click()
        time.sleep(5)
    except:
        print("账号密码定位错误,请重新设置定位")
        email("打卡失败,请手动打卡")
        driver.quit()
        quit()

    try:
        # 获取个人中心标签
        print("进入到个人中心")
        print(f"当前标签页标题:{driver.title}")
        windows = driver.window_handles
        driver.switch_to.window(windows[0])
        # 点击疫情健康打卡 xpath()寻找元素位置
        dk = driver.find_element_by_xpath(r'//*[@id="MyApp2"]/div/div[2]/ul/li[1]/a/img')
        dk.click()
        time.sleep(5)
    except:
        print("如果两次的标签页标题一致,您的账号密码错误;如果不一致,元素定位错误,请重新定位元素")
        email("打卡失败,请手动打卡")
        driver.quit()
        quit()

    try:
        # 跳转到新的标签页
        # 获取所有标签页句柄
        windows = driver.window_handles
        # switch_to_window()改成switch_to.window()就不会有DeprecationWarning警告
        driver.switch_to.window(windows[1])  # 1获取打卡页面标签
        print("进入到打卡页面")
        print(f"当前标签页标题:{driver.title}")
        # 点击提交按钮
        tj = driver.find_element_by_xpath(r'//*[@id="topNav"]/div/div/div[2]/div/div[2]/div[1]/a')
        tj.click()
        time.sleep(5)
        print("打卡成功")
        email("打卡成功")

    except:
        print("打卡失败,原因如下")
        print("您已经打过卡了,或此时不在打卡时间内,为您点击确认再次点击打卡")
        # 打卡官网,默认已达过卡时,直接打开网页,没有iframe标签,确认元素在div中
        # 下例为已达过卡点击确认再次点击提交测试
        qr = driver.find_element_by_xpath('/html/body/div[1]/table/tbody/tr[2]/td[2]/div/div[3]/div/div[1]/div[3]')
        qr.click()
        time.sleep(3)
        # 再次点击打卡按钮
        tj = driver.find_element_by_xpath(r'//*[@id="topNav"]/div/div/div[2]/div/div[2]/div[1]/a')
        tj.click()
        print("打卡是否成功未知,请重新登录查看")
        email("打卡失败,请手动打卡")

        time.sleep(3)

    finally:
        print("浏览器即将退出")
        driver.quit()
        print("浏览器已退出")
        print("程序即将退出")
        quit()


# QQ邮箱推送打卡结果
def email(content):
    # 收件人的邮箱
    amail = ''
    # 函数参数content是打卡的结果
    # 发件人邮箱和收件人邮箱都做成了一个接口,只用传一个参数
    host_server = 'smtp.qq.com'  # qq邮箱smtp服务器
    sender_qq = ''  # 发件人邮箱
    pwd = ''
    receiver = [amail]  # 收件人邮箱

    mail_title = content  # 邮件标题
    mail_content = content  # 邮件正文内容
    # 初始化一个邮件主体
    msg = MIMEMultipart()
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq
    msg['To'] = ";".join(receiver)
    # 邮件正文内容
    msg.attach(MIMEText(mail_content, 'plain', 'utf-8'))

    smtp = SMTP_SSL(host_server)  # ssl登录

    # login(user,password):
    # user:登录邮箱的用户名。
    # password：登录邮箱的密码，像笔者用的是网易邮箱，网易邮箱一般是网页版，需要用到客户端密码，需要在网页版的网易邮箱中设置授权码，该授权码即为客户端密码
    smtp.login(sender_qq, pwd)
    # sendmail(from_addr,to_addrs,msg,...):
    # from_addr:邮件发送者地址
    # to_addrs:邮件接收者地址。字符串列表['接收地址1','接收地址2','接收地址3',...]或'接收地址'
    # msg：发送消息：邮件内容。一般是msg.as_string():as_string()是将msg(MIMEText对象或者MIMEMultipart对象)变为str
    smtp.sendmail(sender_qq, receiver, msg.as_string())
    # quit():用于结束SMTP会话
    smtp.quit()


if __name__ == '__main__':
    driver = openChrome()
    open_dk(driver)
