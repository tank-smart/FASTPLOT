# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 简述：数据分析类
#
# =======使用说明
# 
#
# =======日志
# 
# =============================================================================

# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtCore import (QSize, QCoreApplication, Qt, pyqtSignal,
                          QDataStream, QIODevice)
from PyQt5.QtGui import QIcon, QDragEnterEvent, QDropEvent, QFont
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, 
                             QSizePolicy, QMessageBox, QTreeWidget,
                             QTreeWidgetItem, QDialog, QToolButton, 
                             QHeaderView, QAbstractItemView)

# =============================================================================
# Package models imports
# =============================================================================
from views.custom_dialog import (SelectTemplateDialog, SaveTemplateDialog,
                                 ParameterExportDialog)
from models.datafile_model import Normal_DataFile
import views.config_info as CONFIG

# =============================================================================
# ParasListWithDropEvent
# =============================================================================
class ParasListWithDropEvent(QTreeWidget):

    signal_drop_paras = pyqtSignal(list)    
#    用于显示已选参数，因为需要增加
    def __init__(self, parent = None):
        super().__init__(parent)
#        接受拖放
        self.setAcceptDrops(True)
        
        self._data_dict = None

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
                file_dir = item_stream.readQString()
                sorted_paras.append((paraname, file_dir))
            self.signal_drop_paras.emit(sorted_paras)
            event.acceptProposedAction()
        else:
            event.ignore()

class DataProcessWindow(QWidget):
    
    signal_para_for_plot = pyqtSignal(tuple)
    signal_request_temps = pyqtSignal(str)
    signal_save_temp = pyqtSignal(dict)
    signal_send_status = pyqtSignal(str, int)
    signal_close_dock = pyqtSignal()
# =============================================================================
# 初始化    
# =============================================================================    
    def __init__(self, parent = None):
        
        super().__init__(parent)

#        计算产生的数据
        self.dict_data = {}
        self.count_imported_data = 0
        
        self.paraicon = QIcon(CONFIG.ICON_PARA)
        self.math_icon = QIcon(CONFIG.ICON_MATH_RESULT)

# =============================================================================
# UI模块
# =============================================================================        
    def setup(self):

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.verticalLayout_9 = QVBoxLayout(self)
        self.verticalLayout_9.setContentsMargins(2, 0, 2, 0)
        self.verticalLayout_9.setSpacing(2)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(1)
        self.tool_btn_sel_temp = QToolButton(self)
        self.tool_btn_sel_temp.setMinimumSize(QSize(30, 30))
        self.tool_btn_sel_temp.setMaximumSize(QSize(30, 30))
        self.tool_btn_sel_temp.setIconSize(QSize(22, 22))
        self.tool_btn_sel_temp.setIcon(QIcon(CONFIG.ICON_SEL_TEMP))
        self.horizontalLayout_2.addWidget(self.tool_btn_sel_temp)
        self.tool_btn_save_temp = QToolButton(self)
        self.tool_btn_save_temp.setMinimumSize(QSize(30, 30))
        self.tool_btn_save_temp.setMaximumSize(QSize(30, 30))
        self.tool_btn_save_temp.setIconSize(QSize(22, 22))
        self.tool_btn_save_temp.setIcon(QIcon(CONFIG.ICON_SAVE_TEMP))
        self.horizontalLayout_2.addWidget(self.tool_btn_save_temp)
        self.tool_btn_plot = QToolButton(self)
        self.tool_btn_plot.setMinimumSize(QSize(30, 30))
        self.tool_btn_plot.setMaximumSize(QSize(30, 30))
        self.tool_btn_plot.setIconSize(QSize(22, 22))
        self.tool_btn_plot.setIcon(QIcon(CONFIG.ICON_PLOT))
        self.horizontalLayout_2.addWidget(self.tool_btn_plot)
        self.tool_btn_data_abstract = QToolButton(self)
        self.tool_btn_data_abstract.setMinimumSize(QSize(30, 30))
        self.tool_btn_data_abstract.setMaximumSize(QSize(30, 30))
        self.tool_btn_data_abstract.setIconSize(QSize(22, 22))
        self.tool_btn_data_abstract.setIcon(QIcon(CONFIG.ICON_DATA_ABSTRACT))
        self.horizontalLayout_2.addWidget(self.tool_btn_data_abstract)
        self.tool_btn_up = QToolButton(self)
        self.tool_btn_up.setMinimumSize(QSize(30, 30))
        self.tool_btn_up.setMaximumSize(QSize(30, 30))
        self.tool_btn_up.setIconSize(QSize(22, 22))
        self.tool_btn_up.setIcon(QIcon(CONFIG.ICON_UP))
        self.horizontalLayout_2.addWidget(self.tool_btn_up)
        self.tool_btn_down = QToolButton(self)
        self.tool_btn_down.setMinimumSize(QSize(30, 30))
        self.tool_btn_down.setMaximumSize(QSize(30, 30))
        self.tool_btn_down.setIconSize(QSize(22, 22))
        self.tool_btn_down.setIcon(QIcon(CONFIG.ICON_DOWN))
        self.horizontalLayout_2.addWidget(self.tool_btn_down)
        self.tool_btn_delete = QToolButton(self)
        self.tool_btn_delete.setMinimumSize(QSize(30, 30))
        self.tool_btn_delete.setMaximumSize(QSize(30, 30))
        self.tool_btn_delete.setIconSize(QSize(22, 22))
        self.tool_btn_delete.setIcon(QIcon(CONFIG.ICON_DEL))
        self.horizontalLayout_2.addWidget(self.tool_btn_delete)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_9.addLayout(self.horizontalLayout_2)
        self.tree_widget_paralist = ParasListWithDropEvent(self)
#        让顶级项没有扩展符空白
        self.tree_widget_paralist.setRootIsDecorated(False)
#        设置树组件头部显示方式
        headerview = self.tree_widget_paralist.header()
        headerview.setSectionResizeMode(QHeaderView.ResizeToContents)
        headerview.setMinimumSectionSize(100)
        self.tree_widget_paralist.setHeader(headerview)
        
        self.tree_widget_paralist.setSelectionMode(
                QAbstractItemView.ExtendedSelection)
        
        self.verticalLayout_9.addWidget(self.tree_widget_paralist)

        self.retranslateUi()
        
# =======连接信号与槽
# =============================================================================        
        self.tool_btn_save_temp.clicked.connect(self.slot_save_temp)
        self.tool_btn_sel_temp.clicked.connect(self.slot_emit_request_temps)
        self.tool_btn_plot.clicked.connect(self.slot_plot)
        self.tool_btn_data_abstract.clicked.connect(self.slot_data_abstract)
        self.tool_btn_up.clicked.connect(self.slot_up_para)
        self.tool_btn_down.clicked.connect(self.slot_down_para)
        self.tool_btn_delete.clicked.connect(self.slot_delete_paras)
        self.tree_widget_paralist.signal_drop_paras.connect(self.slot_import_paras)
        
# =============================================================================
# slots模块
# =============================================================================
#    这个函数应该只关注参数的排列顺序，不读取数据
    def slot_import_paras(self, sorted_paras):
        
        if sorted_paras:
            ex_paras = []
            norfile_list = {}

            for para_info in sorted_paras:
                paraname, file_dir = para_info
#                判断导入的参数是否已存在
                if self.is_in_sel_paras(paraname, file_dir):
                    ex_paras.append(paraname)
                else:
#                    避免重复创建文件对象
                    if not (file_dir in norfile_list):
                        norfile_list[file_dir] = Normal_DataFile(file_dir)
                    file = norfile_list[file_dir]
                    filename = file.filename
                    item_para = QTreeWidgetItem(self.tree_widget_paralist)
                    item_para.setIcon(0, self.paraicon)
                    if (self._data_dict and 
                        CONFIG.OPTION['data dict scope paralist'] and
                        paraname in self._data_dict):
                        if CONFIG.OPTION['data dict scope style'] == 0:
                            temp_str = self._data_dict[paraname][0]
                        if CONFIG.OPTION['data dict scope style'] == 1:
                            temp_str = paraname + '(' + self._data_dict[paraname][0] + ')'
                        if CONFIG.OPTION['data dict scope style'] == 2:
                            temp_str = self._data_dict[paraname][0] + '(' + paraname + ')'
                        item_para.setText(0, temp_str)
                    else:
                        item_para.setText(0, paraname)
                    item_para.setData(0, Qt.UserRole, paraname)
                    item_para.setText(1, filename)
                    item_para.setData(1, Qt.UserRole, file_dir)
                    item_para.setText(2, file.time_range[0])
                    item_para.setText(3, file.time_range[1])
                    item_para.setText(4, str(file.sample_frequency))

            if ex_paras:
                print_para = '以下参数已存在：'
                for pa in ex_paras:
                    print_para += ('<br>' + pa)
                ms_box = QMessageBox(QMessageBox.Information,
                                     QCoreApplication.translate('DataAnalysisWindow', '导入参数提示'),
                                     QCoreApplication.translate('DataAnalysisWindow', print_para),
                                     QMessageBox.Ok,
                                     self)
                ms_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
                ms_box.exec_()
#                QMessageBox.information(self,
#                        QCoreApplication.translate('DataAnalysisWindow', '导入参数提示'),
#                        QCoreApplication.translate('DataAnalysisWindow',
#                                                   print_para))
    
    def slot_import_datafactory(self, dict_data_factory):
        
#        不管来源是否一致，都认为是第一次导入
        for name in dict_data_factory:
            data_label = '_DataFactory' + str(self.count_imported_data + 1)
            self.dict_data[data_label] = dict_data_factory[name]
            self.count_imported_data += 1
            data_factory = dict_data_factory[name]
            paralist = data_factory.get_paralist()
            for paraname in paralist:
                item_para = QTreeWidgetItem(self.tree_widget_paralist)
                item_para.setIcon(0, self.math_icon)
                if (self._data_dict and 
                    CONFIG.OPTION['data dict scope paralist'] and
                    paraname in self._data_dict):
                    if CONFIG.OPTION['data dict scope style'] == 0:
                        temp_str = self._data_dict[paraname][0]
                    if CONFIG.OPTION['data dict scope style'] == 1:
                        temp_str = paraname + '(' + self._data_dict[paraname][0] + ')'
                    if CONFIG.OPTION['data dict scope style'] == 2:
                        temp_str = self._data_dict[paraname][0] + '(' + paraname + ')'
                    item_para.setText(0, temp_str)
                else:
                    item_para.setText(0, paraname)
                item_para.setData(0, Qt.UserRole, paraname)
                item_para.setText(1, 'Data in memory')
                item_para.setData(1, Qt.UserRole, data_label)
                item_para.setText(2, data_factory.time_range[0])
                item_para.setText(3, data_factory.time_range[1])
                item_para.setText(4, str(data_factory.sample_frequency))
                

    def slot_emit_request_temps(self):
        
        self.signal_request_temps.emit('para_template')

#    选择参数导出模板
    def slot_sel_temp(self, dict_files, templates):

        if templates:
            input_paras = []
            paras_noexist = []
            isexist = False
            dialog = SelectTemplateDialog(self, templates)
            return_signal = dialog.exec_()
            if (return_signal == QDialog.Accepted):
                if dict_files:
        #            遍历文件，搜索是否存在模板中的参数
        #            不同文件下的同一参数都会找出（这样耗时较长）
        #            也可以找到第一个就停止
                    for paraname in templates[dialog.sel_temp]:
                        isexist = False
                        for file_dir in dict_files:
                            if paraname in dict_files[file_dir]:
                                isexist = True
                                input_paras.append((paraname, file_dir))
        #                        加入以下语句实现找到第一个就停止的功能
        #                        break
                        if not isexist:
                            paras_noexist.append(paraname)
                    if paras_noexist:
                        print_para = '以下参数未找到：'
                        for pa in paras_noexist:
                            print_para += ('<br>' + pa)
                        ms_box = QMessageBox(QMessageBox.Information,
                                             QCoreApplication.translate('DataAnalysisWindow', '导入参数提示'),
                                             QCoreApplication.translate('DataAnalysisWindow', print_para),
                                             QMessageBox.Ok,
                                             self)
                        ms_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
                        ms_box.exec_()
#                        QMessageBox.information(self,
#                                                QCoreApplication.translate('DataAnalysisWindow', '导入模板提示'),
#                                                QCoreApplication.translate('DataAnalysisWindow',
#                                                                           print_para))
                    self.slot_import_paras(input_paras)
                else:
                    QMessageBox.information(self,
                            QCoreApplication.translate('DataAnalysisWindow', '导入模板错误'),
                            QCoreApplication.translate('DataAnalysisWindow', '没有发现数据文件'))
        else:
            QMessageBox.information(self,
                    QCoreApplication.translate('DataAnalysisWindow', '导入模板错误'),
                    QCoreApplication.translate('DataAnalysisWindow', '    没有模板    '))            

#    保存参数导出模板
    def slot_save_temp(self):
        
        count = self.tree_widget_paralist.topLevelItemCount()
        if count:
            temp = {}
            dialog = SaveTemplateDialog(self)
            return_signal = dialog.exec_()
            if (return_signal == QDialog.Accepted):
                temp_name = dialog.temp_name
                if temp_name:
                    temp[temp_name] = []
                    for i in range(count):
                        paraname = self.tree_widget_paralist.topLevelItem(i).data(0, Qt.UserRole)
                        if not(paraname in temp[temp_name]):
                            temp[temp_name].append(paraname)
                    self.signal_save_temp.emit(temp)
#                    这个弹窗应该放在data_manage_window中的，因为在那里才是保存模板的最后一步
                    QMessageBox.information(self,
                            QCoreApplication.translate('DataAnalysisWindow', '保存提示'),
                            QCoreApplication.translate('DataAnalysisWindow', '保存成功'))
                else:
                    QMessageBox.information(self,
                            QCoreApplication.translate('DataAnalysisWindow', '输入提示'),
                            QCoreApplication.translate('DataAnalysisWindow', '未输入模板名'))
        else:
            QMessageBox.information(self,
                    QCoreApplication.translate('DataAnalysisWindow', '保存提示'),
                    QCoreApplication.translate('DataAnalysisWindow', '没有发现参数'))
            
    def slot_plot(self):
        
        if self.tree_widget_paralist:
            self.signal_close_dock.emit()
            items = self.tree_widget_paralist.selectedItems()
            if items:
                self.signal_para_for_plot.emit(self.get_sel_paras_in_tuple())
            else:
                count = self.tree_widget_paralist.topLevelItemCount()
#                设置限制，超过40个参数则认为参数太多，不宜绘图
                if count > 40:
                    QMessageBox.information(self,
                            QCoreApplication.translate('DataAnalysisWindow', '绘图提示'),
                            QCoreApplication.translate('DataAnalysisWindow', '''<p>要绘制的参数已大于40个，
                                                                                <p>参数过多，不予绘制！若真要绘制，请全选中后绘制！'''))
                else:
                    self.signal_para_for_plot.emit(self.get_paras_in_tuple())
        
    def slot_data_abstract(self):
        
        para_tuple = self.get_paras_in_tuple()
        dict_paras, sorted_paras = para_tuple
        if dict_paras :
            dialog = ParameterExportDialog(self, dict_paras)
            dialog.signal_send_status.connect(self.slot_send_status)
            return_signal = dialog.exec_()
            if return_signal == QDialog.Accepted:
                QMessageBox.information(self,
                        QCoreApplication.translate('DataAnalysisWindow', '保存提示'),
                        QCoreApplication.translate('DataAnalysisWindow', '保存成功！'))
                
    def slot_send_status(self, message : str, timeout : int):
        
        self.signal_send_status.emit(message, timeout)
                
    def slot_up_para(self):
        
        if self.tree_widget_paralist:
            loc = self.tree_widget_paralist.indexOfTopLevelItem(
                    self.tree_widget_paralist.currentItem())
            item = self.tree_widget_paralist.takeTopLevelItem(loc)
            if loc == 0:
                self.tree_widget_paralist.insertTopLevelItem(0, item)
                self.tree_widget_paralist.setCurrentItem(item)
            else:
                self.tree_widget_paralist.insertTopLevelItem(loc - 1, item)
                self.tree_widget_paralist.setCurrentItem(item)
    
    def slot_down_para(self):

        if self.tree_widget_paralist:
            count = self.tree_widget_paralist.topLevelItemCount()
            loc = self.tree_widget_paralist.indexOfTopLevelItem(
                    self.tree_widget_paralist.currentItem())
            item = self.tree_widget_paralist.takeTopLevelItem(loc)
            if loc == count - 1:
                self.tree_widget_paralist.insertTopLevelItem(count - 1, item)
                self.tree_widget_paralist.setCurrentItem(item)
            else:
                self.tree_widget_paralist.insertTopLevelItem(loc + 1, item)
                self.tree_widget_paralist.setCurrentItem(item)
                
    def slot_delete_paras(self):
        
        sel_items = self.tree_widget_paralist.selectedItems()
        if len(sel_items):
            message = QMessageBox.warning(self,
                          QCoreApplication.translate('DataAnalysisWindow', '删除参数'),
                          QCoreApplication.translate('DataAnalysisWindow', '确定要删除所选参数吗'),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                for item in sel_items:
                    self.tree_widget_paralist.takeTopLevelItem(
                            self.tree_widget_paralist.indexOfTopLevelItem(item))
# =============================================================================
# 功能函数模块   
# =============================================================================
#    只要参数名一致就认为在这个参数列表中，不区分是否是在不同文件
    def is_in_sel_paras(self, para, file_dir):

        count = self.tree_widget_paralist.topLevelItemCount()
        for i in range(count):
            item = self.tree_widget_paralist.topLevelItem(i)
            paraname = item.data(0, Qt.UserRole)
            fd = item.data(1, Qt.UserRole)
            if para == paraname and fd == file_dir:
                return True
        return False
    
    def get_paras_in_tuple(self):
        
        result = {}
        sorted_paras = []
        dict_df = {}
        if self.tree_widget_paralist:
            count = self.tree_widget_paralist.topLevelItemCount()
            for i in range(count):
                item = self.tree_widget_paralist.topLevelItem(i)
                sorted_paras.append((item.data(0, Qt.UserRole), item.data(1, Qt.UserRole)))
                file_dir = item.data(1, Qt.UserRole)
                if file_dir[0] == '_':
                    if file_dir in dict_df:
                        dict_df[file_dir].append(item.data(0, Qt.UserRole))
                    else:
                        dict_df[file_dir] = []
                        dict_df[file_dir].append(item.data(0, Qt.UserRole))
                else:
                    if file_dir in result:
                        result[file_dir].append(item.data(0, Qt.UserRole))
                    else:
                        result[file_dir] = []
                        result[file_dir].append(item.data(0, Qt.UserRole))
            for name in dict_df:
                result[name] = self.dict_data[name].get_sub_data(dict_df[name])
        return (result, sorted_paras)
    
    def get_sel_paras_in_tuple(self):
        
        result = {}
        sorted_paras = []
        dict_df = {}
        items = self.tree_widget_paralist.selectedItems()
        if items:
            for item in items:
                sorted_paras.append((item.data(0, Qt.UserRole), item.data(1, Qt.UserRole)))
                file_dir = item.data(1, Qt.UserRole)
                if file_dir[0] == '_':
                    if file_dir in dict_df:
                        dict_df[file_dir].append(item.data(0, Qt.UserRole))
                    else:
                        dict_df[file_dir] = []
                        dict_df[file_dir].append(item.data(0, Qt.UserRole))
                else:
                    if file_dir in result:
                        result[file_dir].append(item.data(0, Qt.UserRole))
                    else:
                        result[file_dir] = []
                        result[file_dir].append(item.data(0, Qt.UserRole))
            for name in dict_df:
                result[name] = self.dict_data[name].get_sub_data(dict_df[name])
        return (result, sorted_paras)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.tool_btn_save_temp.setToolTip(_translate('DataAnalysisWindow', '保存为模板'))
        self.tool_btn_sel_temp.setToolTip(_translate('DataAnalysisWindow', '选择模板'))
        self.tool_btn_plot.setToolTip(_translate('DataAnalysisWindow', '绘图'))
        self.tool_btn_data_abstract.setToolTip(_translate('DataAnalysisWindow', '数据导出'))
        self.tool_btn_up.setToolTip(_translate('DataAnalysisWindow', '上移参数'))
        self.tool_btn_down.setToolTip(_translate('DataAnalysisWindow', '下移参数'))
        self.tool_btn_delete.setToolTip(_translate('DataAnalysisWindow', '删除参数'))
        self.tree_widget_paralist.headerItem().setText(0, _translate('DataAnalysisWindow', '参数名'))
        self.tree_widget_paralist.headerItem().setText(1, _translate('DataAnalysisWindow', '所属文件'))
        self.tree_widget_paralist.headerItem().setText(2, _translate('DataAnalysisWindow', '起始时间'))
        self.tree_widget_paralist.headerItem().setText(3, _translate('DataAnalysisWindow', '终止时间'))
        self.tree_widget_paralist.headerItem().setText(4, _translate('DataAnalysisWindow', '采样频率'))
