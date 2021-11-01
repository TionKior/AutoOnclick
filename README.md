# 使用介绍

利用 python3.9+selenium+chromedriver+centos7实现疫情自动打卡

使用简单，开箱即用，只需要简单的配置，结果有邮箱通知

#### windows环境需求

* python3+selenium
* GoogleChrome+chromedriver

#### Linux环境需求

* python3+selenium
* GoogleChrome+chromedriver
* CentOS7，作者使用的是阿里云的服务器
* crontab的使用

#### windows配置测试

__请注意，刚开头的openChrome函数内容在windows测试环境请更改路径__

1. 修改openChrome函数中的路径，指向你的chromedriver

   ```
   # 可视界面下运行浏览器(可视界面下请注释下面代码,return driver不要注释)
   driver = webdriver.Chrome(executable_path=r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")
   ```

2. 配置账号密码
   在代码第 61，62行输入学号和密码

   ```python
   # 封装账号密码
   driver.find_element_by_id("username").send_keys("username")
   driver.find_element_by_id("ppassword").send_keys("password")
   ```

2. 配置发件人和收件人

   在132行输入__收件人__邮箱，可以输入多个，但不推荐！

   ```python
   # 收件人的邮箱
   amail = 'xxx@qq.com'
   ```

   __发件人__设置

   host_server需要根据使用的邮箱的smtp设置

   ```python
   host_server = 'smtp.qq.com'  # qq邮箱smtp服务器
   sender_qq = ''  # 发件人邮箱
   pwd = '' # smtp码,根据网页生成
   ```

#### Linux配置测试

* 介绍：Linux环境才是自动的主要环境，使用__crontab__进行自动运行
* crontab -e 编辑自动运行

1. 注释掉windows配置一行(18行)，取消注释21-28行(Linux无界面化运行)

   __executable_path是你的chromedriver路径__

   ```python
   # 无界面化运行浏览器
   options = webdriver.ChromeOptions()
   options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
   options.add_argument('window-size=1600x900')  # 指定浏览器分辨率
   options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
   options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
   options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
   options.add_argument('--headless')  # 浏览器不提供可视化页面.linux下如果系统不支持可视化不加这条会启动失败
   options.add_argument('disable-infobars')  # 不显示正在受自动化软件控制
   
   # 前面的是配置,后面的是chromedriver.exe可执行路径
   
   # 无界面下运行请解开无界面化运行浏览器以及下面一行代码
   driver = webdriver.Chrome(options=options, executable_path=r"/usr/bin/chromedriver")
   ```

2. 配置python环境，__pip install selenium__依赖包

3. 上传文件，可以使用Xshell7+Xftp7

4. 对话框中运行测试
5. crontab -e编辑每日运行