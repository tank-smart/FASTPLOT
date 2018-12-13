# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 简述：数据导出类
#
# =======使用说明
# 
#
# =======日志
# 
# =============================================================================
import os, json
# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtCore import (QSize, QCoreApplication, pyqtSignal, Qt,
                          QDataStream, QIODevice)
from PyQt5.QtGui import QIcon, QDragEnterEvent, QDropEvent, QFont
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QAction,
                             QMenu, QListWidget, QListWidgetItem,
                             QLineEdit, QAbstractItemView, QGroupBox,
                             QMessageBox, QFileDialog, QSizePolicy,
                             QPushButton, QSpacerItem)

import views.config_info as CONFIG
# =============================================================================
# ParasListWithDropEvent
# =============================================================================
class ParasListWithDropEvent(QListWidget):

    signal_drop_paras = pyqtSignal(list)
    signal_paras_change = pyqtSignal()
#    用于显示已选参数，因为需要增加
    def __init__(self, parent = None):
        
        super().__init__(parent)
#        设置多选模式
        self.setSelectionMode(
                QAbstractItemView.ExtendedSelection)
#        接受拖放
        self.setAcceptDrops(True)
#       让树可支持右键菜单(step 1)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
#        使右键时能弹出菜单(step 2)
        self.customContextMenuRequested.connect(
                self.on_list_paras_menu)
#        添加右键动作
        self.action_delete_paras = QAction(self)
        self.action_delete_paras.setText(QCoreApplication.
                                         translate('ParasListWithDropEvent', '删除参数'))
        self.action_delete_paras.triggered.connect(self.slot_delete_paras)

#    右键菜单的事件处理(step 3)        
    def on_list_paras_menu(self, pos):
        
#        记录右击时鼠标所在的item
        sel_item = self.itemAt(pos)
        
#        如果鼠标不在item上，不显示右键菜单
        if sel_item:
#            创建菜单，添加动作，显示菜单
            menu = QMenu(self)
            menu.addActions([self.action_delete_paras])
            
            menu.exec_(self.mapToGlobal(pos))
            
    def slot_delete_paras(self):
        
        items = self.selectedItems()
        if items:
            message = QMessageBox.warning(self,
                          QCoreApplication.translate('ParasListWithDropEvent', '删除参数'),
                          QCoreApplication.translate('ParasListWithDropEvent', '确定要删除所选参数吗'),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                for item in items:
                    self.takeItem(self.row(item))
                    self.signal_paras_change.emit()

#    重写拖放相关的事件
#    设置部件可接受的MIME type列表，此处的类型是自定义的
    def mimeTypes(self):
        return ['application/x-parasname']
#    拖进事件处理    
    def dragEnterEvent(self, event : QDragEnterEvent):
#        如果拖进来的时树列表才接受
        if event.mimeData().hasFormat('application/x-parasname'):
            event.acceptProposedAction()
        else:
            event.ignore()
#     放下事件处理   
    def dropEvent(self, event : QDropEvent):
        
        sorted_paras = []
        if event.mimeData().hasFormat('application/x-parasname'):
            item_data = event.mimeData().data('application/x-parasname')
            item_stream = QDataStream(item_data, QIODevice.ReadOnly)
            while (not item_stream.atEnd()):
#                不同于绘图的解析，因为此处更关注的是参数的排列顺序
                paraname = item_stream.readQString()
                item_stream.readQString()
                sorted_paras.append(paraname)
            self.signal_drop_paras.emit(sorted_paras)
            event.acceptProposedAction()
        else:
            event.ignore()
# =============================================================================
# ParaTempWindow
# =============================================================================
class ParaTempWindow(QWidget):

    signal_display_paras_template = pyqtSignal()
    signal_close_pt_dock = pyqtSignal()
# =============================================================================
# 初始化    
# =============================================================================    
    def __init__(self, parent = None):
        
        super().__init__(parent)
        
        self.paras_temps = {}
        self._data_dict = None
        self.dir_import = CONFIG.SETUP_DIR
        self.current_temp_change_status = False
        
        self.current_temp = None
#        因为创建和编辑时取消按钮的槽函数应该进行不同的处理，
#        为了让函数能判断正处在创建还是编辑，因此使用该判断
        self.is_creating = False
        
        self.tempicon = QIcon(CONFIG.ICON_TEMPLATE)
        self.paraicon = QIcon(CONFIG.ICON_PARA)
        

# =============================================================================
# UI模块        
# =============================================================================
    def setup(self):

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.horizontalLayout_2 = QHBoxLayout(self)
        self.horizontalLayout_2.setContentsMargins(2, 0, 2, 0)
        self.horizontalLayout_2.setSpacing(2)
        self.group_box_templates = QGroupBox(self)
        self.verticalLayout = QVBoxLayout(self.group_box_templates)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(2)
        self.list_para_templates = QListWidget(self.group_box_templates)
        self.verticalLayout.addWidget(self.list_para_templates)
        self.horizontalLayout_2.addWidget(self.group_box_templates)
        self.group_box_template_setting = QGroupBox(self)
        self.verticalLayout_2 = QVBoxLayout(self.group_box_template_setting)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(2)
        self.label_para_template = QLabel(self.group_box_template_setting)
        self.label_para_template.setMinimumSize(QSize(0, 24))
        self.label_para_template.setMaximumSize(QSize(16777215, 24))
        self.verticalLayout_2.addWidget(self.label_para_template)
        self.line_edit_paras_template_name = QLineEdit(self.group_box_template_setting)
        self.line_edit_paras_template_name.setMinimumSize(QSize(0, 24))
        self.line_edit_paras_template_name.setMaximumSize(QSize(16777215, 24))
        self.verticalLayout_2.addWidget(self.line_edit_paras_template_name)
        self.label_parameters = QLabel(self.group_box_template_setting)
        self.label_parameters.setMinimumSize(QSize(0, 24))
        self.label_parameters.setMaximumSize(QSize(16777215, 24))
        self.verticalLayout_2.addWidget(self.label_parameters)
        self.list_parameters_for_ana = ParasListWithDropEvent(self.group_box_template_setting)
        self.verticalLayout_2.addWidget(self.list_parameters_for_ana)
#        self.btn_box_para_template = QDialogButtonBox(self.group_box_template_setting)
#        self.btn_box_para_template.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
#        self.verticalLayout_2.addWidget(self.btn_box_para_template)
        self.hlayout_btn_sc = QHBoxLayout()
        self.hlayout_btn_sc.setSpacing(4)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hlayout_btn_sc.addItem(spacerItem1)
        self.btn_save = QPushButton(self.group_box_template_setting)
        self.btn_save.setMinimumSize(QSize(0, 24))
        self.btn_save.setMaximumSize(QSize(16777215, 24))
        self.hlayout_btn_sc.addWidget(self.btn_save)
        self.btn_cancel = QPushButton(self.group_box_template_setting)
        self.btn_cancel.setMinimumSize(QSize(0, 24))
        self.btn_cancel.setMaximumSize(QSize(16777215, 24))
        self.hlayout_btn_sc.addWidget(self.btn_cancel)
        self.btn_close = QPushButton(self.group_box_template_setting)
        self.btn_close.setMinimumSize(QSize(0, 24))
        self.btn_close.setMaximumSize(QSize(16777215, 24))
        self.hlayout_btn_sc.addWidget(self.btn_close)
        self.verticalLayout_2.addLayout(self.hlayout_btn_sc)
        
        self.horizontalLayout_2.addWidget(self.group_box_template_setting)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 5)


        self.retranslateUi()
#        加载模板
        self.load_temps()

#        设置每个item是可以被选择的
        self.list_para_templates.setSelectionMode(
                QAbstractItemView.ExtendedSelection)
        
#       让树可支持右键菜单(step 1)
        self.list_para_templates.setContextMenuPolicy(Qt.CustomContextMenu)
      
#        添加右键动作
        self.action_delete_templates = QAction(self.list_para_templates)
        self.action_delete_templates.setText(QCoreApplication.
                                             translate('ParaTempWindow', '删除模板'))
        self.action_create_template = QAction(self.list_para_templates)
        self.action_create_template.setText(QCoreApplication.
                                            translate('ParaTempWindow', '新建模板'))
        self.action_import_templates = QAction(self.list_para_templates)
        self.action_import_templates.setText(QCoreApplication.
                                            translate('ParaTempWindow', '导入模板'))

# =======连接信号与槽
# =============================================================================        
        self.list_para_templates.itemClicked.connect(self.slot_display_template)
        
        self.line_edit_paras_template_name.editingFinished.connect(self.slot_change_temp_name)
#        使右键时能弹出菜单(step 2)
        self.list_para_templates.customContextMenuRequested.connect(
                self.on_list_para_templates_menu)
        self.action_delete_templates.triggered.connect(self.slot_delete_templates)
        self.action_create_template.triggered.connect(self.slot_create_temp)
        self.action_import_templates.triggered.connect(self.slot_import_temps)
        
        self.list_parameters_for_ana.signal_drop_paras.connect(self.slot_import_paras)
        self.list_parameters_for_ana.signal_paras_change.connect(self.slot_para_deled)
        self.btn_save.clicked.connect(self.slot_save_temp)
        self.btn_cancel.clicked.connect(self.slot_cancel_save_temp)
        self.btn_close.clicked.connect(self.slot_close)
#        self.btn_box_para_template.accepted.connect(self.slot_save_temp)
#        self.btn_box_para_template.rejected.connect(self.slot_cancel_save_temp)

# =============================================================================
# slots模块
# =============================================================================
#    右键菜单的事件处理(step 3)
    def on_list_para_templates_menu(self, pos):
        
#        记录右击时鼠标所在的item
        sel_item = self.list_para_templates.itemAt(pos)
#        创建菜单，添加动作，显示菜单
        menu = QMenu(self.list_para_templates)
        menu.addActions([self.action_create_template,
                         self.action_import_templates,
                         self.action_delete_templates])
#        如果鼠标不在item上，不显示右键菜单
        if sel_item:
            self.action_delete_templates.setEnabled(True)
        else:
            self.action_delete_templates.setEnabled(False)
        menu.exec_(self.list_para_templates.mapToGlobal(pos))
    
#    直接覆盖同名的模板,当分析参数窗口保存模板时触发
    def slot_add_para_template(self, template : dict):
        
        if template:
            for name in template:
                new_name = name
                i = 0
                while new_name in self.paras_temps:
                    new_name = name + '(copy ' + str(i) + ')'
                    i += 1
                self.paras_temps[new_name] = template[name]
                self.redisplay_para_templates()

#    显示模板信息
    def slot_display_template(self, item):

        if self.current_temp_change_status:
            message = QMessageBox.warning(self,
                                          QCoreApplication.translate('ParaTempWindow', '保存提示'),
                                          QCoreApplication.translate('ParaTempWindow', '模板：' + self.current_temp.text() + '未保存，是否保存？'),
                                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                self.slot_save_temp()
            else:
                self.current_temp_change_status = False
        if item.text() in self.paras_temps:
            self.current_temp = item
            self.list_parameters_for_ana.clear()
            self.line_edit_paras_template_name.clear()
    #        显示参数列表
            for paraname in self.paras_temps[item.text()]:
                item_para = QListWidgetItem(paraname, self.list_parameters_for_ana)
                item_para.setIcon(self.paraicon)
                if (self._data_dict and 
                    CONFIG.OPTION['data dict scope paralist'] and
                    paraname in self._data_dict):
                    if CONFIG.OPTION['data dict scope style'] == 0:
                        temp_str = paraname + '(' + self._data_dict[paraname][0] + ')'
                    if CONFIG.OPTION['data dict scope style'] == 1:
                        temp_str = paraname + '(' + self._data_dict[paraname][0] + ')'
                    if CONFIG.OPTION['data dict scope style'] == 2:
                        temp_str = self._data_dict[paraname][0] + '(' + paraname + ')'
                    item_para.setText(temp_str)
                else:
                    item_para.setText(paraname)
                item_para.setData(Qt.UserRole, paraname)
    #        显示模板名
            self.line_edit_paras_template_name.setText(item.text())
    
#    删除模板    
    def slot_delete_templates(self):
        
        sel_items = self.list_para_templates.selectedItems()
        if len(sel_items):
            message = QMessageBox.warning(self,
                          QCoreApplication.translate('ParaTempWindow', '删除模板'),
                          QCoreApplication.translate('ParaTempWindow', '确定要删除所选模板吗'),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                for item in sel_items:
                    self.list_para_templates.takeItem(self.list_para_templates.row(item))
                    self.paras_temps.pop(item.text())
#                如果删除完模板后，还有模板就显示第一个模板的信息
                if self.paras_temps:
#                    self.list_para_templates.setCurrentRow(0)
                    self.slot_display_template(self.list_para_templates.currentItem())
                    self.current_temp = self.list_para_templates.currentItem()
                else:
                    self.line_edit_paras_template_name.clear()
                    self.list_parameters_for_ana.clear()
        
    def slot_change_temp_name(self):
        
        temp_name = self.line_edit_paras_template_name.text()
        if temp_name != self.current_temp.text():
            if temp_name in self.paras_temps:
                QMessageBox.information(self,
                                QCoreApplication.translate('ParaTempWindow', '模板名提示'),
                                QCoreApplication.translate('ParaTempWindow', '模板名已存在'))
                self.line_edit_paras_template_name.setText(self.current_temp.text())
                self.current_temp_change_status = False
            else:
                self.current_temp_change_status = True
        else:
            self.current_temp_change_status = False
            
    def slot_import_paras(self, paralist):
        
        if paralist:
            ex_paras = []
            for paraname in paralist:
                if self.list_parameters_for_ana.findItems(paraname, Qt.MatchExactly):
                    ex_paras.append(paraname)
                else:
                    item = QListWidgetItem(paraname, self.list_parameters_for_ana)
                    item.setIcon(self.paraicon)
                    if (self._data_dict and 
                        CONFIG.OPTION['data dict scope paralist'] and
                        paraname in self._data_dict):
                        if CONFIG.OPTION['data dict scope style'] == 0:
                            temp_str = self._data_dict[paraname][0]
                        if CONFIG.OPTION['data dict scope style'] == 1:
                            temp_str = paraname + '(' + self._data_dict[paraname][0] + ')'
                        if CONFIG.OPTION['data dict scope style'] == 2:
                            temp_str = self._data_dict[paraname][0] + '(' + paraname + ')'
                        item.setText(temp_str)
                    else:
                        item.setText(paraname)
                    item.setData(Qt.UserRole, paraname)
            if ex_paras:
                print_para = '<br>以下参数已存在：'
                for pa in ex_paras:
                    print_para += ('<br>' + pa)
                QMessageBox.information(self,
                        QCoreApplication.translate('ParaTempWindow', '导入参数提示'),
                        QCoreApplication.translate('ParaTempWindow', print_para))
            if len(ex_paras) != len(paralist):
                self.current_temp_change_status = True
            else:
                self.current_temp_change_status = False
                
    def slot_save_temp(self):
        
        self.current_temp_change_status = False
        target_temp = self.current_temp.text()
        result_tempname = self.line_edit_paras_template_name.text()
        count = self.list_parameters_for_ana.count()
        self.paras_temps.pop(target_temp)
        if count > 0:
            paras = []
            for i in range(count):
                paras.append(self.list_parameters_for_ana.item(i).data(Qt.UserRole))
            self.paras_temps[result_tempname] = paras
            self.current_temp.setText(result_tempname)
            QMessageBox.information(self,
                            QCoreApplication.translate('ParaTempWindow', '保存提示'),
                            QCoreApplication.translate('ParaTempWindow', '保存成功'))
        else:
            self.list_para_templates.takeItem(self.list_para_templates.row(self.current_temp))
            if self.is_creating:
                QMessageBox.information(self,
                                QCoreApplication.translate('ParaTempWindow', '保存提示'),
                                QCoreApplication.translate('ParaTempWindow', '未创建，因为没有参数'))
            else:
                QMessageBox.information(self,
                                QCoreApplication.translate('ParaTempWindow', '保存提示'),
                                QCoreApplication.translate('ParaTempWindow', '已删除模板中的所有参数，模板已删除'))
#            如果删除完模板后，还有模板就显示第一个模板的信息
            if self.paras_temps:
                self.list_para_templates.setCurrentItem(self.list_para_templates.currentItem())
                self.slot_display_template(self.list_para_templates.currentItem())
                self.current_temp = self.list_para_templates.currentItem()
            else:
                self.line_edit_paras_template_name.clear()
                self.list_parameters_for_ana.clear()
        if self.is_creating:
            self.is_creating = False
    
    def slot_cancel_save_temp(self):
        
        if self.is_creating:
            target_temp = self.current_temp.text()
            self.paras_temps.pop(target_temp)
            self.list_para_templates.takeItem(self.list_para_templates.row(self.current_temp))
#            如果删除完模板后，还有模板就显示第一个模板的信息
            if self.paras_temps:
#                self.list_para_templates.setCurrentRow(0)
                self.slot_display_template(self.list_para_templates.currentItem())
                self.current_temp = self.list_para_templates.currentItem()
            else:
                self.line_edit_paras_template_name.clear()
                self.list_parameters_for_ana.clear()
            self.is_creating = False
        else:
            self.slot_display_template(self.current_temp)
        self.current_temp_change_status = False
        
    def slot_create_temp(self):
        
        self.is_creating = True
        temp_name = 'untitled0'
        i = 1
        while temp_name in self.paras_temps:
            temp_name = 'untitled' + str(i)
            i += 1
        item = QListWidgetItem(temp_name, self.list_para_templates)
        item.setIcon(self.tempicon)
        self.paras_temps[temp_name] = []
        self.slot_display_template(item)
        self.current_temp_change_status = True
        
    def slot_import_temps(self):
        
        para_temps = {}
        if os.path.exists(self.dir_import):
            file_dir, unkown = QFileDialog.getOpenFileName(
                        self, 'Import templates', self.dir_import, 'Templates (*.txt *.csv)')
        else:
            file_dir, unkown = QFileDialog.getOpenFileName(
                        self, 'Import templates', CONFIG.SETUP_DIR, 'Templates (*.txt *.csv)')
        if file_dir:
            file_dir = file_dir.replace('/','\\')
            self.dir_import = os.path.dirname(file_dir)
            try:
                with open(file_dir, 'r') as file:
                    flag = file.readline()
                    if flag != '========\n':
                        raise IOError('Unsupported file!(FastPlot.)')
                    while flag == '========\n':
#                         readline函数会把'\n'也读进来
                         name = file.readline()
#                         去除'\n'
                         name = name.strip('\n')
#                         name = name.split()
                         str_paralist = file.readline()
                         str_paralist = str_paralist.strip('\n')
#                         split函数不加参数则默认使用空格
                         paralist = str_paralist.split()
                         para_temps[name] = paralist
                         flag = file.readline()
            except:
                QMessageBox.information(self,
                                        QCoreApplication.translate('ParaTempWindow', '模板提示'),
                                        QCoreApplication.translate('ParaTempWindow', 
                                                                   '''<p><b>文件内容格式不正确！</b></p>
                                                                   <p>请按下列格式输入：</p>
                                                                   <br>========
                                                                   <br>模板名
                                                                   <br>参数名+空格+参数名+空格+......
                                                                   <br>========
                                                                   <br>......
                                                                   <p>示例：</p>
                                                                   <br>========
                                                                   <br>角度
                                                                   <br>theta AOA FPA'''))
                 
            self.slot_add_para_template(para_temps)
            
    def slot_close(self):

        if self.current_temp_change_status:
            message = QMessageBox.warning(self,
                          QCoreApplication.translate('ParaTempWindow', '关闭提示'),
                          QCoreApplication.translate('ParaTempWindow', '模板：' + self.current_temp.text() + '未保存，是否保存后关闭？'),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                self.slot_save_temp()
            else:
                self.slot_cancel_save_temp()
        self.signal_close_pt_dock.emit()
        
    def slot_para_deled(self):
        
        self.current_temp_change_status = True
# =============================================================================
# 功能函数模块
# =============================================================================
#    从文件中加载参数模板进入内存
    def load_temps(self):
        
        try:
#            导入导出参数的模板
            with open(CONFIG.SETUP_DIR + r'\data\templates_export_paras.json', 'r') as file:
                self.paras_temps = json.load(file)
#                flag = file.readline()
#                while flag == '========\n':
##                     readline函数会把'\n'也读进来
#                     name = file.readline()
##                     去除'\n'
#                     name = name.strip('\n')
#                     str_paralist = file.readline()
#                     str_paralist = str_paralist.strip('\n')
#                     paralist = str_paralist.split()
#                     self.paras_temps[name] = paralist
#                     flag = file.readline()

#        读入数据字典，由于_data_dict这个变量需要比较的初始化，
#        所以采用直接读文件的形式，而不是等data_dict_window类把数据传过来再初始化
            with open(CONFIG.SETUP_DIR + r'\data\data_dicts\\' + CONFIG.OPTION['data dict version']) as f_obj:
                self._data_dict = json.load(f_obj)
        except:
            QMessageBox.information(self,
                            QCoreApplication.translate('ParaTempWindow', '模板提示'),
                            QCoreApplication.translate('ParaTempWindow', '加载模板失败！'))
        
        self.redisplay_para_templates()            
        
#    将内存中的模板导出到文件
    def output_temps(self):

        try:
#            打开保存模板的文件（将从头写入，覆盖之前的内容）
#            with open(CONFIG.SETUP_DIR + r'\data\templates_export_paras.txt', 'w') as file:
##                将内存中的模板一一写入文件
#                for temp in self.paras_temps:
#                    file.write('========\n')
#                    file.write(temp)
#                    file.write('\n')
#                    if self.paras_temps[temp]:
#                        paralist = ''
#                        index = 1
#                        length = len(self.paras_temps[temp])
#                        for para in self.paras_temps[temp]:
#                            if index == length:
#                                paralist += (para + '\n')
#                            else:
#                                paralist += (para + ' ')
#                            index += 1
#                        file.write(paralist)
#                    else:
#                        file.wirte(' \n')
            with open(CONFIG.SETUP_DIR + r'\data\templates_export_paras.json', 'w') as file:
                json.dump(self.paras_temps, file)
        except:
            QMessageBox.information(self,
                            QCoreApplication.translate('ParaTempWindow', '模板提示'),
                            QCoreApplication.translate('ParaTempWindow', '保存模板失败！'))
        
#    更新模板显示
    def redisplay_para_templates(self):

#        显示模板信息
        if self.paras_temps:
            self.list_para_templates.clear()
#            显示模板列表
            for name in self.paras_temps:
                QListWidgetItem(name, self.list_para_templates).setIcon(self.tempicon)
#            设置当前的模板为第一个模板并显示模板信息
            self.list_para_templates.setCurrentRow(0)
            item = self.list_para_templates.currentItem()
            self.slot_display_template(item)
# =============================================================================
# 汉化
# =============================================================================
    
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.group_box_templates.setTitle(_translate("DataManageWindow", "模板列表"))
        self.group_box_template_setting.setTitle(_translate("DataManageWindow", "模板信息"))
        self.label_para_template.setText(_translate("DataManageWindow", "模板名"))
        self.label_parameters.setText(_translate("DataManageWindow", "参数列表"))
        self.btn_save.setText(_translate("DataManageWindow", "保存"))
        self.btn_cancel.setText(_translate("DataManageWindow", "取消"))
        self.btn_close.setText(_translate("DataManageWindow", "关闭窗口"))