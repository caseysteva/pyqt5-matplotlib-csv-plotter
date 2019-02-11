# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 15:14:06 2019

@author: casey

must download win32api... pip install this might be garbage then
"""
import json
import csv
import time
from pathlib import Path
import math

import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp, QApplication, QPushButton, QDesktopWidget,
                            QLabel, QFileDialog, QWidget, QGridLayout, QMenu, QSizePolicy, QMessageBox, QWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, Qt
from win32api import GetSystemMetrics

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np

import random

CURRENT_VERSION = 0.1

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Plotting Data')

        window_width = GetSystemMetrics(0)
        window_height = GetSystemMetrics(1)

        self.resize(0.6 * window_width, 0.6 * window_height)
        self.center()

        self.setWindowIcon(QIcon('Icon.png'))

        #inits
        self.openDirectoryDialog = ""
        self.data = np.empty(shape=(1,2), dtype=np.float)

        #Exit on menubar
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit applicatiion')
        exitAct.triggered.connect(qApp.quit)

        #Open on menubar
        openAct = QAction('&Open', self)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open Directory')
        openAct.triggered.connect(self.openFile)

        #menubar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        fileMenu.addAction(openAct)

        #Central
        centralwidget = QWidget(self)
        self.setCentralWidget(centralwidget)

        #Grid
        grid = QGridLayout(centralwidget)
        self.setLayout(grid)

        #Plot
        plotCan = PlotCanvas(self, width=5, height=4)
        grid.addWidget(plotCan , 0,1)

        #button
        btn = QPushButton("Plot", centralwidget)
        btn.resize(btn.sizeHint())
        grid.addWidget(btn, 0,0)
        btn.clicked.connect(lambda: plotCan.plot(self.data))
       # btn.clicked.connect(plotCan .plot(self.data))

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        '''
        def LoadCSV(datafilename):
    with open(datafilename, 'r') as datacsv:
        reader = csv.reader(datacsv, delimiter=',')
        data = [row for row in reader]
    
    return data 
        '''

    def openFile(self):
        self.csvFile = QFileDialog.getOpenFileName(self, "Get Dir Path")[0]
        self.data = np.loadtxt(self.csvFile, delimiter=',', dtype='S')[2:].astype(np.float)
      
        '''
       trying to load 3 columns
       '''
        
        
        b = [row for row in self.data]
        
    def inkdict2list(inkdict):
        {"initialweight": 9.2835, "finalweight": 10.2011, "speed": 27.620251640479214, "time": 1527695235.0652485}
        listdata = []
        for line in inkdict:
            dataline = []
            dataline.append(line['time'])
            dataline.append(line['initialweight'])
            dataline.append(line['finalweight'])
            dataline.append(line['speed'])
            listdata.append(dataline)
        return listdata

    def SaveCSV(listdata, name):
        filename = str(int(round(time.time(),0))) + name + '.csv'
        with open(filename, 'w') as datacsv:
            writer = csv.writer(datacsv)
            for line in listdata:
                writer.writerow(line)
    if __name__=='__main__':
    #Get the data from the data folder
        datapath = Path('.')
        filelist = [p for p in datapath.iterdir() if p.match('*.csv')]
    
        materials = ['STD']
    
        colorindex= {}
    #colorindex['1SHEETS']=0
        colorindex['_LINVLIN_']=1
        colorindex['_LOGVLIN_']=2
        colorindex['_LOGVLOG_']=3
        colorindex['_LINVLOG_']=4
        
        
    for material in materials:
        fig, sfig1 = plt.subplots()
        for file in filelist:
            if str(file).endswith('E.CSV') and material in str(file):
                filedata = LoadCSV(file)                
                freqlist = [float(line[0]) for line in filedata[3:]]
                elist = [float(line[1]) for line in filedata[3:]]
                ifilename = str(file).split('.')[0]+'I.CSV'
                ifiledata = LoadCSV(ifilename)
                eilist = [float(line[1]) for line in ifiledata[3:]]
                tandlist = [math.tan(eilist[n]/elist[n]) for n in range(0,len(elist))]
                
                
                sfig1.set_xlabel('Freq (Hz)')
                sfig1.set_ylabel(chr(949)+chr(8242), color = 'b')
                sfig1.set_xscale('log')
                sfig1.tick_params(axis='y', labelcolor='b')
                sfig2 = sfig1.twinx()
                #sfig2.set_ylabel(chr(949)+chr(8242)+chr(8242), color = 'g', rotation=-90, labelpad=10)
                sfig2.set_ylabel('tan '+chr(948), color = 'g', rotation=-90, labelpad=10)
                sfig2.tick_params(axis='y', labelcolor='g')
                #sfig2.set_yscale('log')
                
                sfig1.set_xlim(1E7,1E9)
                sfig1.set_ylim(2.2,2.4)
                sfig2.set_ylim(-0.001,0.005)
                balpha = 1
                galpha = 1
                
                alphamin = 0.1
                palpha = 1
    
                for key in colorindex:
                    if key in str(file):
                        palpha = alphamin+(1-alphamin)*0.5**colorindex[key]
                        
                print('printing e')
                sfig1.plot(freqlist,elist, color = 'b', alpha = palpha)
                print('printing i')
                sfig2.plot(freqlist,tandlist, color = 'g', alpha = palpha)
        
        plt.tight_layout()
        fig.savefig('Figure'+ 'Summary' +'tand.png', dpi=600)


#Above is added code
        # How to get python to plot the csv file 
        #Figure out commands and statements to do that 
    
        
        
    def buttonpress(self):
        self.plot(self.data)

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, data = np.empty(shape=(1,2))):
        ax = self.figure.add_subplot(111)
        ax.plot(data[:,0],data[:,1], 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = Example()
    sys.exit(app.exec_())