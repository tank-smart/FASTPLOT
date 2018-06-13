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
        Form.resize(782, 581)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        Form.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.vlayout_sel_testpoints = QtWidgets.QVBoxLayout()
        self.vlayout_sel_testpoints.setSpacing(2)
        self.vlayout_sel_testpoints.setObjectName("vlayout_sel_testpoints")
        self.label_sel_testpoint = QtWidgets.QLabel(Form)
        self.label_sel_testpoint.setMinimumSize(QtCore.QSize(0, 24))
        self.label_sel_testpoint.setMaximumSize(QtCore.QSize(16777215, 24))
        self.label_sel_testpoint.setObjectName("label_sel_testpoint")
        self.vlayout_sel_testpoints.addWidget(self.label_sel_testpoint)
        self.hlayout_sel_testpoints_tool = QtWidgets.QHBoxLayout()
        self.hlayout_sel_testpoints_tool.setSpacing(2)
        self.hlayout_sel_testpoints_tool.setObjectName("hlayout_sel_testpoints_tool")
        self.tool_button_add = QtWidgets.QToolButton(Form)
        self.tool_button_add.setMinimumSize(QtCore.QSize(24, 24))
        self.tool_button_add.setMaximumSize(QtCore.QSize(24, 24))
        self.tool_button_add.setObjectName("tool_button_add")
        self.hlayout_sel_testpoints_tool.addWidget(self.tool_button_add)
        self.tool_button_delete = QtWidgets.QToolButton(Form)
        self.tool_button_delete.setMinimumSize(QtCore.QSize(24, 24))
        self.tool_button_delete.setMaximumSize(QtCore.QSize(24, 24))
        self.tool_button_delete.setObjectName("tool_button_delete")
        self.hlayout_sel_testpoints_tool.addWidget(self.tool_button_delete)
        self.tool_button_copy = QtWidgets.QToolButton(Form)
        self.tool_button_copy.setMinimumSize(QtCore.QSize(24, 24))
        self.tool_button_copy.setMaximumSize(QtCore.QSize(24, 24))
        self.tool_button_copy.setObjectName("tool_button_copy")
        self.hlayout_sel_testpoints_tool.addWidget(self.tool_button_copy)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hlayout_sel_testpoints_tool.addItem(spacerItem)
        self.vlayout_sel_testpoints.addLayout(self.hlayout_sel_testpoints_tool)
        self.table_testpoint = QtWidgets.QTableWidget(Form)
        self.table_testpoint.setObjectName("table_testpoint")
        self.table_testpoint.setColumnCount(4)
        self.table_testpoint.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.table_testpoint.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.table_testpoint.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.table_testpoint.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.table_testpoint.setHorizontalHeaderItem(3, item)
        self.table_testpoint.horizontalHeader().setDefaultSectionSize(150)
        self.table_testpoint.horizontalHeader().setMinimumSectionSize(150)
        self.vlayout_sel_testpoints.addWidget(self.table_testpoint)
        self.verticalLayout.addLayout(self.vlayout_sel_testpoints)
        self.line_h1 = QtWidgets.QFrame(Form)
        self.line_h1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_h1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_h1.setObjectName("line_h1")
        self.verticalLayout.addWidget(self.line_h1)
        self.hlayout_seltest_and_output = QtWidgets.QHBoxLayout()
        self.hlayout_seltest_and_output.setSpacing(4)
        self.hlayout_seltest_and_output.setObjectName("hlayout_seltest_and_output")
        self.vlayout_sel_para = QtWidgets.QVBoxLayout()
        self.vlayout_sel_para.setObjectName("vlayout_sel_para")
        self.label_sel_para = QtWidgets.QLabel(Form)
        self.label_sel_para.setMinimumSize(QtCore.QSize(0, 24))
        self.label_sel_para.setMaximumSize(QtCore.QSize(16777215, 24))
        self.label_sel_para.setObjectName("label_sel_para")
        self.vlayout_sel_para.addWidget(self.label_sel_para)
        self.tree_sel_para_tree = QtWidgets.QTreeWidget(Form)
        self.tree_sel_para_tree.setColumnCount(2)
        self.tree_sel_para_tree.setObjectName("tree_sel_para_tree")
        self.tree_sel_para_tree.header().setDefaultSectionSize(240)
        self.tree_sel_para_tree.header().setMinimumSectionSize(240)
        self.vlayout_sel_para.addWidget(self.tree_sel_para_tree)
        self.hlayout_seltest_and_output.addLayout(self.vlayout_sel_para)
        self.line_v = QtWidgets.QFrame(Form)
        self.line_v.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_v.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_v.setObjectName("line_v")
        self.hlayout_seltest_and_output.addWidget(self.line_v)
        self.vlayout_output_config = QtWidgets.QVBoxLayout()
        self.vlayout_output_config.setSpacing(2)
        self.vlayout_output_config.setObjectName("vlayout_output_config")
        self.label = QtWidgets.QLabel(Form)
        self.label.setMinimumSize(QtCore.QSize(0, 24))
        self.label.setMaximumSize(QtCore.QSize(16777215, 24))
        self.label.setObjectName("label")
        self.vlayout_output_config.addWidget(self.label)
        self.hlayout_out_filetype = QtWidgets.QHBoxLayout()
        self.hlayout_out_filetype.setObjectName("hlayout_out_filetype")
        self.label_file_type = QtWidgets.QLabel(Form)
        self.label_file_type.setMinimumSize(QtCore.QSize(100, 24))
        self.label_file_type.setMaximumSize(QtCore.QSize(100, 24))
        self.label_file_type.setObjectName("label_file_type")
        self.hlayout_out_filetype.addWidget(self.label_file_type)
        self.combo_box_file_type = QtWidgets.QComboBox(Form)
        self.combo_box_file_type.setMinimumSize(QtCore.QSize(0, 24))
        self.combo_box_file_type.setMaximumSize(QtCore.QSize(16777215, 24))
        self.combo_box_file_type.setObjectName("combo_box_file_type")
        self.combo_box_file_type.addItem("")
        self.combo_box_file_type.addItem("")
        self.combo_box_file_type.addItem("")
        self.hlayout_out_filetype.addWidget(self.combo_box_file_type)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hlayout_out_filetype.addItem(spacerItem1)
        self.vlayout_output_config.addLayout(self.hlayout_out_filetype)
        self.hlayout_out_loc = QtWidgets.QHBoxLayout()
        self.hlayout_out_loc.setObjectName("hlayout_out_loc")
        self.label_output_loc = QtWidgets.QLabel(Form)
        self.label_output_loc.setMinimumSize(QtCore.QSize(100, 0))
        self.label_output_loc.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_output_loc.setObjectName("label_output_loc")
        self.hlayout_out_loc.addWidget(self.label_output_loc)
        self.line_edit_location = QtWidgets.QLineEdit(Form)
        self.line_edit_location.setMinimumSize(QtCore.QSize(0, 24))
        self.line_edit_location.setMaximumSize(QtCore.QSize(16777215, 24))
        self.line_edit_location.setObjectName("line_edit_location")
        self.hlayout_out_loc.addWidget(self.line_edit_location)
        self.button_sel_dir = QtWidgets.QToolButton(Form)
        self.button_sel_dir.setMinimumSize(QtCore.QSize(24, 24))
        self.button_sel_dir.setMaximumSize(QtCore.QSize(24, 24))
        self.button_sel_dir.setObjectName("button_sel_dir")
        self.hlayout_out_loc.addWidget(self.button_sel_dir)
        self.vlayout_output_config.addLayout(self.hlayout_out_loc)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vlayout_output_config.addItem(spacerItem2)
        self.hlayout_seltest_and_output.addLayout(self.vlayout_output_config)
        self.verticalLayout.addLayout(self.hlayout_seltest_and_output)
        self.line_h2 = QtWidgets.QFrame(Form)
        self.line_h2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_h2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_h2.setObjectName("line_h2")
        self.verticalLayout.addWidget(self.line_h2)
        self.hlayout_output_btn = QtWidgets.QHBoxLayout()
        self.hlayout_output_btn.setSpacing(10)
        self.hlayout_output_btn.setObjectName("hlayout_output_btn")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hlayout_output_btn.addItem(spacerItem3)
        self.button_confirm = QtWidgets.QPushButton(Form)
        self.button_confirm.setMinimumSize(QtCore.QSize(0, 24))
        self.button_confirm.setMaximumSize(QtCore.QSize(16777215, 24))
        self.button_confirm.setObjectName("button_confirm")
        self.hlayout_output_btn.addWidget(self.button_confirm)
        self.button_reset = QtWidgets.QPushButton(Form)
        self.button_reset.setMinimumSize(QtCore.QSize(0, 24))
        self.button_reset.setMaximumSize(QtCore.QSize(16777215, 24))
        self.button_reset.setObjectName("button_reset")
        self.hlayout_output_btn.addWidget(self.button_reset)
        self.verticalLayout.addLayout(self.hlayout_output_btn)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(2, 3)
        self.label_sel_para.raise_()
        self.tree_sel_para_tree.raise_()
        self.label_output_loc.raise_()
        self.label_sel_testpoint.raise_()
        self.label_sel_testpoint.raise_()
        self.combo_box_file_type.raise_()
        self.label_file_type.raise_()
        self.line_h1.raise_()
        self.line_v.raise_()
        self.line_h2.raise_()
        self.line_h1.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_sel_testpoint.setText(_translate("Form", "Selected testpoints"))
        self.tool_button_add.setText(_translate("Form", "..."))
        self.tool_button_delete.setText(_translate("Form", "..."))
        self.tool_button_copy.setText(_translate("Form", "..."))
        item = self.table_testpoint.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Testpoint name"))
        item = self.table_testpoint.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Start time"))
        item = self.table_testpoint.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Stop time"))
        item = self.table_testpoint.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Output filename"))
        self.label_sel_para.setText(_translate("Form", "Selected parameters"))
        self.tree_sel_para_tree.headerItem().setText(0, _translate("Form", "Original name"))
        self.tree_sel_para_tree.headerItem().setText(1, _translate("Form", "Output name"))
        self.label.setText(_translate("Form", "Output setting"))
        self.label_file_type.setText(_translate("Form", "Output file type"))
        self.combo_box_file_type.setItemText(0, _translate("Form", "TXT file"))
        self.combo_box_file_type.setItemText(1, _translate("Form", "CSV file"))
        self.combo_box_file_type.setItemText(2, _translate("Form", "MAT file"))
        self.label_output_loc.setText(_translate("Form", "Output location"))
        self.button_sel_dir.setText(_translate("Form", "..."))
        self.button_confirm.setText(_translate("Form", "Confirm"))
        self.button_reset.setText(_translate("Form", "Reset"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

