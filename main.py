from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QMessageBox
from PySide2.QtCore import Qt,QSettings, QCoreApplication, Signal, QObject
from PySide2.QtCore import QUrl
from PySide2.QtGui import QDesktopServices
from rxsg_ui import Ui_MainWindow
from othersettingDialog import Ui_SettingDialog
import win32api
import win32gui
import occupyCity as occp
import fenghuo as fh
import cdtMainUI as cdt
import getCursorPos as pos
import threading

curversion = "v1.12"

# Mainwindow
class Mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initInfo()
        self.fh_readInfo()
        #------------------黄巾战场--------------------
        self.ui.setCoordinateZS.clicked.connect(self.setZSCor)
        self.ui.setCoordinateYX.clicked.connect(self.setYXCor)
        self.ui.getHwndButton.clicked.connect(self.getHwndButton)
        self.ui.buttonStart.clicked.connect(self.startButton)
        self.ui.buttonPause.clicked.connect(self.pauseButton)
        self.ui.buttonGoOn.clicked.connect(self.goONButton)
        self.ui.buttonClose.clicked.connect(self.endButton)
        self.ui.exitAct.triggered.connect(QCoreApplication.instance().quit)
        self.ui.otherPara.triggered.connect(self.settingDialogShow)
        self.ui.aboutAct.triggered.connect(self.aboutDialogShow)
        self.ui.versionAct.triggered.connect(self.versionDialogShow)
        self.ui.getnewAction.triggered.connect(self.getNewVersion)

        occp.battleMsg.battleMsgSignal.connect(self.battleMsgSlot)  # 战场信息信号-槽
        occp.battleMsg.curCitySignal.connect(self.changeCurCitySlot)
        occp.battleMsg.tarCitySignal.connect(self.changeTarCitySlot)
        occp.battleMsg.troopSignal.connect(self.changeTroopNumSlot)
        occp.battleMsg.acceSignal.connect(self.changeAcceSlot)
        occp.battleMsg.pauseSignal.connect(self.recvPauseSlot) #暂停信息的信号
        occp.battleMsg.stopSignal.connect(self.recvStopSlot) #停止信息的信号
        #-------------------烽火战场--------------------
        self.ui.fh_city1_set.clicked.connect(self.setCity1Pos)
        self.ui.fh_city2_set.clicked.connect(self.setCity2Pos)
        self.ui.fh_city3_set.clicked.connect(self.setCity3Pos)
        self.ui.fh_city4_set.clicked.connect(self.setCity4Pos)
        self.ui.fh_city5_set.clicked.connect(self.setCity5Pos)
        self.ui.fh_start.clicked.connect(self.fh_startButton)
        self.ui.fh_pause.clicked.connect(self.fh_pauseButton)
        pos.posMsg.posSignal.connect(self.recvCity1Pos)
        pos.posMsg.posSignal.connect(self.recvCity2Pos)
        pos.posMsg.posSignal.connect(self.recvCity3Pos)
        pos.posMsg.posSignal.connect(self.recvCity4Pos)
        pos.posMsg.posSignal.connect(self.recvCity5Pos)
        fh.fhMsg.battleSignal.connect(self.fh_battleMsgSlot)
        fh.fhMsg.finishSignal.connect(self.fh_pauseMsgSlot)
    
    # 重写键盘事件
    def keyPressEvent(self, e):
        global lfupFlag,rndwFlag,hwndFlag
        x,y = win32api.GetCursorPos()
        if (e.key() == Qt.Key_S)and(lfupFlag):
            self.ui.leftUpX.setText("%s"%str(x))
            self.ui.leftUpY.setText("%s"%str(y))
            lfupFlag = False
            self.ui.plainTextEdit.appendPlainText("左上角坐标设置完成")
            self.ui.leftUpX.setEnabled(False)
            self.ui.leftUpY.setEnabled(False)
        if (e.key() == Qt.Key_S)and(rndwFlag):
            self.ui.rightDownX.setText("%s"%str(x))
            self.ui.rightDownY.setText("%s"%str(y))
            rndwFlag = False
            self.ui.plainTextEdit.appendPlainText("右下角坐标设置完成")
            self.ui.rightDownX.setEnabled(False)
            self.ui.rightDownY.setEnabled(False)
        if (e.key() == Qt.Key_S)and(hwndFlag):
            hwnd = win32gui.WindowFromPoint((x,y))
            self.ui.hwndLine.setText("%#x"%hwnd)
            hwndFlag = False
            self.ui.plainTextEdit.appendPlainText("游戏窗口句柄获取完成")
            self.ui.hwndLine.setEnabled(False)  
    
    # 设置左上角坐标
    def setZSCor(self):
        global lfupFlag
        self.ui.plainTextEdit.appendPlainText("正在设置左上角坐标...")
        self.ui.plainTextEdit.appendPlainText("鼠标移动到游戏界面左上角，按S键确定坐标")
        lfupFlag = True
        self.ui.leftUpX.setEnabled(True)
        self.ui.leftUpY.setEnabled(True)
    
    # 设置右下角坐标
    def setYXCor(self):
        global rndwFlag
        self.ui.plainTextEdit.appendPlainText("正在设置右下角坐标...")
        self.ui.plainTextEdit.appendPlainText("鼠标移动到游戏界面右下角，按S键确定坐标")
        rndwFlag = True
        self.ui.rightDownX.setEnabled(True)
        self.ui.rightDownY.setEnabled(True)
    
    # 获取当前窗口句柄
    def getHwndButton(self):
        global hwndFlag
        self.ui.plainTextEdit.appendPlainText("正在获取游戏窗口句柄...")
        self.ui.plainTextEdit.appendPlainText("将鼠标移动到游戏界面上，按S键确定游戏窗口句柄")
        hwndFlag = True
        self.ui.hwndLine.setEnabled(True)

    # -----------------------黄巾战场设置--------------------------   
    # 保存当前软件设置
    def saveInfo(self):
        settings = QSettings("config.ini",QSettings.IniFormat)
        settings.setValue("leftUpX",self.ui.leftUpX.text())
        settings.setValue("leftUpY",self.ui.leftUpY.text())
        settings.setValue("rightDownX",self.ui.rightDownX.text())
        settings.setValue("rightDownY",self.ui.rightDownY.text())
        settings.setValue("RouteType",self.ui.comboRoute.currentIndex())
        settings.setValue("CommandType",self.ui.comboCommand.currentIndex())
        settings.setValue("ArmType",self.ui.comboArm.currentIndex())
        settings.setValue("PlayerNum",self.ui.comboPlayerNum.currentIndex())
    
    # 读取先前的软件设置
    def initInfo(self):
        settings = QSettings("config.ini",QSettings.IniFormat)
        leftUpX = settings.value("leftUpX")
        leftUpY = settings.value("leftUpY")
        rightDownX = settings.value("rightDownX")
        rightDownY = settings.value("rightDownY")
        routetype = int(settings.value("RouteType"))
        commandtype = int(settings.value("CommandType"))
        armtype = int(settings.value("ArmType"))
        playernum = int(settings.value("PlayerNum"))

        self.ui.leftUpX.setText(leftUpX)
        self.ui.leftUpY.setText(leftUpY)
        self.ui.rightDownX.setText(rightDownX)
        self.ui.rightDownY.setText(rightDownY)
        self.ui.comboRoute.setCurrentIndex(routetype)
        self.ui.comboCommand.setCurrentIndex(commandtype)
        self.ui.comboArm.setCurrentIndex(armtype)
        self.ui.comboPlayerNum.setCurrentIndex(playernum)
    
    # 获取战场参数
    def getBallteMess(self):
        pnum = self.ui.comboPlayerNum.currentIndex()+1 #战场人数
        commadtype = self.ui.comboCommand.currentIndex()+1 #指挥方案
        armtype = self.ui.comboArm.currentIndex()+1 #军队方案
        routetype = self.ui.comboRoute.currentIndex()+1 #战场路线
        return (pnum, commadtype, armtype, routetype)
    
    # 获取界面参数
    def getUIMess(self):
        leftUpX = int(self.ui.leftUpX.text())
        leftUpY = int(self.ui.leftUpY.text())
        rightDownX = int(self.ui.rightDownX.text())
        rightDownY = int(self.ui.rightDownY.text())
        return(leftUpX, leftUpY, rightDownX, rightDownY)

    # 点击开始按钮后的事件
    def startButton(self):
        # 检查窗口句柄
        hwnd = self.ui.hwndLine.text()
        if(hwnd == ''):
            self.ui.plainTextEdit.appendPlainText("未获取窗口句柄，请检查！")
        else:
            self.saveInfo()
            # 获取界面参数
            (leftUpX, leftUpY, rightDownX, rightDownY) = self.getUIMess()
            leftUp = [leftUpX, leftUpY]
            rightDown = [rightDownX, rightDownY]
            hwnd = cdt.str2hex(hwnd)
            cdt.initialCoornadite(leftUp, rightDown, hwnd)
            # 获取战场参数
            (pnum, commandtype, armtype, routetype) = self.getBallteMess()
            occp.initialSetting(pnum, commandtype, armtype, routetype, hwnd)
            # 调整全局指挥时延
            settings = QSettings("config.ini",QSettings.IniFormat)
            t_delay = int(settings.value("delayTime"))*0.1
            occp.changeDelayTime(t_delay)
            # 按钮可用性调整
            self.ui.buttonPause.setEnabled(True)
            self.ui.buttonStart.setEnabled(False)
            self.ui.comboRoute.setEnabled(False)
            self.ui.comboCommand.setEnabled(False)
            self.ui.comboArm.setEnabled(False)
            self.ui.comboPlayerNum.setEnabled(False)
            self.ui.tabWidget.setTabEnabled(1,False)
            # 开线程运行脚本
            runThread = threading.Thread(target=occp.run, daemon=True)
            runThread.start()
    
    def pauseButton(self):
        # 设置按钮可用性
        self.ui.buttonPause.setEnabled(False)
        # 开启线程
        pauseThread = threading.Thread(target=occp.pause, daemon=True)
        pauseThread.start()

    def goONButton(self):
        curCity = self.ui.comboFromCity.currentIndex()
        tarCity = self.ui.comboToCity.currentIndex() + 1
        troopNum = self.ui.troopNum.text()
        isAcce = self.ui.comboAcce.currentIndex()
        if(troopNum == ''):
            self.ui.plainTextEdit.appendPlainText("请输入军队数量！")
            return
        else:
            troopNum = int(troopNum)
            occp.changeBattleMess(curCity, tarCity, troopNum, isAcce) #更新出发城市、目标城市、是否加速
            # 调整全局指挥时延
            settings = QSettings("config.ini",QSettings.IniFormat)
            t_delay = int(settings.value("delayTime"))*0.1
            occp.changeDelayTime(t_delay)
            # 设置按钮可用性
            self.ui.comboFromCity.setEnabled(False)
            self.ui.comboToCity.setEnabled(False)
            self.ui.troopNum.setEnabled(False)
            self.ui.comboAcce.setEnabled(False)
            self.ui.buttonPause.setEnabled(True)
            self.ui.buttonGoOn.setEnabled(False)
            self.ui.buttonClose.setEnabled(False)
            # 开启线程
            goonThread = threading.Thread(target=occp.goon, daemon=True)
            goonThread.start()
    
    def endButton(self):
        endThread = threading.Thread(target=occp.end, daemon=True)
        endThread.start()
    
    # 定义槽函数，接受程序发送来的战场信息
    # 接收战场信息
    def battleMsgSlot(self, msg):
        self.ui.plainTextEdit.appendPlainText(msg)
    # 接收当前城市
    def changeCurCitySlot(self, citynum):
        self.ui.comboFromCity.setCurrentIndex(citynum)
    # 接收目标城市
    def changeTarCitySlot(self, citynum):
        self.ui.comboToCity.setCurrentIndex(citynum-1)
    # 接收城市守军数量
    def changeTroopNumSlot(self, troopnum):
        self.ui.troopNum.setText("%d"%troopnum)
    # 接收是否有全局加速
    def changeAcceSlot(self):
        self.ui.comboAcce.setCurrentIndex(1)
    # 接收暂停信号
    def recvPauseSlot(self):
        # 设置按钮可用性
        self.ui.comboFromCity.setEnabled(True)
        self.ui.comboToCity.setEnabled(True)
        self.ui.troopNum.setEnabled(True)
        self.ui.comboAcce.setEnabled(True)
        self.ui.buttonGoOn.setEnabled(True)
        self.ui.buttonClose.setEnabled(True)
    # 接收停止信号
    def recvStopSlot(self):
        # 设置按钮可用性
        self.ui.comboRoute.setEnabled(True)
        self.ui.comboCommand.setEnabled(True)
        self.ui.comboArm.setEnabled(True)
        self.ui.comboPlayerNum.setEnabled(True)
        self.ui.buttonPause.setEnabled(False)
        self.ui.buttonGoOn.setEnabled(False)
        self.ui.buttonClose.setEnabled(False)
        self.ui.buttonStart.setEnabled(True)
        self.ui.comboFromCity.setEnabled(False)
        self.ui.comboToCity.setEnabled(False)
        self.ui.troopNum.setEnabled(False)
        self.ui.comboAcce.setEnabled(False)
        self.ui.tabWidget.setTabEnabled(1,True)   
    
    # -----------------------烽火战场设置---------------------------
    #设置城市1坐标
    def setCity1Pos(self):
        self.ui.fh_city1_x.setEnabled(True)
        self.ui.fh_city1_y.setEnabled(True)
        posThread = threading.Thread(target=pos.getPos, daemon=True)
        posThread.start()
    def recvCity1Pos(self, x, y):
        if(self.ui.fh_city1_x.isEnabled()):
            self.ui.fh_city1_x.setText(str(x))
            self.ui.fh_city1_x.setEnabled(False)
        if(self.ui.fh_city1_y.isEnabled()):
            self.ui.fh_city1_y.setText(str(y))
            self.ui.fh_city1_y.setEnabled(False)
    #设置城市2坐标
    def setCity2Pos(self):
        self.ui.fh_city2_x.setEnabled(True)
        self.ui.fh_city2_y.setEnabled(True)
        posThread = threading.Thread(target=pos.getPos, daemon=True)
        posThread.start()
    def recvCity2Pos(self, x, y):
        if(self.ui.fh_city2_x.isEnabled()):
            self.ui.fh_city2_x.setText(str(x))
            self.ui.fh_city2_x.setEnabled(False)
        if(self.ui.fh_city2_y.isEnabled()):
            self.ui.fh_city2_y.setText(str(y))
            self.ui.fh_city2_y.setEnabled(False)
    #设置城市3坐标
    def setCity3Pos(self):
        self.ui.fh_city3_x.setEnabled(True)
        self.ui.fh_city3_y.setEnabled(True)
        posThread = threading.Thread(target=pos.getPos, daemon=True)
        posThread.start()
    def recvCity3Pos(self, x, y):
        if(self.ui.fh_city3_x.isEnabled()):
            self.ui.fh_city3_x.setText(str(x))
            self.ui.fh_city3_x.setEnabled(False)
        if(self.ui.fh_city3_y.isEnabled()):
            self.ui.fh_city3_y.setText(str(y))
            self.ui.fh_city3_y.setEnabled(False)
    #设置城市4坐标
    def setCity4Pos(self):
        self.ui.fh_city4_x.setEnabled(True)
        self.ui.fh_city4_y.setEnabled(True)
        posThread = threading.Thread(target=pos.getPos, daemon=True)
        posThread.start()
    def recvCity4Pos(self, x, y):
        if(self.ui.fh_city4_x.isEnabled()):
            self.ui.fh_city4_x.setText(str(x))
            self.ui.fh_city4_x.setEnabled(False)
        if(self.ui.fh_city4_y.isEnabled()):
            self.ui.fh_city4_y.setText(str(y))
            self.ui.fh_city4_y.setEnabled(False)
    #设置城市5坐标
    def setCity5Pos(self):
        self.ui.fh_city5_x.setEnabled(True)
        self.ui.fh_city5_y.setEnabled(True)
        posThread = threading.Thread(target=pos.getPos, daemon=True)
        posThread.start()
    def recvCity5Pos(self, x, y):
        if(self.ui.fh_city5_x.isEnabled()):
            self.ui.fh_city5_x.setText(str(x))
            self.ui.fh_city5_x.setEnabled(False)
        if(self.ui.fh_city5_y.isEnabled()):
            self.ui.fh_city5_y.setText(str(y))
            self.ui.fh_city5_y.setEnabled(False)
    # 保存烽火战场设置
    def fh_saveInfo(self):
        settings = QSettings("config.ini",QSettings.IniFormat)
        settings.setValue("city1X",self.ui.fh_city1_x.text())
        settings.setValue("city1Y",self.ui.fh_city1_y.text())
        settings.setValue("city1type",self.ui.fh_city1_type.currentIndex())
        settings.setValue("city1num",self.ui.fh_city1_num.text())
 
        settings.setValue("city2X",self.ui.fh_city2_x.text())
        settings.setValue("city2Y",self.ui.fh_city2_y.text())
        settings.setValue("city2type",self.ui.fh_city2_type.currentIndex())
        settings.setValue("city2num",self.ui.fh_city2_num.text())

        settings.setValue("city3X",self.ui.fh_city3_x.text())
        settings.setValue("city3Y",self.ui.fh_city3_y.text())
        settings.setValue("city3type",self.ui.fh_city3_type.currentIndex())
        settings.setValue("city3num",self.ui.fh_city3_num.text())
  
        settings.setValue("city4X",self.ui.fh_city4_x.text())
        settings.setValue("city4Y",self.ui.fh_city4_y.text())
        settings.setValue("city4type",self.ui.fh_city4_type.currentIndex())
        settings.setValue("city4num",self.ui.fh_city4_num.text())

        settings.setValue("city5X",self.ui.fh_city5_x.text())
        settings.setValue("city5Y",self.ui.fh_city5_y.text())
        settings.setValue("city5type",self.ui.fh_city5_type.currentIndex())
        settings.setValue("city5num",self.ui.fh_city5_num.text())
    # 读取设置
    def fh_readInfo(self):
        settings = QSettings("config.ini",QSettings.IniFormat)
        city1X = settings.value("city1X")
        city1Y = settings.value("city1Y")
        city1type = settings.value("city1type")
        city1num = settings.value("city1num")

        city2X = settings.value("city2X")
        city2Y = settings.value("city2Y")
        city2type = settings.value("city2type")
        city2num = settings.value("city2num")

        city3X = settings.value("city3X")
        city3Y = settings.value("city3Y")
        city3type = settings.value("city3type")
        city3num = settings.value("city3num")

        city4X = settings.value("city4X")
        city4Y = settings.value("city4Y")
        city4type = settings.value("city4type")
        city4num = settings.value("city4num")

        city5X = settings.value("city5X")
        city5Y = settings.value("city5Y")
        city5type = settings.value("city5type")
        city5num = settings.value("city5num")

        self.ui.fh_city1_x.setText(city1X)
        self.ui.fh_city1_y.setText(city1Y)
        self.ui.fh_city1_type.setCurrentIndex(int(city1type))
        self.ui.fh_city1_num.setText(city1num)

        self.ui.fh_city2_x.setText(city2X)
        self.ui.fh_city2_y.setText(city2Y)
        self.ui.fh_city2_type.setCurrentIndex(int(city2type))
        self.ui.fh_city2_num.setText(city2num)

        self.ui.fh_city3_x.setText(city3X)
        self.ui.fh_city3_y.setText(city3Y)
        self.ui.fh_city3_type.setCurrentIndex(int(city3type))
        self.ui.fh_city3_num.setText(city3num)

        self.ui.fh_city4_x.setText(city4X)
        self.ui.fh_city4_y.setText(city4Y)
        self.ui.fh_city4_type.setCurrentIndex(int(city4type))
        self.ui.fh_city4_num.setText(city4num)

        self.ui.fh_city5_x.setText(city5X)
        self.ui.fh_city5_y.setText(city5Y)
        self.ui.fh_city5_type.setCurrentIndex(int(city5type))
        self.ui.fh_city5_num.setText(city5num)
    # 烽火战场获取界面信息
    def fh_getUIMessage(self):
        city1X = int(self.ui.fh_city1_x.text())
        city1Y = int(self.ui.fh_city1_y.text())
        city1type = self.ui.fh_city1_type.currentIndex()
        city1num = int(self.ui.fh_city1_num.text())
        city1 = [city1X, city1Y, city1type, city1num]

        city2X = int(self.ui.fh_city2_x.text())
        city2Y = int(self.ui.fh_city2_y.text())
        city2type = self.ui.fh_city2_type.currentIndex()
        city2num = int(self.ui.fh_city2_num.text())
        city2 = [city2X, city2Y, city2type, city2num]

        city3X = int(self.ui.fh_city3_x.text())
        city3Y = int(self.ui.fh_city3_y.text())
        city3type = self.ui.fh_city3_type.currentIndex()
        city3num = int(self.ui.fh_city3_num.text())
        city3 = [city3X, city3Y, city3type, city3num]

        city4X = int(self.ui.fh_city4_x.text())
        city4Y = int(self.ui.fh_city4_y.text())
        city4type = self.ui.fh_city4_type.currentIndex()
        city4num = int(self.ui.fh_city4_num.text())
        city4 = [city4X, city4Y, city4type, city4num]

        city5X = int(self.ui.fh_city5_x.text())
        city5Y = int(self.ui.fh_city5_y.text())
        city5type = self.ui.fh_city5_type.currentIndex()
        city5num = int(self.ui.fh_city5_num.text())
        city5 = [city5X, city5Y, city5type, city5num]

        return (city1, city2, city3, city4, city5)
    # 烽火战场开始按钮
    def fh_startButton(self):
        hwnd = self.ui.hwndLine.text()
        if(hwnd == ''):
            self.ui.fh_plaintext.appendPlainText("未获取窗口句柄，请检查！")
        else:
            self.fh_saveInfo()
            # 获取屏幕界面参数
            (leftUpX, leftUpY, rightDownX, rightDownY) = self.getUIMess()
            leftUp = [leftUpX, leftUpY]
            rightDown = [rightDownX, rightDownY]
            hwnd = cdt.str2hex(hwnd)
            cdt.initialCoornadite(leftUp, rightDown, hwnd)
            # 获取烽火界面参数
            (city1, city2, city3, city4, city5) = self.fh_getUIMessage()
            fh.iniCityInfo(city1, city2, city3, city4, city5) #城市信息
            isAcce = self.ui.fh_acce.isChecked()
            fh.changeAcceState(isAcce) #是否加速
            fh.pauseflag = False
            # 界面可用性调整
            self.ui.fh_city1_set.setEnabled(False)
            self.ui.fh_city2_set.setEnabled(False)
            self.ui.fh_city3_set.setEnabled(False)
            self.ui.fh_city4_set.setEnabled(False)
            self.ui.fh_city5_set.setEnabled(False)
            self.ui.fh_city1_num.setEnabled(False)
            self.ui.fh_city2_num.setEnabled(False)
            self.ui.fh_city3_num.setEnabled(False)
            self.ui.fh_city4_num.setEnabled(False)
            self.ui.fh_city5_num.setEnabled(False)
            self.ui.fh_city1_type.setEnabled(False)
            self.ui.fh_city2_type.setEnabled(False)
            self.ui.fh_city3_type.setEnabled(False)
            self.ui.fh_city4_type.setEnabled(False)
            self.ui.fh_city5_type.setEnabled(False)
            self.ui.tabWidget.setTabEnabled(0,False)
            self.ui.fh_start.setEnabled(False)
            self.ui.fh_pause.setEnabled(True)
            # 启动线程
            fhThread = threading.Thread(target=fh.excuteBattle, daemon=True)
            fhThread.start()
    # 烽火战场暂停按钮
    def fh_pauseButton(self):
        fhpauseThread = threading.Thread(target=fh.pause, daemon=True)
        fhpauseThread.start()
    # 烽火战场槽函数
    # 接收战场信息
    def fh_battleMsgSlot(self, msg):
        self.ui.fh_plaintext.appendPlainText(msg)
    # 接收暂停信息
    def fh_pauseMsgSlot(self):
        # 界面可用性调整
        self.ui.fh_city1_set.setEnabled(True)
        self.ui.fh_city2_set.setEnabled(True)
        self.ui.fh_city3_set.setEnabled(True)
        self.ui.fh_city4_set.setEnabled(True)
        self.ui.fh_city5_set.setEnabled(True)
        self.ui.fh_city1_num.setEnabled(True)
        self.ui.fh_city2_num.setEnabled(True)
        self.ui.fh_city3_num.setEnabled(True)
        self.ui.fh_city4_num.setEnabled(True)
        self.ui.fh_city5_num.setEnabled(True)
        self.ui.fh_city1_type.setEnabled(True)
        self.ui.fh_city2_type.setEnabled(True)
        self.ui.fh_city3_type.setEnabled(True)
        self.ui.fh_city4_type.setEnabled(True)
        self.ui.fh_city5_type.setEnabled(True)
        self.ui.tabWidget.setTabEnabled(0,True)
        self.ui.fh_start.setEnabled(True)
        self.ui.fh_pause.setEnabled(False)

    # -----------------“设置”-“其它”对话框----------------------------
    def settingDialogShow(self):
        sdialog = settingDialog() #“设置”对话框
        sdialog.settingMsg.sliderSignal.connect(self.battleMsgSlot)
        sdialog.exec_()
        sdialog.settingMsg.sliderSignal.disconnect(self.battleMsgSlot)
    
    def getNewVersion(self):
        QDesktopServices.openUrl(QUrl("https://www.cnblogs.com/betaOrionis/p/17381509.html"))
    
    # "关于"对话框
    def aboutDialogShow(self):
        QMessageBox.about(self, "关于软件", "本软件使用方法请参考同一文件夹下的使用说明书。\n"+
                          "本软件为黄巾战场辅助软件，为热血三国游戏爱好者情怀所做，仅限学习、研究使用，不收取任何费用。基本原理为模拟鼠标点击，与游戏内数据的交互均通过游戏允许的途径（即鼠标、键盘输入）。\n"+
                          "如果您喜欢该软件，请在游戏内多多照顾。后续若有时间，应该能把自动刷烽火战场、自动历练、自动读取报告并购买属性的功能加入本软件中。\n"+
                          "若该软件侵犯您的权益，请联系作者，本人视情况采取相应措施。\n"+
                          "by.betaOrionis(流云和月)")
    # "当前版本"对话框
    def versionDialogShow(self):
        QMessageBox.about(self, "当前版本", "当前版本：%s\n"%curversion +
                          "主要功能："+"黄巾战场、烽火战场")

# “设置”对话框
class settingDialog(QDialog, Ui_SettingDialog):
    # 设置信号函数
    class settingSignal(QObject):
        sliderSignal = Signal(str)

        def sendSliderSignal(self, message):
            self.sliderSignal.emit(message)
    
    settingMsg = settingSignal()
    
    # 对话框初始化
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_SettingDialog()
        self.ui.setupUi(self)
        self.iniInfo()

        self.ui.buttonBox.accepted.connect(self.onclickButton)
    
    def onclickButton(self):
        self.saveInfo()
        s = "当前全局时延已设为%d毫秒"%(self.ui.timeDelaySlider.value()*100)
        self.settingMsg.sendSliderSignal(s)
    
    def saveInfo(self):
        settings = QSettings("config.ini",QSettings.IniFormat)
        settings.setValue("delayTime",self.ui.timeDelaySlider.value())
    
    def iniInfo(self):
        settings = QSettings("config.ini",QSettings.IniFormat)
        slidervalue = int(settings.value("delayTime"))
        self.ui.timeDelaySlider.setValue(slidervalue)
    

def welcome():
    mess1 = "当前版本：%s 作者：betaOrionis(流云和月) "%curversion
    mess2 = "******************************************"
    mainwindow.ui.plainTextEdit.appendPlainText(mess1)
    mainwindow.ui.plainTextEdit.appendPlainText(mess2)
    fh_mess = "烽火战场脚本在使用前请先看一遍说明书！"
    mainwindow.ui.fh_plaintext.appendPlainText(mess1)
    mainwindow.ui.fh_plaintext.appendPlainText(mess2)
    mainwindow.ui.fh_plaintext.appendPlainText(fh_mess)

if __name__ == "__main__":
    lfupFlag = False
    rndwFlag = False
    hwndFlag = False

    app = QApplication([])
    mainwindow = Mainwindow()
    mainwindow.show()
    welcome()
    
    app.exec_()