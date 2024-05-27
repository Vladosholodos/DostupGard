# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Stats2.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_stats_window(object):
    def setupUi(self, stats_window):
        stats_window.setObjectName("stats_window")
        stats_window.setWindowModality(QtCore.Qt.NonModal)
        stats_window.resize(573, 555)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(stats_window.sizePolicy().hasHeightForWidth())
        stats_window.setSizePolicy(sizePolicy)
        stats_window.setMinimumSize(QtCore.QSize(0, 0))
        stats_window.setMaximumSize(QtCore.QSize(666666, 66666))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Лого.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        stats_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(stats_window)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 381, 493))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox.setEnabled(True)
        self.comboBox.setMaximumSize(QtCore.QSize(340, 16777215))
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.statsTable = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statsTable.sizePolicy().hasHeightForWidth())
        self.statsTable.setSizePolicy(sizePolicy)
        self.statsTable.setMinimumSize(QtCore.QSize(350, 351))
        self.statsTable.setMaximumSize(QtCore.QSize(16666, 16666))
        self.statsTable.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.statsTable.setLineWidth(0)
        self.statsTable.setObjectName("statsTable")
        self.statsTable.setColumnCount(0)
        self.statsTable.setRowCount(0)
        self.verticalLayout.addWidget(self.statsTable)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.filter_edit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.filter_edit.setObjectName("filter_edit")
        self.horizontalLayout_2.addWidget(self.filter_edit)
        self.filter_but = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.filter_but.setObjectName("filter_but")
        self.horizontalLayout_2.addWidget(self.filter_but)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 390, 51, 111))
        self.label.setObjectName("label")
        stats_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(stats_window)
        QtCore.QMetaObject.connectSlotsByName(stats_window)

    def retranslateUi(self, stats_window):
        _translate = QtCore.QCoreApplication.translate
        stats_window.setWindowTitle(_translate("stats_window", "Статистика"))
        self.pushButton.setText(_translate("stats_window", "Статистика"))
        self.filter_but.setText(_translate("stats_window", "Искать"))
        self.label.setText(_translate("stats_window", "Фильтр"))