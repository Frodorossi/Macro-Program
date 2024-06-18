
# MK4 implements threading to eliminate the bug where the program stops responding when clicking on the macro window while
# the macro is 'live'

# Created by Victor De Feo

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
import threading

class window(QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        os.chdir(directory+'\\Interfaces')
        uic.loadUi('MacrosUI.ui', self)
        
        #Connecting UI buttons to code
        self.bEditMacro = self.findChild(QPushButton, 'bEditMacro')
        self.bDeleteMacro = self.findChild(QPushButton, 'bDeleteMacro')
        self.bMasterMoveUp = self.findChild(QPushButton, 'bMasterMoveUp')
        self.bMasterMoveDown = self.findChild(QPushButton, 'bMasterMoveDown')
        self.bAssign1 = self.findChild(QPushButton, 'bAssign1')
        self.bAssign2 = self.findChild(QPushButton, 'bAssign2')
        self.bAssign3 = self.findChild(QPushButton, 'bAssign3')
        self.bAssign4 = self.findChild(QPushButton, 'bAssign4')
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
        self.bSaveToMasterList = self.findChild(QPushButton, 'bSaveToMasterList')
        self.bRepeats = self.findChild(QPushButton, 'bRepeats')
        
        self.MasterlistWidget = self.findChild(QListWidget, 'MasterlistWidget')
        self.Assigned1 = self.findChild(QListWidget, 'Assigned1')
        self.Assigned2 = self.findChild(QListWidget, 'Assigned2')
        self.Assigned3 = self.findChild(QListWidget, 'Assigned3')
        self.Assigned4 = self.findChild(QListWidget, 'Assigned4')
        self.EditlistWidget = self.findChild(QListWidget, 'EditlistWidget')
        self.repeatsList = self.findChild(QListWidget, 'Repeats')
        
        self.actionOpen = self.findChild(QAction, 'actionOpen')
        self.actionSave = self.findChild(QAction, 'actionSave')
        self.actionInstructions = self.findChild(QAction, 'actionInstructions')
        self.actionAcceptable_Inputs = self.findChild(QAction, 'actionAcceptable_Inputs')
        
        #Connecting buttons to functions
        self.bEditMacro.clicked.connect(self.EditMacro)
        self.bDeleteMacro.clicked.connect(self.DeleteMacro)
        self.bMasterMoveUp.clicked.connect(self.MasterMoveUp)
        self.bMasterMoveDown.clicked.connect(self.MasterMoveDown)
        self.bAssign1.clicked.connect(self.AssignMacro1)
        self.bAssign2.clicked.connect(self.AssignMacro2)
        self.bAssign3.clicked.connect(self.AssignMacro3)
        self.bAssign4.clicked.connect(self.AssignMacro4)
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
        self.bSaveToMasterList.clicked.connect(self.SaveToMasterList)
        self.bRepeats.clicked.connect(self.getRepeats)

        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionInstructions.triggered.connect(self.openInstructions)
        self.actionAcceptable_Inputs.triggered.connect(self.openInputs)
    
    #======================================================================
    # This section takes input from the user to assign a key to be the trigger for one of 4 possible Macros to be called.
    # Macros are chosen from the masterList and copied to the armedMacros list that is used for calling of macros.
    
    def EditMacro(self):
        if not len(masterList) == 0:
            currentIndex = self.MasterlistWidget.currentRow()
            editList.clear()
            for j in range(len(masterList[currentIndex])-1):
                editList.append(masterList[currentIndex][j+1])
            self.EditlistWidget.clear()
            self.repopulate()
    
    def DeleteMacro(self):
        if not len(masterList) == 0:
            currentIndex = self.MasterlistWidget.currentRow()
            self.MasterlistWidget.takeItem(currentIndex)
            masterList.pop(currentIndex)
    
    def MasterMoveUp(self):
        currentIndex = self.MasterlistWidget.currentRow()
        if not currentIndex < 1:
            last = self.MasterlistWidget.takeItem(currentIndex)
            self.MasterlistWidget.insertItem(currentIndex-1, last)
            self.MasterlistWidget.setCurrentRow(currentIndex-1)
            masterList.insert(currentIndex-1, masterList.pop(currentIndex))
    
    def MasterMoveDown(self):
        currentIndex = self.MasterlistWidget.currentRow()
        if not currentIndex == len(masterList)-1:
            last = self.MasterlistWidget.takeItem(currentIndex)
            self.MasterlistWidget.insertItem(currentIndex+1, last)
            self.MasterlistWidget.setCurrentRow(currentIndex+1)
            masterList.insert(currentIndex+1, masterList.pop(currentIndex))
    
    def AssignMacro1(self):
        text, ok = QInputDialog.getText(self, 'Macro 1', 'Input key to trigger Macro')
        if ok and text is not None:
            if text in AcceptableInput:
                armedMacros[0].clear()
                armedMacros[0].append(str(text))
                repeats = self.getRepeats()
                armedMacros[0].append(str(repeats))
                masterIndex = self.MasterlistWidget.currentRow()
                for i in range(len(masterList[masterIndex])):
                    armedMacros[0].append(masterList[masterIndex][i])
                print(armedMacros)
                self.Assigned1.clear()
                self.Assigned1.insertItem(0, '\'' + str(armedMacros[0][1]) + '\'' + ' is bound to ' + '\'' + str(armedMacros[0][0]) +'\'' + ' key, and will run ' + str(repeats) + ' times.')
            else:
                self.msg()
    
    def AssignMacro2(self):
        text, ok = QInputDialog.getText(self, 'Macro 2', 'Input key to trigger Macro')
        if ok and text is not None:
            if text in AcceptableInput:
                armedMacros[1].clear()
                armedMacros[1].append(str(text))
                repeats = self.getRepeats()
                armedMacros[0].append(str(repeats))
                masterIndex = self.MasterlistWidget.currentRow()
                for i in range(len(masterList[masterIndex])):
                    armedMacros[1].append(masterList[masterIndex][i])
                print(armedMacros)
                self.Assigned2.clear()
                self.Assigned2.insertItem(0, '\'' + str(armedMacros[1][1]) + '\'' + ' is bound to ' + '\'' + str(armedMacros[1][0]) +'\'' + ' key, and will run ' + str(repeats) + ' times.')
            else:
                self.msg()
    
    def AssignMacro3(self):
        text, ok = QInputDialog.getText(self, 'Macro 3', 'Input key to trigger Macro')
        if ok and text is not None:
            if text in AcceptableInput:
                armedMacros[2].clear()
                armedMacros[2].append(str(text))
                repeats = self.getRepeats()
                armedMacros[0].append(str(repeats))
                masterIndex = self.MasterlistWidget.currentRow()
                for i in range(len(masterList[masterIndex])):
                    armedMacros[2].append(masterList[masterIndex][i])
                print(armedMacros)
                self.Assigned3.clear()
                self.Assigned3.insertItem(0, '\'' + str(armedMacros[2][1]) + '\'' + ' is bound to ' + '\'' + str(armedMacros[2][0]) +'\'' + ' key, and will run ' + str(repeats) + ' times.')
            else:
                self.msg()
    
    def AssignMacro4(self):
        text, ok = QInputDialog.getText(self, 'Macro 4', 'Input key to trigger Macro')
        if ok and text is not None:
            if text in AcceptableInput:
                armedMacros[3].clear()
                armedMacros[3].append(str(text))
                repeats = self.getRepeats()
                armedMacros[0].append(str(repeats))
                masterIndex = self.MasterlistWidget.currentRow()
                for i in range(len(masterList[masterIndex])):
                    armedMacros[3].append(masterList[masterIndex][i])
                print(armedMacros)
                self.Assigned4.clear()
                self.Assigned4.insertItem(0, '\'' + str(armedMacros[3][1]) + '\'' + ' is bound to ' + '\'' + str(armedMacros[3][0]) +'\'' + ' key, and will run ' + str(repeats) + ' times.')
            else:
                self.msg()
    
    #=================================================================================
    
    #=================================================================================
    # This section is for the buttons that create and modify the macro in the EditListWidget and the editList.
    # The right list widget is tied to the editList and is meant to be temporary for creating and editing macros
    # and saving them to the masterList. 
    
    def hotKey(self):
        currentIndex = self.EditlistWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Hotkey', 'Input first key')
        if text in AcceptableInput:
            if ok and text is not None:
                text2, ok = QInputDialog.getText(self, 'Hotkey', 'Input second key')
                if text2 in AcceptableInput:
                    if ok and text2 is not None:
                        self.HK2(text, text2, currentIndex)
                        editList.insert(currentIndex+1, ['mhotKey', text, text2])
                else:
                    self.msg()
        else:
            self.msg()
    
    def HK2(self, text, text2, currentIndex):
        self.EditlistWidget.insertItem(currentIndex+1, 'Hotkey: '+ text + ' + ' + text2)
        self.EditlistWidget.setCurrentRow(currentIndex+1)
    
    def Press(self):
        currentIndex = self.EditlistWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Press', 'Input key to press')
        if text in AcceptableInput:
            if ok and text is not None:
                self.P2(text, '', currentIndex)
                editList.insert(currentIndex+1, ['mPress', text, ''])
            else:
                self.msg()
        else:
            self.msg()
    
    def P2(self, text, y, currentIndex):
        self.EditlistWidget.insertItem(currentIndex+1, 'Press: '+ text)
        self.EditlistWidget.setCurrentRow(currentIndex+1)

    def MultiPress(self):
        currentIndex = self.EditlistWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Multi Press', 'Input key to press')
        if text in AcceptableInput:
            if ok and text is not None:
                iterations, ok = QInputDialog.getInt(self, 'Multi Press', 'Input how many times to repeat')
                if ok and iterations is not None:
                    self.MP2(text, iterations, currentIndex)
                    editList.insert(currentIndex+1, ['mMultiPress', text, str(iterations)])
                else:
                    self.msg()
        else:
            self.msg()
    
    def MP2(self, text, iterations, currentIndex):
        self.EditlistWidget.insertItem(currentIndex+1, 'Press: '+ text + ' ' + str(iterations) + ' times')
        self.EditlistWidget.setCurrentRow(currentIndex+1)
    
    def Hold(self):
        currentIndex = self.EditlistWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Hold', 'Input key to hold')
        if text in AcceptableInput:
            if ok and text is not None:
                self.H2(text, '', currentIndex)
                self.R2(text, '', currentIndex+1)
                editList.insert(currentIndex+1, ['mHold', text, ''])
                editList.insert(currentIndex+2, ['mRelease', text, ''])
            else:
                self.msg()
        else:
            self.msg()
    
    def H2(self, text, y, currentIndex):
        self.EditlistWidget.insertItem(currentIndex+1, 'Hold: '+ text)
        self.EditlistWidget.setCurrentRow(currentIndex+1)
                
    def Release(self):
        currentIndex = self.EditlistWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Release', 'Input key to release')
        if text in AcceptableInput:
            if ok and text is not None:
                self.R2(text, '', currentIndex)
                editList.insert(currentIndex+1, ['mRelease', text, ''])
            else:
                self.msg()
        else:
            self.msg()
    
    def R2(self, text, y, currentIndex):
        self.EditlistWidget.insertItem(currentIndex+1, 'Release: '+ text)
        self.EditlistWidget.setCurrentRow(currentIndex+1)
    
    def Wait(self):
        currentIndex = self.EditlistWidget.currentRow()
        text, ok = QInputDialog.getDouble(self, 'Wait', 'Input how long to wait in seconds')
        if ok and text is not None:
            self.Wa2(text, '', currentIndex)
            editList.insert(currentIndex+1, ['mWait', str(text), ''])
    
    def Wa2(self, text, y, currentIndex):
        self.EditlistWidget.insertItem(currentIndex+1, 'Wait: '+ str(text) + ' seconds')
        self.EditlistWidget.setCurrentRow(currentIndex+1)
    
    def Write(self):
        currentIndex = self.EditlistWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'Write', 'Type characters to write')
        if ok and text is not None:
            self.Wr2(text, '', currentIndex)
            editList.insert(currentIndex+1, ['mWrite', text, ''])
    
    def Wr2(self, text, y, currentIndex):
        self.EditlistWidget.insertItem(currentIndex+1, 'Write: '+ text)
        self.EditlistWidget.setCurrentRow(currentIndex+1)
    
    def Copy(self):
        currentIndex = self.EditlistWidget.currentRow()
        last = self.EditlistWidget.item(currentIndex).clone()
        self.EditlistWidget.insertItem(currentIndex+1, last)
        self.EditlistWidget.setCurrentRow(currentIndex+1)
        editList.insert(currentIndex+1, editList[currentIndex])
        
    def MoveUp(self):
        currentIndex = self.EditlistWidget.currentRow()
        if not currentIndex < 1:
            last = self.EditlistWidget.takeItem(currentIndex)
            self.EditlistWidget.insertItem(currentIndex-1, last)
            self.EditlistWidget.setCurrentRow(currentIndex-1)
            editList.insert(currentIndex-1, editList.pop(currentIndex))
    
    def MoveDown(self):
        currentIndex = self.EditlistWidget.currentRow()
        if not currentIndex == len(editList)-1:
            last = self.EditlistWidget.takeItem(currentIndex)
            self.EditlistWidget.insertItem(currentIndex+1, last)
            self.EditlistWidget.setCurrentRow(currentIndex+1)
            editList.insert(currentIndex+1, editList.pop(currentIndex))
    
    def Remove(self):
        if not len(editList) == 0:
            currentIndex = self.EditlistWidget.currentRow()
            self.EditlistWidget.takeItem(currentIndex)
            editList.pop(currentIndex)
    
    def ListClear(self):
        self.EditlistWidget.clear()
        editList.clear()
    
    def Click(self):
        currentIndex = self.EditlistWidget.currentRow()
        self.Cl2('', '', currentIndex)
        editList.insert(currentIndex+1, ['mClick', '', ''])
    
    def Cl2(self, x, y, currentIndex):
        self.EditlistWidget.insertItem(currentIndex+1, 'Mouse Click')
        self.EditlistWidget.setCurrentRow(currentIndex+1)
    
    def RightClick(self):
        currentIndex = self.EditlistWidget.currentRow()
        self.RCl2('', '', currentIndex)
        editList.insert(currentIndex+1, ['mRightClick', '', ''])
    
    def RCl2(self, x, y, currentIndex):
        self.EditlistWidget.insertItem(currentIndex+1, 'Right Click')
        self.EditlistWidget.setCurrentRow(currentIndex+1)
    
    def DoubleClick(self):
        currentIndex = self.EditlistWidget.currentRow()
        self.DCl2('', '', currentIndex)
        editList.insert(currentIndex+1, ['mDoubleClick', '', ''])
    
    def DCl2(self, x, y, currentIndex):
        self.EditlistWidget.insertItem(currentIndex+1, 'Double Click')
        self.EditlistWidget.setCurrentRow(currentIndex+1)
    
    def MouseHold(self):
        currentIndex = self.EditlistWidget.currentRow()
        self.MH2('', '', currentIndex)
        self.MR2('', '', currentIndex+1)
        editList.insert(currentIndex+1, ['mMouseHold', '', ''])
        editList.insert(currentIndex+2, ['mMouseRelease', '', ''])
    
    def MH2(self, x, y, currentIndex):
        self.EditlistWidget.insertItem(currentIndex+1, 'Mouse Hold')
        self.EditlistWidget.setCurrentRow(currentIndex+1)
    
    def MouseRelease(self):
        currentIndex = self.EditlistWidget.currentRow()
        self.MR2('', '', currentIndex)
        editList.insert(currentIndex+1, ['mMouseRelease', '', ''])
    
    def MR2(self, x, y, currentIndex):
        self.EditlistWidget.insertItem(currentIndex+1, 'Mouse Release')
        self.EditlistWidget.setCurrentRow(currentIndex+1)
    
    def MouseMove(self):
        currentIndex = self.EditlistWidget.currentRow()
        xcord, ok = QInputDialog.getInt(self, 'Mouse Move', 'Input X coordinate')
        if ok and xcord is not None:
            ycord, ok = QInputDialog.getInt(self, 'Mouse Move', 'Input Y coordinate')
            if ok and ycord is not None:
                self.MM2(xcord, ycord, currentIndex)
                editList.insert(currentIndex+1, ['mMouseMove', str(xcord), str(ycord)])
            else:
                self.msg()
        else:
            self.msg()
    
    def MM2(self, x, y, currentIndex):
        self.EditlistWidget.insertItem(currentIndex+1, 'Move Mouse to: X:'+str(x)+' Y:'+str(y))
        self.EditlistWidget.setCurrentRow(currentIndex+1)
    
    def MoveRelative(self):
        currentIndex = self.EditlistWidget.currentRow()
        xcord, ok = QInputDialog.getInt(self, 'Mouse Move', 'Input X increase or decrease (+/-)')
        if ok and xcord is not None:
            if '-' not in str(xcord):
                xcord = '+'+str(xcord)
            ycord, ok = QInputDialog.getInt(self, 'Mouse Move', 'Input Y increase or decrease (+/-)')
            if ok and ycord is not None:
                if '-' not in str(ycord):
                    ycord = '+'+str(ycord)
                self.MR2(xcord, ycord, currentIndex)
                editList.insert(currentIndex+1, ['mMoveRelative', str(xcord), str(ycord)])
            else:
                self.msg()
        else:
            self.msg()
    
    def MR2(self, x, y, currentIndex):
        self.EditlistWidget.insertItem(currentIndex+1, 'Move Mouse: X'+str(x)+', Y'+str(y))
        self.EditlistWidget.setCurrentRow(currentIndex+1)
    
    def ClickandDrag(self):
        currentIndex = self.EditlistWidget.currentRow()
        xcord, ok = QInputDialog.getInt(self, 'Click and Drag', 'Input X coordinate to drag to (+/-)')
        if ok and xcord is not None:
            if '-' not in str(xcord):
                xcord = '+'+str(xcord)
            ycord, ok = QInputDialog.getInt(self, 'Click and Drag', 'Input Y coordinate to drag to (+/-)')
            if ok and ycord is not None:
                if '-' not in str(ycord):
                    ycord = '+'+str(ycord)
                self.CD2(xcord, ycord, currentIndex)
                editList.insert(currentIndex+1, ['mClickandDrag', str(xcord), str(ycord)])
            else:
                self.msg()
        else:
            self.msg()
    
    def CD2(self, x, y, currentIndex):
        self.EditlistWidget.insertItem(currentIndex+1, 'Click and Drag to: X'+str(x)+' Y'+str(y))
        self.EditlistWidget.setCurrentRow(currentIndex+1)
    
    #===========================================================================================
    
    #===========================================================================================
    # This section is for buttons that modify the MasterListWidget and the masterList that stores all the macros for use.
    
    def SaveToMasterList(self):
        overwrite = False
        text, ok = QInputDialog.getText(self, 'Name', 'What would you like to name this Macro?')
        if ok and text is not None:
            MlistIndex = -1
            print('Master list is ' + str(masterList))
            if len(masterList) > 0:
                for j in range(len(masterList)):
                    if text == masterList[j][0]:
                        overwrite = self.overwriteMsg(text)
                        if overwrite == False:
                            return
                        MlistIndex = j
                        print(masterList[j])
                        print(masterList[j][0])
                        masterList[j] = [masterList[j][0]]
                        print('Name found in Master list, new value for ' + masterList[j][0] + ' is ' + str(masterList[j]))
            if MlistIndex == -1:
                print('Name not found in Master List, appending to end')
                MlistIndex = len(masterList)
                masterList.append([text])
            for i in range(len(editList)):
                masterList[MlistIndex].append(editList[i])
            print('Full Master list is now ' + str(masterList))
            print('Edit list is ' + str(editList))
            self.updateMasterListWidget()
    
    #===========================================================================================
    
    # The triggering key (subject to name change) is what arms the macros. Before this key is pressed, the macros will not run
    # when the activation keys are presed
    
    def TriggeringKey(self):
        global running
        if running == False:
            x =threading.Thread(target=runMacro, daemon= True)
            x.start()
            print('hey')
            
    def msg(self):
        msg = QMessageBox(self)
        msg.setWindowTitle('Incorrect input')
        msg.setText('The input you entered cannot be accepted. Check the acceptable inputs list')
        msg.exec_()
    
    def overwriteMsg(self, name):
        msg = QMessageBox.question(self, 'Overwrite', 'You are about to overwrite ' + str(name) +', would you like to continue?', buttons = QMessageBox.Yes | QMessageBox.No)
        if msg == QMessageBox.Yes:
            return True
        else:
            return False
    
    def openFile(self):
        global editList
        oname, _ = QFileDialog.getOpenFileName(self, 'Open File', directory+'\\Saves', 'JSON Files (*.json)')
        if oname:
            self.EditlistWidget.clear()
            editList.clear()
            editList = json.load(open(oname))
            self.repopulate()
    
    def saveFile(self):
        sname, _ = QFileDialog.getSaveFileName(self, 'Save File', directory +'\\Saves', 'JSON Files (*.json)')
        if sname:
            with open(sname, 'w') as outfile:
                json.dump(editList, outfile)
    
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
        for i in range(len(editList)):
            self.repopDictionary[editList[i][0]](self, editList[i][1], editList[i][2], i)
    
    def updateMasterListWidget(self):
        self.MasterlistWidget.clear()
        for i in range(len(masterList)):
            self.MasterlistWidget.insertItem(i, masterList[i][0])

    def openInputs(self):
        inputWindow().exec_()
    
    def openInstructions(self):
        instructionsWindow().exec_()
    
    def openCoordinateWindow(self):
        coordinateWindow().exec_()
    
    def getRepeats(self):
        repeats, ok = QInputDialog.getInt(self, 'Repeats', 'Input how many times to repeat the macro')
        if ok and repeats is not None:
            return repeats
            #global Repeats
            #Repeats = repeats
            #self.repeatsList.clear()
            #self.repeatsList.insertItem(0, 'Repeats: ' + str(Repeats))
            

        
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
        x, y = pag.position()
        self.clabel.setText('X:'+str(x)+' Y:'+str(y))

    
AcceptableInput = [' ', '!', '"', '#', '$', '%', '&', "'", '(',
                    ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
                    '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`',
                    'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
                    'add', 'alt', 'backspace', 'capslock', 'clear', 'ctrl', 'del', 'delete',
                    'divide', 'down', 'end', 'enter', 'esc', 'escape', 'f1', 'f10',
                    'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
                    'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'insert',
                    'left', 'pagedown', 'pageup', 'pgdn', 'win', 
                    'pgup', 'printscreen', 'prntscrn',
                    'prtsc', 'prtscr', 'return', 'right', 
                    'shift', 'space', 'subtract', 'tab','up', 'command']

editList = []
masterList = []
armedMacros = [[''], [''], [''], ['']]
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
    global armedMacros
    print(str(key))
    for i in range(len(armedMacros)):
        if str(key) == 'Key.'+ armedMacros[i][0]:
            print('hola')
            begin(i)
        if key == Key.esc:
            running = False
            return False

def runMacro():
    global running
    if running == False:
        running = True
        with Listener(on_press=show) as listener:
            listener.join()

def begin(macroNumber):
    Repeats = armedMacros[macroNumber][1]
    for j in range(int(Repeats)):
        for i in range(len(armedMacros[macroNumber])-3):
            if keyboard.is_pressed('esc'):
                break
            callDictionary[armedMacros[macroNumber][i+3][0]](armedMacros[macroNumber][i+3][1], armedMacros[macroNumber][i+3][2])

def app():
    app = QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    
    app()

