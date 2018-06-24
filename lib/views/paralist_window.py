# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 简述：参数窗口类
#
# =======使用说明
# 。。。
#
# =======日志
# 
# =============================================================================
import re
# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtCore import (Qt, pyqtSignal, QCoreApplication, QMimeData, 
                          QByteArray, QDataStream, QIODevice)
from PyQt5.QtGui import QCloseEvent, QIcon
from PyQt5.QtWidgets import (QWidget, QDockWidget,QLineEdit, QMenu, 
                             QTreeWidget, QTreeWidgetItem, QAction,
                             QSizePolicy, QVBoxLayout, QAbstractItemView,
                             QMessageBox)
# =============================================================================
# Package views imports
# =============================================================================
from models.datafile_model import Normal_DataFile

# =============================================================================
# ParasTree
# =============================================================================
class ParasTree(QTreeWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
    
#    自定义MIME type的结构，将参数名和参数所在的文件名存入
    def mimeData(self, items):
        mime_data = QMimeData()
        byte_array = QByteArray()
        stream = QDataStream(byte_array, QIODevice.WriteOnly)
        for item in items:
            if item:
                if item.parent():
                    stream.writeQString(item.text(0))
                    stream.writeQString(item.parent().data(0, Qt.UserRole))
        mime_data.setData('application/x-parasname', byte_array)
        return mime_data
        
# =============================================================================
# ParalistWindow
# =============================================================================
class ParalistWindow(QDockWidget):
# =============================================================================
# 自定义信号模块
# =============================================================================
#    参数窗口关闭信号，此信号在主窗口中进行信号与槽连接
    signal_close = pyqtSignal()
#    导出数据的信号，带有字典型参数（存储了文件路径和参数名的信息）
    signal_export_para = pyqtSignal(dict)
#    快速绘图的信号，带有字典型参数（存储了文件路径和参数名的信息）
    signal_quick_plot = pyqtSignal(dict)
#    搜索参数的信号
    signal_search_para = pyqtSignal(str)
    
    signal_delete_files = pyqtSignal(list)
    
# =============================================================================
# 初始化
# =============================================================================
    def __init__(self, parent = None):
        
        super().__init__(parent)
#        设置文件与参数的图标
        self.fileicon = QIcon(r"E:\DAGUI\lib\icon\datafile.png")
        self.paraicon = QIcon(r"E:\DAGUI\lib\icon\parameter.png")
    
# =============================================================================
# UI模块
# =============================================================================
    def setup(self):
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.layout_paralist_dock = QWidget(self)
        self.layout_paralist_dock.setObjectName("layout_paralist_dock")
        self.vlayout_paralist_dock = QVBoxLayout(self.layout_paralist_dock)
        self.vlayout_paralist_dock.setContentsMargins(1, 1, 1, 1)
        self.vlayout_paralist_dock.setSpacing(2)
        self.vlayout_paralist_dock.setObjectName("vlayout_paralist_dock")
        
#        行输入部件的定义
        self.line_edit_search_para = QLineEdit(self.layout_paralist_dock)
        self.line_edit_search_para.setToolTip("")
        self.line_edit_search_para.setInputMask("")
        self.line_edit_search_para.setText("")
        self.line_edit_search_para.setMaxLength(32766)
        self.line_edit_search_para.setFrame(True)
        self.line_edit_search_para.setEchoMode(QLineEdit.Normal)
        self.line_edit_search_para.setAlignment(
                Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.line_edit_search_para.setReadOnly(False)
        self.line_edit_search_para.setObjectName("line_edit_search_para")
        self.vlayout_paralist_dock.addWidget(self.line_edit_search_para)
        
#        文件树显示部件的定义
        self.datafiles_tree = ParasTree(self.layout_paralist_dock)
        self.datafiles_tree.setObjectName(
                "datafiles_tree")
#        可拖出树部件中的项
        self.datafiles_tree.setDragEnabled(True)
        self.datafiles_tree.header().setVisible(False)
#        设置每个item是可以被选择的
        self.datafiles_tree.setSelectionMode(
                QAbstractItemView.ExtendedSelection)
#        让树可支持右键菜单(step 1)
        self.datafiles_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.vlayout_paralist_dock.addWidget(self.datafiles_tree)        
#        添加右键动作
        self.action_export = QAction(self.datafiles_tree)
        self.action_export.setText(QCoreApplication.
                                   translate("ParalistDock", "导出参数"))
        self.action_quick_plot = QAction(self.datafiles_tree)
        self.action_quick_plot.setText(QCoreApplication.
                                       translate("ParalistDock", "快速绘图"))
        self.action_delete_files = QAction(self.datafiles_tree)
        self.action_delete_files.setText(QCoreApplication.
                                       translate("ParalistDock", "删除文件"))
        
        self.setWidget(self.layout_paralist_dock)
        
# =======连接信号与槽
# =============================================================================
#        使右键时能弹出菜单(step 2)
        self.datafiles_tree.customContextMenuRequested.connect(
                self.on_tree_context_menu)
        
        self.action_export.triggered.connect(self.slot_export_para)
        self.action_quick_plot.triggered.connect(self.slot_quick_plot)
        self.action_delete_files.triggered.connect(self.slot_delete_files)
        
        self.line_edit_search_para.textChanged.connect(self.slot_search_para)

# =============================================================================
# Slots模块
# =============================================================================
#    重载关闭事件，需要增加一个关闭的信号让菜单栏下的勾选去掉        
    def closeEvent(self, event: QCloseEvent):
        
#        当窗口关闭后发出信号
        self.signal_close.emit()
        event.accept()

#    右键菜单的事件处理(step 3)
    def on_tree_context_menu(self, pos):
        
#        记录右击时鼠标所在的item
        sel_item = self.datafiles_tree.itemAt(pos)
        
#        如果鼠标不在item上，不显示右键菜单
        if sel_item:
#            创建菜单，添加动作，显示菜单
            menu = QMenu(self.datafiles_tree)
            menu.addAction(self.action_export)
            menu.addAction(self.action_quick_plot)
            menu.addAction(self.action_delete_files)
            if sel_item.parent():
                self.action_export.setDisabled(False)
                self.action_quick_plot.setDisabled(False)
                self.action_delete_files.setDisabled(True)
            else:
                self.action_export.setDisabled(True)
                self.action_quick_plot.setDisabled(True)
                self.action_delete_files.setDisabled(False)
            menu.exec_(self.datafiles_tree.mapToGlobal(pos))
            
    def slot_import_datafiles(self, file_dirs):
        
        if file_dirs:
            for file_dir in file_dirs:
                if self.is_in_files_tree(file_dir):
                    QMessageBox.information(self,
                            QCoreApplication.translate("ParalistWindow", "导入提示"),
                            QCoreApplication.translate("ParalistWindow", "文件已存在"))
                else:
                    root = QTreeWidgetItem(self.datafiles_tree) 
#                    设置图标
                    root.setIcon(0,self.fileicon)
#                    显示文件名而不是路径
                    pos = file_dir.rindex('\\')
                    filename = file_dir[pos+1:]
                    root.setText(0, filename)
#                    将路径作为数据存入item中
                    root.setData(0, Qt.UserRole, file_dir)
                    root.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    file = Normal_DataFile(file_dir)
                    for para in file.paras_in_file:
                        child = QTreeWidgetItem(root)
                        child.setIcon(0,self.paraicon)
                        child.setText(0,para)

    def slot_delete_files(self, files):

#        获取选中的item列表
        sel_items = self.datafiles_tree.selectedItems()
        if sel_items:
            message = QMessageBox.warning(self,
                          QCoreApplication.translate("ParalistWindow", "删除文件"),
                          QCoreApplication.translate("ParalistWindow",
                                            """<p>确定要删除文件吗？"""),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                for item in sel_items:
#                    判断选中的是参数还是文件
                    if item.parent():
                        pass
                    else:
                        index = self.datafiles_tree.indexOfTopLevelItem(item)
                        self.datafiles_tree.takeTopLevelItem(index)

#    搜索参数并显示在参数窗口里
    def slot_search_para(self, para_name):
        
        if self.datafiles_tree:
            count = self.datafiles_tree.topLevelItemCount()
            pattern = re.compile('.*' + para_name + '.*')
            for i in range(count):
                item = self.datafiles_tree.topLevelItem(i)
                child_count = item.childCount()
                for child_index in range(child_count):
                    paraname = item.child(child_index).text(0)
                    if re.match(pattern, paraname):
                        item.child(child_index).setHidden(False)
                    else:
                        item.child(child_index).setHidden(True)
            self.datafiles_tree.expandAll()
    
    def slot_export_para(self):
#        获得被选项的文件路径和参数列表
        sel_items = self.get_dict_sel_item()
#        传递出去
        self.signal_export_para.emit(sel_items)
    
    def slot_quick_plot(self):
        
#        获得被选项的文件路径和参数列表
        sel_items = self.get_dict_sel_item()
#        传递出去
        self.signal_quick_plot.emit(sel_items)

# =============================================================================
# 功能函数模块   
# =============================================================================
    def get_dict_sel_item(self):
        
        result = {}
#        获取选中的item列表
        sel_items = self.datafiles_tree.selectedItems()
        if sel_items:
            for item in sel_items:
    #            判断选中的是参数还是文件
                if item.parent():
                    fileitem = item.parent()
                    file_dir = fileitem.data(0, Qt.UserRole)
#                    判断文件是否已经存在
                    if (file_dir in result):
                        result[file_dir].append(item.text(0))
                    else:
                        result[file_dir] = []
                        result[file_dir].append(item.text(0))
        return result

    def get_dict_files_tree(self):
        
        result = {}
        count = self.datafiles_tree.topLevelItemCount()
        if count > 0:            
            for i in range(count):
                item = self.datafiles_tree.topLevelItem(i)
                file_dir = item.data(0, Qt.UserRole)
                result[file_dir] = []
                child_count = item.childCount()
                for child_index in range(child_count):
                    paraname = item.child(child_index).text(0)
                    result[file_dir].append(paraname)
        return result

    def is_in_files_tree(self, file_dir):
        
        count = self.datafiles_tree.topLevelItemCount()
        for index in range(count):
            fd = self.datafiles_tree.topLevelItem(index).data(0, Qt.UserRole)
            if file_dir == fd:
                return True
        return False