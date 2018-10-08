# -*- coding: utf-8 -*-

#from PyQt5.QtGui import QIcon
import sys
import os.path as osp
import matplotlib
# =============================================================================
# 软件名
# =============================================================================
SOFTNAME = 'FastPlot(beta 0.1)'
# =============================================================================
# 路径
# =============================================================================
SETUP_DIR = osp.abspath(osp.join(osp.dirname(sys.argv[0]), osp.pardir))
DIR_HELP_DOC = SETUP_DIR + r'\data\docs'
DIR_HELP_VIDEO = SETUP_DIR + r'\data\videos'
# =============================================================================
# 软件设置
# =============================================================================
#默认设置
OPTION = {'dir of importing' : '',
          'data dict scope paralist' : True,
          'data dict scope plot' : True,
          'data dict scope style' : 1,#0-参数名，1-软件标识符(参数名)，2-参数名(软件标识符)
          'work dir' : SETUP_DIR,
          'plot fontsize' : 8,
          'plot fontcolor' : 'black',
          'plot font arrow' : False,
          'plot markline style' : '--',
          'plot markline color' : 'red',
          'plot markline marker' : 'None'}
# =============================================================================
# 字体
# =============================================================================
FONT_MSYH = matplotlib.font_manager.FontProperties(
                fname = SETUP_DIR + r'\data\fonts\msyh.ttf',
                size = 8)
# =============================================================================
# 图标
# =============================================================================
FTCC_LOGO = SETUP_DIR + r'\lib\icon\ftcc.png'

ICON_WINDOW = SETUP_DIR + r'\lib\icon\fastplot.ico'

ICON_ABOUT = SETUP_DIR + r'\lib\icon\information.ico'
ICON_DATA_ABSTRACT = SETUP_DIR + r'\lib\icon\data_abstract.ico'
ICON_ADD_LINE_MARK = SETUP_DIR + r'\lib\icon\line_marker.ico'

ICON_BACK = SETUP_DIR + r'\lib\icon\back.ico'

ICON_CLEAR = SETUP_DIR + r'\lib\icon\clear.ico'

ICON_DATA_MAN = SETUP_DIR + r'\lib\icon\datamanage.ico'
ICON_DATA_PROC = SETUP_DIR + r'\lib\icon\data_process.ico'
ICON_DATA_SIFT = SETUP_DIR + r'\lib\icon\data_sift.ico'
ICON_DEL = SETUP_DIR + r'\lib\icon\delete.ico'
ICON_DOWN = SETUP_DIR + r'\lib\icon\down.ico'

ICON_EIXT = SETUP_DIR + r'\lib\icon\exit.png'

ICON_FILE = SETUP_DIR + r'\lib\icon\datafile.ico'
ICON_FILE_EXPORT = SETUP_DIR + r'\lib\icon\file_export.ico'
ICON_FORWARD = SETUP_DIR + r'\lib\icon\forward.ico'

ICON_HLINE = SETUP_DIR + r'\lib\icon\h_line.ico'
ICON_HOME = SETUP_DIR + r'\lib\icon\home.ico'

ICON_LINE = SETUP_DIR + r'\lib\icon\line.ico'
ICON_MATHEMATICS = SETUP_DIR + r'\lib\icon\caculator.ico'
ICON_MATH_RESULT = SETUP_DIR + r'\lib\icon\math_result.ico'
ICON_MULT_AXIS = SETUP_DIR + r'\lib\icon\mult_axis.ico'

ICON_OPEN_NORDATA = SETUP_DIR + r'\lib\icon\nor_data.ico'

ICON_PAN = SETUP_DIR + r'\lib\icon\pan.ico'
ICON_PANELS = SETUP_DIR + r'\lib\icon\panels.ico'
ICON_PARA = SETUP_DIR + r'\lib\icon\parameter.ico'
ICON_PARA_DICT = SETUP_DIR + r'\lib\icon\para_dict.ico'
ICON_PARA_TEMP = SETUP_DIR + r'\lib\icon\para_temp.ico'
ICON_PARA_VALUE = SETUP_DIR + r'\lib\icon\para_value.ico'
ICON_PLOT = SETUP_DIR + r'\lib\icon\quick_plot.ico'
#ICON_PLOT_SETTING = SETUP_DIR + r'\lib\icon\plot_setting.ico'

ICON_SAVE = SETUP_DIR + r'\lib\icon\save.ico'
ICON_SAVE_TEMP = SETUP_DIR + r'\lib\icon\save_template.ico'
ICON_SEL_TEMP = SETUP_DIR + r'\lib\icon\use_template.ico'
ICON_SETTING = SETUP_DIR + r'\lib\icon\setting.ico'
ICON_SINGLE_AXIS = SETUP_DIR + r'\lib\icon\sin_axis.ico'
ICON_STACK_AXIS = SETUP_DIR + r'\lib\icon\stack_axis.ico'

ICON_TEMPLATE = SETUP_DIR + r'\lib\icon\template.ico'
ICON_TEXT = SETUP_DIR + r'\lib\icon\text.ico'
ICON_TIME = SETUP_DIR + r'\lib\icon\time.ico'

ICON_UP = SETUP_DIR + r'\lib\icon\up.ico'

ICON_VLINE = SETUP_DIR + r'\lib\icon\v_line.ico'

ICON_ZOOM = SETUP_DIR + r'\lib\icon\zoom.ico'
