"""
author: jchZhao
last modified: April 2022
"""
################这是selenium###################
from multiprocessing.connection import wait
from sched import scheduler
from click import option
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver import chrome
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from time import sleep
#----------------------for GUI---------------------------
from cProfile import label
import re
from turtle import onclick
import wx
from datetime import datetime
import threading
#---------------------for scheduler----------------------
from calendar import month
from apscheduler.schedulers.blocking import BlockingScheduler #single process used
from apscheduler.schedulers.background import BackgroundScheduler #mutilplied process used
from datetime import datetime
#---------------------main work--------------------------

def magic_work(windows,usr_p:str,pwd_p:str):
    try:
        #------------------------兰大个人工作台地址---------------------------
        url = 'http://my.lzu.edu.cn:8080/login?service=http://my.lzu.edu.cn'
        #------------------------定义一个浏览器对象---------------------------
        opt = Options()            # 创建Chrome参数对象
        # opt.headless = True
        opt.add_argument('--headless')
        my_driver = webdriver.Chrome(options=opt)
        #------------------------打开工作台主页-------------------------------
        my_driver.get(url)
        #------------------------定位账号、密码和登录按钮的位置----------------
        usr = my_driver.find_element(by=By.ID,value='username')
        pwd = my_driver.find_element(by=By.ID,value='password')
        but = my_driver.find_element(by=By.XPATH,value='/html/body/div[1]/div[2]/div/div/form/div/button')
        #------------------------输入我的账号和密码---------------------------
    
        usr.send_keys(usr_p)
        pwd.send_keys(pwd_p)
        #------------------------等待浏览器加载完成---------------------------
        wait = WebDriverWait(my_driver, 10)
        #------------------------提交填写完成的表单---------------------------
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div/form/div/button')))
        #------------------------点击登录------------------------------------
        but.click()
        #------------------------等待2秒-------------------------------------
        sleep(1)
        #debug info, useless
        # print('hhhh')

        #------------------------定位到“健康打卡”网页app----------------------
        li = my_driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/ul[1]/li[3]')
        #------------------------鼠标悬停以展示“进入”按钮----------------------
        ActionChains(my_driver).move_to_element(li).perform()
        #------------------------定位“进入”按钮-------------------------------
        p = my_driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/ul[1]/li[3]/a[1]/div[2]/p[2]')
        #------------------------点击进入-------------------------------------
        p.click()
        #------------------------切换上下文到iframe---------------------------
        iframe = my_driver.find_element(By.TAG_NAME, "iframe")
        my_driver.switch_to.frame(iframe)

        #------------------------定位到“上报”按钮-----------------------------
        app_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view/uni-form/span/uni-view[13]/uni-button')))
        #------------------------click to submit----------------------------
        app_button.click()
        #debug info, useless
        # print('chl')
        #------------------------wait for about 3 seconds-------------------
        sleep(1)
        #------------------------close explorer, done-----------------------
        my_driver.quit()
        wx.CallAfter(windows.LogMessage,True)
        # print('finished')
    except Exception:
        wx.CallAfter(windows.LogMessage,False)

#-------------------------------GUI for this project-------------------------
class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title)
        self.gard_days = 0
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):

        self.panel = wx.Panel(self,size=(600,600))

        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.fgs = wx.FlexGridSizer(3, 2, 9, 25)

        self.title = wx.StaticText(self.panel, label="usr")
        self.author = wx.StaticText(self.panel, label="pwd")
        self.start = wx.Button(self.panel,label='STart')
        self.start.Bind(wx.EVT_BUTTON,self.onclick)

        toyou = wx.StaticText(self.panel,label='magic work from now on')

        self.tc1 = wx.TextCtrl(self.panel)
        self.tc2 = wx.TextCtrl(self.panel,style=wx.TE_PASSWORD)
        # tc3 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        self.fgs.AddMany([(self.title), (self.tc1, 1, wx.EXPAND), (self.author),
            (self.tc2, 1, wx.EXPAND)])

        self.vbox.Add(self.fgs, proportion=1, flag=wx.ALIGN_CENTER_HORIZONTAL,border=15)
        self.vbox.Add(self.start,proportion=0,flag=wx.ALIGN_CENTER_HORIZONTAL,border=25)
        self.vbox.Add(toyou,proportion=0,flag=wx.ALIGN_CENTER_HORIZONTAL,border=25)
        self.panel.SetSizer(self.vbox)

    def onclick(self,e):
        if self.start.GetLabelText() == 'STart':
            usr_r = self.tc1.GetValue()
            pwd_r = self.tc2.GetValue()
            next = True
            if len(usr_r)==0 or len(pwd_r)==0:
                toP = wx.MessageDialog(self.panel,message='usr & pwd must be valued',style=wx.YES_DEFAULT|wx.ICON_QUESTION)
                if toP.ShowModal() == wx.ID_OK:
                    next = False
                    toP.Destroy()
            if next:
                self.title.Hide()
                self.author.Hide()
                self.tc1.Hide()
                self.tc2.Hide()
                self.gard = wx.StaticText(self.panel)
                # print('type = {}'.format(type(usr_r)))
                self.tc1.Clear()
                self.tc2.Clear()
                dts = datetime.now()
                ltxt = 'start time = '+str(dts.year)+'.'+str(dts.month)+'.'+str(dts.day)+' '+str(dts.hour)+':'+str(dts.minute)+'\ngard you for '+str(self.gard_days)+' days'

                self.gard.SetLabelText(ltxt)
            
                self.thread = Working_thread(self,usr_r,pwd_r)
                self.thread.start()
                self.start.SetLabelText('Stop')
            
        else:
            self.title.Show()
            self.author.Show()
            self.tc1.Show()
            self.tc2.Show()
            self.gard.Hide()
            self.thread.stop()
            self.start.SetLabelText('STart')
    def LogMessage(self,msg):
        if msg:
            dts = datetime.now()
            self.gard_days = self.gard_days + 1
            ltxt2 = 'start time = '+str(dts.year)+'.'+str(dts.month)+'.'+str(dts.day)+' '+str(dts.hour)+':'+str(dts.minute)+'\ngard you for '+str(self.gard_days)+' days'
            self.gard.SetLabelText(ltxt2)
            self.Refresh()
        else:
            ltxt2 = 'I\'m sorry but it defeated'
            self.gard.SetLabelText(ltxt2)
            self.Refresh()
#-------------------------multiplied task concurrent---------------------------#
class Working_thread(threading.Thread):
    def __init__(self,window,usr:str,pwd:str):
        threading.Thread.__init__(self)
        self.usr = usr
        self.pwd = pwd
        self.window = window
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
    def run(self):
        # print("execute a thread emmm.")
        #设置时区在亚洲/上海
        self.scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
        #every 7:34 pick it up
        self.scheduler.add_job(magic_work,args=[self.window,self.usr,self.pwd], id='auto',trigger="cron",hour='7',minute=34)
        self.scheduler.start()
        
    def stop(self):
        self.scheduler.shutdown(wait=False)
        self.timeToQuit.set()

def main():

    app = wx.App()
    ex = Example(None, title='punch Robot')
    app.MainLoop()


if __name__ == '__main__':
    main()
