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
from PyQt5.QtCore import (QSize, QCoreApplication, Qt, QObject, pyqtSignal,
                          QDataStream, QIODevice)
from PyQt5.QtGui import QIcon, QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QComboBox, QSpacerItem, QSizePolicy, QFrame,
                             QTabWidget, QStackedWidget, QPushButton,
                             QGroupBox, QPlainTextEdit, QMessageBox, 
                             QTreeWidget, QTreeWidgetItem, QDialog, 
                             QDialogButtonBox, QMenu, QAction, QLineEdit,
                             QToolButton, QHeaderView, QAbstractItemView)

# =============================================================================
# Package models imports
# =============================================================================
from views.custom_dialog import SelParasDialog
from views.custom_dialog import (SelectTemplateDialog, SaveTemplateDialog,
                                 ParameterExportDialog)
from models.datafile_model import Normal_DataFile
import views.constant as CONSTANT

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

class SiftResultViewWidget(QWidget):

    def __init__(self, parent = None, expr = ''):
        
        super().__init__(parent)
        
        self.expr = expr
        self.setup()
        
    def setup(self):

        self.verticalLayout_8 = QVBoxLayout(self)
        self.verticalLayout_8.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_8.setSpacing(2)
        self.group_box_view_expression = QGroupBox(self)
        self.verticalLayout_6 = QVBoxLayout(self.group_box_view_expression)
        self.verticalLayout_6.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_6.setSpacing(2)
        self.plain_text_edit_view_expression = QPlainTextEdit(self.group_box_view_expression)
        self.plain_text_edit_view_expression.setEnabled(False)
        self.plain_text_edit_view_expression.setPlainText(self.expr)
        self.verticalLayout_6.addWidget(self.plain_text_edit_view_expression)
        self.verticalLayout_8.addWidget(self.group_box_view_expression)
        self.group_box_sift_result = QGroupBox(self)
        self.verticalLayout_7 = QVBoxLayout(self.group_box_sift_result)
        self.verticalLayout_7.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_7.setSpacing(2)
        self.tree_widget_sift_result = QTreeWidget(self.group_box_sift_result)
        self.verticalLayout_7.addWidget(self.tree_widget_sift_result)
        self.verticalLayout_8.addWidget(self.group_box_sift_result)
        self.verticalLayout_8.setStretch(0, 2)
        self.verticalLayout_8.setStretch(1, 5)
        
        self.retranslateUi()
        
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.group_box_view_expression.setTitle(_translate('DataAnalysisWindow', '条件表达式'))
        self.group_box_sift_result.setTitle(_translate('DataAnalysisWindow', '结果'))
        self.tree_widget_sift_result.headerItem().setText(0, _translate('DataAnalysisWindow', '文件对象'))
        self.tree_widget_sift_result.headerItem().setText(1, _translate('DataAnalysisWindow', '状态'))
        self.tree_widget_sift_result.headerItem().setText(2, _translate('DataAnalysisWindow', '捕捉点'))
        self.tree_widget_sift_result.headerItem().setText(3, _translate('DataAnalysisWindow', '持续时间'))

class DataAnalysisWindow(QWidget):
    
    signal_para_for_plot = pyqtSignal(tuple)
    signal_request_temps = pyqtSignal(str)
    signal_save_temp = pyqtSignal(dict)
# =============================================================================
# 初始化    
# =============================================================================    
    def __init__(self, parent = None):
        
        super().__init__(parent)

#        不允许改动这个变量，因为该变量连接着主窗口的变量
        self._current_files = []
        
        self.tab_result_count = 0
#        设置文件与参数的图标
        self.paraicon = QIcon(CONSTANT.ICON_PARA)
        self.curve_icon = QIcon(CONSTANT.ICON_CURVE)
        self.time_icon = QIcon(CONSTANT.ICON_TIME)

# =============================================================================
# UI模块
# =============================================================================        
    def setup(self):
        
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(2, 0, 2, 0)
        self.verticalLayout.setSpacing(2)
        self.horizontalLayout = QHBoxLayout()
        self.label_analysis_type = QLabel(self)
        self.label_analysis_type.setMinimumSize(QSize(100, 24))
        self.label_analysis_type.setMaximumSize(QSize(100, 24))
        self.horizontalLayout.addWidget(self.label_analysis_type)
        self.combo_box_analysis_type = QComboBox(self)
        self.combo_box_analysis_type.setMinimumSize(QSize(120, 24))
        self.combo_box_analysis_type.setMaximumSize(QSize(120, 24))
        self.combo_box_analysis_type.addItem('')
        self.combo_box_analysis_type.addItem('')
        self.horizontalLayout.addWidget(self.combo_box_analysis_type)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)
        self.stackedWidget = QStackedWidget(self)
        
        self.page_data_process = QWidget()
        self.verticalLayout_10 = QVBoxLayout(self.page_data_process)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setSpacing(2)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.tool_btn_sel_temp = QToolButton(self.page_data_process)
        self.tool_btn_sel_temp.setMinimumSize(QSize(28, 28))
        self.tool_btn_sel_temp.setMaximumSize(QSize(28, 28))
        self.tool_btn_sel_temp.setIcon(QIcon(CONSTANT.ICON_SEL_TEMP))
        self.horizontalLayout_2.addWidget(self.tool_btn_sel_temp)
        self.tool_btn_save_temp = QToolButton(self.page_data_process)
        self.tool_btn_save_temp.setMinimumSize(QSize(28, 28))
        self.tool_btn_save_temp.setMaximumSize(QSize(28, 28))
        self.tool_btn_save_temp.setIcon(QIcon(CONSTANT.ICON_SAVE_TEMP))
        self.horizontalLayout_2.addWidget(self.tool_btn_save_temp)
        self.tool_btn_plot = QToolButton(self.page_data_process)
        self.tool_btn_plot.setMinimumSize(QSize(28, 28))
        self.tool_btn_plot.setMaximumSize(QSize(28, 28))
        self.tool_btn_plot.setIcon(QIcon(CONSTANT.ICON_PLOT_PARAS))
        self.horizontalLayout_2.addWidget(self.tool_btn_plot)
        self.tool_btn_data_abstract = QToolButton(self.page_data_process)
        self.tool_btn_data_abstract.setMinimumSize(QSize(28, 28))
        self.tool_btn_data_abstract.setMaximumSize(QSize(28, 28))
        self.tool_btn_data_abstract.setIcon(QIcon(CONSTANT.ICON_DATA_ABSTRACT))
        self.horizontalLayout_2.addWidget(self.tool_btn_data_abstract)
        self.tool_btn_up = QToolButton(self.page_data_process)
        self.tool_btn_up.setMinimumSize(QSize(28, 28))
        self.tool_btn_up.setMaximumSize(QSize(28, 28))
        self.tool_btn_up.setIcon(QIcon(CONSTANT.ICON_UP))
        self.horizontalLayout_2.addWidget(self.tool_btn_up)
        self.tool_btn_down = QToolButton(self.page_data_process)
        self.tool_btn_down.setMinimumSize(QSize(28, 28))
        self.tool_btn_down.setMaximumSize(QSize(28, 28))
        self.tool_btn_down.setIcon(QIcon(CONSTANT.ICON_DOWN))
        self.horizontalLayout_2.addWidget(self.tool_btn_down)
        self.tool_btn_delete = QToolButton(self.page_data_process)
        self.tool_btn_delete.setMinimumSize(QSize(28, 28))
        self.tool_btn_delete.setMaximumSize(QSize(28, 28))
        self.tool_btn_delete.setIcon(QIcon(CONSTANT.ICON_DEL))
        self.horizontalLayout_2.addWidget(self.tool_btn_delete)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_9.addLayout(self.horizontalLayout_2)
        self.tree_widget_paralist = ParasListWithDropEvent(self.page_data_process)
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
        self.verticalLayout_10.addLayout(self.verticalLayout_9)

        self.stackedWidget.addWidget(self.page_data_process)
        
        self.page_data_sift = QWidget()
        self.verticalLayout_5 = QVBoxLayout(self.page_data_sift)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        
        self.tab_widget_datasift = QTabWidget(self.page_data_sift)
        self.tab_widget_datasift.setTabsClosable(True)
        self.tab_sift = QWidget()
        self.verticalLayout_4 = QVBoxLayout(self.tab_sift)
        self.verticalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_4.setSpacing(2)
        self.group_box_expression = QGroupBox(self.tab_sift)
        self.verticalLayout_2 = QVBoxLayout(self.group_box_expression)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(2)
        self.plain_text_edit_expression = QPlainTextEdit(self.group_box_expression)
        
        self.plain_text_edit_expression.setContextMenuPolicy(Qt.CustomContextMenu)
#        添加右键动作
        self.action_add_para = QAction(self.plain_text_edit_expression)
        self.action_add_para.setText(QCoreApplication.
                                   translate('DataAnalysisWindow', '添加参数'))
        
        self.verticalLayout_2.addWidget(self.plain_text_edit_expression)
        self.verticalLayout_4.addWidget(self.group_box_expression)
        self.group_box_aggregates = QGroupBox(self.tab_sift)
        self.verticalLayout_3 = QVBoxLayout(self.group_box_aggregates)
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_3.setSpacing(2)
        self.push_btn_add_aggregate = QPushButton(self.group_box_aggregates)
        self.push_btn_add_aggregate.setMinimumSize(QSize(0, 24))
        self.push_btn_add_aggregate.setMaximumSize(QSize(16777215, 24))
        self.verticalLayout_3.addWidget(self.push_btn_add_aggregate)
        self.tree_widget_aggragate_para = QTreeWidget(self.group_box_aggregates)
        
#        让顶级项没有扩展符空白
        self.tree_widget_aggragate_para.setRootIsDecorated(False)
        
        self.verticalLayout_3.addWidget(self.tree_widget_aggragate_para)
        self.verticalLayout_4.addWidget(self.group_box_aggregates)
        self.button_box_sift = QDialogButtonBox(self.tab_sift)
        self.button_box_sift.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.verticalLayout_4.addWidget(self.button_box_sift)
        self.verticalLayout_4.setStretch(0, 2)
        self.verticalLayout_4.setStretch(1, 4)
        self.tab_widget_datasift.addTab(self.tab_sift, '')
        
        self.verticalLayout_5.addWidget(self.tab_widget_datasift)
        self.stackedWidget.addWidget(self.page_data_sift)
        self.verticalLayout.addWidget(self.stackedWidget)

        self.retranslateUi()
        self.stackedWidget.setCurrentIndex(0)
        self.tab_widget_datasift.setCurrentIndex(0)
        
# =======连接信号与槽
# =============================================================================        
        self.combo_box_analysis_type.currentIndexChanged.connect(self.slot_show_page)
        
        self.button_box_sift.accepted.connect(self.slot_sift_ok)
        self.button_box_sift.rejected.connect(self.slot_sift_cancel)
        
        self.plain_text_edit_expression.customContextMenuRequested.connect(
                self.expression_context_menu)
        self.action_add_para.triggered.connect(self.slot_add_para)
        
        self.tab_widget_datasift.tabCloseRequested.connect(self.slot_close_tab)
        self.push_btn_add_aggregate.clicked.connect(self.slot_add_aggregate)
        
#        数据处理页
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
    def slot_show_page(self, index):
        
        self.stackedWidget.setCurrentIndex(index)
        
# =============================================================================
# 数据处理页的slot
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
                    item_para.setText(0, paraname)
                    item_para.setText(1, filename)
                    item_para.setData(1, Qt.UserRole, file_dir)
                    item_para.setText(2, file.time_range[0])
                    item_para.setText(3, file.time_range[1])
                    item_para.setText(4, str(file.sample_frequency))

            if ex_paras:
                print_para = '<br>以下参数已存在：'
                for pa in ex_paras:
                    print_para += ('<br>' + pa)
                QMessageBox.information(self,
                        QCoreApplication.translate('DataAnalysisWindow', '导入参数提示'),
                        QCoreApplication.translate('DataAnalysisWindow',
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
                                                QCoreApplication.translate('DataAnalysisWindow', '导入模板提示'),
                                                QCoreApplication.translate('DataAnalysisWindow',
                                                                           print_para))
                    self.slot_import_paras(imput_paras)
                else:
                    QMessageBox.information(self,
                            QCoreApplication.translate('DataAnalysisWindow', '导入模板错误'),
                            QCoreApplication.translate('DataAnalysisWindow', '没有发现数据文件'))
        else:
            QMessageBox.information(self,
                    QCoreApplication.translate('DataAnalysisWindow', '导入模板错误'),
                    QCoreApplication.translate('DataAnalysisWindow', '没有模板'))            

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
                        temp[temp_name].append(self.tree_widget_paralist.topLevelItem(i).text(0))
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
        
        self.signal_para_for_plot.emit(self.get_paras_in_tuple())
        
    def slot_data_abstract(self):
        
        para_tuple = self.get_paras_in_tuple()
        dict_paras, sorted_paras = para_tuple
        if dict_paras :
            dialog = ParameterExportDialog(self, dict_paras)
            return_signal = dialog.exec_()
            if return_signal == QDialog.Accepted:
                QMessageBox.information(self,
                        QCoreApplication.translate('DataAnalysisWindow', '保存提示'),
                        QCoreApplication.translate('DataAnalysisWindow', '保存成功！'))
                
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
                          QCoreApplication.translate('DataAnalysisWindow', '确定要删除这些参数吗'),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                for item in sel_items:
                    self.tree_widget_paralist.takeTopLevelItem(
                            self.tree_widget_paralist.indexOfTopLevelItem(item))

# =============================================================================
# 数据筛选页
# =============================================================================
    def slot_sift_ok(self):
        
        list_files = self._current_files
        str_condition = self.plain_text_edit_expression.toPlainText()
        if list_files and str_condition:
#            创建一个结果显示窗口
            self.tab_result_count += 1
            tab_sift_result = SiftResultViewWidget(self.tab_widget_datasift,  str_condition)
            self.tab_widget_datasift.addTab(
                    tab_sift_result, 
                    QCoreApplication.translate('DataAnalysisWindow',
                                               '筛选结果' + str(self.tab_result_count)))
            self.tab_widget_datasift.setCurrentIndex(
                    self.tab_widget_datasift.indexOf(tab_sift_result))
        else:
            QMessageBox.information(self,
                    QCoreApplication.translate('DataAnalysisWindow', '提示'),
                    QCoreApplication.translate('DataAnalysisWindow','没有足够的输入'))
        
    def slot_sift_cancel(self):
        
        self.plain_text_edit_expression.clear()
        self.tree_widget_aggragate_para.clear()
        
    def expression_context_menu(self, pos):

        menu = QMenu(self.plain_text_edit_expression)
        menu.addActions([self.action_add_para])
        menu.exec_(self.plain_text_edit_expression.mapToGlobal(pos))
        
    def slot_add_aggregate(self):
        
#        采用单选模式
        dialog = SelParasDialog(self, self._current_files, 0)
        return_signal = dialog.exec_()
        paras = []
        if (return_signal == QDialog.Accepted):
            paras = dialog.get_list_sel_paras()
            if paras:
                widget_aggregate = QWidget(self.tree_widget_aggragate_para)
                vlayout = QVBoxLayout()
                vlayout.setContentsMargins(2, 2, 2, 2)
                combo_box = QComboBox(widget_aggregate)
                combo_box.addItem(QCoreApplication.translate('DataAnalysisWindow', '整段数据'))
                combo_box.addItem(QCoreApplication.translate('DataAnalysisWindow', '最大值'))
                combo_box.addItem(QCoreApplication.translate('DataAnalysisWindow', '最小值'))
                combo_box.addItem(QCoreApplication.translate('DataAnalysisWindow', '平均值'))
                vlayout.addWidget(combo_box)
                widget_aggregate.setLayout(vlayout)
                
                widget_para = QWidget(self.tree_widget_aggragate_para)
                hlayout = QHBoxLayout()
                hlayout.setContentsMargins(2, 2, 2, 2)
                hlayout.setSpacing(2)
                line_edit = QLineEdit(widget_para)
                line_edit.setReadOnly(True)
                line_edit.setText(paras[0])
                hlayout.addWidget(line_edit)
                button = QPushButton(widget_para)
                button.setText(QCoreApplication.translate('DataAnalysisWindow', '删除'))
                hlayout.addWidget(button)
                widget_para.setLayout(hlayout)
                item = QTreeWidgetItem(self.tree_widget_aggragate_para)
                self.tree_widget_aggragate_para.addTopLevelItem(item)
                self.tree_widget_aggragate_para.setItemWidget(item, 0, widget_aggregate)
                self.tree_widget_aggragate_para.setItemWidget(item, 1, widget_para)
                button.clicked.connect(self.slot_delete_aggregate)
                
    def slot_delete_aggregate(self):
        
        sender = QObject.sender(self)
        item = self.tree_widget_aggragate_para.itemAt(sender.pos())
        self.tree_widget_aggragate_para.takeTopLevelItem(
                self.tree_widget_aggragate_para.indexOfTopLevelItem(item))
        
    def slot_update_current_files(self, files : list):
        
        self._current_files = files
    
    def slot_add_para(self):
        
#        采用单选模式
        dialog = SelParasDialog(self, self._current_files, 0)
        return_signal = dialog.exec_()
        if (return_signal == QDialog.Accepted):
            paras = dialog.get_list_sel_paras()
            if paras:
                self.plain_text_edit_expression.insertPlainText('[' + paras[0] + ']')
                
    def slot_close_tab(self, index : int):
        
#        不允许关闭第一个tab
        if index > 0:
            message = QMessageBox.warning(self,
                          QCoreApplication.translate('DataAnalysisWindow', '关闭'),
                          QCoreApplication.translate('DataAnalysisWindow',
                                            '''<p>确定要关闭吗？'''),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                self.tab_widget_datasift.removeTab(index)

# =============================================================================
# 功能函数模块   
# =============================================================================
# =============================================================================
# 数据处理页
# =============================================================================
#    只要参数名一致就认为在这个参数列表中，不区分是否是在不同文件
    def is_in_sel_paras(self, para, file_dir):

        count = self.tree_widget_paralist.topLevelItemCount()
        for i in range(count):
            item = self.tree_widget_paralist.topLevelItem(i)
            paraname = item.text(0)
            fd = item.data(1, Qt.UserRole)
            if para == paraname and fd == file_dir:
                return True
        return False
    
    def get_paras_in_tuple(self):
        
        result = {}
        sorted_paras = []
        if self.tree_widget_paralist:
            count = self.tree_widget_paralist.topLevelItemCount()
            for i in range(count):
                item = self.tree_widget_paralist.topLevelItem(i)
                sorted_paras.append(item.text(0))
                file_dir = item.data(1, Qt.UserRole)
                if file_dir in result:
                    result[file_dir].append(item.text(0))
                else:
                    result[file_dir] = []
                    result[file_dir].append(item.text(0))
        return (result, sorted_paras)
    
# =============================================================================
# 数据筛选页
# =============================================================================

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.label_analysis_type.setText(_translate('DataAnalysisWindow', '数据分析类型'))
        self.combo_box_analysis_type.setItemText(0, _translate('DataAnalysisWindow', '数据处理'))
        self.combo_box_analysis_type.setItemText(1, _translate('DataAnalysisWindow', '数据筛选'))
        self.group_box_expression.setTitle(_translate('DataAnalysisWindow', '条件表达式'))
        self.group_box_aggregates.setTitle(_translate('DataAnalysisWindow', '筛选目标'))
        self.push_btn_add_aggregate.setText(_translate('DataAnalysisWindow', '添加新目标'))
        self.tree_widget_aggragate_para.headerItem().setText(0, _translate('DataAnalysisWindow', '条件'))
        self.tree_widget_aggragate_para.headerItem().setText(1, _translate('DataAnalysisWindow', '参数'))
        self.tab_widget_datasift.setTabText(self.tab_widget_datasift.indexOf(self.tab_sift), _translate('DataAnalysisWindow', '数据筛选'))
        self.tool_btn_save_temp.setToolTip(_translate('DataAnalysisWindow', '保存为模板'))
        self.tool_btn_sel_temp.setToolTip(_translate('DataAnalysisWindow', '选择模板'))
        self.tool_btn_plot.setToolTip(_translate('DataAnalysisWindow', '绘图'))
        self.tool_btn_data_abstract.setToolTip(_translate('DataAnalysisWindow', '数据提取'))
        self.tool_btn_up.setToolTip(_translate('DataAnalysisWindow', '上移参数'))
        self.tool_btn_down.setToolTip(_translate('DataAnalysisWindow', '下移参数'))
        self.tool_btn_delete.setToolTip(_translate('DataAnalysisWindow', '删除参数'))
        self.tree_widget_paralist.headerItem().setText(0, _translate('DataAnalysisWindow', '参数名'))
        self.tree_widget_paralist.headerItem().setText(1, _translate('DataAnalysisWindow', '所属文件'))
        self.tree_widget_paralist.headerItem().setText(2, _translate('DataAnalysisWindow', '起始时间'))
        self.tree_widget_paralist.headerItem().setText(3, _translate('DataAnalysisWindow', '终止时间'))
        self.tree_widget_paralist.headerItem().setText(4, _translate('DataAnalysisWindow', '采样频率'))

