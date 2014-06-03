#! /usr/bin/env python
#coding=utf-8

import re,wx

class mFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, u'字符串处理', size=(600,520))
        panel = wx.Panel(self, -1)
        wx.StaticText(panel,-1,u"输入:",pos = (10, 10),size = (40, -1))
        wx.StaticText(panel,-1,u"输出:",pos = (300, 10),size = (40, -1))
        self.t1 = wx.TextCtrl(panel, -1, "",style=wx.TE_MULTILINE|wx.HSCROLL,size=(250,250),pos=(10,40))
        self.t2 = wx.TextCtrl(panel, -1, "",style=wx.TE_MULTILINE|wx.HSCROLL,size=(250,250),pos=(300,40))
        
        wx.StaticText(panel,-1,u"目标字符串:",pos = (10, 300),size = (80, -1))
        self.message1 = wx.TextCtrl(panel,-1,"",pos = (90, 300),size = (200, -1))
        wx.StaticText(panel,-1,u"替换为:",pos = (10, 340),size = (80, -1))
        self.message2 = wx.TextCtrl(panel,-1,"self",pos = (90, 340),size = (200, -1))
        wx.StaticText(panel,-1,u"在前面添加:",pos = (10, 380),size = (80, -1))
        self.message3 = wx.TextCtrl(panel,-1,"",pos = (90, 380),size = (200, -1))
        wx.StaticText(panel,-1,u"在后面添加:",pos = (10, 420),size = (80, -1))
        self.message4 = wx.TextCtrl(panel,-1,"",pos = (90, 420),size = (200, -1))
        
        self.b1 = wx.Button(panel,-1,"go",pos = (400,340),size = (80,80))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.b1)
        self.b1.SetDefault()
        self.b2 = wx.Button(panel,-1,u"←",pos = (350,300),size = (80,30))
        self.Bind(wx.EVT_BUTTON, self.OnClick1, self.b2)
        self.b3 = wx.Button(panel,-1,u"→",pos = (450,300),size = (80,30))
        self.Bind(wx.EVT_BUTTON, self.OnDoCopy, self.b3)
        self.b3 = wx.Button(panel,-1,"C",pos = (50,10),size = (30,18))
        self.Bind(wx.EVT_BUTTON, self.clear, self.b3)
        
        self.strm = ""
        
    def OnClick(self, event):
        
        str = self.t1.GetValue()       
        if str == "":
            return
        str1 = self.message1.GetValue()
        if str1 == "":
            return
        
        str2 = self.message2.GetValue()
        str3 = self.message3.GetValue()
        str4 = self.message4.GetValue()
        strr = ""
              
        strre = re.compile(str1.encode("utf-8"))
        list = strre.findall(str)      
        
        str2 = str2.replace(u"\\n",u"\n")
        str3 = str3.replace(u"\\n",u"\n")
        str4 = str4.replace(u"\\n",u"\n")
        str2 = str2.replace(u"\\t",u"\t")
        str3 = str3.replace(u"\\t",u"\t")
        str4 = str4.replace(u"\\t",u"\t")
        
        for x in list:
            qd = str.find(x)
            hd = str.find(x)+len(x)
            if str2 == "self":
                strr = strr+str[:qd]+str3+x+str4
            else:
                strr = strr+str[:qd]+str3+str2+str4
            str = str[hd:]
        strr = strr+str
        self.strm = strr
                    
        self.t2.SetLabel(self.strm)
        
    def OnClick1(self, event):
        
        self.t1.SetLabel(self.strm)
        
    def OnDoCopy(self, event):
        
        data = wx.TextDataObject()
        data.SetText(self.strm)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(data)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Unable to open the clipboard", "Error")
    def clear(self,event):
        self.t1.SetLabel("")
        
app = wx.PySimpleApp()
frm = mFrame()
frm.Show()
app.MainLoop()
