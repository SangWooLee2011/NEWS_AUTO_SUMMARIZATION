# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'article_analysis_system.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
import re, os, subprocess
from article_analysis import Data_by_category
from PyQt5 import QtCore, QtGui, QtWidgets
import webbrowser

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(817, 652)
        self.data1 = Data_by_category("National", 70)
        self.data2 = Data_by_category("Sports", 70)
        self.data3 = Data_by_category("World", 70)
        self.data_index  = 0


        self.clicked_index = 0

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 30, 751, 551))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.category_button_1 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.category_button_1.setObjectName("category_button_1")
        self.horizontalLayout.addWidget(self.category_button_1)
        self.category_button_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.category_button_2.setObjectName("category_button_2")
        self.horizontalLayout.addWidget(self.category_button_2)
        self.category_button_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.category_button_3.setObjectName("category_button_3")
        self.horizontalLayout.addWidget(self.category_button_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.synchronization_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.synchronization_button.setObjectName("synchronization_button")
        self.horizontalLayout_3.addWidget(self.synchronization_button)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.listWidget = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()

        for i in range(140):
            item = QtWidgets.QListWidgetItem()
            self.listWidget.addItem(item)

        self.verticalLayout.addWidget(self.listWidget)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.slabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.slabel.setObjectName("slabel")
        self.horizontalLayout_2.addWidget(self.slabel)
        self.link_to_article_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.link_to_article_button.setObjectName("link_to_article_button")
        self.horizontalLayout_2.addWidget(self.link_to_article_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.surmary_textBW = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.surmary_textBW.setObjectName("surmary_textBW")
        self.verticalLayout_2.addWidget(self.surmary_textBW)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 817, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        self.category_button_1.clicked.connect(self.category1)
        self.category_button_2.clicked.connect(self.category2)
        self.category_button_3.clicked.connect(self.category3)
        self.synchronization_button.clicked.connect(self.sync_article)
        self.link_to_article_button.clicked.connect(self.open_url)
        self.listWidget.itemClicked['QListWidgetItem*'].connect(self.list_clicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.category1()

    def sync_article(self):
        newMessage = QtWidgets.QMessageBox()
        newMessage.about(newMessage,"Updating", "The system will stop while it updates articles, and it takes about 6 minutes.")
        subprocess.call(['python.exe', "Web_Crawaler.py"])
        self.data1 = Data_by_category("National", 70)
        self.data2 = Data_by_category("Sports", 70)
        self.data3 = Data_by_category("World", 70)
        self.surmary_textBW.setHtml(_translate("MainWindow",
                                               "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                               "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                               "p, li { white-space: pre-wrap; }\n"
                                               "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                               "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Update completed</p></body></html>"))


    def category1(self):

        for i in range(140):
            item = self.listWidget.item(i)
            item.setText("(" + str(i) + ")" + self.data1.articleData[i].title)
            self.data_index = 1

    def category2(self):
        for i in range(140):
            item = self.listWidget.item(i)
            item.setText("("+str(i)+")"+ self.data2.articleData[i].title)
            self.data_index = 2

    def category3(self):
        for i in range(140):
            item = self.listWidget.item(i)
            item.setText("(" + str(i) + ")" + self.data3.articleData[i].title)
            self.data_index = 3


    def list_clicked(self, i):
        self.index = int(re.findall('\d+', i.text()[0:4])[0])
        summary =""
        if(self.data_index==1):
            for sentence in self.data1.articleData[self.index].summary:
                summary += sentence
        elif(self.data_index==2):
            for sentence in self.data2.articleData[self.index].summary:
                summary += sentence
        elif (self.data_index == 3):
            for sentence in self.data3.articleData[self.index].summary:
                summary += sentence

        self.surmary_textBW.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                     "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                     "p, li { white-space: pre-wrap; }\n"
                                     "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"+ summary +"</p></body></html>")

    def open_url(self):
        url=""
        if (self.data_index == 1):
            url += self.data1.articleData[self.index].url
        elif (self.data_index == 2):
            url += self.data2.articleData[self.index].url
        elif (self.data_index == 3):
            url += self.data3.articleData[self.index].url
        webbrowser.open(url)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Article Analysis System(Sang-woo Lee)"))
        self.category_button_1.setText(_translate("MainWindow", "National"))
        self.category_button_2.setText(_translate("MainWindow", "Sports"))
        self.category_button_3.setText(_translate("MainWindow", "World"))
        self.synchronization_button.setText(_translate("MainWindow", "뉴스 기사 동기화(약 5분정도 소요)"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.slabel.setText(_translate("MainWindow", "기사 요약 보기"))
        self.link_to_article_button.setText(_translate("MainWindow", "기사 원문"))
        self.surmary_textBW.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">기사요약</p></body></html>"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


