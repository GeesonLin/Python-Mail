# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import datetime
import traceback
import logging
import os
import re
import sys

# 测试用来执行函数
def login(browser, acct, passwd):
	url = "http://qiye.163.com/login/?from=ym"
	browser.get(url)
	time.sleep(1)                                               # 睡眠1秒钟
	try:
		# 输入账号和密码
		browser.find_element_by_id("accname").send_keys(acct)   # 输入用户名
		browser.find_element_by_id("accpwd").send_keys(passwd)   # 输入密码
 
		# 点击按钮提交登录表单
		browser.find_element_by_xpath('//button[@type="submit"]').click()
		time.sleep(1)                                   # 睡眠1秒钟

		# 验证登录成功的URL
		currUrl = browser.current_url
		info = re.match(r'http:\/\/mail.ym.163.com\/jy3\/main.jsp\?sid=.*', currUrl)
		if info:
			print("login success")
			return True
		else:
			print("failure")
			return False
	except:
		print("failure")
		login_Log()  # 跟踪日志
 
# 写错误日志并截图
def login_Log():
	# 组合日志文件名（当前文件名+当前时间）.比如：case_login_success-20150817192533
	basename = os.path.splitext(os.path.basename(__file__))[0]
	print(basename)
	logFile = basename+"-"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".log"
	logging.basicConfig(filename=logFile)  # 将日志记录到文件中
	s = traceback.format_exc()
	logging.error(s)     # 记录错误的日志
	browser.get_screenshot_as_file("./"+logFile+"-error.png")  # 截取登录的图片

def clear_trash(browser):
	try:
		# 回到主窗口
		browser.switch_to_window(browser.window_handles[-1])
		browser.switch_to_frame("folder")
		browser.find_element_by_xpath('//a[@title="清空"]').click()

		time.sleep(1)
		browser.switch_to_window(browser.window_handles[0])
		browser.find_element_by_xpath('//input[@id="btnSysOk"]').click()
	except:
		login_Log()  # 跟踪日志

def rm_mail(browser):
	try:
		# 需要先定位frame才能查找到对应的元素
		browser.switch_to_frame("folder")
		browser.find_element_by_xpath('//a[@title="收件箱"]').click()
		#browser.find_element_by_id("lnk1").click()

		# 回到主窗口
		browser.switch_to_window(browser.window_handles[-1])
		browser.switch_to_frame("foldmain")

		p = 0
		while p < 10:
			browser.find_element_by_xpath('//input[@type="checkbox"]').click()
			browser.find_element_by_xpath('//input[@action="move"]').click()
			p += 1
		
		clear_trash(browser)
	except:
		# We think it as no checkbox exception, so all mail has moved to trash now
		clear_trash(browser)
 
if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: ./clear_mialbox.py mail_account mail_password!")
		sys.exit(1)

	account = sys.argv[1]
	password = sys.argv[2]
	browser = webdriver.Chrome()  # 启动chrome浏览器

	if login(browser, account, password):            # 登录邮箱
		rm_mail(browser)
	#browser.quit()                # 退出浏览器
