import win32api
import keyboard
import time
from PySide2.QtCore import Signal, QObject

pauseflag = False #设置暂停点全局变量为False
def pausekey_press(key):
    global pauseflag
    if key.name == 's':
        pauseflag = True
keyboard.on_press(pausekey_press) #设置按ESC键暂停程序

cursorPos = [0, 0]
# 信号函数
class positionSignal(QObject):
    posSignal = Signal(int, int)

    def sendPosSignal(self, x, y):
        self.posSignal.emit(x,y)
posMsg = positionSignal()

# 获取鼠标位置函数
def getPos():
    global cursorPos, pauseflag
    pauseflag = False
    while 1:
        time.sleep(0.2)
        if(pauseflag):
            x,y = win32api.GetCursorPos()
            cursorPos[0] = x
            cursorPos[1] = y
            pauseflag = False
            posMsg.sendPosSignal(cursorPos[0],cursorPos[1])
            break

if __name__ == '__main__':
    print("请按S键确定当前鼠标位置")
    getPos()
    print(cursorPos[0], cursorPos[1])