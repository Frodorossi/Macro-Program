# MK1 was the test run that got most of the functionality of the macro
# it used a .py file for the ui instead of a .ui and did not support saving

# Created by Victor De Feo

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox, QApplication
from MacrosUI import Ui_MainWindow
import sys
import pyautogui as pag
import time
import keyboard
from pynput.keyboard import Key, Listener

class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #Button connections
        if running == False:
            self.ui.bHotKey.clicked.connect(self.hotKey)
            self.ui.bPress.clicked.connect(self.Press)
            self.ui.bMultiPress.clicked.connect(self.MultiPress)
            self.ui.bHold.clicked.connect(self.Hold)
            self.ui.bRelease.clicked.connect(self.Release)
            self.ui.bWait.clicked.connect(self.Wait)
            self.ui.bWrite.clicked.connect(self.Write)
            self.ui.bCopy.clicked.connect(self.Copy)
            self.ui.bMoveUp.clicked.connect(self.MoveUp)
            self.ui.bMoveDown.clicked.connect(self.MoveDown)
            self.ui.bRemove.clicked.connect(self.Remove)
            self.ui.bTrigger.clicked.connect(self.TriggeringKey)
    
    def hotKey(self):
        currentIndex = self.ui.listWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Hotkey', 'Input first key')
        if text in AcceptableInput:
            if ok and text is not None:
                text2, ok = QInputDialog.getText(self, 'Hotkey', 'Input second key')
                if text2 in AcceptableInput:
                    if ok and text2 is not None:
                        self.ui.listWidget.insertItem(currentIndex+1, 'Hotkey: '+ text + ' + ' + text2)
                        self.ui.listWidget.setCurrentRow(currentIndex+1)
                        commandList.append([mhotKey, text, text2])
                else:
                    self.msg()
        else:
            self.msg()
    
    def Press(self):
        currentIndex = self.ui.listWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Press', 'Input key to press')
        if text in AcceptableInput:
            if ok and text is not None:
                self.ui.listWidget.insertItem(currentIndex+1, 'Press: '+ text)
                self.ui.listWidget.setCurrentRow(currentIndex+1)
                commandList.append([mPress, text, ''])
        else:
            self.msg()     

    def MultiPress(self):
        currentIndex = self.ui.listWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Multi Press', 'Input key to press')
        if text in AcceptableInput:
            if ok and text is not None:
                iterations, ok = QInputDialog.getInt(self, 'Multi Press', 'Input how many times to repeat')
                if ok and iterations is not None:
                    self.ui.listWidget.insertItem(currentIndex+1, 'Press: '+ text + ' ' + str(iterations) + ' times')
                    self.ui.listWidget.setCurrentRow(currentIndex+1)
                    commandList.append([mMultiPress, text, str(iterations)])
        else:
            self.msg()
    
    def Hold(self):
        currentIndex = self.ui.listWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Hold', 'Input key to hold')
        if text in AcceptableInput:
            if ok and text is not None:
                self.ui.listWidget.insertItem(currentIndex+1, 'Hold: '+ text)
                self.ui.listWidget.insertItem(currentIndex+2, 'Release: '+ text)
                self.ui.listWidget.setCurrentRow(currentIndex+2)
                commandList.append([mHold, text, ''])
                commandList.append([mRelease, text, ''])
        else:
            self.msg()
    
    def Release(self):
        currentIndex = self.ui.listWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Release', 'Input key to release')
        if text in AcceptableInput:
            if ok and text is not None:
                self.ui.listWidget.insertItem(currentIndex+1, 'Release: '+ text)
                self.ui.listWidget.setCurrentRow(currentIndex+1)
                commandList.append([mRelease, text, ''])
        else:
            self.msg()
    
    def Wait(self):
        currentIndex = self.ui.listWidget.currentRow()
        text, ok = QInputDialog.getDouble(self, 'Wait', 'Input how long to wait in seconds')
        if ok and text is not None:
            self.ui.listWidget.insertItem(currentIndex+1, 'Wait: '+ str(text) + ' seconds')
            self.ui.listWidget.setCurrentRow(currentIndex+1)
            commandList.append([mWait, str(text), ''])
    
    def Write(self):
        currentIndex = self.ui.listWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Write', 'Type characters to write')
        if ok and text is not None:
            self.ui.listWidget.insertItem(currentIndex+1, 'Write: '+ text)
            self.ui.listWidget.setCurrentRow(currentIndex+1)
            commandList.append([mWrite, text, ''])
    
    def Copy(self):
        currentIndex = self.ui.listWidget.currentRow()
        last = self.ui.listWidget.item(currentIndex).clone()
        self.ui.listWidget.insertItem(currentIndex+1, last)
        self.ui.listWidget.setCurrentRow(currentIndex+1)
        commandList.insert(currentIndex+1, commandList[currentIndex])
        
    def MoveUp(self):
        currentIndex = self.ui.listWidget.currentRow()
        last = self.ui.listWidget.takeItem(currentIndex)
        self.ui.listWidget.insertItem(currentIndex-1, last)
        self.ui.listWidget.setCurrentRow(currentIndex-1)
        commandList.insert(currentIndex-1, commandList.pop(currentIndex))
    
    def MoveDown(self):
        currentIndex = self.ui.listWidget.currentRow()
        last = self.ui.listWidget.takeItem(currentIndex)
        self.ui.listWidget.insertItem(currentIndex+1, last)
        self.ui.listWidget.setCurrentRow(currentIndex+1)
        commandList.insert(currentIndex+1, commandList.pop(currentIndex))
    
    def Remove(self):
        currentIndex = self.ui.listWidget.currentRow()
        self.ui.listWidget.takeItem(currentIndex)
        commandList.pop(currentIndex)
    
    def TriggeringKey(self):
        global running
        if running == False:
            runMacro()
            
    def msg(self):
        msg = QMessageBox()
        msg.setWindowTitle('Incorrect input')
        msg.setText('The input you entered cannot be accepted. Check the acceptable inputs list')
        msg.exec_()
    
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
    
def show(key):
    global running
    print(key)
    if key == Key.insert:
        begin()
    return False

def runMacro():
    global running
    if running == False:
        running = True
        with Listener(on_press=show) as listener:
            listener.join()

def begin():
    global running
    for i in range(len(commandList)):
        if keyboard.is_pressed('esc'):
            break
        commandList[i][0](commandList[i][1], commandList[i][2])
    running = False

def app():
    app = QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec_())

app()