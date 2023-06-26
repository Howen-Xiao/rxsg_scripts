# 本文件包含游戏内所有坐标、战场两个城市之间的距离参数
import win32gui

# 定义坐标系类
class cdt: #坐标，包含三个属性：名称，x，y
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

# 定义坐标转换函数
def translateCor(oriCor, scare, offset): #坐标转换
    x = oriCor.x *scare + offset[0]
    y = oriCor.y *scare + offset[1]
    newCor = cdt(oriCor.name, x, y)
    return newCor

# 字符串转换16进制
def str2hex(s):
    # s: '0x4B'
    s = s[2:]   # 去掉’0x‘
    odata = 0
    su = s.upper()
    for c in su:
        tmp = ord(c)    # ACSII码
        if tmp <= ord('9') :
            odata = odata << 4  # 高位的数值乘以2^4
            odata += tmp - ord('0')
        elif ord('A') <= tmp <= ord('F'):
            odata = odata << 4
            odata += tmp - ord('A') + 10
    return odata

# 游戏窗口原坐标
oriLeftUp = [0,0]
oriRightDown = [1000,600]

# 游戏窗口句柄参数
hwnd = 0x0000

# 游戏主界面坐标
ori_mainUI = []
ori_mainUI.append(cdt('城内',312,18)) #0
ori_mainUI.append(cdt('城池',378,18)) #1
ori_mainUI.append(cdt('地图',456,18)) #2
ori_mainUI.append(cdt('战场',524,18)) #3
ori_mainUI.append(cdt('将领',734,18)) #4
ori_mainUI.append(cdt('军队',790,18)) #5
ori_mainUI.append(cdt('联盟',858,18)) #6
ori_mainUI.append(cdt('任务',926,18)) #7
ori_mainUI.append(cdt('报告',790,576)) #8
ori_mainUI.append(cdt('开关',958,510)) #9
ori_mainUI.append(cdt('斩妖杀怪',944,190)) #10
ori_mainUI.append(cdt('过关斩将',950,274)) #11
mainUI = ori_mainUI.copy()

# ---------------------黄巾战场-------------------------
# -----------------------------------------------------
# 战场城市坐标
ori_city = []
ori_city.append(cdt('襄阳',410,368)) #襄阳 编号0
ori_city.append(cdt('樊城',565,366)) #樊城 编号1
ori_city.append(cdt('西鄂精山',722,403)) #西鄂精山 编号2
ori_city.append(cdt('泾阳',802,400)) #泾阳 编号3
ori_city.append(cdt('宛城',861,430)) #宛城 编号4
ori_city.append(cdt('高陵',729,487)) #高陵 编号5
ori_city.append(cdt('汝南',809,483)) #汝南 编号6
ori_city.append(cdt('南阳',587,278)) #南阳 编号7
ori_city.append(cdt('颍川',514,299)) #颍川 编号8
ori_city.append(cdt('西华',439,281)) #西华 编号9
ori_city.append(cdt('阳翟',542,213)) #阳翟 编号10
ori_city.append(cdt('河内',534,150)) #河内 编号11
ori_city.append(cdt('新野',728,305)) #新野 编号12
ori_city.append(cdt('武平',798,223)) #武平 编号13
ori_city.append(cdt('陈留',856,312)) #陈留 编号14
ori_city.append(cdt('仓亭',926,273)) #仓亭 编号15
ori_city.append(cdt('广宗',906,225)) #广宗 编号16
ori_city.append(cdt('下曲阳',820,160)) #下曲阳 编号17
ori_city.append(cdt('巨鹿',906,144)) #巨鹿 编号18
city = ori_city.copy()
# 战场动作
ori_battleMove = [] #攻击城市
ori_battleMove.append(cdt("攻击第一支军队", 850, 210))
ori_battleMove.append(cdt("攻击第二支军队", 850, 234))
ori_battleMove.append(cdt("关闭",862, 468))
battleMove = ori_battleMove.copy()
ori_supply = [] #补给军队
ori_supply.append(cdt("选择军队", 670,545))
ori_supply.append(cdt("配置军队", 675,565))
ori_supply.append(cdt("方案",720,130))
ori_supply.append(cdt("选择方案",735,167))
ori_supply.append(cdt("保存",585,505))
ori_supply.append(cdt("步长",0,23))
supply = ori_supply.copy()
ori_supply_dy = 23
supply_dy = ori_supply_dy
ori_command = [] #战场指挥界面
ori_command.append(cdt("下一回合",520,525))
ori_command.append(cdt("使用兵法",600,525))
ori_command.append(cdt("关闭",935,525))
command = ori_command.copy()
ori_arm = [] #战场兵种界面
ori_arm.append(cdt("兵种1",352,200))
ori_arm.append(cdt("兵种2",410,200))
ori_arm.append(cdt("兵种3",352,250))
ori_arm.append(cdt("兵种4",410,250))
ori_arm.append(cdt("兵种5",352,300))
ori_arm.append(cdt("兵种6",410,300))
ori_arm.append(cdt("兵种7",352,350))
ori_arm.append(cdt("兵种8",410,350))
ori_arm.append(cdt("兵种9",352,400))
ori_arm.append(cdt("兵种10",410,400))
ori_arm.append(cdt("兵种11",352,450))
ori_arm.append(cdt("兵种12",410,450))
arm = ori_arm.copy()
# 兵种动作偏移量
ori_mov_x = 32
ori_mov_y = 12
ori_mov_dy = 20
mov_x = ori_mov_x
mov_y = ori_mov_y
mov_dy = ori_mov_dy
# 战场距离
distance = [[0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [1,0,1,2,3,2,3,1,2,3,2,3,2,3,4,5,6,7,8],
            [2,1,0,1,2,1,2,2,3,4,3,4,3,4,5,6,7,8,9],
            [2,2,1,0,1,2,3,3,4,5,4,5,4,5,6,7,8,9,10],
            [2,3,2,1,0,3,4,4,5,6,5,6,5,6,7,8,9,10,11],
            [2,2,1,2,3,0,1,3,4,5,4,5,4,5,6,7,8,9,10],
            [2,3,2,3,4,1,0,4,5,6,5,6,5,6,7,8,9,10,11],
            [2,1,2,3,4,3,4,0,1,2,1,2,1,2,3,4,5,6,7],
            [2,2,3,4,5,4,5,1,0,1,2,3,2,3,4,5,6,7,8],
            [2,3,4,5,6,5,6,2,1,0,3,4,3,4,5,6,7,8,9],
            [2,2,3,4,5,4,5,1,2,3,0,1,2,3,4,5,6,7,8],
            [2,3,4,5,6,5,6,2,3,4,1,0,3,4,5,6,7,8,9],
            [2,2,3,4,5,4,5,1,2,3,2,3,0,1,2,3,4,5,6],
            [2,3,4,5,6,5,6,2,3,4,3,4,1,0,1,2,3,4,5],
            [2,4,5,6,7,6,7,3,4,5,4,5,2,1,0,1,2,3,4],
            [2,5,6,7,8,7,8,4,5,6,5,6,3,2,1,0,1,2,3],
            [2,6,7,8,9,8,9,5,6,7,6,7,4,3,2,1,0,1,2],
            [2,7,8,9,10,9,10,6,7,8,7,8,5,4,3,2,1,0,1],
            [2,8,9,10,11,10,11,7,8,9,8,9,6,5,4,3,2,1,0]]

# ------------------主界面“军队”页面----------------------
# -------------------------------------------------------
ori_armUI = []
ori_armUI.append(cdt("指挥第一支军队",920,200))
armUI = ori_armUI.copy()

# ------------------主界面“任务”页面----------------------
# -------------------------------------------------------
ori_taskUI = []
ori_taskUI.append(cdt("战场任务",755,125))
ori_taskUI.append(cdt("第一项任务",387,195))
ori_taskUI.append(cdt("领取奖励",835,530))
ori_taskUI.append(cdt("关闭",915,530))
taskUI = ori_taskUI.copy()

# --------------------烽火征途---------------------------
ori_fenghuoUI = []
ori_fenghuoUI.append(cdt("挑战名将",732,514))
ori_fenghuoUI.append(cdt("查看结果",584,518))
ori_fenghuoUI.append(cdt("离开",634,426))
ori_fenghuoUI.append(cdt("攻击城市",644,434))
ori_fenghuoUI.append(cdt("名将加速",844,118))
ori_fenghuoUI.append(cdt("城市加速",854,196))
ori_fenghuoUI.append(cdt("加速确定",586,278))
fenghuoUI = ori_fenghuoUI.copy()

# -------------------大地图出征--------------------------
ori_mapattack = []
ori_mapattack.append(cdt("X",812,538))
ori_mapattack.append(cdt("Y",864,538))
ori_mapattack.append(cdt("查找",904,538))
ori_mapattack.append(cdt("屏幕中心",628,292))
ori_mapattack.append(cdt("攻击",618,364))
ori_mapattack.append(cdt("军队方案",396,454))
ori_mapattack.append(cdt("方案一",359,504))
ori_mapattack.append(cdt("选择将领",806,188))
ori_mapattack.append(cdt("第一位将领",810,232))
ori_mapattack.append(cdt("出征",794,514))
ori_mapattack.append(cdt("伤兵营",606,188)) #10
ori_mapattack.append(cdt("降兵营",764,190)) #11
ori_mapattack.append(cdt("全部治疗",698,472)) #12
ori_mapattack.append(cdt("确定",588,274)) #13
ori_mapattack.append(cdt("关闭",770,468)) #14
ori_mapattack.append(cdt("校场关闭",924,516)) #15
mapattack = ori_mapattack.copy()

# --------------------坐标变换---------------------------
def initialCoornadite(leftUp, rightDown, rechwnd):
    scare = (rightDown[0] - leftUp[0])/1000
    offset = leftUp

    global hwnd
    hwnd = rechwnd
    
    if(hwnd!=0):
        windowRec = win32gui.GetWindowRect(hwnd) # 目标句柄窗口的坐标
        offset[0] = offset[0] - windowRec[0]
        offset[1] = offset[1] - windowRec[1]

    global mainUI, city, battleMove, supply, command, arm, armUI, taskUI, fenghuoUI, mapattack
    for i in range(len(ori_mainUI)):
        mainUI[i] = translateCor(ori_mainUI[i], scare, offset)

    for i in range(len(ori_city)):
        city[i] = translateCor(ori_city[i], scare, offset)

    for i in range(len(ori_battleMove)):
        battleMove[i] = translateCor(ori_battleMove[i], scare, offset)

    for i in range(len(ori_supply)):
        supply[i] = translateCor(ori_supply[i], scare, offset)

    for i in range(len(ori_command)):
        command[i] = translateCor(ori_command[i], scare, offset)
    
    for i in range(len(ori_arm)):
        arm[i] = translateCor(ori_arm[i], scare, offset)

    for i in range(len(ori_armUI)):
        armUI[i] = translateCor(ori_armUI[i], scare, offset)

    for i in range(len(ori_taskUI)):
        taskUI[i] = translateCor(ori_taskUI[i], scare, offset)
    
    for i in range(len(ori_fenghuoUI)):
        fenghuoUI[i] = translateCor(ori_fenghuoUI[i], scare, offset)
    
    for i in range(len(ori_mapattack)):
        mapattack[i] = translateCor(ori_mapattack[i], scare, offset)

    global mov_x, mov_y, mov_dy, supply_dy
    mov_x = ori_mov_x*scare
    mov_y = ori_mov_y*scare
    mov_dy = ori_mov_dy*scare
    supply_dy = ori_supply_dy*scare

if __name__ == '__main__':
    scare = 1.5
    offset = [0, 0]
    print(ori_city[0].x, ori_city[0].y)
    print(city[0].x, city[0].y)
    for i in range(len(city)):
        city[i] = translateCor(ori_city[i], scare, offset)
    print(ori_city[0].x, ori_city[0].y)
    print(city[0].x, city[0].y)
