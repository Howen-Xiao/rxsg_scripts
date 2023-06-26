# 本文件定义了战场指挥方案
import cdtMainUI as cdt
import win32gui
import win32con
import win32api
import time

t_delay_battle = 0.1 #战斗指挥时延，每个命令后自动设置时延，防止刷新不出

def doClick(hwnd, cx, cy): #后台点击
    long_position = win32api.MAKELONG(int(cx), int(cy))#模拟鼠标指针 传送到指定坐标
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)#模拟鼠标按下
    time.sleep(t_delay_battle)
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)#模拟鼠标弹起
    time.sleep(t_delay_battle)

# 改变战场指挥时延
def changeDelayTime(t):
    global t_delay_battle
    t_delay_battle = t

# 自定义兵种类
class armClass:
    # 初始化兵种类
    def __init__(self, num):
        self.x = cdt.arm[num].x
        self.y = cdt.arm[num].y
    # 重新设定兵种位置
    def resetPosition(self, num):
        self.x = cdt.arm[num].x
        self.y = cdt.arm[num].y 
    # 兵种动作
    # 前进
    def mov(self):
        nx = self.x + cdt.mov_x
        ny = self.y + cdt.mov_y
        doClick(cdt.hwnd, self.x, self.y)
        # time.sleep(t_delay_battle)
        doClick(cdt.hwnd, nx, ny)
    # 防御
    def dfc(self):
        nx = self.x + cdt.mov_x
        ny = self.y + cdt.mov_y + cdt.mov_dy
        doClick(cdt.hwnd, self.x, self.y)
        # time.sleep(t_delay_battle)
        doClick(cdt.hwnd, nx, ny) 
    # 后退
    def bck(self):
        nx = self.x + cdt.mov_x
        ny = self.y + cdt.mov_y + cdt.mov_dy*2
        doClick(cdt.hwnd, self.x, self.y)
        # time.sleep(t_delay_battle)
        doClick(cdt.hwnd, nx, ny)   
     
def useTactics(): #使用兵法
    doClick(cdt.hwnd, cdt.command[1].x, cdt.command[1].y)

def nextRound(): #下一回合
    doClick(cdt.hwnd, cdt.command[0].x, cdt.command[0].y)

def closeCommand(): #关闭指挥界面窗口
    doClick(cdt.hwnd, cdt.command[2].x, cdt.command[2].y)

def battleCommand_1(tail=1): #战场指挥方案1，简单战场，直接下一回合
    nextRound()
    nextRound()
    nextRound()
    nextRound()
    nextRound()
    nextRound()
    nextRound()
    if(tail):
        closeCommand()

def battleCommand_2(tail=1): #战场指挥方案2，精英战场，带减速兵法
    CH = armClass(0)
    CN = armClass(1)
    TS = armClass(2)
    CH.dfc()
    CN.bck()
    TS.bck()
    nextRound() #1
    nextRound() #2
    nextRound() #3
    nextRound() #4
    useTactics() #使用兵法
    nextRound() #5
    nextRound() #6
    nextRound() #7
    nextRound() #8
    nextRound() #9
    nextRound() #10
    nextRound() #11
    nextRound() #12
    nextRound() #13
    nextRound() #14
    nextRound() #15
    nextRound() #16
    nextRound() #17
    useTactics() #使用兵法
    CN.mov()
    nextRound() #18
    nextRound() #19
    nextRound() #20
    if(tail):
        closeCommand()

def battleCommand_3(tail=1): #战场指挥方案3，困难战场
    CH = armClass(0)
    QQ = armClass(1)
    CN = armClass(2)
    TS = armClass(3)
    QZ = armClass(4)
    CH.dfc()
    QQ.dfc()
    CN.bck()
    TS.bck()
    QZ.dfc()
    nextRound() #第1回合
    useTactics() #使用兵法
    nextRound() #第2回合
    nextRound() #第3回合
    nextRound() #第4回合
    nextRound() #第5回合
    useTactics() #使用兵法
    nextRound() #第6回合
    nextRound() #第7回合
    nextRound() #第8回合
    nextRound() #第9回合
    useTactics() #使用兵法
    nextRound() #第10回合
    nextRound() #第11回合
    nextRound() #第12回合
    nextRound() #第13回合
    nextRound() #第14回合
    if(tail):
        closeCommand()

def battleCommand_4(tail=1): #战场指挥方案4，极难战场，最后一回合床弩前进
    CH = armClass(0)
    CN = armClass(1)
    TS = armClass(2)
    CH.dfc()
    CN.bck()
    TS.bck()
    nextRound() #第1回合
    useTactics() #使用兵法
    nextRound() #第2回合
    nextRound() #第3回合
    nextRound() #第4回合
    nextRound() #第5回合
    useTactics() #使用兵法
    nextRound() #第6回合
    nextRound() #第7回合
    nextRound() #第8回合
    nextRound() #第9回合
    useTactics() #使用兵法
    nextRound() #第10回合
    nextRound() #第11回合
    nextRound() #第12回合
    nextRound() #第13回合
    if(tail):
        closeCommand()

if __name__ == '__main__':
    hwnd = 0x000205FC
    leftUp = [210,135]
    rightDown = [1710,1025]
    cdt.initialCoornadite(leftUp, rightDown, hwnd)

    battleCommand_3()

    



