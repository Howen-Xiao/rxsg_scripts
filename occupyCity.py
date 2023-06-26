# 本文件定义战场路线、清理城市守军的步骤
import win32gui
import win32con
import win32api
import time
import cdtMainUI as cdt
import battleCommand as bat
from PySide2.QtCore import Signal, QObject

playerNum = 1 #玩家数量
commandType = 1 #指挥方案
armtype = 1 #军队配置方案
routetype = 1 #出征路线
hwnd = cdt.hwnd
pauseflag = False #设置暂停点全局变量为False
endflag = False #设置结束脚本标记
curCity = 0 #当前城市
tarCity = 1 #目标城市
troopnum = playerNum*3 #军队数量
acce = 1 # 全局加速系数，当拿到加速任务后变为0.4

# 初始化战场人数、战场难度
def initialSetting(pnum, battle, arm, rtype, hd):
    global playerNum, commandType, armtype, routetype, hwnd
    global pauseflag, endflag
    global curCity, tarCity, troopnum, acce
    # 接收界面传来的参数
    playerNum = pnum
    commandType = battle
    armtype = arm
    routetype = rtype
    hwnd = hd
    # 标记初始化
    pauseflag = False
    endflag = False
    # 其他参数初始化
    curCity = 0 #当前城市
    tarCity = 1 #目标城市
    acce = 1
    troopnum = playerNum*3

# 战场路线
route1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18] #路线1-全刷
route2 = [0,1,7,12,13,14,15,16,17,18] #路线2-仅刷主线
route3 = [0,1,7,8,9,12,13,14,15,16,17,18] #路线3-拿攻击
route4 = [0,1,2,3,4,7,12,13,14,15,16,17,18] #路线4-拿加速
route5 = [0,1,2,3,4,5,6,7,8,9,12,13,14,15,16,17,18] #路线5
route = [route1, route2, route3, route4, route5]

# 设置后台点击
t_delay_battle = 0.1 #战斗指挥时延，每个命令后自动设置时延，防止刷新不出

def doClick(hwnd, cx, cy): #后台点击
    long_position = win32api.MAKELONG(int(cx), int(cy))#模拟鼠标指针 传送到指定坐标
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)#模拟鼠标按下
    time.sleep(t_delay_battle)
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)#模拟鼠标弹起
    time.sleep(t_delay_battle)

def doubleClick(hwnd, cx, cy): #后台双击
    long_position = win32api.MAKELONG(int(cx), int(cy))#模拟鼠标指针 传送到指定坐标
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)#模拟鼠标按下
    time.sleep(0.05)
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)#模拟鼠标弹起
    time.sleep(0.05)
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)#模拟鼠标按下
    time.sleep(0.05)
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)#模拟鼠标弹起
    time.sleep(0.05) 

# 改变战场指挥时延
def changeDelayTime(t):
    global t_delay_battle
    t_delay_battle = t

# 定义信号函数
class BattleSingal(QObject):
    battleMsgSignal = Signal(str)
    curCitySignal = Signal(int)
    tarCitySignal = Signal(int)
    troopSignal = Signal(int)
    acceSignal = Signal()
    pauseSignal = Signal()
    stopSignal = Signal()

    def sendMsg(self, msg):
        self.battleMsgSignal.emit(msg)
    
    def sendCurCityNum(self, citynum):
        self.curCitySignal.emit(citynum)
    
    def sendTarCityNum(self, citynum):
        self.tarCitySignal.emit(citynum)
    
    def sendtroopNum(self, troopnum):
        self.troopSignal.emit(troopnum)
    
    def sendAcceSignal(self):
        self.acceSignal.emit()
    
    def sendPauseStateSignal(self):
        self.pauseSignal.emit()
    
    def sendStopStateSignal(self):
        self.stopSignal.emit()

battleMsg = BattleSingal()

# 打完战场补兵
def supply(plannum):
    time.sleep(t_delay_battle*2)
    doClick(cdt.hwnd, cdt.supply[0].x, cdt.supply[0].y) #选择军队
    time.sleep(t_delay_battle)
    doClick(cdt.hwnd, cdt.supply[1].x, cdt.supply[1].y) #设置军队
    time.sleep(t_delay_battle)
    doClick(cdt.hwnd, cdt.supply[2].x, cdt.supply[2].y) #设置方案
    doClick(cdt.hwnd, cdt.supply[3].x, cdt.supply[3].y + cdt.supply_dy*(plannum-1)) #选择方案
    doClick(cdt.hwnd, cdt.supply[4].x, cdt.supply[4].y) #保存
    time.sleep(t_delay_battle*2)

# 领取任务奖励
def reward(): 
    time.sleep(0.5)
    doClick(cdt.hwnd, cdt.mainUI[7].x, cdt.mainUI[7].y) #任务栏目
    time.sleep(1)
    doClick(cdt.hwnd, cdt.taskUI[0].x, cdt.taskUI[0].y) #战场任务
    time.sleep(1)
    doClick(cdt.hwnd, cdt.taskUI[1].x, cdt.taskUI[1].y) #战场任务
    time.sleep(1)
    doClick(cdt.hwnd, cdt.taskUI[2].x, cdt.taskUI[2].y) #战场任务
    time.sleep(1)
    doClick(cdt.hwnd, cdt.taskUI[3].x, cdt.taskUI[3].y) #战场任务
    time.sleep(1)

# 攻击城市
def attackCity(toCity):
    doClick(cdt.hwnd, cdt.city[toCity].x, cdt.city[toCity].y)
    time.sleep(0.25)

# 攻击城市守军
def attackArm(armnum):
    doClick(cdt.hwnd, cdt.battleMove[armnum].x, cdt.battleMove[armnum].y)

# 关闭城市页面
def closeCity():
    doClick(cdt.hwnd, cdt.battleMove[2].x, cdt.battleMove[2].y)

# 打开军事页面
def openArmPage():
    doClick(cdt.hwnd, cdt.mainUI[5].x, cdt.mainUI[5].y)

# 指挥第几只军队
def commandArm(armnum):
    doClick(cdt.hwnd, cdt.armUI[armnum].x, cdt.armUI[armnum].y)

# 双击将领头像窗口指挥部队
def commandArm2():
    doubleClick(cdt.hwnd, cdt.supply[0].x, cdt.supply[0].y)

# 等待时间
def waiting(t):
    for i in range(int(t)):
        time.sleep(1)
        if(pauseflag):
            return

# 暂停后直接输入出发点、目的地、军队数量
def inputNewMess(route):
    print("城市代码如下:")
    for i in range(len(cdt.city)):
        print("%d.%s"%(i, cdt.city[i].name), end='\t')
    print()
    # 输入并检测出发城市
    boolean = True
    while boolean:
        fromNum = int(input("请输入出发城市编号："))
        for i in range(len(route)):
            if(route[i] == fromNum):
                boolean = False
        if(boolean):
            print("当前路线不含该城市，请重新输入！")
    # 输入并检测目的城市
    boolean = True
    while boolean:
        toNum = int(input("请输入目的城市编号："))
        for i in range(len(route)):
            if(route[i] == toNum):
                boolean = False
        if(boolean):
            print("当前路线不含该城市，请重新输入！")
    # 输入军队数量
    troopnum = int(input("请输入军队数量："))
    return (fromNum, toNum, troopnum)

# 找到某一城市在方案中的位置
def findCityIndex(route, cityNum):
    notFind = True
    for i in range(len(route)):
        if(route[i] == cityNum):
            notFind = False
            break
    if notFind:
        return -1
    else:
        return i

# 占领城市
def occupyCity(fromCity, toCity, troopNum):
    global pauseflag
    # 起步城市，目的城市，城市守军数量
    s = "正在攻击城市%s"%cdt.city[toCity].name
    print(s)
    battleMsg.sendMsg(s)
    leftArm = troopNum # 剩余军队数量
    battleMsg.sendtroopNum(leftArm)
    curCity = fromCity # 当前城市设为出发城市
    while(leftArm > 0):
         #暂停检测点1
        if pauseflag: return
        attackCity(toCity) # 攻击城市
        # 河内是个特殊城市，军队数量少1支，需要判断
        if(toCity == 11):
            attackArm(1)
        # 如果是其他城市，先攻击军队，最后打守将
        else:
            if(leftArm == 1): #如果仅剩1支军队
                attackArm(0)
            else:
                attackArm(1)
        #暂停检测点2
        if pauseflag: return 
        # # 打开军事页面
        # openArmPage()
        # #暂停检测点3
        # if pauseflag: return 
        # # 计算出征时间
        t = int(30 * cdt.distance[curCity][toCity] * acce) + 1
        waiting(t)
        #暂停检测点4
        if pauseflag: return 
        # 当前城市位置改变
        curCity = toCity
        # 发送信号
        battleMsg.sendCurCityNum(curCity)
        # 指挥第一支军队
        # commandArm(0)
        commandArm2()
        # 樊城第一支部队需要多等一段时间，防止刷不出来
        if((toCity==1)and(leftArm == troopnum)):
            time.sleep(1)
        else:
            time.sleep(t_delay_battle*2)
        # 判断当前是否是巨鹿最后一支军队，如果是，不要补给，停在结算页面
        tail = 1
        if((toCity==18)and(leftArm==1)): #如果是巨鹿最后一支军队，不要补给
            tail = 0
        # 战术
        if(commandType == 1):
            bat.battleCommand_1(tail) #简单战场
            if(tail):
                supply(armtype)
        elif(commandType == 2):
            bat.battleCommand_2(tail) #精英战场
            if(tail):
                supply(armtype)
        elif(commandType == 3):
            bat.battleCommand_3(tail) #指挥方案三
            if(tail):
                supply(armtype)
        elif(commandType == 4):
            bat.battleCommand_4(tail) #指挥方案四
            if(tail):
                supply(armtype)
        # 完成后，剩余军队数量-1,当前城市设为目标城市
        s = "已清理%d支军队"%(troopNum-leftArm+1)
        print(s)
        battleMsg.sendMsg(s)
        leftArm = leftArm - 1
        battleMsg.sendtroopNum(leftArm)
        # 设置反应时间，防止页面刷不出来
        time.sleep(t_delay_battle)

# 执行出征路线
def excuteRoute(routeNum):
    global pauseflag, endflag
    global acce
    global curCity, tarCity, troopnum
    # 设置当前战场路线
    curRoute = route[routeNum-1]
    # 每个城市的守军数量
    troopnum = playerNum*3
    # 设置当前城市
    i = 0
    curCity = curRoute[i]
    tarCity = curRoute[i+1]
    # 结束条件：当前城市不是最后一座城市
    routelen = len(curRoute)
    while(i<routelen-1):
        # 如果目标城市是河内，军队数量-1
        if(tarCity == 11):
            troopnum = troopnum - 1
        occupyCity(curCity, tarCity, troopnum) 
        # 如果暂停
        if pauseflag: 
            print("程序已暂停")
            battleMsg.sendMsg("程序已暂停")  #发送状态信息
            battleMsg.sendPauseStateSignal()  #发送暂停信息
            while pauseflag:
                time.sleep(0.5)
                if(endflag):
                    print("当前战场流程已结束")
                    battleMsg.sendMsg("当前战场流程已结束")
                    battleMsg.sendStopStateSignal()
                    return  #结束脚本
            continue
        else:
            # 如果顺利刷完该城市
            # 补给
            # 放在攻击队伍里了，打完一支补给一次
            # supply()
            # 当前城市设为目标城市
            curCity = tarCity # 更新当前城市
            i = findCityIndex(curRoute, curCity) # 找到当前城市的索引
            if(i<routelen-1):
                tarCity = curRoute[i+1] # 更新目标城市
                battleMsg.sendTarCityNum(tarCity)
                troopnum = playerNum*3 # 城市守军数量恢复
            else: #如果是最后一个城市
                print("战场路线成功完成！")
                battleMsg.sendMsg("战场路线成功完成！")
                battleMsg.sendStopStateSignal()
            # 如果当前城市是宛城，领取奖励，并且改变加速系数
            if(curCity == 4):
                reward()
                acce = 0.4
                battleMsg.sendAcceSignal()
            # 如果当前城市是汝南、西华、河内，领取奖励
            if(curCity == 6)or(curCity == 9)or(curCity == 11):
                reward()

# 改变战场信息：出发城市、目标城市、军队数量
def changeBattleMess(newCurcity, newTarcity, newTroopnum, isAcce):
    global curCity,tarCity,troopnum,acce
    curCity = newCurcity
    tarCity = newTarcity
    troopnum = newTroopnum
    if(isAcce):
        acce = 0.4
    else:
        acce = 1

# 开始脚本
def run():
    msg = "正在执行路线%d，脚本2秒后启动..."%routetype
    print(msg)
    battleMsg.sendMsg(msg)
    time.sleep(2)
    excuteRoute(routetype)

# 暂停脚本
def pause():
    global pauseflag
    print("正在暂停脚本...")
    battleMsg.sendMsg("正在暂停脚本...")
    if(not(pauseflag)):
        pauseflag = True

# 继续脚本
def goon():
    global pauseflag
    print("重新启动脚本...")
    battleMsg.sendMsg("重新启动脚本...")
    if(pauseflag):
        pauseflag = False

# 结束脚本
def end():
    global endflag
    if(not(endflag)):
        endflag = True

if __name__ == '__main__':
    hwnd = 0x00141E1C
    leftUp = [530,135]
    rightDown = [2030,1035]
    cdt.initialCoornadite(leftUp, rightDown, hwnd)

    playerNum = 4
    commandType = 4
    armtype = 4
    routetype = 1
    initialSetting(playerNum, commandType, armtype)

    print("正在启动脚本...")
    time.sleep(3)
    excuteRoute(routetype)
    
