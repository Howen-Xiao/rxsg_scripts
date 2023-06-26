import cdtMainUI as cdt
import occupyCity as occp
import battleCommand as bat
import win32api
import win32con
import win32gui
import time
import winsound
from PySide2.QtCore import Signal, QObject
#自动刷烽火战场

pauseflag = False
total_count = 0 #全局计数
acceflag = False #是否加速
# 城市信息
city1 = [0,0,0,0]
city2 = [0,0,0,0]
city3 = [0,0,0,0]
city4 = [0,0,0,0]
city5 = [0,0,0,0]

# 接受城市信息
def iniCityInfo(rec_city1, rec_city2, rec_city3, rec_city4, rec_city5):
    global city1, city2, city3, city4, city5
    city1 = rec_city1.copy()
    city2 = rec_city2.copy()
    city3 = rec_city3.copy()
    city4 = rec_city4.copy()
    city5 = rec_city5.copy()

# 暂停
def pause():
    global pauseflag
    print("正在暂停脚本...")
    fhMsg.sendBattleMessSignal("正在暂停脚本...")
    if(not(pauseflag)):
        pauseflag = True

# 是否加速
def changeAcceState(isAcce):
    global acceflag
    acceflag = isAcce

# 设置后台点击
t_delay_battle = 0.1 #战斗指挥时延，每个命令后自动设置时延，防止刷新不出

def doClick(hwnd, cx, cy): #后台点击
    long_position = win32api.MAKELONG(int(cx), int(cy))#模拟鼠标指针 传送到指定坐标
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)#模拟鼠标按下
    time.sleep(t_delay_battle)
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)#模拟鼠标弹起
    time.sleep(t_delay_battle)

# 设置信号函数
class fhSignal(QObject):
    battleSignal = Signal(str)
    finishSignal = Signal()

    def sendBattleMessSignal(self, msg):
        self.battleSignal.emit(msg)

    def sendfinishSignal(self):
        self.finishSignal.emit()

fhMsg = fhSignal()

# 设置等待函数,等待T秒，如果暂停指针改变则立刻暂停
def waitingTime(t):
    for i in range(t):
        time.sleep(1)
        if(pauseflag):
            print("程序已暂停")
            return

#挑战名将
def fenghuo_general(hwnd, city, num):
    if(pauseflag): return #暂停指令后退出
    global total_count
    if(hwnd!=0):
        windowRec = win32gui.GetWindowRect(hwnd) # 目标句柄窗口的坐标
        nx = city[0] - windowRec[0]
        ny = city[1] - windowRec[1]
    i = 0
    if(num != 0):
        s = "本城市为斗将战"
        print(s)
        fhMsg.sendBattleMessSignal(s)
    while(i<num):
        # 第一次打开，需要等足够时间，以防加载不出来
        if(total_count != 0):
            t = 1
        else:
            t = 2
        if(pauseflag): return #暂停指令后退出
        doClick(hwnd, nx, ny)
        time.sleep(t)
        if((acceflag)and(total_count != 0 )):
            doClick(hwnd, cdt.fenghuoUI[4].x, cdt.fenghuoUI[4].y) #名将加速
            time.sleep(t)
            doClick(hwnd, cdt.fenghuoUI[6].x, cdt.fenghuoUI[6].y) #加速确定
            time.sleep(t)
        doClick(hwnd, cdt.fenghuoUI[0].x, cdt.fenghuoUI[0].y) #挑战名将
        time.sleep(t)
        doClick(hwnd, cdt.fenghuoUI[1].x, cdt.fenghuoUI[1].y) #查看结果
        time.sleep(t)
        doClick(hwnd, cdt.fenghuoUI[2].x, cdt.fenghuoUI[2].y) #离开
        time.sleep(t)
        s = "已完成%d次出征"%(i+1)
        print(s)
        fhMsg.sendBattleMessSignal(s)
        if(pauseflag): 
            print("返回")
            return #暂停指令后退出
        i = i + 1
        total_count = total_count + 1
        if(not(acceflag)):
            waitingTime(99)

#挑战城池
def fenghuo_city(hwnd, city, num):
    if(pauseflag): return #暂停指令后退出
    global total_count
    if(hwnd!=0):
        windowRec = win32gui.GetWindowRect(hwnd) # 目标句柄窗口的坐标
        nx = city[0] - windowRec[0]
        ny = city[1] - windowRec[1]
    i = 0
    if(num != 0):
        s = "正在攻击新城市"
        print("正在攻击新城市")
        fhMsg.sendBattleMessSignal(s)
    while(i<num):
        # 第一次打开城池，需要等足够时间，以防加载不出来
        if(total_count != 0):
            t = 1
        else:
            t = 2
        if(pauseflag): return #暂停指令后退出
        doClick(hwnd, nx, ny)
        time.sleep(t) #打开城池
        if((acceflag)and(total_count != 0 )):
            doClick(hwnd, cdt.fenghuoUI[5].x, cdt.fenghuoUI[5].y) #城池加速
            time.sleep(0.5)
            doClick(hwnd, cdt.fenghuoUI[6].x, cdt.fenghuoUI[6].y) #加速确定
            time.sleep(0.5)
        doClick(hwnd, cdt.fenghuoUI[3].x, cdt.fenghuoUI[3].y) #挑战
        time.sleep(t)
        occp.openArmPage() #打开军事页面
        time.sleep(t)
        occp.commandArm(0) #指挥第一支军队     
        time.sleep(t)
        bat.battleCommand_4() #指挥部队
        time.sleep(t)
        if(pauseflag): return #暂停指令后退出
        s = "已完成%d次出征"%(i+1)
        print(s)
        fhMsg.sendBattleMessSignal(s)
        i = i + 1
        total_count = total_count + 1
        if(not(acceflag)):
            waitingTime(99)

# 执行烽火战场指令
def excuteBattle():
    global total_count
    total_count = 0
    hwnd = cdt.hwnd
    sum = city1[3] + city2[3] + city3[3] + city4[3] + city5[3] #总次数
    # 城市1
    if(city1[2] == 0): #军队战
        fenghuo_city(hwnd, city1, city1[3])
    elif(city1[2] == 1): #斗将战
        fenghuo_general(hwnd, city1, city1[3])

    # 城市2
    if(city2[3] != 0)and(total_count != 0)and(not(acceflag)):
        waitingTime(99)
    if(city2[2] == 0): #军队战
        fenghuo_city(hwnd, city2, city2[3])
    elif(city2[2] == 1): #斗将战
        fenghuo_general(hwnd, city2, city2[3])

    # 城市3
    if(city3[3] != 0)and(total_count != 0)and(not(acceflag)):
        waitingTime(99)
    if(city3[2] == 0): #军队战
        fenghuo_city(hwnd, city3, city3[3])
    elif(city3[2] == 1): #斗将战
        fenghuo_general(hwnd, city3, city3[3])

    # 城市4
    if(city4[3] != 0)and(total_count != 0)and(not(acceflag)):
        waitingTime(99)
    if(city4[2] == 0): #军队战
        fenghuo_city(hwnd, city4, city4[3])
    elif(city4[2] == 1): #斗将战
        fenghuo_general(hwnd, city4, city4[3])

    # 城市5
    if(city5[3] != 0)and(total_count != 0)and(not(acceflag)):
        waitingTime(99)
    if(city5[2] == 0): #军队战
        fenghuo_city(hwnd, city5, city5[3])
    elif(city5[2] == 1): #斗将战
        fenghuo_general(hwnd, city5, city5[3])
    # 战场完成结算
    s = "烽火战场已结束"
    print(s)
    fhMsg.sendBattleMessSignal(s)
    fhMsg.sendfinishSignal()

if __name__ == '__main__':
    hwnd = 0x0012034E
    leftUp = [210,135]
    rightDown = [1710,1025]
    acceflag = False  #是否加速
    cdt.initialCoornadite(leftUp, rightDown, hwnd)

    city2_1 = [1375,662] #吕布
    city2_2 = [1272,582] #许褚
    city2_3 = [1213,668] #高顺
    city2_4 = [1142,729] #张辽
    city2_5 = [1042,674] #臧霸

    # fenghuo_general(city2_1, 10)
    # fenghuo_general(city2_2, 10)
    fenghuo_city(city2_3, 18)
    fenghuo_city(city2_4, 20)
    fenghuo_city(city2_5, 10)

    winsound.Beep(600,1000)