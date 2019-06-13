#-*- coding: utf-8 -*-
from unipus import Unipus 
import wx
#import win32api
#import sys, os

APP_TITLE = u'shuake'

class LOG:
    def __init__(self):
        pass 
    def info(self,*a):
        pstr = ''
        for s in a:
            if isinstance(s,str):
                pstr +=s
        print(pstr)
    def warn(self,*a):
        pstr = ''
        for s in a:
            if isinstance(s,str):
                pstr +=s
        print(pstr)

    def error(self,*a):
        pstr = ''
        for s in a:
            if isinstance(s,str):
                pstr +=s
        print(pstr)
        
class mainFrame(wx.Frame):
    '''程序主窗口类，继承自wx.Frame'''
 
    def __init__(self, parent):
        '''构造函数'''
        wx.Frame.__init__(self, parent, -1, APP_TITLE)
        self.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.SetSize((640, 480))
        self.Center()
        wx.StaticText(self, -1, u'用户：', pos=(10,50), size=(40, -1), style=wx.ALIGN_LEFT)
        self.username = wx.TextCtrl(self, -1, '', pos=(50, 45), size=(150, -1), name='TC01', style=wx.TE_LEFT)
        wx.StaticText(self, -1, u'密码：', pos=(210,50), size=(40, -1), style=wx.ALIGN_LEFT)
        self.passwd = wx.TextCtrl(self, -1, '', pos=(250, 45), size=(150, -1), name='TC02', style=wx.TE_PASSWORD|wx.ALIGN_LEFT)
        btn_refresh = wx.Button(self, -1, u'刷新课程列表', pos=(480, 45), size=(100, 25))
        #btn_meb = wx.Button(self, -1, u'鼠标所有事件', pos=(350, 180), size=(100, 25))
        #btn_close = wx.Button(self, -1, u'关闭窗口', pos=(350, 210), size=(100, 25))
        self.logger = LOG()
        wx.StaticText(self, -1, u'课程列表 ', pos=(30, 80), size=(100, -1), style=wx.ALIGN_LEFT)
        self.course_list = wx.CheckListBox(self,-1,pos=(10,100),size=(200,300),name="CL0",choices=[""],style=wx.ALIGN_LEFT|wx.VSCROLL|wx.HSCROLL)
        
        wx.StaticText(self, -1, u'课程单元 ', pos=(250, 80), size=(100, -1), style=wx.ALIGN_LEFT)
        self.unit_list  = wx.CheckListBox(self,-1,pos=(220,100),size=(200,300),name="CL1",choices=[""],style=wx.ALIGN_LEFT|wx.VSCROLL|wx.HSCROLL)
        self.courses = []        
        
        wx.StaticText(self, -1, u'答题时间(s) ', pos=(480, 120), size=(100, -1), style=wx.ALIGN_LEFT)
        self.ans_time = wx.TextCtrl(self, -1, '', pos=(480,140), size=(100, -1), name='TC03', style=wx.TE_LEFT)
        
        btn_courses = wx.Button(self, -1, u'按课程答题', pos=(480, 200), size=(100, 25))
        btn_units   = wx.Button(self, -1, u'按单元答题', pos=(480, 250), size=(100, 25))
        btn_download   = wx.Button(self, -1, u'下载答案', pos=(480, 300), size=(100, 25))
        # list 选择事件
        self.course_list.Bind(wx.EVT_CHECKLISTBOX, self.EvtChecklistBox)
        self.unit_list.Bind(wx.EVT_CHECKLISTBOX, self.EvtChecklistBox)
        #self.Bind(wx.EVT_BUTTON, self.OnClose, btn_close)
 
        # 鼠标事件 
        btn_refresh.Bind(wx.EVT_LEFT_DOWN, self.OnRefresh)
        btn_courses.Bind(wx.EVT_LEFT_DOWN, self.OnAnserByAll)
        btn_units  .Bind(wx.EVT_LEFT_DOWN, self.OnAnserByUnit)
        btn_download.Bind(wx.EVT_LEFT_DOWN, self.OnDownloadAnswer)
        # 系统事件
        self.Bind(wx.EVT_CLOSE, self.OnClose)
 
    def EvtChecklistBox(self, evt):
        '''显示课程类容以及单元内容'''
 
        obj = evt.GetEventObject()
        objName = obj.GetName()
        sel = evt.GetSelection()
        if objName == 'CL0':
            for checked in self.course_list.GetCheckedItems():
                if sel != checked:
                    self.course_list.Check(checked,check=False)
            if self.course_list.IsChecked(sel):
                units = [unit['unitName']+'   --' for unit in self.courses[sel]['units']]
                self.unit_list.Clear()
                self.unit_list.InsertItems(units,0)
                    
    def OnClose(self, evt):
        '''关闭窗口事件函数'''
 
        dlg = wx.MessageDialog(None, u'确定要关闭本窗口？', u'操作提示', wx.YES_NO | wx.ICON_QUESTION)
        if(dlg.ShowModal() == wx.ID_YES):
            self.Destroy()
 
    def OnRefresh(self, evt):
        '''左键按下事件函数'''
        users = self.username.GetValue()
        passwd = self.passwd.GetValue()
        #self.unipus = Unipus(self,'13015265988', 'wq19980506')
        self.unipus = Unipus(self,users,passwd)
        self.unipus.login()
        activated_course_list, not_activated_course_list = self.unipus.get_course_list()
        self.courses = activated_course_list
        courses_name = [ course['name']+'   --' for course in activated_course_list]
        self.units = {'abcd':['1','2','3'],'asdvd':['2','3','4'],'dfagb':['4','5','6']}
        self.course_list.Clear()
        self.course_list.InsertItems(courses_name,0)
    def OnAnserByAll(self,evt):
        itms = self.course_list.GetCheckedItems()
        time_str = self.ans_time.GetValue()
        if time_str:
            times = int(time_str,10) 
        else:
            times = 10000
        if itms and self.courses :
            self.unipus.learn_for_all_unit(self.courses[itms[0]]['id'], times)
            #print(self.courses[itms[0]]['id'], times)
        
    
    def OnAnserByUnit(self,evt):
        course_itms = self.course_list.GetCheckedItems()
        unit_itms = self.unit_list.GetCheckedItems()
        time_str = self.ans_time.GetValue()
        if time_str:
            times = int(time_str,10) 
        else:
            times = 10000
        if course_itms and self.courses :
            for unit in unit_itms:
                self.unipus.learn_for_unit(self.courses[course_itms[0]]['id'],self.courses[course_itms[0]]['units'][unit]['unitId'], times)
                #print(self.courses[course_itms[0]]['id'],self.courses[course_itms[0]]['units'][unit]['unitId'], 1000)

    def OnDownloadAnswer(self,evt):
        itms = self.course_list.GetCheckedItems()
        if itms:
            course_id = self.courses[itms[0]]['id']
            self.unipus.download_test_answer_for_course(course_id)
            
class mainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = mainFrame(None)
        self.Frame.Show()
        return True

if __name__ == "__main__":
    app = mainApp()
    app.MainLoop()