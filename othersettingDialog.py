# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerfkfnPV.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_SettingDialog(object):
    def setupUi(self, SettingDialog):
        if not SettingDialog.objectName():
            SettingDialog.setObjectName(u"SettingDialog")
        SettingDialog.resize(273, 113)
        self.buttonBox = QDialogButtonBox(SettingDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 80, 251, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.timeDelaySlider = QSlider(SettingDialog)
        self.timeDelaySlider.setObjectName(u"timeDelaySlider")
        self.timeDelaySlider.setGeometry(QRect(90, 41, 160, 21))
        self.timeDelaySlider.setMinimum(1)
        self.timeDelaySlider.setMaximum(5)
        self.timeDelaySlider.setSingleStep(5)
        self.timeDelaySlider.setPageStep(5)
        self.timeDelaySlider.setOrientation(Qt.Horizontal)
        self.label = QLabel(SettingDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 40, 54, 21))
        self.label_2 = QLabel(SettingDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(90, 10, 61, 21))
        self.label_3 = QLabel(SettingDialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(190, 10, 61, 21))

        self.retranslateUi(SettingDialog)
        self.buttonBox.accepted.connect(SettingDialog.accept)
        self.buttonBox.rejected.connect(SettingDialog.reject)

        QMetaObject.connectSlotsByName(SettingDialog)
    # setupUi

    def retranslateUi(self, SettingDialog):
        SettingDialog.setWindowTitle(QCoreApplication.translate("SettingDialog", u"\u5176\u5b83\u8bbe\u7f6e", None))
        self.label.setText(QCoreApplication.translate("SettingDialog", u"\u5168\u5c40\u5ef6\u65f6", None))
        self.label_2.setText(QCoreApplication.translate("SettingDialog", u"\u6700\u5feb100ms", None))
        self.label_3.setText(QCoreApplication.translate("SettingDialog", u"\u6700\u6162500ms", None))
    # retranslateUi
