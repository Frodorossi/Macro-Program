
# MK2 uses .ui files to greate the windows, thus allowing for later editing of the UI
# without needing to reconvert the .ui file. Implements saving/loading as well as information screens
# and is a usable proof of concept that only allows keyboard control.
# this version will turned to a .exe as a proof of concept, but will be added to in the next version
# to include mouse control as well.

# Created by Victor De Feo


from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QPushButton, QListWidget, QInputDialog, QLineEdit, QMessageBox, QApplication, QAction, QFileDialog, QDialog, QWidget
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
        uic.loadUi('MacrosUIMk1.ui', self)
        
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
        self.bTrigger = self.findChild(QPushButton, 'bTrigger')
        
        self.listWidget = self.findChild(QListWidget, 'listWidget')
        
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
            self.bTrigger.clicked.connect(self.TriggeringKey)

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
                        print(commandList, currentIndex)
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
                print(commandList, currentIndex)
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
                    print(commandList, currentIndex)
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
                commandList.insert(currentIndex+1, ['mHold', text, ''])
                commandList.insert(currentIndex+2, ['mRelease', text, ''])
                print(commandList, currentIndex)
        else:
            self.msg()
    
    def H2(self, text, y, currentIndex):
        self.listWidget.insertItem(currentIndex+1, 'Hold: '+ text)
        self.listWidget.insertItem(currentIndex+2, 'Release: '+ text)
        self.listWidget.setCurrentRow(currentIndex+2)
                
    def Release(self):
        currentIndex = self.listWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Release', 'Input key to release')
        if text in AcceptableInput:
            if ok and text is not None:
                self.R2(text, '', currentIndex)
                commandList.insert(currentIndex+1, ['mRelease', text, ''])
                print(commandList, currentIndex)
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
            print(commandList, currentIndex)
    
    def Wa2(self, text, y, currentIndex):
        self.listWidget.insertItem(currentIndex+1, 'Wait: '+ str(text) + ' seconds')
        self.listWidget.setCurrentRow(currentIndex+1)
    
    def Write(self):
        currentIndex = self.listWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Write', 'Type characters to write')
        if ok and text is not None:
            self.Wr2(text, '', currentIndex)
            commandList.insert(currentIndex+1, ['mWrite', text, ''])
            print(commandList, currentIndex)
    
    def Wr2(self, text, y, currentIndex):
        self.listWidget.insertItem(currentIndex+1, 'Write: '+ text)
        self.listWidget.setCurrentRow(currentIndex+1)
    
    def Copy(self):
        currentIndex = self.listWidget.currentRow()
        last = self.listWidget.item(currentIndex).clone()
        self.listWidget.insertItem(currentIndex+1, last)
        self.listWidget.setCurrentRow(currentIndex+1)
        commandList.insert(currentIndex+1, commandList[currentIndex])
        print(commandList, currentIndex)
        
    def MoveUp(self):
        currentIndex = self.listWidget.currentRow()
        if not currentIndex < 1:
            last = self.listWidget.takeItem(currentIndex)
            self.listWidget.insertItem(currentIndex-1, last)
            self.listWidget.setCurrentRow(currentIndex-1)
            commandList.insert(currentIndex-1, commandList.pop(currentIndex))
            print(commandList, currentIndex)
    
    def MoveDown(self):
        currentIndex = self.listWidget.currentRow()
        if not currentIndex == len(commandList)-1:
            last = self.listWidget.takeItem(currentIndex)
            self.listWidget.insertItem(currentIndex+1, last)
            self.listWidget.setCurrentRow(currentIndex+1)
            commandList.insert(currentIndex+1, commandList.pop(currentIndex))
            print(commandList, currentIndex)
    
    def Remove(self):
        if not len(commandList) == 0:
            currentIndex = self.listWidget.currentRow()
            self.listWidget.takeItem(currentIndex)
            commandList.pop(currentIndex)
            print(commandList, currentIndex)
    
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
    'mWrite': Wr2
    }
    
    def repopulate(self):
        for i in range(len(commandList)):
            self.repopDictionary[commandList[i][0]](self, commandList[i][1], commandList[i][2], i)

    def openInputs(self):
        inputWindow().exec_()
    
    def openInstructions(self):
        instructionsWindow().exec_()

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

callDictionary = {
    'mhotKey': mhotKey,
    'mPress': mPress,
    'mMultiPress': mMultiPress,
    'mHold': mHold,
    'mRelease': mRelease,
    'mWait': mWait,
    'mWrite': mWrite
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