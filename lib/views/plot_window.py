# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 简述：绘图窗口类
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
from PyQt5.QtWidgets import (QWidget, QToolButton, QSpacerItem,
                             QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QMessageBox, QScrollArea, QProgressDialog,
                             QTabWidget, QApplication, QFrame, QDialog)
from PyQt5.QtCore import (QCoreApplication, QSize, pyqtSignal, QDataStream,
                          QIODevice, Qt)
from PyQt5.QtGui import QIcon, QKeyEvent, QFont

# =============================================================================
# Package views imports
# =============================================================================
from models.figure_model import (FastPlotCanvas, SingleAxisXTimePlotCanvas,
                                 StackAxisPlotCanvas, SingleAxisPlotCanvas)
from views.custom_dialog import DisplayParaValuesDialog, SelectPlotTemplateDialog
import views.config_info as CONFIG
# =============================================================================
# FigureWindow
# =============================================================================
class FigureWindow(QScrollArea):

    signal_resize = pyqtSignal(QSize)
    signal_drop_paras = pyqtSignal(tuple)
    
    def __init__(self, parent = None, fig_style = None):
        
        super().__init__(parent)
        
        if fig_style == 'fast_plot_fig':
            self.canva = FastPlotCanvas(self)
        if fig_style == 'single_axis_fig':
            self.canva = SingleAxisPlotCanvas(self)
        if fig_style == 'single_axis_xtime_fig':
            self.canva = SingleAxisXTimePlotCanvas(self)
        if fig_style == 'stack_axis_fig':
            self.canva = StackAxisPlotCanvas(self)
        self.setWidget(self.canva)
        self.setWidgetResizable(True)
        self.setAcceptDrops(True)
        
    def resizeEvent(self, event):
        
        self.signal_resize.emit(event.size())
        QScrollArea.resizeEvent(self, event)
        
#    重写拖放相关的事件
#    设置部件可接受的MIME type列表，此处的类型是自定义的
    def mimeTypes(self):
        return ['application/x-parasname']
#    拖进事件处理    
    def dragEnterEvent(self, event):
#        如果拖进来的时树列表才接受
        if event.mimeData().hasFormat('application/x-parasname'):
            event.acceptProposedAction()
        else:
            event.ignore()
#     放下事件处理   
    def dropEvent(self, event):
        
        paras = {}
        if event.mimeData().hasFormat('application/x-parasname'):
            item_data = event.mimeData().data('application/x-parasname')
            item_stream = QDataStream(item_data, QIODevice.ReadOnly)
#            对拖进来的数据进行解析
#            按数据流中的参数排列顺序存储参数到此参数列表
            sorted_paras = []
            while (not item_stream.atEnd()):
                paraname = item_stream.readQString()
                file_dir = item_stream.readQString()
                sorted_paras.append((paraname, file_dir))
                if not (file_dir in paras):
                    paras[file_dir] = []
                    paras[file_dir].append(paraname)
                else:
                    paras[file_dir].append(paraname)  
            self.signal_drop_paras.emit((paras, sorted_paras))
            event.acceptProposedAction()
        else:
            event.ignore()
        
# =============================================================================
# PlotWindow
# =============================================================================
class PlotWindow(QWidget):

    signal_request_temps = pyqtSignal(str)
    signal_save_temp = pyqtSignal(dict)
    signal_is_display_menu = pyqtSignal(bool)
    signal_send_status = pyqtSignal(str, int)
# =============================================================================
# 初始化    
# =============================================================================
    def __init__(self, parent = None):
        
        super().__init__(parent)
        
        self.current_clicked_btn = None
        self.on_saving_fig = False
        
        self.current_count_axes = 0
#        用户保存的时刻
        self.timestamps = []
#        当前绘图窗口
        self.current_fig_win = None
        self.current_fig_style = 'fast_plot_fig'
        
        self._current_files = None
        self._dict_filetype = None
        self._data_dict = None

# =============================================================================
# UI模块        
# =============================================================================
    def setup(self):
        
        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
#        该窗口的主布局器，水平
        self.horizontalLayout_2 = QHBoxLayout(self)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        
        self.tab_widget_figure = QTabWidget(self)
        self.tab_widget_figure.setTabsClosable(True)
        self.tab_widget_figure.setMovable(True)
#        创建画布部件
        self.current_fig_win = FigureWindow(self.tab_widget_figure, 'fast_plot_fig')
        self.current_canva = self.current_fig_win.canva
        self.tab_widget_figure.addTab(self.current_fig_win,
                                      QIcon(CONFIG.ICON_MULT_AXIS),
                                      QCoreApplication.translate('PlotWindow',
                                                                 '多坐标图'))
#        创建右侧的工具栏
        self.widget_plot_tools = QWidget(self)
        self.widget_plot_tools.setMinimumSize(QSize(32, 0))
        self.widget_plot_tools.setMaximumSize(QSize(32, 16777215))
#        子布局器，垂直，布局工具按钮
        self.verticalLayout = QVBoxLayout(self.widget_plot_tools)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
#        创建放大缩小按钮并加入工具栏
        self.button_home = QToolButton(self.widget_plot_tools)
        self.button_home.setMinimumSize(QSize(30, 30))
        self.button_home.setMaximumSize(QSize(30, 30))
        self.button_home.setIconSize(QSize(22, 22))
        self.button_home.setIcon(QIcon(CONFIG.ICON_HOME))
        self.verticalLayout.addWidget(self.button_home)
        self.button_pan = QToolButton(self.widget_plot_tools)
        self.button_pan.setCheckable(True)
        self.button_pan.setMinimumSize(QSize(30, 30))
        self.button_pan.setMaximumSize(QSize(30, 30))
        self.button_pan.setIconSize(QSize(22, 22))
        self.button_pan.setIcon(QIcon(CONFIG.ICON_PAN))
        self.verticalLayout.addWidget(self.button_pan)
        self.button_zoom = QToolButton(self.widget_plot_tools)
        self.button_zoom.setCheckable(True)
        self.button_zoom.setMinimumSize(QSize(30, 30))
        self.button_zoom.setMaximumSize(QSize(30, 30))
        self.button_pan.setIconSize(QSize(22, 22))
        self.button_zoom.setIcon(QIcon(CONFIG.ICON_ZOOM))
        self.verticalLayout.addWidget(self.button_zoom)
#        self.button_plot_setting = QToolButton(self.widget_plot_tools)
#        self.button_plot_setting.setMinimumSize(QSize(30, 30))
#        self.button_plot_setting.setMaximumSize(QSize(30, 30))
#        self.button_plot_setting.setIconSize(QSize(22, 22))
#        self.button_plot_setting.setIcon(QIcon(CONFIG.ICON_PLOT_SETTING))
#        self.verticalLayout.addWidget(self.button_plot_setting)
#        self.button_edit = QToolButton(self.widget_plot_tools)
#        self.button_edit.setMinimumSize(QSize(30, 30))
#        self.button_edit.setMaximumSize(QSize(30, 30))
#        self.button_edit.setObjectName('button_edit')
#        self.button_edit.setIcon(QIcon(CONFIG.ICON_EDIT))
#        self.verticalLayout.addWidget(self.button_edit)
#        self.button_config = QToolButton(self.widget_plot_tools)
#        self.button_config.setMinimumSize(QSize(30, 30))
#        self.button_config.setMaximumSize(QSize(30, 30))
#        self.button_config.setObjectName('button_config')
#        self.button_config.setIcon(QIcon(CONFIG.ICON_CONFIG))
#        self.verticalLayout.addWidget(self.button_config)
        self.button_back = QToolButton(self.widget_plot_tools)
        self.button_back.setMinimumSize(QSize(30, 30))
        self.button_back.setMaximumSize(QSize(30, 30))
        self.button_back.setIconSize(QSize(22, 22))
        self.button_back.setIcon(QIcon(CONFIG.ICON_BACK))
        self.verticalLayout.addWidget(self.button_back)
        self.button_forward = QToolButton(self.widget_plot_tools)
        self.button_forward.setMinimumSize(QSize(30, 30))
        self.button_forward.setMaximumSize(QSize(30, 30))
        self.button_forward.setIconSize(QSize(22, 22))
        self.button_forward.setIcon(QIcon(CONFIG.ICON_FORWARD))
        self.verticalLayout.addWidget(self.button_forward)    
        self.button_save = QToolButton(self.widget_plot_tools)
        self.button_save.setMinimumSize(QSize(30, 30))
        self.button_save.setMaximumSize(QSize(30, 30))
        self.button_save.setIconSize(QSize(22, 22))
        self.button_save.setIcon(QIcon(CONFIG.ICON_SAVE))
        self.verticalLayout.addWidget(self.button_save)
#        self.button_sel_temp = QToolButton(self.widget_plot_tools)
#        self.button_sel_temp.setMinimumSize(QSize(30, 30))
#        self.button_sel_temp.setMaximumSize(QSize(30, 30))
#        self.button_sel_temp.setObjectName('button_sel_temp')
#        self.button_sel_temp.setIcon(QIcon(CONFIG.ICON_SEL_TEMP))
#        self.verticalLayout.addWidget(self.button_sel_temp)
#        self.button_save_temp = QToolButton(self.widget_plot_tools)
#        self.button_save_temp.setMinimumSize(QSize(30, 30))
#        self.button_save_temp.setMaximumSize(QSize(30, 30))
#        self.button_save_temp.setObjectName('button_save_temp')
#        self.button_save_temp.setIcon(QIcon(CONFIG.ICON_SAVE_TEMP))
#        self.verticalLayout.addWidget(self.button_save_temp)
        self.button_get_paravalue = QToolButton(self.widget_plot_tools)
        self.button_get_paravalue.setCheckable(True)
        self.button_get_paravalue.setMinimumSize(QSize(30, 30))
        self.button_get_paravalue.setMaximumSize(QSize(30, 30))
        self.button_get_paravalue.setIconSize(QSize(22, 22))
        self.button_get_paravalue.setIcon(QIcon(CONFIG.ICON_PARA_VALUE))
        self.verticalLayout.addWidget(self.button_get_paravalue)
        self.button_clear_canvas = QToolButton(self.widget_plot_tools)
        self.button_clear_canvas.setMinimumSize(QSize(30, 30))
        self.button_clear_canvas.setMaximumSize(QSize(30, 30))
        self.button_clear_canvas.setIconSize(QSize(22, 22))
        self.button_clear_canvas.setIcon(QIcon(CONFIG.ICON_CLEAR))
        self.verticalLayout.addWidget(self.button_clear_canvas)
#        self.button_add_sa_fig = QToolButton(self.widget_plot_tools)
#        self.button_add_sa_fig.setMinimumSize(QSize(30, 30))
#        self.button_add_sa_fig.setMaximumSize(QSize(30, 30))
#        self.button_add_sa_fig.setIconSize(QSize(22, 22))
#        self.button_add_sa_fig.setIcon(QIcon(CONFIG.ICON_SINGLE_AXIS))
#        self.verticalLayout.addWidget(self.button_add_sa_fig)
#        self.button_add_ma_fig = QToolButton(self.widget_plot_tools)
#        self.button_add_ma_fig.setMinimumSize(QSize(30, 30))
#        self.button_add_ma_fig.setMaximumSize(QSize(30, 30))
#        self.button_add_ma_fig.setIconSize(QSize(22, 22))
#        self.button_add_ma_fig.setIcon(QIcon(CONFIG.ICON_MULT_AXIS))
#        self.verticalLayout.addWidget(self.button_add_ma_fig)
#        self.button_add_sta_fig = QToolButton(self.widget_plot_tools)
#        self.button_add_sta_fig.setMinimumSize(QSize(30, 30))
#        self.button_add_sta_fig.setMaximumSize(QSize(30, 30))
#        self.button_add_sta_fig.setIconSize(QSize(22, 22))
#        self.button_add_sta_fig.setIcon(QIcon(CONFIG.ICON_STACK_AXIS))
#        self.verticalLayout.addWidget(self.button_add_sta_fig)
#        
#        self.button_add_ux_fig = QToolButton(self.widget_plot_tools)
#        self.button_add_ux_fig.setMinimumSize(QSize(30, 30))
#        self.button_add_ux_fig.setMaximumSize(QSize(30, 30))
#        self.button_add_ux_fig.setIconSize(QSize(22, 22))
#        self.button_add_ux_fig.setIcon(QIcon(CONFIG.ICON_STACK_AXIS))
#        self.verticalLayout.addWidget(self.button_add_ux_fig)
        
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)
        self.line_2 = QFrame(self)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_2)
        
        self.button_add_text = QToolButton(self.widget_plot_tools)
        self.button_add_text.setCheckable(True)
        self.button_add_text.setMinimumSize(QSize(30, 30))
        self.button_add_text.setMaximumSize(QSize(30, 30))
        self.button_add_text.setIconSize(QSize(22, 22))
        self.button_add_text.setIcon(QIcon(CONFIG.ICON_TEXT))
        self.verticalLayout.addWidget(self.button_add_text)
        self.button_add_hl = QToolButton(self.widget_plot_tools)
        self.button_add_hl.setCheckable(True)
        self.button_add_hl.setMinimumSize(QSize(30, 30))
        self.button_add_hl.setMaximumSize(QSize(30, 30))
        self.button_add_hl.setIconSize(QSize(22, 22))
        self.button_add_hl.setIcon(QIcon(CONFIG.ICON_HLINE))
        self.verticalLayout.addWidget(self.button_add_hl)
        self.button_add_vl = QToolButton(self.widget_plot_tools)
        self.button_add_vl.setCheckable(True)
        self.button_add_vl.setMinimumSize(QSize(30, 30))
        self.button_add_vl.setMaximumSize(QSize(30, 30))
        self.button_add_vl.setIconSize(QSize(22, 22))
        self.button_add_vl.setIcon(QIcon(CONFIG.ICON_VLINE))
        self.verticalLayout.addWidget(self.button_add_vl)
        self.button_add_line = QToolButton(self.widget_plot_tools)
        self.button_add_line.setCheckable(True)
        self.button_add_line.setMinimumSize(QSize(30, 30))
        self.button_add_line.setMaximumSize(QSize(30, 30))
        self.button_add_line.setIconSize(QSize(22, 22))
        self.button_add_line.setIcon(QIcon(CONFIG.ICON_LINE))
        self.verticalLayout.addWidget(self.button_add_line)
        self.button_save_temp = QToolButton(self.widget_plot_tools)
        self.button_save_temp.setMinimumSize(QSize(30, 30))
        self.button_save_temp.setMaximumSize(QSize(30, 30))
        self.button_save_temp.setIconSize(QSize(22, 22))
        self.button_save_temp.setIcon(QIcon(CONFIG.ICON_SAVE_TEMP))
        self.verticalLayout.addWidget(self.button_save_temp)
        self.button_sel_temp = QToolButton(self.widget_plot_tools)
        self.button_sel_temp.setMinimumSize(QSize(30, 30))
        self.button_sel_temp.setMaximumSize(QSize(30, 30))
        self.button_sel_temp.setIconSize(QSize(22, 22))
        self.button_sel_temp.setIcon(QIcon(CONFIG.ICON_SEL_TEMP))
        self.verticalLayout.addWidget(self.button_sel_temp)
        self.button_sel_data_inter = QToolButton(self.widget_plot_tools)
        self.button_sel_data_inter.setCheckable(True)
        self.button_sel_data_inter.setMinimumSize(QSize(30, 30))
        self.button_sel_data_inter.setMaximumSize(QSize(30, 30))
        self.button_sel_data_inter.setIconSize(QSize(22, 22))
        self.button_sel_data_inter.setIcon(QIcon(CONFIG.ICON_DATA_CUT))
        self.verticalLayout.addWidget(self.button_sel_data_inter)
        spacerItem = QSpacerItem(20, 219, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        
#        self.para_value_window = QWidget(self)
#        self.para_value_window.setMinimumSize(QSize(250, 0))
#        self.para_value_window.setMaximumSize(QSize(250, 16777215))
#        
#        self.vl_para_window = QVBoxLayout(self.para_value_window)
#        self.vl_para_window.setContentsMargins(2, 2, 2, 0)
#        self.vl_para_window.setSpacing(2)
#        self.group_box_time_interval = QGroupBox(self.para_value_window)
#        self.vl_gbtr = QVBoxLayout(self.group_box_time_interval)
#        self.vl_gbtr.setContentsMargins(2, 2, 2, 2)
#        self.vl_gbtr.setSpacing(2)
#        self.hl_combo = QHBoxLayout()
#        self.hl_combo.setSpacing(4)
#        self.combo_box_time_intervals = QComboBox(self.group_box_time_interval)
#        self.combo_box_time_intervals.setMinimumSize(QSize(0, 24))
#        self.combo_box_time_intervals.setMaximumSize(QSize(16777215, 24))
#        self.hl_combo.addWidget(self.combo_box_time_intervals)
#        self.tool_btn_time_interval = QToolButton(self.group_box_time_interval)
#        self.tool_btn_time_interval.setMinimumSize(QSize(24, 24))
#        self.tool_btn_time_interval.setMaximumSize(QSize(24, 24))
#        self.hl_combo.addWidget(self.tool_btn_time_interval)
#        self.vl_gbtr.addLayout(self.hl_combo)
#        self.hl_combo_2 = QHBoxLayout()
#        self.hl_combo_2.setSpacing(4)
#        self.combo_box_time = QComboBox(self.group_box_time_interval)
#        self.combo_box_time.setMinimumSize(QSize(0, 24))
#        self.combo_box_time.setMaximumSize(QSize(16777215, 24))
#        self.hl_combo_2.addWidget(self.combo_box_time)
#        self.tool_btn_time = QToolButton(self.group_box_time_interval)
#        self.tool_btn_time.setMinimumSize(QSize(24, 24))
#        self.tool_btn_time.setMaximumSize(QSize(24, 24))
#        self.hl_combo_2.addWidget(self.tool_btn_time)
#        self.vl_gbtr.addLayout(self.hl_combo_2)
#        self.vl_para_window.addWidget(self.group_box_time_interval)
#        self.group_box_time = QGroupBox(self.para_value_window)
#        self.vl_gbt = QVBoxLayout(self.group_box_time)
#        self.vl_gbt.setContentsMargins(2, 2, 2, 0)
#        self.vl_gbt.setSpacing(2)
#        self.label_time = QLabel(self.group_box_time)
#        self.label_time.setMinimumSize(QSize(0, 24))
#        self.label_time.setMaximumSize(QSize(16777215, 24))
#        self.vl_gbt.addWidget(self.label_time)
#        self.table_widget_value = QTableWidget(self.group_box_time)
#        self.table_widget_value.setColumnCount(2)
#        self.table_widget_value.setRowCount(0)
#        item = QTableWidgetItem()
#        self.table_widget_value.setHorizontalHeaderItem(0, item)
#        item = QTableWidgetItem()
#        self.table_widget_value.setHorizontalHeaderItem(1, item)
#        self.table_widget_value.horizontalHeader().setDefaultSectionSize(119)
#        self.table_widget_value.verticalHeader().setVisible(False)
#        self.vl_gbt.addWidget(self.table_widget_value)
#        self.vl_para_window.addWidget(self.group_box_time)
        
#        先添加工具栏在添加包括画布/滑块的水平子布局器
        self.horizontalLayout_2.addWidget(self.widget_plot_tools)
        self.horizontalLayout_2.addWidget(self.tab_widget_figure)
#        self.horizontalLayout_2.addWidget(self.para_value_window)
#        self.para_value_window.setHidden(True)

        self.retranslateUi()
# =======连接信号与槽
# =============================================================================
        self.button_pan.clicked.connect(self.slot_pan)
        self.button_zoom.clicked.connect(self.slot_zoom)
        self.button_save.clicked.connect(self.slot_save_figure)
#        self.button_sel_temp.clicked.connect(self.slot_emit_request_plot_temps)
#        self.button_save_temp.clicked.connect(self.slot_save_temp)
        self.button_clear_canvas.clicked.connect(self.slot_clear_canvas)
        self.button_get_paravalue.clicked.connect(self.slot_paravalue_btn_clicked)
#        self.button_add_sa_fig.clicked.connect(self.slot_add_sa_fig)
#        self.button_add_ma_fig.clicked.connect(self.slot_add_ma_fig)
#        self.button_add_sta_fig.clicked.connect(self.slot_add_stack_fig)
#        self.button_add_ux_fig.clicked.connect(self.slot_add_ux_fig)
        self.button_add_text.clicked.connect(self.slot_add_text)
        self.button_add_hl.clicked.connect(self.slot_add_hline)
        self.button_add_vl.clicked.connect(self.slot_add_vline)
        self.button_add_line.clicked.connect(self.slot_add_line)
        self.button_sel_temp.clicked.connect(self.slot_sel_plot_temp)
        self.button_sel_data_inter.clicked.connect(self.slot_sel_data_inter)

#        self.combo_box_time.activated.connect(self.slot_display_paravalue_ontime)
#        self.tool_btn_time.clicked.connect(self.slot_import_paravalue)
        
#        self.combo_box_time_intervals.activated.connect(self.slot_display_tinterval)
#        self.tool_btn_time_interval.clicked.connect(self.slot_save_interval_data)
        
        self.tab_widget_figure.tabCloseRequested.connect(self.slot_close_tab)
        self.tab_widget_figure.currentChanged.connect(self.slot_fig_win_change)
        
        self.connect_cfw_sink_signal()
        
        self.current_canva.signal_progress.connect(self.set_value)

#    连接与绘图窗口有关的信号槽
    def connect_cfw_sink_signal(self):

#        self.button_plot_setting.clicked.connect(self.current_canva.slot_plot_setting)
#        self.button_edit.clicked.connect(self.current_canva.toolbar.edit_parameters)
#        self.button_config.clicked.connect(self.current_canva.toolbar.configure_subplots)
        self.button_home.clicked.connect(self.current_canva.slot_home)
        self.button_back.clicked.connect(self.current_canva.toolbar.back)
        self.button_forward.clicked.connect(self.current_canva.toolbar.forward)
        self.button_save_temp.clicked.connect(self.current_canva.save_plot_temp)
        self.current_fig_win.signal_resize.connect(self.slot_resize_canvas)
        self.current_fig_win.signal_drop_paras.connect(self.slot_plot)
#        画布的右键菜单
        self.signal_is_display_menu.connect(self.current_canva.slot_set_display_menu)
        
        self.current_canva.signal_added_artist.connect(self.slot_uncheck_add_artist_btn)
        self.current_canva.signal_adjust_win.connect(self.adjust_fig_win)
        
#        self.current_canva.signal_cursor_xdata.connect(self.slot_display_paravalue)
#        self.current_canva.signal_send_time.connect(self.slot_save_time)
#        self.current_canva.signal_send_tinterval.connect(self.slot_save_tinterval)
 
#    断开与绘图窗口有关的信号槽       
    def diconnect_cfw_sink_signal(self):
        
#        self.button_plot_setting.clicked.connect(self.current_canva.slot_plot_setting)
#        self.button_edit.clicked.connect(self.current_canva.toolbar.edit_parameters)
#        self.button_config.clicked.connect(self.current_canva.toolbar.configure_subplots)
        self.button_home.clicked.disconnect(self.current_canva.slot_home)
        self.button_back.clicked.disconnect(self.current_canva.toolbar.back)
        self.button_forward.clicked.disconnect(self.current_canva.toolbar.forward)
        self.button_save_temp.clicked.disconnect(self.current_canva.save_plot_temp)
        self.current_fig_win.signal_resize.disconnect(self.slot_resize_canvas)
        self.current_fig_win.signal_drop_paras.disconnect(self.slot_plot)
#        画布的右键菜单
        self.signal_is_display_menu.disconnect(self.current_canva.slot_set_display_menu)
        
        self.current_canva.signal_added_artist.connect(self.slot_uncheck_add_artist_btn)
        self.current_canva.signal_adjust_win.disconnect(self.adjust_fig_win)
        
#        self.current_canva.signal_cursor_xdata.disconnect(self.slot_display_paravalue)
#        self.current_canva.signal_send_time.disconnect(self.slot_save_time)
#        self.current_canva.signal_send_tinterval.disconnect(self.slot_save_tinterval)

# =============================================================================
# slots模块
# =============================================================================   
    def add_PDialog(self):
        self.pdialog = QProgressDialog(self)
        self.pdialog.setWindowTitle('绘图中...')
        self.pdialog.setValue(0)
        self.pdialog.show()
        
    def set_value(self, value):
        if self.pdialog:
            self.pdialog.setValue(value)
            if value >= 100: 
                self.pdialog.close() 
            QApplication.processEvents()
        
    def pDialog_close(self):
        if self.pdialog:
            self.pdialog.close()

        
#    输入参数为一个包含两个参数的元组，元组第一个参数是字典型，存储文件名及与之对应的变量列表
#    元组第二个参数是列表，存储已排序的参数
#    这样定义数据类型的原因是绘图既需要读取数据也需要参数排列顺序
    def slot_plot(self, datadict_and_paralist : tuple):
        
        datadict = sorted_paras = xpara = None
        if len(datadict_and_paralist) == 3:
            datadict, sorted_paras, xpara = datadict_and_paralist
        elif len(datadict_and_paralist) == 2:
            datadict, sorted_paras = datadict_and_paralist
        else:
            return
        
        if datadict and sorted_paras:
#            在绘图前把正在进行的操作都停止
#            if (self.current_clicked_btn and 
#                self.current_clicked_btn.isChecked()):
#                    self.current_clicked_btn.click()
#                    self.current_clicked_btn = None
            self.current_canva._data_dict = self._data_dict
            
            self.signal_send_status.emit('绘图中...', 0)
            self.add_PDialog()
            self.current_canva.dict_filetype = self._dict_filetype
            self.current_canva.plot_paras(datadict, sorted_paras)
            self.pDialog_close()
            self.signal_send_status.emit('绘图完成！', 1500)
            
#            self.adjust_fig_win()
            
    def slot_resize_canvas(self, scroll_area_size):
        
        if (not self.current_fig_win.widgetResizable()) and (not self.on_saving_fig):
            height = self.current_count_axes * int(self.current_fig_win.height() * 1.05) / 4
            if scroll_area_size.height() > height:
                self.current_canva.resize(scroll_area_size)
            else:
                self.current_canva.resize(scroll_area_size.width(),
                                       self.current_canva.size().height())
#            设置图四边的空白宽度
            self.current_canva.adjust_figure()
            
    def adjust_fig_win(self):
        
        self.current_count_axes = self.current_canva.count_axes
        if self.current_count_axes > 4:
            self.current_fig_win.setWidgetResizable(False)
#            乘以1.05是估计的，刚好能放下四张图，
#            减去的19是滚动条的宽度
            if type(self.current_canva) == StackAxisPlotCanvas:
                if self.current_count_axes > 7:
                    n = self.current_count_axes - 7
                    d = 3 * (n - 1) + 4
                    height = self.current_fig_win.height() + d * 20
                    self.current_canva.resize(self.current_fig_win.width() - 19,
                                              height)
                else:
                    self.current_fig_win.setWidgetResizable(True)
            else:
                height = int(self.current_fig_win.height() * 1.05) / 4
                self.current_canva.resize(self.current_fig_win.width() - 19,
                                          self.current_count_axes * height)
        else:
            self.current_fig_win.setWidgetResizable(True)
        
    def slot_pan(self):
        
        self.current_canva.slot_pan()
        
        if self.button_pan.isChecked():
            self.current_canva.current_cursor_inaxes = Qt.SizeAllCursor
            self.signal_is_display_menu.emit(False)
#            保证功能冲突的按钮不能同时处于按下状态，zoom和pan由于使用自带的函数，
#            无法控制功能实现过程，在调用的时候已经处理好功能唯一性了
            if (self.current_clicked_btn and
                self.current_clicked_btn != self.button_pan and 
                self.current_clicked_btn.isChecked()):
                if self.current_clicked_btn == self.button_zoom:
                    self.current_clicked_btn.setChecked(False)
                else:
                    self.current_clicked_btn.click()
            self.current_clicked_btn = self.button_pan
        else:
            self.current_canva.current_cursor_inaxes = Qt.ArrowCursor
#            因为缩放时占用了右键，所以需要禁止右键菜单弹出
            self.signal_is_display_menu.emit(True)
            self.current_canva.slot_disconnect_pan()

        
    def slot_zoom(self):
        
        self.button_zoom.setCheckable(True)
        self.current_canva.toolbar.zoom()
        
        if self.button_zoom.isChecked():
            self.current_canva.current_cursor_inaxes = Qt.CrossCursor
            self.signal_is_display_menu.emit(False)
#            保证功能冲突的按钮不能同时处于按下状态，zoom和pan由于使用自带的函数，
#            无法控制功能实现过程，在调用的时候已经处理好功能唯一性了
            if (self.current_clicked_btn and
                self.current_clicked_btn != self.button_zoom and 
                self.current_clicked_btn.isChecked()):
                if self.current_clicked_btn == self.button_pan:
                    self.current_clicked_btn.setChecked(False)
                else:
                    self.current_clicked_btn.click()
            self.current_clicked_btn = self.button_zoom
        else:
            self.current_canva.current_cursor_inaxes = Qt.ArrowCursor
            self.signal_is_display_menu.emit(True)
        
#    def slot_emit_request_plot_temps(self):
#        
#        self.signal_request_temps.emit('plot_template')
        
#    def slot_sel_temp(self, dict_files, templates):
#
#        if templates:
#            export_paras = {}
#            sorted_paras = []
#            dialog = SelectTemplateDialog(self, templates)
#            return_signal = dialog.exec_()
#            if (return_signal == QDialog.Accepted):
#                if dict_files:
#        #            遍历文件，搜索是否存在模板中的参数
#        #            不同文件下的同一参数都会找出（这样耗时较长）
#        #            也可以找到第一个就停止
#                    for paraname in templates[dialog.sel_temp]:
#                        for file_dir in dict_files:
#                            if paraname in dict_files[file_dir]:
#                                if file_dir in export_paras:
#                                    export_paras[file_dir].append(paraname)
#                                else:
#                                    export_paras[file_dir] = []
#                                    export_paras[file_dir].append(paraname)
#                                sorted_paras.append(paraname)
#        #                        加入以下语句实现找到第一个就停止的功能
#        #                        break
#                    self.slot_plot((export_paras, sorted_paras))
#                else:
#                    QMessageBox.information(self,
#                            QCoreApplication.translate('DataExportWindow', '导入模板错误'),
#                            QCoreApplication.translate('DataExportWindow', '没有发现数据文件'))
#        else:
#            QMessageBox.information(self,
#                    QCoreApplication.translate('DataExportWindow', '导入模板错误'),
#                    QCoreApplication.translate('DataExportWindow', '没有模板')) 
    
#    def slot_save_temp(self):
#        
#        if self.current_canva.paralist:
#            temp = {}
#            dialog = SaveTemplateDialog(self)
#            return_signal = dialog.exec_()
#            if (return_signal == QDialog.Accepted):
#                temp_name = dialog.temp_name
#                if temp_name:
#                    temp[temp_name] = self.current_canva.paralist[1:]
#                    self.signal_save_temp.emit(temp)
#                else:
#                    QMessageBox.information(self,
#                            QCoreApplication.translate('DataExportWindow', '输入提示'),
#                            QCoreApplication.translate('DataExportWindow', '未输入模板名'))
#        else:
#            QMessageBox.information(self,
#                    QCoreApplication.translate('DataExportWindow', '保存错误'),
#                    QCoreApplication.translate('DataExportWindow', '没有发现图表')) 
        
    def slot_paravalue_btn_clicked(self):

#        在调用该槽函数时，按钮已处于被选中状态（不知为何）
        if self.button_get_paravalue.isChecked():

#            保证功能冲突的按钮不能同时处于按下状态
            if (self.current_clicked_btn and 
                self.current_clicked_btn != self.button_get_paravalue and 
                self.current_clicked_btn.isChecked()):
                    self.current_clicked_btn.click()
            self.current_clicked_btn = self.button_get_paravalue

            dialog = DisplayParaValuesDialog(self)
            dialog.move(30,100)
            self.current_canva._data_dict = self._data_dict
            self.current_canva.signal_cursor_xdata.connect(dialog.slot_display_paravalue)
            self.current_canva.slot_connect_display_paravalue()
            self.button_get_paravalue.clicked.connect(dialog.accept)
            dialog.rejected.connect(self.button_get_paravalue.click)
            dialog.show()
        else:
            self.current_canva.slot_diaconnect_display_paravalue()
            
#    def slot_save_time(self):
#
#        self.timestamps.append(self.label_time.text())
#        self.combo_box_time.addItem(self.label_time.text())
#        self.combo_box_time.setCurrentIndex(self.combo_box_time.count() - 1)
        
#    def slot_save_tinterval(self, timeinterval : tuple):
#        
#        name, stime, etime = timeinterval
#        tinterval = name + '(' + stime + ' - ' + etime + ')'
#        self.combo_box_time_intervals.addItem(tinterval, name)
#        self.combo_box_time_intervals.setCurrentIndex(self.combo_box_time_intervals.count() - 1)
        
#    def slot_import_paravalue(self):
#        
#        dict_paravalue = {}
#        paralist = ['TIME']
#        for time in self.timestamps:
#            dt = datetime.strptime(time, '%H:%M:%S.%f')
#            paravalue = self.current_canva.get_paravalue(dt)
#            for para_tuple in paravalue:
#                paraname, value = para_tuple
#                if paraname in dict_paravalue:
#                    dict_paravalue[paraname].append(value)
#                else:
#                    dict_paravalue[paraname] = []
#                    dict_paravalue[paraname].append(value)
#                if not(paraname in paralist):
#                    paralist.append(paraname)
#            if 'TIME' in dict_paravalue:
#                dict_paravalue['TIME'].append(time)
#            else:
#                dict_paravalue['TIME'] = []
#                dict_paravalue['TIME'].append(time)
#        if dict_paravalue:
#            df = pd.DataFrame(dict_paravalue)
##            按指定顺序放置列
#            df = df[paralist]
#            file_dir, flag = QFileDialog.getSaveFileName(self, 
#                                                         QCoreApplication.translate('PlotWindow', '保存参数值'),
#                                                         CONFIG.SETUP_DIR,
#                                                         QCoreApplication.translate('PlotWindow', 'Text Files (*.txt);;CSV Files (*.csv);;Matlab Files (*.mat)'))
#            if file_dir:
#                if flag == 'Text Files (*.txt)':
#                    df.to_csv(file_dir, '\t' , index=False, encoding='utf-8')
#                if flag == 'CSV Files (*.csv)':
#                    df.to_csv(file_dir, ',' , index=False, encoding='utf-8')
#                if flag == 'Matlab Files (*.mat)':
#                    sio.savemat(file_dir, df.to_dict('list'))
#                QMessageBox.information(self,
#                        QCoreApplication.translate('PlotWindow', '保存提示'),
#                        QCoreApplication.translate('PlotWindow', '保存成功'))
                                                 
#    显示复选框中选中时刻对应的参数值
#    def slot_display_paravalue_ontime(self, index):
#        
#        str_time = self.combo_box_time.itemText(index)
#        if str_time:
#            self.label_time.setText(str_time)
#            dt = datetime.strptime(str_time, '%H:%M:%S.%f')
#            paravalue = self.current_canva.get_paravalue(dt)
#            count = len(paravalue)
#            self.table_widget_value.clearContents()
#            self.table_widget_value.setRowCount(count)
#            for row, para_tuple in enumerate(paravalue):
#                paraname, value = para_tuple
#                item1 = QTableWidgetItem(paraname)
#                self.table_widget_value.setItem(row, 0, item1)
#                item2 = QTableWidgetItem(str(value))
#                self.table_widget_value.setItem(row, 1, item2)
#                
#    def slot_display_tinterval(self, index):
#        
#        name = self.combo_box_time_intervals.itemData(index)
#        self.current_canva.slot_set_tlim(name)
            
#    实时显示参数值
#    def slot_display_paravalue(self, time : str, paravalue : list):
#        
##        显示时间
#        self.label_time.setText(time)
#        
#        count = len(paravalue)
#        self.table_widget_value.clearContents()
#        self.table_widget_value.setRowCount(count)
#        for row, para_tuple in enumerate(paravalue):
#            paraname, value = para_tuple
#            item1 = QTableWidgetItem(paraname)
#            self.table_widget_value.setItem(row, 0, item1)
#            item2 = QTableWidgetItem(str(value))
#            self.table_widget_value.setItem(row, 1, item2)

    def slot_clear_canvas(self):
        
        if self.current_canva.fig.axes:
            message = QMessageBox.warning(self,
                  QCoreApplication.translate('PlotWindow', '清除画布'),
                  QCoreApplication.translate('PlotWindow', '确定要清除画布吗'),
                  QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                if (self.current_clicked_btn and 
                    self.current_clicked_btn.isChecked()):
                        self.current_clicked_btn.click()
                        self.current_clicked_btn = None
                self.current_canva.slot_clear_canvas()
#                如果画的图多会出现滚动条，此时清除画布，滚动条不会消失，因此采用此行解决
                self.current_fig_win.setWidgetResizable(True)
                self.current_count_axes = 0
                self.timestamps = []
                self.current_canva.time_intervals = {}
#                self.combo_box_time.clear()
#                self.combo_box_time_intervals.clear()
#                self.label_time.setText('00:00:00.000')
#                self.table_widget_value.clearContents()
#                self.table_widget_value.setRowCount(0)
        
    def slot_save_figure(self):
        
        if self.current_canva.fig.axes:
            if (self.current_clicked_btn and 
                self.current_clicked_btn.isChecked()):
                    self.current_clicked_btn.click()
                    self.current_clicked_btn = None
#            将画布变形成合适的尺寸
            self.current_fig_win.setWidgetResizable(False)
            self.on_saving_fig = True
            if type(self.current_canva) == StackAxisPlotCanvas:
                self.current_canva.visible_axis_sel_status(False)
            self.current_canva.adjust_savefig()
            
#            保存变形后的画布
            self.current_canva.toolbar.save_figure()
            self.on_saving_fig = False
            if type(self.current_canva) == StackAxisPlotCanvas:
                self.current_canva.visible_axis_sel_status(True)
            
#            将画布还原回查看状态下的尺寸
            self.adjust_fig_win()
            self.current_canva.adjust_figure()
            
    def slot_close_tab(self, index : int):
        
        message = QMessageBox.warning(self,
                      QCoreApplication.translate('PlotWindow', '关闭'),
                      QCoreApplication.translate('PlotWindow',
                                        '''<p>确定要关闭吗？'''),
                      QMessageBox.Yes | QMessageBox.No)
        if (message == QMessageBox.Yes):
            self.tab_widget_figure.removeTab(index)
            if self.tab_widget_figure.count() == 0:
                self.slot_add_ma_fig()
                
            
    def slot_send_status(self, message : str, timeout : int):
        
        self.signal_send_status.emit(message, timeout)
        
#    def slot_save_interval_data(self):
#        
#        self.current_canva.slot_sel_function(self._current_files)
        
    def slot_fig_win_change(self, index):
        
        if index >= 0:
            if self.button_pan.isChecked():
                self.button_pan.click()
            if self.button_zoom.isChecked():
                self.button_zoom.click()
            if self.button_get_paravalue.isChecked():
                self.button_get_paravalue.click()
            self.diconnect_cfw_sink_signal()
            self.current_canva.slot_disconnect()
            self.current_fig_win = self.tab_widget_figure.currentWidget()
            self.current_canva = self.current_fig_win.canva
            self.connect_cfw_sink_signal()
            self.tab_widget_figure.setCurrentIndex(index)
            
            self.current_count_axes = self.current_canva.count_axes
            if type(self.current_canva) == StackAxisPlotCanvas:
                self.button_zoom.setEnabled(False)
                self.button_back.setEnabled(False)
                self.button_forward.setEnabled(False)
            else:
                self.button_zoom.setEnabled(True)
                self.button_back.setEnabled(True)
                self.button_forward.setEnabled(True)
            if type(self.current_canva) == SingleAxisPlotCanvas:
                self.button_get_paravalue.setEnabled(False)
                self.button_sel_data_inter.setEnabled(False)
            else:
                self.button_get_paravalue.setEnabled(True)
                self.button_sel_data_inter.setEnabled(True)
    
#    def slot_add_sa_fig(self):
#        
##        禁止直接拖入绘图区域方式画图
#        self.tab_widget_figure.setEnabled(False)
#
#        uxplot_dialog = ParaSetup_Dialog(self)
##        将dialog accept函数发出的信号连接画图函数
#        uxplot_dialog.signal_accept.connect(self.slot_single_plot)
#        uxplot_dialog.rejected.connect(self.slot_enable_figure)
#        uxplot_dialog.set_maindata(self._current_files, self._data_dict)
#        uxplot_dialog.show()
#        
#        
#    def slot_enable_figure(self):
#        
#        self.tab_widget_figure.setEnabled(True)
#    
#    def slot_single_plot(self, tuple_info):
#        
#        self.tab_widget_figure.setEnabled(True)
#        dictdata, sorted_paras, xpara = tuple_info
#        if xpara:
#            sa_fig_win = FigureWindow(self.tab_widget_figure, 'single_axis_fig')
#            self.tab_widget_figure.addTab(sa_fig_win,
#                                          QIcon(CONFIG.ICON_SINGLE_AXIS),
#                                          QCoreApplication.translate('PlotWindow',
#                                                                     '单坐标图'))
#            self.slot_fig_win_change(self.tab_widget_figure.indexOf(sa_fig_win))
#            sa_fig_win.canva.signal_progress.connect(self.set_value)
#            self.slot_plot(tuple_info)
#        else:
#            sa_fig_win = FigureWindow(self.tab_widget_figure, 'single_axis_xtime_fig')
#            self.tab_widget_figure.addTab(sa_fig_win,
#                                          QIcon(CONFIG.ICON_SINGLE_AXIS),
#                                          QCoreApplication.translate('PlotWindow',
#                                                                     '单坐标时间图'))
#            self.slot_fig_win_change(self.tab_widget_figure.indexOf(sa_fig_win))
#            sa_fig_win.canva.signal_progress.connect(self.set_value)
#
#            self.slot_plot(tuple_info)
            
    def slot_add_sa_fig(self):
        
        sa_fig_win = FigureWindow(self.tab_widget_figure, 'single_axis_xtime_fig')
        self.tab_widget_figure.addTab(sa_fig_win,
                                      QIcon(CONFIG.ICON_SINGLE_AXIS),
                                      QCoreApplication.translate('PlotWindow',
                                                                 '单坐标图'))
        self.slot_fig_win_change(self.tab_widget_figure.indexOf(sa_fig_win))
        sa_fig_win.canva.signal_progress.connect(self.set_value)
    
    def slot_add_ma_fig(self):
        
        ma_fig_win = FigureWindow(self.tab_widget_figure, 'fast_plot_fig')
        self.tab_widget_figure.addTab(ma_fig_win,
                                      QIcon(CONFIG.ICON_MULT_AXIS),
                                      QCoreApplication.translate('PlotWindow',
                                                                 '多坐标图'))
        self.slot_fig_win_change(self.tab_widget_figure.indexOf(ma_fig_win))
        ma_fig_win.canva.signal_progress.connect(self.set_value)
        
    def slot_add_stack_fig(self):
        
        stack_fig_win = FigureWindow(self.tab_widget_figure, 'stack_axis_fig')
        self.tab_widget_figure.addTab(stack_fig_win,
                                      QIcon(CONFIG.ICON_STACK_AXIS),
                                      QCoreApplication.translate('PlotWindow',
                                                                 '重叠图'))
        self.slot_fig_win_change(self.tab_widget_figure.indexOf(stack_fig_win))
        stack_fig_win.canva.signal_progress.connect(self.set_value)
        
    def slot_add_sut_fig(self):
        
        sut_fig_win = FigureWindow(self.tab_widget_figure, 'single_axis_fig')
        self.tab_widget_figure.addTab(sut_fig_win,
                                      QIcon(CONFIG.ICON_SINGLE_UT_AXIS),
                                      QCoreApplication.translate('PlotWindow',
                                                                 '散点图'))
        self.slot_fig_win_change(self.tab_widget_figure.indexOf(sut_fig_win))
        sut_fig_win.canva.signal_progress.connect(self.set_value)
        
#    绘制非时间轴的图
#    def slot_add_ux_fig(self):
#        
#        ux_fig_win = FigureWindow(self.tab_widget_figure, 'custom_axis_fig')
##        禁止直接拖入绘图区域方式画图
#        ux_fig_win.setAcceptDrops(False)
#        self.tab_widget_figure.addTab(ux_fig_win,
#                                      QIcon(CONFIG.ICON_MULT_AXIS),
#                                      QCoreApplication.translate('PlotWindow',
#                                                                 '自定义坐标图'))
#        self.slot_fig_win_change(self.tab_widget_figure.indexOf(ux_fig_win))
#        ux_fig_win.canva.signal_progress.connect(self.set_value)
#        uxplot_dialog = ParaSetup_Dialog(ux_fig_win.canva)
#        uxplot_dialog.set_maindata(self._current_files, self._data_dict)
#        uxplot_dialog.show()
##        将dialog accept函数发出的信号连接画图函数
#        uxplot_dialog.signal_accept.connect(self.slot_plot)
        
    def slot_add_text(self):
        
        if self.button_add_text.isChecked():
#            保证功能冲突的按钮不能同时处于按下状态
            if (self.current_clicked_btn and 
                self.current_clicked_btn != self.button_add_text and 
                self.current_clicked_btn.isChecked()):
                    self.current_clicked_btn.click()
            self.current_clicked_btn = self.button_add_text
            
            self.current_canva.slot_add_annotation()
        else:
            self.current_canva.slot_disconnect()
            
    def slot_uncheck_add_artist_btn(self, flag):
        
        if flag == 'text' and self.button_add_text.isChecked():
            self.button_add_text.setChecked(False)
        if flag == 'hline' and self.button_add_hl.isChecked():
            self.button_add_hl.setChecked(False)
        if flag == 'vline' and self.button_add_vl.isChecked():
            self.button_add_vl.setChecked(False)
        if flag == 'line' and self.button_add_line.isChecked():
            self.button_add_line.setChecked(False)
        if flag == 'vspan' and self.button_sel_data_inter.isChecked():
            self.button_sel_data_inter.setChecked(False)
    
    def slot_add_hline(self):
        
        if self.button_add_hl.isChecked():
#            保证功能冲突的按钮不能同时处于按下状态
            if (self.current_clicked_btn and 
                self.current_clicked_btn != self.button_add_hl and 
                self.current_clicked_btn.isChecked()):
                    self.current_clicked_btn.click()
            self.current_clicked_btn = self.button_add_hl
            
            self.current_canva.slot_add_mark_hline()
        else:
            self.current_canva.slot_disconnect()
    
    def slot_add_vline(self):
        
        if self.button_add_vl.isChecked():
#            保证功能冲突的按钮不能同时处于按下状态
            if (self.current_clicked_btn and 
                self.current_clicked_btn != self.button_add_vl and 
                self.current_clicked_btn.isChecked()):
                    self.current_clicked_btn.click()
            self.current_clicked_btn = self.button_add_vl
            
            self.current_canva.slot_add_mark_vline()
        else:
            self.current_canva.slot_disconnect()
    
    def slot_add_line(self):
        
        if self.button_add_line.isChecked():
#            保证功能冲突的按钮不能同时处于按下状态
            if (self.current_clicked_btn and 
                self.current_clicked_btn != self.button_add_line and 
                self.current_clicked_btn.isChecked()):
                    self.current_clicked_btn.click()
            self.current_clicked_btn = self.button_add_line
            
            self.current_canva.slot_add_arb_markline()
        else:
            self.current_canva.slot_disconnect()
    
    def slot_sel_data_inter(self):
        
        if self.button_sel_data_inter.isChecked():
#            保证功能冲突的按钮不能同时处于按下状态
            if (self.current_clicked_btn and 
                self.current_clicked_btn != self.button_sel_data_inter and 
                self.current_clicked_btn.isChecked()):
                    self.current_clicked_btn.click()
            self.current_clicked_btn = self.button_sel_data_inter
            
            self.current_canva.slot_sel_data_inter()
        else:
            self.current_canva.slot_release_data_inter()
            
    def slot_sel_plot_temp(self):
        
        if self.current_canva.fig.axes:
            dialog = SelectPlotTemplateDialog(self)
            return_signal = dialog.exec_()
            if (return_signal == QDialog.Accepted):
                if dialog.sel_temp:
                    self.current_canva.apply_plot_temp(dialog.sel_temp)
        else:
            QMessageBox.information(self,
                                    QCoreApplication.translate('PlotWindow', '模板应用提示'),
                                    QCoreApplication.translate('PlotWindow', '尚未绘图...'))
            
#    实现按下Esc键后当前操作取消的功能
    def keyPressEvent(self, event : QKeyEvent):
        
        if event.key() == Qt.Key_Escape and self.current_clicked_btn:
            if self.current_clicked_btn.isChecked():
                self.current_clicked_btn.click()

# =============================================================================
# 功能函数模块
# =============================================================================
                
    
    
# =============================================================================
# 汉化
# =============================================================================
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('PlotWindow', 'Plot'))
        self.button_home.setToolTip(_translate('PlotWindow', '原始大小'))
        self.button_pan.setToolTip(_translate('PlotWindow', '移动与缩放'))
        self.button_zoom.setToolTip(_translate('PlotWindow', '框选缩放'))
#        self.button_plot_setting.setToolTip(_translate('PlotWindow', '绘图设置'))
#        self.button_config.setToolTip(_translate('PlotWindow', '画布设置'))
#        self.button_edit.setToolTip(_translate('PlotWindow', '图表设置'))
        self.button_forward.setToolTip(_translate('PlotWindow', '前进'))
        self.button_back.setToolTip(_translate('PlotWindow', '后退'))
        self.button_save.setToolTip(_translate('PlotWindow', '保存'))
#        self.button_save_temp.setToolTip(_translate('PlotWindow', '保存模板'))
#        self.button_sel_temp.setToolTip(_translate('PlotWindow', '选择模板'))
        self.button_clear_canvas.setToolTip(_translate('PlotWindow', '清空画布'))
        self.button_get_paravalue.setToolTip(_translate('PlotWindow', '取参数值'))
#        self.button_add_sa_fig.setToolTip(_translate('PlotWindow', '单坐标图'))
#        self.button_add_ma_fig.setToolTip(_translate('PlotWindow', '多坐标图'))
#        self.button_add_sta_fig.setToolTip(_translate('PlotWindow', '重叠图'))
#        self.button_add_ux_fig.setToolTip(_translate('PlotWindow', '自定义坐标图'))
        self.button_add_text.setToolTip(_translate('PlotWindow', '添加文字标注'))
        self.button_add_hl.setToolTip(_translate('PlotWindow', '添加水平标记线'))
        self.button_add_vl.setToolTip(_translate('PlotWindow', '添加垂直标记线'))
        self.button_add_line.setToolTip(_translate('PlotWindow', '添加任意标记线'))
        self.button_save_temp.setToolTip(_translate('PlotWindow', '保存绘图模板'))
        self.button_sel_temp.setToolTip(_translate('PlotWindow', '选择绘图模板'))
        self.button_sel_data_inter.setToolTip(_translate('PlotWindow', '选择数据段'))
        
#        self.group_box_time_interval.setTitle(_translate('PlotWindow', '时间查看器'))
#        self.tool_btn_time_interval.setText(_translate('PlotWindow', '...'))
#        self.tool_btn_time.setText(_translate('PlotWindow', '...'))
#        self.group_box_time.setTitle(_translate('PlotWindow', '参数值'))
#        self.label_time.setText(_translate('PlotWindow', '00:00:00.000'))
#        item = self.table_widget_value.horizontalHeaderItem(0)
#        item.setText(_translate('PlotWindow', '参数名'))
#        item = self.table_widget_value.horizontalHeaderItem(1)
#        item.setText(_translate('PlotWindow', '参数值'))
