#! /usr/bin/env python
#coding=utf-8

import wx
import time
import threading
import os
            
class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1,u"延时关机",size=(300, 300))
        #wx.Frame.__init__(self, None, -1, "Shaped Window",
        #                style = wx.FRAME_SHAPED | wx.SIMPLE_BORDER  ,size=(300, 300) ,pos=(300,300)  )
        self.delta = wx.Point(0,0)
        
        p = wx.Panel(self)
        wx.StaticText(p,-1,u"输入延迟关机的秒数:",pos = (10,10),size = (120, -1))
        self.text = wx.TextCtrl(p,-1,"",pos = (130, 10),size = (150, -1))             
        
        self.btn = wx.Button(p, -1, "go", (120,220))
        self.Bind(wx.EVT_BUTTON, self.OnToggleItem, self.btn)
        self.btn.SetDefault()
        
        self.isend = True
        
        self.message1 = wx.StaticText(p,-1,u"模式二默认是今天0点",pos = (10, 120),size = (200, -1))
        self.message2 = wx.StaticText(p,-1,"",pos = (10,150))
        
        ctime = time.localtime()
        self.yearList = map(str,range(ctime.tm_year,ctime.tm_year+5))
        self.monthList = map(str,range(1,13))
        self.dayList = map(str,range(1,32))
        self.hourList = map(str,range(0,24))
        self.minList = map(str,range(0,60))
        self.sList = map(str,range(0,60))
        
        wx.StaticText(p,-1,u"年:",pos = (10, 40))
        wx.StaticText(p,-1,u"月:",pos = (100, 40))
        wx.StaticText(p,-1,u"日:",pos = (190, 40))
        wx.StaticText(p,-1,u"时:",pos = (10, 80))
        wx.StaticText(p,-1,u"分:",pos = (100, 80))
        wx.StaticText(p,-1,u"秒:",pos = (190, 80))
        
        self.yS = wx.Choice(p, -1, (30, 40), choices=self.yearList)
        self.mS = wx.Choice(p, -1, (120, 40), choices=self.monthList)
        self.dS = wx.Choice(p, -1, (210, 40), choices=self.dayList)
        self.hS = wx.Choice(p, -1, (30, 80), choices=self.hourList)
        self.MS = wx.Choice(p, -1, (120, 80), choices=self.minList)
        self.sS = wx.Choice(p, -1, (210, 80), choices=self.sList)
        
        self.clockt=threading.Thread(target=self.clock)
        self.clockt.setDaemon(True)
        self.clockt.start() 
        
        
    def OnExit(self, event):
        self.Close()

    def OnToggleItem(self, event):
        if self.isend == True:
            if self.text.GetValue() == "":
                rq = threading.Thread(target=self.riqi)
                rq.setDaemon(True)
                rq.start()
                return
            try:
                snum = float(self.text.GetValue())
            except:
                self.message1.SetLabel(u"那是数字么？")
                return
            self.isend = False
            self.btn.SetLabel("stop")
            self.timer=threading.Thread(target=self.taketime)
            self.timer.setDaemon(True)
            self.timer.start()            
        else:
            self.isend = True
            os.system("shutdown -a")
            self.btn.SetLabel("go")
            self.message1.SetLabel(u"已停止")
            
    
    def taketime(self):
        snum = float(self.text.GetValue())
        ct = time.time()
        while time.time()-ct<snum:
            if self.isend == True:
                break                          
            self.message1.SetLabel(u"剩余时间:"+str(snum-(int(time.time()-ct))))
            time.sleep(1)
        if self.isend == False:  
            self.message1.SetLabel(u"执行关机……")
            os.system("shutdown -s")
    
    def riqi(self):
        ct = time.localtime()
        
        ys = self.yS.GetSelection()+ct.tm_year
        ms = self.mS.GetSelection()+1
        ds = self.dS.GetSelection()+1
        hs = self.hS.GetSelection()
        Ms = self.MS.GetSelection()
        ss = self.sS.GetSelection()
        
        if ys < ct.tm_year:
            ys = ct.tm_year
        if ms == 0:
            ms = ct.tm_mon
        if ds == 0:
            ds = ct.tm_mday
        if hs == -1:
            hs = 0
        if Ms == -1:
            Ms = 0
        if ss == -1:
            ss = 0
        try:
            t = time.strptime(str(ys)+"-"+str(ms)+"-"+str(ds)+" "+str(hs)+":"+str(Ms)+":"+str(ss),"%Y-%m-%d %H:%M:%S")
        except:
            self.message1.SetLabel(u"该时间不存在……")
            return
            
        if t <= ct: 
            self.message1.SetLabel(u"时间已经过去了……")
            return
        else:
            self.message1.SetLabel(u"计划关机时间 "+time.strftime("%m/%d/%y %H:%M:%S",t))
        
        self.isend = False
        self.btn.SetLabel("stop")
        
        while (time.localtime() < t ) and (self.isend == False):
            time.sleep(1)
        if self.isend == False:
            self.message1.SetLabel(u"执行关机……")
            os.system("shutdown -s")
    
    def clock(self):
        while 1:
            self.message2.SetLabel(time.strftime("%Z %c",time.localtime()))
            time.sleep(1)
    

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()

    
