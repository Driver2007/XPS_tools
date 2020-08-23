# -*- coding: utf-8 -*-

import sys
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import pyqtgraph as pg
import os
import configparser

ELEMENTS = configparser.ConfigParser()
ELEMENTS.read("elements.ini")

class SelectElement_Dialog(QtWidgets.QDialog):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Select elements")
        
        self.frame_vs_atomic_number = {i: None for i in range(0,118)}
        columns = 19
        rows = 10
        lanthanoid_number = 2
        actinoid_number = 2
        self.atomic_number = 0
        
        self.element_button = []
        self.label_atomic_mass_nr = []
        self.label_title = []
        self.label = []
        self.cmenu = []
        
        self.frames = [[QtWidgets.QGroupBox(self) for x in range(rows)] for y in range(columns)]
        
        
        for row in range(0,rows):
            for column in range(0,columns):
                self.frames[column][row].resize(50,50)
                self.frames[column][row].move(10+55*column,10+55*row)
     
                if (row == 1 and column > 1) and (row == 1 and column < 18):
                    continue
                elif (row == 2  and column > 2) and (row == 2 and column < 13):
                    continue
                elif (row == 3  and column > 2) and (row == 3 and column < 13):
                    continue
                else:
                    if row != 0 and column != 0 and row <8:
                        while (self.atomic_number > 56 and self.atomic_number < 71):
                            self.atomic_number += 1
                            lanthanoid_number += 1
                            self.frame_vs_atomic_number[self.atomic_number] = (lanthanoid_number,8)
                            self.frames[lanthanoid_number][8].setTitle(str(self.atomic_number))
                            self.frames[lanthanoid_number][8].setObjectName("ColoredGroupBox_"+str(self.atomic_number))
                            color = "rgba(0, 255, 0, 50%) "
                            self.frames[lanthanoid_number][8].setStyleSheet("QGroupBox#ColoredGroupBox_"+str(self.atomic_number)+" { background-color: " + color + "; border: 1px solid " + color + "; }")  # ... and here
                        else:
                            while (self.atomic_number > 87 and self.atomic_number < 102):
                                self.atomic_number += 1
                                actinoid_number += 1
                                self.frame_vs_atomic_number[self.atomic_number] = (actinoid_number,8)
                                self.frames[actinoid_number][9].setTitle(str(self.atomic_number))
                                self.frames[actinoid_number][9].setObjectName("ColoredGroupBox_"+str(self.atomic_number))
                                color = "rgba(0, 255, 0, 50%) "
                                self.frames[actinoid_number][9].setStyleSheet("QGroupBox#ColoredGroupBox_"+str(self.atomic_number)+" { background-color: " + color + "; border: 1px solid " + color + "; }")  # ... and here
                            else:
                                self.atomic_number += 1
                                self.frames[column][row].setTitle(str(self.atomic_number))
                                self.frames[column][row].setObjectName("ColoredGroupBox_"+str(self.atomic_number))
                                self.frame_vs_atomic_number[self.atomic_number] = (column,row)
                                if column == 1 or column == 2 and row < 8: 
                                    color = "rgba(0, 0, 255, 50%) "
                                    self.frames[column][row].setStyleSheet("QGroupBox#ColoredGroupBox_"+str(self.atomic_number)+" { background-color: " + color + "; border: 1px solid " + color + "; }")  # ... and here
                                if column > 2 and column < 13 and row < 8:
                                    color = "rgba(255, 0, 0, 50%) "
                                    self.frames[column][row].setStyleSheet("QGroupBox#ColoredGroupBox_"+str(self.atomic_number)+" { background-color: " + color + "; border: 1px solid " + color + "; }")  # ... and here
                                if column > 12 and row < 8:
                                    color = "rgba(255, 255, 0, 50%) "
                                    self.frames[column][row].setStyleSheet("QGroupBox#ColoredGroupBox_"+str(self.atomic_number)+" { background-color: " + color + "; border: 1px solid " + color + "; }")  # ... and here
        i = 0
        for element in ELEMENTS.sections():
            self.element_button.append(QtWidgets.QPushButton(self.frames[self.frame_vs_atomic_number[int(element)][0]][self.frame_vs_atomic_number[int(element)][1]]))
            self.element_button[i].setText(ELEMENTS[element]["label"])
            self.element_button[i].setGeometry(QtCore.QRect(25, 0, 20, 20))
            
            self.label_atomic_mass_nr.append(QtWidgets.QLabel(self.frames[self.frame_vs_atomic_number[int(element)][0]][self.frame_vs_atomic_number[int(element)][1]]))
            self.label_atomic_mass_nr[i].setText(ELEMENTS[element]["mass"])
            self.label_atomic_mass_nr[i].move(5,35)

            self.label_title.append(QtWidgets.QLabel(self.frames[self.frame_vs_atomic_number[int(element)][0]][self.frame_vs_atomic_number[int(element)][1]]))
            self.label_title[i].setText(ELEMENTS[element]["title"])
            self.label_title[i].move(5,20)
            #self.label_title = []
            i += 1
    
    def contextMenuEvent(self, event):
        i = 0
        for element in ELEMENTS.sections():
            self.cmenu.append(QtWidgets.QMenu(self.frames[self.frame_vs_atomic_number[int(element)][0]][self.frame_vs_atomic_number[int(element)][1]]))

            newAct = self.cmenu[i].addAction("New")
            i += 1    
                                #self.labels[column][row] = QtWidgets.QLabel(self.frames[column][row])
                                #self.labels[column][row].setObjectName("label_"+str(row)+"_"+str(column))
                                #self.labels[column][row].setText(str(self.atomic_number))
                                #self.labels[column][row].move(10,10)      
    
class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("gui_core_level_identifier.ui", self)
        self.setWindowTitle("XPS core level identifier")
        self.select_elements_dialog = SelectElement_Dialog()
        
        self.resize(730,350)
        self.data_x = [1, 1]
        self.data_y = [0, 1]
################    initial variables#######################################
        self.kinetic_energy = True
        self.wf_dsp.setValue(5.0)
        self.ph_energy_dsp.valueChanged.connect(self.photon_energy_v_change)
        self.wf_dsp.valueChanged.connect(self.wf_v_change)

        self.photon_energy = 0.0
        self.work_function = 0.0
################    graph widget  #########################################        
        self.graphWidget = pg.PlotWidget(self)
        self.graphWidget.showGrid(True, True, alpha=0.3)
        self.graphWidget.move(10,40)
        self.graphWidget.resize(700,300)
        self.graphWidget.plotItem.setLabel("bottom", text= "Kinetic_energy (eV)")
        #plot data: x, y values
        self.curve = self.graphWidget.plot(self.data_x, self.data_y)
        
########## controll elements on the panel  ###################################
        self.kin_energy_cb.stateChanged.connect(self.x_axis_kinetic_energy)
        self.bind_energy_cb.stateChanged.connect(self.x_axis_binding_energy)
        self.select_elements_bs.clicked.connect(self.select_elements)
        
    def select_elements(self):
        self.select_elements_dialog.show()

        
        
    def wf_v_change(self):
        self.photon_energy_v_change()               

    def photon_energy_v_change(self):
        self.work_function = self.wf_dsp.value()
        self.photon_energy = self.ph_energy_dsp.value()
        print (self.kinetic_energy)
        if self.kinetic_energy == True:
            self.x_axis_kinetic_energy(True)
        else:
            self.x_axis_binding_energy(True)

    def x_axis_kinetic_energy (self, state):
        self.kinetic_energy = True
        self.bind_energy_cb.setChecked(False)
        self.graphWidget.plotItem.setLabel("bottom", text= "Kinetic energy (eV)")
        if self.photon_energy > self.work_function:
            self.graphWidget.plotItem.setXRange(-10, (self.photon_energy - self.work_function),padding = 0.0)
            self.graphWidget.plotItem.invertX(False)
        else:
            print ("check photon energy")
            
            
    def x_axis_binding_energy (self, state):
        self.kinetic_energy = False
        self.kin_energy_cb.setChecked(False)
        self.graphWidget.plotItem.setLabel("bottom", text= "Binding energy (eV)")
        if self.photon_energy > self.work_function:
            self.graphWidget.plotItem.setXRange((self.photon_energy - self.work_function), -10)
            self.graphWidget.plotItem.invertX(True)
        else:
            print ("check photon energy")
            
        
if os.path.exists("elements.ini"):        
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
