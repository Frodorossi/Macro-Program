
# MK3 implements mouse control, allowing the user to define mouse movement and mouse clicks.

# Created by Victor De Feo
#test


from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QMainWindow, QPushButton, QListWidget, QInputDialog, QLineEdit, QMessageBox, QApplication, QAction, QFileDialog, QDialog, QWidget, QLabel
import sys
import pyautogui as pag
import time
import keyboard
from pynput.keyboard import Key, Listener
import numpy as np
import json
import os

class window(QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        os.chdir(directory+'\\Interfaces')
        uic.loadUi('MacrosUIMk3.ui', self)
        
        self.bHotKey = self.findChild(QPushButton, 'bHotKey')
        self.bPress = self.findChild(QPushButton, 'bPress')
        self.bMultiPress = self.findChild(QPushButton, 'bMultiPress')
        self.bHold = self.findChild(QPushButton, 'bHold')
        self.bRelease = self.findChild(QPushButton, 'bRelease')
        self.bWait = self.findChild(QPushButton, 'bWait')
        self.bWrite = self.findChild(QPushButton, 'bWrite')
        self.bCopy = self.findChild(QPushButton, 'bCopy')
        self.bMoveUp = self.findChild(QPushButton, 'bMoveUp')
        self.bMoveDown = self.findChild(QPushButton, 'bMoveDown')
        self.bRemove = self.findChild(QPushButton, 'bRemove')
        self.bClick = self.findChild(QPushButton, 'bClick')
        self.bRightClick = self.findChild(QPushButton, 'bRightClick')
        self.bDoubleClick = self.findChild(QPushButton, 'bDoubleClick')
        self.bMouseMove = self.findChild(QPushButton, 'bMouseMove')
        self.bMoveRelative = self.findChild(QPushButton, 'bMoveRelative')
        self.bClickandDrag = self.findChild(QPushButton, 'bClickandDrag')
        self.bTrigger = self.findChild(QPushButton, 'bTrigger')
        self.bMousePosition = self.findChild(QPushButton, 'bMousePosition')
        self.bClear = self.findChild(QPushButton, 'bClear')
        self.bRepeats = self.findChild(QPushButton, 'bRepeats')
        
        self.listWidget = self.findChild(QListWidget, 'listWidget')
        self.repeatsList = self.findChild(QListWidget, 'Repeats')
        
        self.actionOpen = self.findChild(QAction, 'actionOpen')
        self.actionSave = self.findChild(QAction, 'actionSave')
        self.actionInstructions = self.findChild(QAction, 'actionInstructions')
        self.actionAcceptable_Inputs = self.findChild(QAction, 'actionAcceptable_Inputs')
        
        #Button connections
        if running == False:
            self.bHotKey.clicked.connect(self.hotKey)
            self.bPress.clicked.connect(self.Press)
            self.bMultiPress.clicked.connect(self.MultiPress)
            self.bHold.clicked.connect(self.Hold)
            self.bRelease.clicked.connect(self.Release)
            self.bWait.clicked.connect(self.Wait)
            self.bWrite.clicked.connect(self.Write)
            self.bCopy.clicked.connect(self.Copy)
            self.bMoveUp.clicked.connect(self.MoveUp)
            self.bMoveDown.clicked.connect(self.MoveDown)
            self.bRemove.clicked.connect(self.Remove)
            self.bClick.clicked.connect(self.Click)
            self.bRightClick.clicked.connect(self.RightClick)
            self.bDoubleClick.clicked.connect(self.DoubleClick)
            self.bMouseMove.clicked.connect(self.MouseMove)
            self.bMoveRelative.clicked.connect(self.MoveRelative)
            self.bClickandDrag.clicked.connect(self.ClickandDrag)
            self.bTrigger.clicked.connect(self.TriggeringKey)
            self.bMousePosition.clicked.connect(self.openCoordinateWindow)
            self.bClear.clicked.connect(self.ListClear)
            self.bRepeats.clicked.connect(self.getRepeats)

            self.actionOpen.triggered.connect(self.openFile)
            self.actionSave.triggered.connect(self.saveFile)
            self.actionInstructions.triggered.connect(self.openInstructions)
            self.actionAcceptable_Inputs.triggered.connect(self.openInputs)
    
    def hotKey(self):
        currentIndex = self.listWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Hotkey', 'Input first key')
        if text in AcceptableInput:
            if ok and text is not None:
                text2, ok = QInputDialog.getText(self, 'Hotkey', 'Input second key')
                if text2 in AcceptableInput:
                    if ok and text2 is not None:
                        self.HK2(text, text2, currentIndex)
                        commandList.insert(currentIndex+1, ['mhotKey', text, text2])
                else:
                    self.msg()
        else:
            self.msg()
    
    def HK2(self, text, text2, currentIndex):
        self.listWidget.insertItem(currentIndex+1, 'Hotkey: '+ text + ' + ' + text2)
        self.listWidget.setCurrentRow(currentIndex+1)
    
    def Press(self):
        currentIndex = self.listWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Press', 'Input key to press')
        if text in AcceptableInput:
            if ok and text is not None:
                self.P2(text, '', currentIndex)
                commandList.insert(currentIndex+1, ['mPress', text, ''])
            else:
                self.msg()
        else:
            self.msg()
    
    def P2(self, text, y, currentIndex):
        self.listWidget.insertItem(currentIndex+1, 'Press: '+ text)
        self.listWidget.setCurrentRow(currentIndex+1)

    def MultiPress(self):
        currentIndex = self.listWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Multi Press', 'Input key to press')
        if text in AcceptableInput:
            if ok and text is not None:
                iterations, ok = QInputDialog.getInt(self, 'Multi Press', 'Input how many times to repeat')
                if ok and iterations is not None:
                    self.MP2(text, iterations, currentIndex)
                    commandList.insert(currentIndex+1, ['mMultiPress', text, str(iterations)])
                else:
                    self.msg()
        else:
            self.msg()
    
    def MP2(self, text, iterations, currentIndex):
        self.listWidget.insertItem(currentIndex+1, 'Press: '+ text + ' ' + str(iterations) + ' times')
        self.listWidget.setCurrentRow(currentIndex+1)
    
    def Hold(self):
        currentIndex = self.listWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Hold', 'Input key to hold')
        if text in AcceptableInput:
            if ok and text is not None:
                self.H2(text, '', currentIndex)
                self.R2(text, '', currentIndex+1)
                commandList.insert(currentIndex+1, ['mHold', text, ''])
                commandList.insert(currentIndex+2, ['mRelease', text, ''])
            else:
                self.msg()
        else:
            self.msg()
    
    def H2(self, text, y, currentIndex):
        self.listWidget.insertItem(currentIndex+1, 'Hold: '+ text)
        self.listWidget.setCurrentRow(currentIndex+1)
                
    def Release(self):
        currentIndex = self.listWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Release', 'Input key to release')
        if text in AcceptableInput:
            if ok and text is not None:
                self.R2(text, '', currentIndex)
                commandList.insert(currentIndex+1, ['mRelease', text, ''])
            else:
                self.msg()
        else:
            self.msg()
    
    def R2(self, text, y, currentIndex):
        self.listWidget.insertItem(currentIndex+1, 'Release: '+ text)
        self.listWidget.setCurrentRow(currentIndex+1)
    
    def Wait(self):
        currentIndex = self.listWidget.currentRow()
        text, ok = QInputDialog.getDouble(self, 'Wait', 'Input how long to wait in seconds')
        if ok and text is not None:
            self.Wa2(text, '', currentIndex)
            commandList.insert(currentIndex+1, ['mWait', str(text), ''])
    
    def Wa2(self, text, y, currentIndex):
        self.listWidget.insertItem(currentIndex+1, 'Wait: '+ str(text) + ' seconds')
        self.listWidget.setCurrentRow(currentIndex+1)
    
    def Write(self):
        currentIndex = self.listWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Write', 'Type characters to write')
        if ok and text is not None:
            self.Wr2(text, '', currentIndex)
            commandList.insert(currentIndex+1, ['mWrite', text, ''])
    
    def Wr2(self, text, y, currentIndex):
        self.listWidget.insertItem(currentIndex+1, 'Write: '+ text)
        self.listWidget.setCurrentRow(currentIndex+1)
    
    def Copy(self):
        currentIndex = self.listWidget.currentRow()
        last = self.listWidget.item(currentIndex).clone()
        self.listWidget.insertItem(currentIndex+1, last)
        self.listWidget.setCurrentRow(currentIndex+1)
        commandList.insert(currentIndex+1, commandList[currentIndex])
        
    def MoveUp(self):
        currentIndex = self.listWidget.currentRow()
        if not currentIndex < 1:
            last = self.listWidget.takeItem(currentIndex)
            self.listWidget.insertItem(currentIndex-1, last)
            self.listWidget.setCurrentRow(currentIndex-1)
            commandList.insert(currentIndex-1, commandList.pop(currentIndex))
    
    def MoveDown(self):
        currentIndex = self.listWidget.currentRow()
        if not currentIndex == len(commandList)-1:
            last = self.listWidget.takeItem(currentIndex)
            self.listWidget.insertItem(currentIndex+1, last)
            self.listWidget.setCurrentRow(currentIndex+1)
            commandList.insert(currentIndex+1, commandList.pop(currentIndex))
    
    def Remove(self):
        if not len(commandList) == 0:
            currentIndex = self.listWidget.currentRow()
            self.listWidget.takeItem(currentIndex)
            commandList.pop(currentIndex)
    
    def ListClear(self):
        self.listWidget.clear()
        commandList.clear()
    
    def Click(self):
        currentIndex = self.listWidget.currentRow()
        self.Cl2('', '', currentIndex)
        commandList.insert(currentIndex+1, ['mClick', '', ''])
    
    def Cl2(self, x, y, currentIndex):
        self.listWidget.insertItem(currentIndex+1, 'Mouse Click')
        self.listWidget.setCurrentRow(currentIndex+1)
    
    def RightClick(self):
        currentIndex = self.listWidget.currentRow()
        self.RCl2('', '', currentIndex)
        commandList.insert(currentIndex+1, ['mRightClick', '', ''])
    
    def RCl2(self, x, y, currentIndex):
        self.listWidget.insertItem(currentIndex+1, 'Right Click')
        self.listWidget.setCurrentRow(currentIndex+1)
    
    def DoubleClick(self):
        currentIndex = self.listWidget.currentRow()
        self.DCl2('', '', currentIndex)
        commandList.insert(currentIndex+1, ['mDoubleClick', '', ''])
    
    def DCl2(self, x, y, currentIndex):
        self.listWidget.insertItem(currentIndex+1, 'Double Click')
        self.listWidget.setCurrentRow(currentIndex+1)
    
    def MouseHold(self):
        currentIndex = self.listWidget.currentRow()
        self.MH2('', '', currentIndex)
        self.MR2('', '', currentIndex+1)
        commandList.insert(currentIndex+1, ['mMouseHold', '', ''])
        commandList.insert(currentIndex+2, ['mMouseRelease', '', ''])
    
    def MH2(self, x, y, currentIndex):
        self.listWidget.insertItem(currentIndex+1, 'Mouse Hold')
        self.listWidget.setCurrentRow(currentIndex+1)
    
    def MouseRelease(self):
        currentIndex = self.listWidget.currentRow()
        self.MR2('', '', currentIndex)
        commandList.insert(currentIndex+1, ['mMouseRelease', '', ''])
    
    def MR2(self, x, y, currentIndex):
        self.listWidget.insertItem(currentIndex+1, 'Mouse Release')
        self.listWidget.setCurrentRow(currentIndex+1)
    
    def MouseMove(self):
        currentIndex = self.listWidget.currentRow()
        xcord, ok = QInputDialog.getInt(self, 'Mouse Move', 'Input X coordinate')
        if ok and xcord is not None:
            ycord, ok = QInputDialog.getInt(self, 'Mouse Move', 'Input Y coordinate')
            if ok and ycord is not None:
                self.MM2(xcord, ycord, currentIndex)
                commandList.insert(currentIndex+1, ['mMouseMove', str(xcord), str(ycord)])
            else:
                self.msg()
        else:
            self.msg()
    
    def MM2(self, x, y, currentIndex):
        self.listWidget.insertItem(currentIndex+1, 'Move Mouse to: X:'+str(x)+' Y:'+str(y))
        self.listWidget.setCurrentRow(currentIndex+1)
    
    def MoveRelative(self):
        currentIndex = self.listWidget.currentRow()
        xcord, ok = QInputDialog.getInt(self, 'Mouse Move', 'Input X increase or decrease (+/-)')
        if ok and xcord is not None:
            if '-' not in str(xcord):
                xcord = '+'+str(xcord)
            ycord, ok = QInputDialog.getInt(self, 'Mouse Move', 'Input Y increase or decrease (+/-)')
            if ok and ycord is not None:
                if '-' not in str(ycord):
                    ycord = '+'+str(ycord)
                self.MR2(xcord, ycord, currentIndex)
                commandList.insert(currentIndex+1, ['mMoveRelative', str(xcord), str(ycord)])
            else:
                self.msg()
        else:
            self.msg()
    
    def MR2(self, x, y, currentIndex):
        self.listWidget.insertItem(currentIndex+1, 'Move Mouse: X'+str(x)+', Y'+str(y))
        self.listWidget.setCurrentRow(currentIndex+1)
    
    def ClickandDrag(self):
        currentIndex = self.listWidget.currentRow()
        xcord, ok = QInputDialog.getInt(self, 'Click and Drag', 'Input X coordinate to drag to (+/-)')
        if ok and xcord is not None:
            if '-' not in str(xcord):
                xcord = '+'+str(xcord)
            ycord, ok = QInputDialog.getInt(self, 'Click and Drag', 'Input Y coordinate to drag to (+/-)')
            if ok and ycord is not None:
                if '-' not in str(ycord):
                    ycord = '+'+str(ycord)
                self.CD2(xcord, ycord, currentIndex)
                commandList.insert(currentIndex+1, ['mClickandDrag', str(xcord), str(ycord)])
            else:
                self.msg()
        else:
            self.msg()
    
    def CD2(self, x, y, currentIndex):
        self.listWidget.insertItem(currentIndex+1, 'Click and Drag to: X'+str(x)+' Y'+str(y))
        self.listWidget.setCurrentRow(currentIndex+1)
    
    def TriggeringKey(self):
        global running
        if running == False:
            runMacro()
            
    def msg(self):
        msg = QMessageBox()
        msg.setWindowTitle('Incorrect input')
        msg.setText('The input you entered cannot be accepted. Check the acceptable inputs list')
        msg.exec_()
    
    def openFile(self):
        global commandList
        oname, _ = QFileDialog.getOpenFileName(self, 'Open File', directory+'\\Saves', 'JSON Files (*.json)')
        if oname:
            self.listWidget.clear()
            commandList.clear()
            commandList = json.load(open(oname))
            self.repopulate()
    
    def saveFile(self):
        sname, _ = QFileDialog.getSaveFileName(self, 'Save File', directory +'\\Saves', 'JSON Files (*.json)')
        if sname:
            with open(sname, 'w') as outfile:
                json.dump(commandList, outfile)
    
    repopDictionary = {
    'mhotKey': HK2,
    'mPress': P2,
    'mMultiPress': MP2,
    'mHold': H2,
    'mRelease': R2,
    'mWait': Wa2,
    'mWrite': Wr2,
    'mClick': Cl2,
    'mRightClick': RCl2,
    'mDoubleClick': DCl2,
    'mMouseMove': MM2,
    'mMoveRelative': MR2,
    'mClickandDrag': CD2
    }
    
    def repopulate(self):
        for i in range(len(commandList)):
            self.repopDictionary[commandList[i][0]](self, commandList[i][1], commandList[i][2], i)

    def openInputs(self):
        inputWindow().exec_()
    
    def openInstructions(self):
        instructionsWindow().exec_()
    
    def openCoordinateWindow(self):
        coordinateWindow().exec_()
    
    def getRepeats(self):
        repeats, ok = QInputDialog.getInt(self, 'Repeats', 'Input how many times to repeat the macro')
        if ok and repeats is not None:
            global Repeats
            Repeats = repeats
            self.repeatsList.clear()
            self.repeatsList.insertItem(0, 'Repeats: ' + str(Repeats))
            

        
class instructionsWindow(QDialog):
    def __init__(self):
        super(instructionsWindow, self).__init__()
        os.chdir(directory+'\\Interfaces')
        uic.loadUi('Instructions.ui', self)

class inputWindow(QDialog):
    def __init__(self):
        super(inputWindow, self).__init__()
        os.chdir(directory+'\\Interfaces')
        uic.loadUi('Inputs.ui', self)

class coordinateWindow(QDialog):
    def __init__(self):
        super(coordinateWindow, self).__init__()
        os.chdir(directory+'\\Interfaces')
        uic.loadUi('Coordinates.ui', self)
        self.clabel = self.findChild(QLabel, 'Coordinates')
        self.setMouseTracking(True)
        self.showMaximized()
        self.setWindowOpacity(0.60)
    
    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        self.clabel.setText('X:'+str(x)+' Y:'+str(y))

    
AcceptableInput = [' ', '!', '"', '#', '$', '%', '&', "'", '(',
                    ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
                    '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`',
                    'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
                    'add', 'alt', 'backspace', 'capslock', 'clear', 'ctrl', 'del', 'delete',
                    'divide', 'down', 'end', 'enter', 'esc', 'escape', 'f1', 'f10',
                    'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
                    'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
                    'left', 'pagedown', 'pageup', 'pgdn',
                    'pgup', 'printscreen', 'prntscrn',
                    'prtsc', 'prtscr', 'return', 'right', 
                    'shift', 'space', 'subtract', 'tab','up', 'command']

commandList = []
running = False
directory = os.getcwd()
Repeats = 1

def mhotKey(x, y):
    pag.hotkey(x, y)

def mPress(x, y):
    pag.press(x)

def mMultiPress(x, y):
    for i in range(int(y)):
        pag.press(x)

def mHold(x, y):
    pag.keyDown(x)

def mRelease(x, y):
    pag.keyUp(x)

def mWait(x, y):
    time.sleep(float(x))

def mWrite(x, y):
    pag.write(x)

def mClick(x, y):
    pag.click()

def mRightClick(x, y):
    pag.click(button='right')

def mDoubleClick(x, y):
    pag.doubleClick()

def mMouseMove(x, y):
    pag.moveTo(int(x), int(y))

def mMoveRelative(x, y):
    x1, y1 = pag.position()
    pag.moveTo(x1+int(x), y1+int(y))

def mClickandDrag(x, y):
    x1, y1 = pag.position()
    pag.dragTo(x1+int(x), y1+int(y), 1, button='left')

callDictionary = {
    'mhotKey': mhotKey,
    'mPress': mPress,
    'mMultiPress': mMultiPress,
    'mHold': mHold,
    'mRelease': mRelease,
    'mWait': mWait,
    'mWrite': mWrite,
    'mClick': mClick,
    'mRightClick': mRightClick,
    'mDoubleClick': mDoubleClick,
    'mMouseMove': mMouseMove,
    'mMoveRelative': mMoveRelative,
    'mClickandDrag': mClickandDrag
}
    
def show(key):
    global running
    print(key)
    if key == Key.insert:
        begin()
    if key == Key.esc:
        running = False
        return False

def runMacro():
    global running
    if running == False:
        running = True
        with Listener(on_press=show) as listener:
            listener.join()

def begin():
    for j in range(Repeats):
        for i in range(len(commandList)):
            if keyboard.is_pressed('esc'):
                break
            callDictionary[commandList[i][0]](commandList[i][1], commandList[i][2])

def app():
    app = QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec_())

app()