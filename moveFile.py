#! /usr/bin/env python
#coding=utf-8

import wx,re,os,threading,shutil

class mFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, u'文件处理', size=(400,520))
        panel = wx.Panel(self, -1)
        menuFile = wx.Menu()
        menuFile.Append(1, u"&关于")
        menuFile.AppendSeparator()
        menuFile.Append(2, u"使用说明")
        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, u"&帮助")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=1)
        self.Bind(wx.EVT_MENU, self.Onshuoming, id=2)
        
        wx.StaticText(panel,-1,u"原文件夹:",pos = (10, 10),size = (80, -1))
        wx.StaticText(panel,-1,u"目标文件夹:",pos = (10, 80),size = (80, -1))
        wx.StaticText(panel,-1,u"目标文件:",pos = (10, 150),size = (80, -1))
        wx.StaticText(panel,-1,u"自动改名:",pos = (10, 350),size = (80, -1))
        
        self.t1 = wx.TextCtrl(panel, -1, "",size=(250,-1),pos=(10,40))
        self.t2 = wx.TextCtrl(panel, -1, "",size=(250,-1),pos=(10,110))
        self.t3 = wx.TextCtrl(panel, -1, "",size=(250,-1),pos=(10,180))
        self.t4 = wx.ListCtrl(panel, -1,style=wx.LC_REPORT| wx.BORDER_NONE,size=(360,100),pos=(10,240))
        self.t4.InsertColumn(0, u"文件名", wx.LIST_FORMAT_LEFT, 80)
        self.t4.InsertColumn(1, u"位置", wx.LIST_FORMAT_LEFT, 280)
        self.t5 = wx.TextCtrl(panel, -1, "self",size=(250,-1),pos=(10,380))
        
        self.b1 = wx.Button(panel,-1,u"浏览",size=(40,-1),pos=(300,40))
        self.b2 = wx.Button(panel,-1,u"浏览",size=(40,-1),pos=(300,110))
        self.b3 = wx.Button(panel,-1,u"查找",size=(40,-1),pos=(30,210))
        self.b4 = wx.Button(panel,-1,u"复制",size=(40,-1),pos=(120,210))
        self.b5 = wx.Button(panel,-1,u"剪切",size=(40,-1),pos=(220,210))
        self.b6 = wx.Button(panel,-1,u"Internet临时文件夹",size=(140,-1),pos=(100,10))
        self.b3.SetDefault()
        
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.b1)
        self.Bind(wx.EVT_BUTTON, self.OnClick1, self.b2)
        self.Bind(wx.EVT_BUTTON, self.OnClick2, self.b3)
        self.Bind(wx.EVT_BUTTON, self.copy, self.b4)
        self.Bind(wx.EVT_BUTTON, self.cut, self.b5)
        self.Bind(wx.EVT_BUTTON, self.cache, self.b6)
    
    def OnClick(self, event):        
        dialog = wx.DirDialog(None, u"选择源文件夹:",
                  style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.t1.SetValue(dialog.GetPath())
        dialog.Destroy()        
        
    def OnClick1(self, event):        
        dialog = wx.DirDialog(None, u"选择目标文件夹:",
                  style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.t2.SetValue(dialog.GetPath())
        dialog.Destroy()
    
    def OnClick2(self, event):        
        if self.t3.GetValue()=="" or self.t1.GetValue()=="":
            wx.MessageBox(u"信息不足", u"错误",wx.ICON_QUESTION)            
            return
        s = threading.Thread(target=self.search)
        s.setDaemon(True)
        s.start()
        
    def search(self):
        index = 0
        self.t4.DeleteAllItems()
        namere = re.compile(self.t3.GetValue())
        source = self.t1.GetValue()
        for dirpath,dirnames,filenames in os.walk(source):
            for name in filenames:
                if namere.search(name)!=None:
                    self.t4.InsertStringItem(index,name)
                    self.t4.SetStringItem(index,1,os.path.join(dirpath,name))
                    index = index+1
        if index == 0:
            wx.MessageBox(u"没有找到匹配文件", u"错误",wx.ICON_QUESTION)
        
    def copy(self, event):
        if self.t4.GetSelectedItemCount() == 0 :
            wx.MessageBox(u"没有文件被选中", u"错误",wx.ICON_QUESTION)
            return
        if self.t2.GetValue()=="":
            wx.MessageBox(u"目标文件夹不能为空", u"错误",wx.ICON_QUESTION)
            return
        item = -1
        while(1):
            item = self.t4.GetNextItem(item,
                                         wx.LIST_NEXT_ALL,
                                         wx.LIST_STATE_SELECTED)
            if item == -1:
                break            
            print repr(self.t4.GetItem(item,1).GetText())
            name = self.t2.GetValue()
            if os.path.dirname(self.t4.GetItem(item,1).GetText())==name:
                wx.MessageBox(u"目标文件在指定文件夹", u"错误",wx.ICON_QUESTION)
                return
            
            if self.t5.GetValue()=="self":
                name = name+self.t4.GetItemText(item)
            else:
                name = name+self.t5.GetValue()
            result = 0
            if os.path.isfile(name):
                dlg = wx.MessageDialog(None, u'目标地址已经存在一个同名文件，是否继续？\n继续，该文件会被覆盖',
                                          u'错误', wx.YES_NO | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                dlg.Destroy()
            if result == wx.ID_NO:
                return 
            shutil.copy(self.t4.GetItem(item,1).GetText(),name)
            wx.MessageBox(u"操作成功！\n"+os.path.basename(self.t4.GetItem(item,1).GetText())+u"复制成功", u"完成",wx.ICON_INFORMATION) 
            
    def cut(self, event):        
        if self.t4.GetSelectedItemCount() == 0:
            wx.MessageBox(u"没有文件被选中", u"错误",wx.ICON_QUESTION)
            return        
        if self.t2.GetValue()=="":
            wx.MessageBox(u"目标文件夹不能为空", u"错误",wx.ICON_QUESTION)
            return
        item = -1
        while(1):
            item = self.t4.GetNextItem(item,
                                         wx.LIST_NEXT_ALL,
                                         wx.LIST_STATE_SELECTED)
            if item == -1:
                break            
            print repr(self.t4.GetItem(item,1).GetText())
            name = self.t2.GetValue()
            if os.path.dirname(self.t4.GetItem(item,1).GetText())==name:
                wx.MessageBox(u"目标文件在指定文件夹", u"错误",wx.ICON_QUESTION)
                return            
            if self.t5.GetValue()=="self":
                name = name+self.t4.GetItemText(item)
            else:
                name = name+self.t5.GetValue()
            result = 0
            if os.path.isfile(name):
                dlg = wx.MessageDialog(None, u'目标地址已经存在一个同名文件，是否继续？\n继续，该文件会被覆盖',
                                          u'错误', wx.YES_NO | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                dlg.Destroy()
            if result == wx.ID_NO:
                return 
            shutil.copy(self.t4.GetItem(item,1).GetText(),name)
            os.remove(self.t4.GetItem(item,1).GetText())
            wx.MessageBox(u"操作成功！\n"+os.path.basename(self.t4.GetItem(item,1).GetText())+u"移动成功", u"完成",wx.ICON_INFORMATION) 

    def cache(self, event):
        self.t1.SetValue("C:\Users\leviathan\AppData\Local\Microsoft\Windows\Temporary Internet Files")
        
    def OnAbout(self, event):
        wx.MessageBox(u"by leviathan", u"about",wx.ICON_INFORMATION) 
    
    def Onshuoming(self, event):
        txt = u"①选择一个文件夹作为源文件夹,程序会从这个文件夹里面查找你要的文件。\n②选择一个文件夹作为复制或者移动的目的文件夹。\n③点查找，选择你要的文件夹，然后点击复制或者剪切。\nPS:如果要改名字，请直接将完整文件名，包括扩展名输入到最下面的框内。"        
        wx.MessageBox(txt, u"help",wx.ICON_INFORMATION)
            
app = wx.PySimpleApp()
frm = mFrame()
frm.Show()
app.MainLoop()
