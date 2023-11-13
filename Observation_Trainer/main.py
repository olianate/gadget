"""
观察力训练
"""

import random

import wx


class MyWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='观察训练')

        # 创建面板
        self.main_panel = wx.Panel(self)
        self.top_panel = wx.Panel(self.main_panel)

        # 创建标签
        self.correct_label = wx.StaticText(self.top_panel, label='正确数: 0')
        self.error_label = wx.StaticText(self.top_panel, label='错误数: 0')
        self.center_label = wx.StaticText(self.main_panel, label='Center Text')
        time_label = wx.StaticText(self.top_panel, label='时间ms:')
        nums_label = wx.StaticText(self.top_panel, label='位数')
        self.nums_ctl = wx.SpinCtrl(self.top_panel, value='2', min=2, max=6)
        self.time_ctl = wx.SpinCtrl(
            self.top_panel, value='1000', min=200, max=1000)

        # 设置标签的字体和颜色
        font = wx.Font(12, wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.correct_label.SetFont(font)
        self.correct_label.SetForegroundColour(wx.GREEN)

        self.error_label.SetFont(font)
        self.error_label.SetForegroundColour(wx.RED)

        self.center_label.SetFont(wx.Font(
            16, wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM))
        self.center_label.SetForegroundColour(wx.BLACK)

        time_label.SetFont(font)
        time_label.SetForegroundColour(wx.BLACK)

        nums_label.SetFont(font)
        nums_label.SetForegroundColour(wx.BLACK)

        # 添加输入文本框
        self.input_text = wx.TextCtrl(
            self.main_panel,
            style=wx.TE_PROCESS_ENTER | wx.ALIGN_CENTER_HORIZONTAL)
        self.input_text.SetMinSize((100, -1))
        self.input_text.Bind(wx.EVT_TEXT_ENTER, self.on_enter)

        self.start_btn = wx.Button(
            self.main_panel, label='Start', style=wx.ALIGN_CENTER_HORIZONTAL)
        self.start_btn.Bind(wx.EVT_BUTTON, self.start)

        # 设置顶部面板的布局
        topsizer = wx.BoxSizer(wx.HORIZONTAL)
        topsizer.Add(self.correct_label, 0, wx.ALL, 5)
        topsizer.Add(self.error_label, 0, wx.ALL, 5)
        topsizer.AddStretchSpacer(1)
        topsizer.Add(nums_label, 0, wx.ALL, 5)
        topsizer.Add(self.nums_ctl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        topsizer.Add(time_label, 0, wx.ALL, 5)
        topsizer.Add(self.time_ctl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.top_panel.SetSizer(topsizer)

        # 设置主面板的布局
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(self.top_panel, 0, wx.EXPAND)
        mainsizer.AddStretchSpacer(1)
        mainsizer.Add(self.center_label, 0,
                      wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)
        mainsizer.AddStretchSpacer(1)
        mainsizer.Add(self.input_text, 0, wx.ALIGN_CENTER_HORIZONTAL)
        mainsizer.Add(self.start_btn, 0,  wx.ALIGN_CENTER_HORIZONTAL)
        mainsizer.AddStretchSpacer(1)

        self.main_panel.SetSizer(mainsizer)

        # 设置窗口的布局
        window_sizer = wx.BoxSizer(wx.VERTICAL)
        window_sizer.Add(self.main_panel, 1, wx.EXPAND)
        self.SetSizer(window_sizer)

        self.Show()

        self.center_label.Hide()
        self.input_text.Hide()

        # 绑定事件
        self.time_ctl.Bind(wx.EVT_SPINCTRL, self.on_time_changed)
        self.nums_ctl.Bind(wx.EVT_SPINCTRL, self.on_nums_changed)

    def on_time_changed(self, event):
        self.display_time = event.GetEventObject().GetValue()

    def on_nums_changed(self, event):
        self.nums = event.GetEventObject().GetValue()

    def set_display_time(self, nums, display_time):
        self.nums = nums
        self.display_time = display_time
        self.time_ctl.SetValue(display_time)
        self.nums_ctl.SetValue(nums)

    def start_timer(self, event):
        self.timer.Stop()
        self.timer.Unbind(wx.EVT_TIMER)

        self.center_label.SetLabel('Go')
        self.Refresh()

        self.show_random_number()

    def start(self, event):
        self.finished = False
        self.set_display_time(2, 1000)
        self.correct_count = 0
        self.error_count = 0
        self.start_btn.Hide()

        self.center_label.SetLabel('Ready!')
        self.center_label.Show()
        self.Refresh()

        # 开始计时器
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.start_timer, self.timer)
        self.timer.StartOnce(1000)

    def generate_random_number(self):
        if self.nums < 2 or self.nums > 6:
            return "位数参数应在2-6之间"

        min_value = 10 ** (self.nums - 1)
        max_value = 10 ** self.nums - 1
        return random.randint(min_value, max_value)

    def show_random_number(self):
        if self.finished:
            return

        # 生成随机数
        random_num = self.generate_random_number()

        # 在中间文本显示随机数
        self.input_text.Hide()
        self.input_text.SetValue('')
        self.center_label.SetLabel(str(random_num))
        self.center_label.Show()
        self.Refresh()

        # 启动定时器以在显示时间结束后显示输入文本框
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.show_input_text, self.timer)
        self.timer.StartOnce(self.display_time)

    def show_input_text(self, event):
        # 停止定时器
        self.timer.Stop()

        # 显示输入文本框， 隐藏文字
        self.center_label.Hide()
        self.input_text.Show()
        self.input_text.SetFocus()

    def on_enter(self, event):
        # sourcery skip: extract-duplicate-method, merge-else-if-into-elif
        # 获取用户输入
        user_input = self.input_text.GetValue()

        # 获取之前显示的随机数
        random_num = int(self.center_label.GetLabel())

        # 判断用户输入和随机数是否相同
        if user_input == str(random_num):
            self.correct_count += 1
        else:
            self.error_count += 1

        # 更新正确数和错误数的显示
        self.correct_label.SetLabel(f'正确数: {self.correct_count}')
        self.error_label.SetLabel(f'错误数: {self.error_count}')
        self.Refresh()

        if (self.correct_count + self.error_count) % 10 == 0:
            if self.error_count / (self.correct_count + self.error_count) < 0.3:
                if self.display_time > 200:
                    self.set_display_time(self.nums, self.display_time-200)
                    self.error_count = 0
                    self.correct_count = 0
                elif self.nums < 6:
                    self.set_display_time(self.nums+1, 1000)
                    self.error_count = 0
                    self.correct_count = 0
                else:
                    self.finished = True
                    self.center_label.SetLabel('训练完成')
                    self.center_label.Show()
                    self.start_btn.Show()
            else:
                if self.display_time < 1000:
                    self.set_display_time(self.nums, self.display_time+200)
                    self.error_count = 0
                    self.correct_count = 0
                elif self.nums > 2:
                    self.set_display_time(self.nums-1, 1000)
                    self.error_count = 0
                    self.correct_count = 0
                else:
                    self.finished = True
                    self.center_label.SetLabel('训练失败，请重新训练')
                    self.center_label.Show()
                    self.start_btn.Show()

        self.show_random_number()


app = wx.App()

frame = MyWindow()
frame.SetSize((500, 400))
frame.Show()


app.MainLoop()
