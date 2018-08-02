# -*- coding: utf-8 -*-

# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtCore import (QSize, QCoreApplication, Qt, pyqtSignal,
                          QDataStream, QIODevice, QMimeData, QByteArray)
from PyQt5.QtGui import QIcon, QDropEvent, QDragEnterEvent
from PyQt5.QtWidgets import (QDockWidget, QVBoxLayout, QHBoxLayout, QSpacerItem,
                             QSizePolicy,QMessageBox, QListWidget, QWidget,
                             QListWidgetItem, QToolButton, QAbstractItemView,
                             QDialog)

# =============================================================================
# Package models imports
# =============================================================================
import views.constant as CONSTANT
from views.custom_dialog import SelectTemplateDialog, SaveTemplateDialog

# =============================================================================
# SelectedParasTree
# =============================================================================
class ParasListWithDropEvent(QListWidget):

    signal_drop_paras = pyqtSignal(list)    
#    用于显示已选参数，因为需要增加
    def __init__(self, parent = None):
        super().__init__(parent)
#        接受拖放
        self.setAcceptDrops(True)

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

class AnalysisParasWindow(QDockWidget):

    signal_para_for_plot = pyqtSignal(tuple)
    signal_request_temps = pyqtSignal(str)
    signal_save_temp = pyqtSignal(dict)

# =============================================================================
# 初始化    
# =============================================================================     
    def __init__(self, parent = None):
        
        super().__init__(parent)
        self.paraicon = QIcon(CONSTANT.ICON_PARA)

# =============================================================================
# UI模块        
# =============================================================================        
    def setup(self):

        self.dock_widget_contents = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.dock_widget_contents)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(2)
        
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        
        self.tool_btn_sel_temp = QToolButton(self)
        self.tool_btn_sel_temp.setMinimumSize(QSize(28, 28))
        self.tool_btn_sel_temp.setMaximumSize(QSize(28, 28))
        self.tool_btn_sel_temp.setIcon(QIcon(CONSTANT.ICON_SEL_TEMP))
        self.horizontalLayout.addWidget(self.tool_btn_sel_temp)
        self.tool_btn_save_temp = QToolButton(self)
        self.tool_btn_save_temp.setMinimumSize(QSize(28, 28))
        self.tool_btn_save_temp.setMaximumSize(QSize(28, 28))
        self.tool_btn_save_temp.setIcon(QIcon(CONSTANT.ICON_SAVE_TEMP))
        self.horizontalLayout.addWidget(self.tool_btn_save_temp)
        
        self.tool_btn_plot = QToolButton(self)
        self.tool_btn_plot.setMinimumSize(QSize(28, 28))
        self.tool_btn_plot.setMaximumSize(QSize(28, 28))
        self.tool_btn_plot.setIcon(QIcon(CONSTANT.ICON_PLOT_PARAS))
        self.horizontalLayout.addWidget(self.tool_btn_plot)
        self.tool_btn_data_abstract = QToolButton(self)
        self.tool_btn_data_abstract.setMinimumSize(QSize(28, 28))
        self.tool_btn_data_abstract.setMaximumSize(QSize(28, 28))
        self.tool_btn_data_abstract.setIcon(QIcon(CONSTANT.ICON_DATA_ABSTRACT))
        self.horizontalLayout.addWidget(self.tool_btn_data_abstract)
        
        self.tool_btn_up = QToolButton(self.dock_widget_contents)
        self.tool_btn_up.setIcon(QIcon(CONSTANT.ICON_UP))
        self.tool_btn_up.setMinimumSize(QSize(28, 28))
        self.tool_btn_up.setMaximumSize(QSize(28, 28))
        self.horizontalLayout.addWidget(self.tool_btn_up)
        self.tool_btn_down = QToolButton(self.dock_widget_contents)
        self.tool_btn_down.setIcon(QIcon(CONSTANT.ICON_DOWN))
        self.tool_btn_down.setMinimumSize(QSize(28, 28))
        self.tool_btn_down.setMaximumSize(QSize(28, 28))
        self.horizontalLayout.addWidget(self.tool_btn_down)
        self.tool_btn_delete = QToolButton(self.dock_widget_contents)
        self.tool_btn_delete.setIcon(QIcon(CONSTANT.ICON_DEL))
        self.tool_btn_delete.setMinimumSize(QSize(28, 28))
        self.tool_btn_delete.setMaximumSize(QSize(28, 28))
        self.horizontalLayout.addWidget(self.tool_btn_delete)
        spacerItem = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        self.list_paras = ParasListWithDropEvent(self.dock_widget_contents)
        self.list_paras.setSelectionMode(
                QAbstractItemView.ExtendedSelection)
        self.verticalLayout.addWidget(self.list_paras)
        self.setWidget(self.dock_widget_contents)

        self.retranslateUi()
        
        self.tool_btn_save_temp.clicked.connect(self.slot_save_temp)
        self.tool_btn_sel_temp.clicked.connect(self.slot_emit_request_temps)
        self.tool_btn_plot.clicked.connect(self.slot_plot)
        self.tool_btn_data_abstract.clicked.connect(self.slot_data_abstract)
        self.tool_btn_up.clicked.connect(self.slot_up_para)
        self.tool_btn_down.clicked.connect(self.slot_down_para)
        self.tool_btn_delete.clicked.connect(self.slot_delete_paras)
        self.list_paras.signal_drop_paras.connect(self.slot_import_paras)

# =============================================================================
# slots模块
# =============================================================================
#    这个函数应该只关注参数的排列顺序，不读取数据
    def slot_import_paras(self, sorted_paras):
        
        if sorted_paras:
            ex_paras = []

            for para_info in sorted_paras:
                paraname, file_dir = para_info

#                判断导入的参数是否已存在
                if self.is_in_sel_paras(paraname):
                    ex_paras.append(paraname)
                else:
                    item_para = QListWidgetItem(paraname, self.list_paras)
                    item_para.setIcon(self.paraicon)
                    item_para.setData(Qt.UserRole, file_dir)

            if ex_paras:
                print_para = '<br>以下参数已存在：'
                for pa in ex_paras:
                    print_para += ('<br>' + pa)
                QMessageBox.information(self,
                        QCoreApplication.translate('DataExportWindow', '导入参数提示'),
                        QCoreApplication.translate('DataExportWindow',
                                                   print_para))

    def slot_emit_request_temps(self):
        
        self.signal_request_temps.emit('para_template')

#    选择参数导出模板
    def slot_sel_temp(self, dict_files, templates):

        if templates:
            imput_paras = []
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
                                imput_paras.append((paraname, file_dir))
        #                        加入以下语句实现找到第一个就停止的功能
        #                        break
                        if not isexist:
                            paras_noexist.append(paraname)
                    if paras_noexist:
                        print_para = '<br>以下参数未找到：'
                        for pa in paras_noexist:
                            print_para += ('<br>' + pa)
                        QMessageBox.information(self,
                                                QCoreApplication.translate('DataExportWindow', '导入模板提示'),
                                                QCoreApplication.translate('DataExportWindow',
                                                                           print_para))
                    self.slot_import_paras(imput_paras)
                else:
                    QMessageBox.information(self,
                            QCoreApplication.translate('DataExportWindow', '导入模板错误'),
                            QCoreApplication.translate('DataExportWindow', '没有发现数据文件'))
        else:
            QMessageBox.information(self,
                    QCoreApplication.translate('DataExportWindow', '导入模板错误'),
                    QCoreApplication.translate('DataExportWindow', '没有模板'))            

#    保存参数导出模板
    def slot_save_temp(self):
        
        count = self.list_paras.count()
        if count:
            temp = {}
            dialog = SaveTemplateDialog(self)
            return_signal = dialog.exec_()
            if (return_signal == QDialog.Accepted):
                temp_name = dialog.temp_name
                if temp_name:
                    temp[temp_name] = []
                    for i in range(count):
                        temp[temp_name].append(self.list_paras.item(i).text())
                    self.signal_save_temp.emit(temp)
                else:
                    QMessageBox.information(self,
                            QCoreApplication.translate('DataExportWindow', '输入提示'),
                            QCoreApplication.translate('DataExportWindow', '未输入模板名'))
        else:
            QMessageBox.information(self,
                    QCoreApplication.translate('DataExportWindow', '保存错误'),
                    QCoreApplication.translate('DataExportWindow', '没有发现参数'))
            
    def slot_plot(self):
        
        self.signal_para_for_plot.emit(self.get_paras_in_tuple())
        
    def slot_data_abstract(self):
        
        pass
                
    def slot_up_para(self):
        
        if self.list_paras:
            loc = self.list_paras.currentRow()
            item = self.list_paras.takeItem(loc)
            if loc == 0:
                self.list_paras.insertItem(0, item)
                self.list_paras.setCurrentItem(item)
            else:
                self.list_paras.insertItem(loc - 1, item)
                self.list_paras.setCurrentItem(item)
    
    def slot_down_para(self):

        if self.list_paras:
            count = self.list_paras.count()
            loc = self.list_paras.currentRow()
            item = self.list_paras.takeItem(loc)
            if loc == count:
                self.list_paras.insertItem(count, item)
                self.list_paras.setCurrentItem(item)
            else:
                self.list_paras.insertItem(loc + 1, item)
                self.list_paras.setCurrentItem(item)
                
    def slot_delete_paras(self):
        
        sel_items = self.list_paras.selectedItems()
        if len(sel_items):
            message = QMessageBox.warning(self,
                          QCoreApplication.translate('DataExportWindow', '删除参数'),
                          QCoreApplication.translate('DataExportWindow', '确定要删除这些参数吗'),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                for item in sel_items:
                    self.list_paras.takeItem(self.list_paras.row(item))

# =============================================================================
# 功能函数模块
# =============================================================================
#    只要参数名一致就认为在这个参数列表中，不区分是否是在不同文件
    def is_in_sel_paras(self, para):

        count = self.list_paras.count()
        for i in range(count):
            item = self.list_paras.item(i)
            paraname = item.text()
            if para == paraname:
                return True
        return False
    
    def get_paras_in_tuple(self):
        
        result = {}
        sorted_paras = []
        if self.list_paras:
            count = self.list_paras.count()
            for i in range(count):
                item = self.list_paras.item(i)
                sorted_paras.append(item.text())
                file_dir = item.data(Qt.UserRole)
                if file_dir in result:
                    result[file_dir].append(item.text())
                else:
                    result[file_dir] = []
                    result[file_dir].append(item.text())
        return (result, sorted_paras)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('ParasListWithDropEvent', '分析参数'))
        self.tool_btn_save_temp.setToolTip(_translate('ParasListWithDropEvent', '保存为模板'))
        self.tool_btn_sel_temp.setToolTip(_translate('ParasListWithDropEvent', '选择模板'))
        self.tool_btn_plot.setToolTip(_translate('ParasListWithDropEvent', '绘图'))
        self.tool_btn_data_abstract.setToolTip(_translate('ParasListWithDropEvent', '数据提取'))
        self.tool_btn_up.setToolTip(_translate('ParasListWithDropEvent', '上移参数'))
        self.tool_btn_down.setToolTip(_translate('ParasListWithDropEvent', '下移参数'))
        self.tool_btn_delete.setToolTip(_translate('ParasListWithDropEvent', '删除参数'))