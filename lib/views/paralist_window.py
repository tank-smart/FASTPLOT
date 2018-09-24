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
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QDockWidget,QLineEdit, QMenu, 
                             QTreeWidget, QTreeWidgetItem, QAction, 
                             QVBoxLayout, QAbstractItemView, QMessageBox)
# =============================================================================
# Package views imports
# =============================================================================
import views.config_info as CONFIG

# =============================================================================
# ParasTree
# =============================================================================
class ParasTree(QTreeWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
#        可拖出树部件中的项
        self.setDragEnabled(True)
    
#    自定义MIME type的结构，将参数名和参数所在的文件名存入
    def mimeData(self, items):
        mime_data = QMimeData()
        byte_array = QByteArray()
        stream = QDataStream(byte_array, QIODevice.WriteOnly)
        for item in items:
            if item:
                if item.parent():
                    stream.writeQString(item.data(0, Qt.UserRole))
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
#    导出数据的信号，带有字典型参数（存储了文件路径和参数名的信息）
    signal_into_analysis = pyqtSignal(list)
#    快速绘图的信号，带有字典型参数（存储了文件路径和参数名的信息）
    signal_quick_plot = pyqtSignal(tuple)
#    删除的文件
    signal_delete_files = pyqtSignal(list)
#    要计算的参数
    signal_into_mathematics = pyqtSignal(str)
#    要增加的数据字典
    signal_into_data_dict = pyqtSignal(str)
    
# =============================================================================
# 初始化
# =============================================================================
    def __init__(self, parent = None):
        
        super().__init__(parent)
        
#        设置文件与参数的图标
        self.fileicon = QIcon(CONFIG.ICON_FILE)
        self.paraicon = QIcon(CONFIG.ICON_PARA)
        
        self.sel_paraname = ''
        self._data_dict = None
    
# =============================================================================
# UI模块
# =============================================================================
    def setup(self):
        
        self.setWindowTitle(QCoreApplication.translate('ParalistDock', '参数浏览器'))

        self.paralist_dock_contents = QWidget(self)
        self.vlayout_paralist_dock = QVBoxLayout(self.paralist_dock_contents)
        self.vlayout_paralist_dock.setContentsMargins(2, 2, 2, 2)
        self.vlayout_paralist_dock.setSpacing(2)
        
#        行输入部件的定义
        self.line_edit_search_para = QLineEdit(self.paralist_dock_contents)
        self.line_edit_search_para.setPlaceholderText(QCoreApplication.
                                                      translate('ParalistDock', '过滤器'))
        self.line_edit_search_para.setMinimumHeight(28)
        self.line_edit_search_para.setMaxLength(32766)
        self.line_edit_search_para.setFrame(True)
        self.line_edit_search_para.setEchoMode(QLineEdit.Normal)
        self.line_edit_search_para.setAlignment(
                Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.line_edit_search_para.setReadOnly(False)
        self.vlayout_paralist_dock.addWidget(self.line_edit_search_para)
        
#        文件树显示部件的定义
        self.datafiles_tree = ParasTree(self.paralist_dock_contents)
        self.datafiles_tree.header().setVisible(False)
#        设置多选模式
        self.datafiles_tree.setSelectionMode(
                QAbstractItemView.ExtendedSelection)
#        让树可支持右键菜单(step 1)
        self.datafiles_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.vlayout_paralist_dock.addWidget(self.datafiles_tree)        
#        添加右键动作
        self.action_into_analysis = QAction(self.datafiles_tree)
        self.action_into_analysis.setText(QCoreApplication.
                                   translate('ParalistDock', '添加至分析'))
        self.action_into_mathematics = QAction(self.datafiles_tree)
        self.action_into_mathematics.setText(QCoreApplication.
                                             translate('ParalistDock', '添加至计算'))
        self.action_into_data_dict = QAction(self.datafiles_tree)
        self.action_into_data_dict.setText(QCoreApplication.
                                           translate('ParalistDock', '添加字典'))
        self.action_quick_plot = QAction(self.datafiles_tree)
        self.action_quick_plot.setText(QCoreApplication.
                                       translate('ParalistDock', '快速绘图'))
        self.action_delete_files = QAction(self.datafiles_tree)
        self.action_delete_files.setText(QCoreApplication.
                                       translate('ParalistDock', '删除文件'))
        self.action_expand_all = QAction(self.datafiles_tree)
        self.action_expand_all.setText(QCoreApplication.
                                       translate('ParalistDock', '展开列表'))
        self.action_collapse_all = QAction(self.datafiles_tree)
        self.action_collapse_all.setText(QCoreApplication.
                                         translate('ParalistDock', '收起列表'))
        
        self.setWidget(self.paralist_dock_contents)
        
# =======连接信号与槽
# =============================================================================
#        使右键时能弹出菜单(step 2)
        self.datafiles_tree.customContextMenuRequested.connect(
                self.on_tree_context_menu)
        
        self.action_into_analysis.triggered.connect(self.slot_into_analysis)
        self.action_into_mathematics.triggered.connect(self.slot_into_mathematics)
        self.action_into_data_dict.triggered.connect(self.slot_into_data_dict)
        self.action_quick_plot.triggered.connect(self.slot_quick_plot)
        self.action_delete_files.triggered.connect(self.slot_delete_files)
        self.action_collapse_all.triggered.connect(self.slot_collapse_all)
        self.action_expand_all.triggered.connect(self.slot_expand_all)
        
        self.line_edit_search_para.textChanged.connect(self.slot_search_para)

# =============================================================================
# Slots模块
# =============================================================================
#    右键菜单的事件处理(step 3)
    def on_tree_context_menu(self, pos):
        
#        记录右击时鼠标所在的item
        sel_item = self.datafiles_tree.itemAt(pos)
        
#        如果鼠标不在item上，不显示右键菜单
        if sel_item:
#            创建菜单，添加动作，显示菜单
            self.sel_paraname = sel_item.data(0, Qt.UserRole)
            menu = QMenu(self.datafiles_tree)
            menu.addActions([self.action_quick_plot,
                             self.action_into_analysis,
                             self.action_into_mathematics,
                             self.action_into_data_dict,
                             self.action_delete_files,
                             self.action_expand_all,
                             self.action_collapse_all])
            if sel_item.parent():
                self.action_into_analysis.setDisabled(False)
                self.action_into_mathematics.setDisabled(False)
                self.action_into_data_dict.setDisabled(False)
                self.action_quick_plot.setDisabled(False)
                self.action_delete_files.setDisabled(True)
            else:
                self.action_into_analysis.setDisabled(True)
                self.action_into_mathematics.setDisabled(True)
                self.action_into_data_dict.setDisabled(True)
                self.action_quick_plot.setDisabled(True)
                self.action_delete_files.setDisabled(False)
            menu.exec_(self.datafiles_tree.mapToGlobal(pos))
            
    def slot_import_datafiles(self, file_dirs):
        
        if file_dirs:
            for file_dir in file_dirs:
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
                flag = True
                for para in file_dirs[file_dir]:
#                        跳过时间这个参数名
                    if flag:
                        flag = False
                    else:
                        child = QTreeWidgetItem(root)
                        child.setIcon(0, self.paraicon)
                        child.setData(0, Qt.UserRole, para)
                        if (self._data_dict and 
                            CONFIG.OPTION['data dict scope paralist'] and
                            para in self._data_dict):
                            if CONFIG.OPTION['data dict scope style'] == 0:
                                temp_str = self._data_dict[para][0]
                            if CONFIG.OPTION['data dict scope style'] == 1:
                                temp_str = para + '(' + self._data_dict[para][0] + ')'
                            if CONFIG.OPTION['data dict scope style'] == 2:
                                temp_str = self._data_dict[para][0] + '(' + para + ')'
                            child.setText(0, temp_str)
                        else:
                            child.setText(0, para)

    def slot_delete_files(self):

#        获取选中的item列表
        file_list = []
        sel_items = self.datafiles_tree.selectedItems()
        if sel_items:
            message = QMessageBox.warning(self,
                          QCoreApplication.translate('ParalistWindow', '删除文件'),
                          QCoreApplication.translate('ParalistWindow',
                                            '''<p>确定要删除所选文件吗？'''),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                for item in sel_items:
#                    判断选中的是参数还是文件
                    if item.parent():
                        pass
                    else:
                        file_list.append(item.data(0, Qt.UserRole))
                        index = self.datafiles_tree.indexOfTopLevelItem(item)
                        self.datafiles_tree.takeTopLevelItem(index)
        if file_list:
            self.signal_delete_files.emit(file_list)

#    搜索参数并显示在参数窗口里
    def slot_search_para(self, para_name):
        
        if self.datafiles_tree:
            count = self.datafiles_tree.topLevelItemCount()
            pattern = re.compile('.*' + para_name + '.*')
            for i in range(count):
                num_para_in_show = 0
                item = self.datafiles_tree.topLevelItem(i)
                child_count = item.childCount()
                for child_index in range(child_count):
                    para_alias = item.child(child_index).text(0)
                    paraname = item.child(child_index).data(0, Qt.UserRole)
                    if re.match(pattern, para_alias) or re.match(pattern, paraname):
                        item.child(child_index).setHidden(False)
                        num_para_in_show += 1
                    else:
                        item.child(child_index).setHidden(True)
                if num_para_in_show == 0:
                    item.setHidden(True)
                else:
                    item.setHidden(False)
            self.datafiles_tree.expandAll()
    
    def slot_into_analysis(self):
#        获得被选项的文件路径和参数列表
        dict_r, list_r = self.get_sel_item()
#        传递出去
        self.signal_into_analysis.emit(list_r)
        
    def slot_into_mathematics(self):

        if self.sel_paraname:
#            传递出去
            self.signal_into_mathematics.emit(self.sel_paraname)
            
    def slot_into_data_dict(self):
        
        if self.sel_paraname:
#            传递出去
            self.signal_into_data_dict.emit(self.sel_paraname)
    
    def slot_quick_plot(self):

#        传递出去
        self.signal_quick_plot.emit(self.get_sel_item())
        
    def slot_expand_all(self):
        
        self.datafiles_tree.expandAll()
        
    def slot_collapse_all(self):
        
        self.datafiles_tree.collapseAll()

# =============================================================================
# 功能函数模块   
# =============================================================================
    def get_sel_item(self):
        
        dict_result = {}
        list_result = []
#        获取选中的item列表
        sel_items = self.datafiles_tree.selectedItems()
        if sel_items:
            for item in sel_items:
    #            判断选中的是参数还是文件
                if item.parent():
                    fileitem = item.parent()
                    file_dir = fileitem.data(0, Qt.UserRole)
#                    判断文件是否已经存在
                    if (file_dir in dict_result):
                        dict_result[file_dir].append(item.data(0, Qt.UserRole))
                    else:
                        dict_result[file_dir] = []
                        dict_result[file_dir].append(item.data(0, Qt.UserRole))
                    list_result.append((item.data(0, Qt.UserRole), file_dir))
        return (dict_result, list_result)

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
                    paraname = item.child(child_index).data(0, Qt.UserRole)
                    result[file_dir].append(paraname)
        return result