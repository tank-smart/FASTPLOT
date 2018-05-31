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

# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication
from PyQt5.QtGui import QCloseEvent, QIcon
from PyQt5.QtWidgets import (QWidget, QDockWidget,QLineEdit, QMenu, 
                             QTreeWidget, QTreeWidgetItem, QAction,
                             QSizePolicy, QVBoxLayout, QAbstractItemView,
                             QHeaderView)

# =============================================================================
<<<<<<< HEAD:lib/views/paralist_window.py
# ParalistWindow
# =============================================================================
class ParalistWindow(QDockWidget):

# =============================================================================
# 自定义信号模块
# =============================================================================
=======
# ParalistDock
# =============================================================================
class ParalistDock(QDockWidget):

# =============================================================================
# 自定义信号模块
# =============================================================================
>>>>>>> 058f8ba1896ebc91db7f8433a6b6b1975d8dc28d:lib/views/paralist_dock.py
#    参数窗口关闭信号
    signal_close = pyqtSignal()
#    导出数据的信号，带有字典型参数（存储了文件路径和参数名的信息）
    signal_export_para = pyqtSignal(dict)
#    快速绘图的信号，带有字典型参数（存储了文件路径和参数名的信息）
    signal_quick_plot = pyqtSignal(dict)
#    搜索参数的信号
    signal_search_para = pyqtSignal(str)
    
# =============================================================================
# 初始化
# =============================================================================
<<<<<<< HEAD:lib/views/paralist_window.py
    def __init__(self, parent = None):
        super().__init__(parent)
=======
    def __init__(self):
        QStackedWidget.__init__(self)
>>>>>>> 058f8ba1896ebc91db7f8433a6b6b1975d8dc28d:lib/views/paralist_dock.py
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
        self.tree_widget_display_datafile = QTreeWidget(self.layout_paralist_dock)
        self.tree_widget_display_datafile.setObjectName(
                "tree_widget_display_datafile")
        self.tree_widget_display_datafile.header().setVisible(False)
#        设置每个item是可以被选择的
        self.tree_widget_display_datafile.setSelectionMode(
                QAbstractItemView.ExtendedSelection)
#        让树可支持右键菜单(step 1)
        self.tree_widget_display_datafile.setContextMenuPolicy(Qt.CustomContextMenu)
        self.vlayout_paralist_dock.addWidget(self.tree_widget_display_datafile)        
#        添加右键动作
        self.action_export = QAction(self.tree_widget_display_datafile)
        self.action_export.setText(QCoreApplication.
                                   translate("ParalistDock", "导出参数"))
        self.action_quick_plot = QAction(self.tree_widget_display_datafile)
        self.action_quick_plot.setText(QCoreApplication.
                                       translate("ParalistDock", "快速绘图"))
        self.action_delete_file = QAction(self.tree_widget_display_datafile)
        self.action_delete_file.setText(QCoreApplication.
                                       translate("ParalistDock", "删除文件"))
        
<<<<<<< HEAD:lib/views/paralist_window.py
        self.setWidget(self.layout_paralist_dock)
        
=======
>>>>>>> 058f8ba1896ebc91db7f8433a6b6b1975d8dc28d:lib/views/paralist_dock.py
# =======连接信号与槽
# =============================================================================
#        使右键时能弹出菜单(step 2)
        self.tree_widget_display_datafile.customContextMenuRequested.connect(
                self.on_tree_context_menu)
        
        self.action_export.triggered.connect(self.slot_export_para)
        self.action_quick_plot.triggered.connect(self.slot_quick_plot)
        self.action_delete_file.triggered.connect(self.slot_delete_file)
        
        self.line_edit_search_para.textChanged.connect(self.slot_search_para)

# =============================================================================
# Slots模块
# =============================================================================
#    右键菜单的事件处理(step 3)
    def on_tree_context_menu(self, pos):
        
#        记录右击时鼠标所在的item
        sel_item = self.tree_widget_display_datafile.itemAt(pos)
        
#        如果鼠标不在item上，不显示右键菜单
        if sel_item:
#            创建菜单，添加动作，显示菜单
            menu = QMenu(self.tree_widget_display_datafile)
            menu.addAction(self.action_export)
            menu.addAction(self.action_quick_plot)
            menu.addAction(self.action_delete_file)
            if sel_item.parent():
                self.action_delete_file.setDisabled(True)
            else:
                self.action_delete_file.setDisabled(False)
            menu.exec_(self.tree_widget_display_datafile.mapToGlobal(pos))
            
    def slot_export_para(self):
#        获得被选项的文件路径和参数列表
        sel_items = self.get_dict_sel_item()
#        传递出去
        self.signal_export_para.emit(sel_items)
    
    def slot_quick_plot(self):
        
        pass

    def slot_delete_file(self):
        
        pass
    
#    当参数搜索行有用户输入时将搜索参数的信号发出
    def slot_search_para(self, paraname):
        self.signal_search_para.emit(paraname)

#    重载关闭事件，需要增加一个关闭的信号让菜单栏下的勾选去掉        
    def closeEvent(self, event: QCloseEvent):
        event.accept()
        self.signal_close.emit()

# =============================================================================
# 功能函数模块   
# =============================================================================
    def display_file_group(self, file_group , is_expand_all = False):

#        不确定是否真的删除了
        self.tree_widget_display_datafile.clear()        
        if file_group:  #file_name is a dict
            
            for file_dir in file_group:
                root = QTreeWidgetItem(self.tree_widget_display_datafile) #QTreeWidgetItem object: root
#                设置图标
                root.setIcon(0,self.fileicon)
#                显示文件名而不是路径
                pos = file_dir.rindex('\\')
                filename = file_dir[pos+1:]
                root.setText(0, filename) #set text of treewidget
#                将路径作为数据存入item中
                root.setData(0, Qt.UserRole, file_dir)
                for para in file_group[file_dir]:
                    child = QTreeWidgetItem(root)  #child of root
                    child.setIcon(0,self.paraicon)
                    child.setText(0,para)
            
            if is_expand_all:
                self.tree_widget_display_datafile.expandAll()

    def get_dict_sel_item(self):
        
        result = {}
#        获取选中的item列表
        sel_items = self.tree_widget_display_datafile.selectedItems()
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