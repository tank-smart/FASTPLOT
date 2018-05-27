# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\DAGUI\lib\views\data_export.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(510, 500)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.sel_para = QtWidgets.QLabel(Form)
        self.sel_para.setObjectName("sel_para")
        self.verticalLayout.addWidget(self.sel_para)
        
        self.sel_para_tree = QtWidgets.QTreeWidget(Form)
        self.sel_para_tree.setColumnCount(2)
        self.sel_para_tree.setObjectName("sel_para_tree")
        self.sel_para_tree.header().setDefaultSectionSize(240)
        self.sel_para_tree.header().setMinimumSectionSize(240)
        
        self.verticalLayout.addWidget(self.sel_para_tree)
        self.sel_testpoint = QtWidgets.QLabel(Form)
        self.sel_testpoint.setObjectName("sel_testpoint")
        self.verticalLayout.addWidget(self.sel_testpoint)
        spacerItem = QtWidgets.QSpacerItem(20, 164, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.export_loc = QtWidgets.QLabel(Form)
        self.export_loc.setObjectName("export_loc")
        self.verticalLayout.addWidget(self.export_loc)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.location_view = QtWidgets.QLineEdit(Form)
        self.location_view.setMinimumSize(QtCore.QSize(0, 24))
        self.location_view.setMaximumSize(QtCore.QSize(16777215, 24))
        self.location_view.setObjectName("location_view")
        self.horizontalLayout_2.addWidget(self.location_view)
        self.sel_dir = QtWidgets.QToolButton(Form)
        self.sel_dir.setMinimumSize(QtCore.QSize(24, 24))
        self.sel_dir.setMaximumSize(QtCore.QSize(24, 24))
        self.sel_dir.setObjectName("sel_dir")
        self.horizontalLayout_2.addWidget(self.sel_dir)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.button_confirm = QtWidgets.QPushButton(Form)
        self.button_confirm.setObjectName("button_confirm")
        self.horizontalLayout.addWidget(self.button_confirm)
        self.button_cancel = QtWidgets.QPushButton(Form)
        self.button_cancel.setObjectName("button_cancel")
        self.horizontalLayout.addWidget(self.button_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.sel_para.setText(_translate("Form", "Selected parameters"))
        self.sel_para_tree.headerItem().setText(0, _translate("Form", "Original Name"))
        self.sel_para_tree.headerItem().setText(1, _translate("Form", "Output Name"))
        self.sel_testpoint.setText(_translate("Form", "Select testpoint"))
        self.export_loc.setText(_translate("Form", "Export location"))
        self.sel_dir.setText(_translate("Form", "..."))
        self.button_confirm.setText(_translate("Form", "Confirm"))
        self.button_cancel.setText(_translate("Form", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

