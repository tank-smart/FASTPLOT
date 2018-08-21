# -*- coding: utf-8 -*-

#from PyQt5.QtGui import QIcon
import sys
import os.path as osp
import matplotlib

SETUP_DIR = osp.abspath(osp.join(osp.dirname(sys.argv[0]), osp.pardir))
FONT_MSYH = matplotlib.font_manager.FontProperties(
                fname = SETUP_DIR + r'\data\fonts\msyh.ttf',
                size = 8)

ICON_WINDOW = SETUP_DIR + r'\lib\icon\window.png'

ICON_OPEN = SETUP_DIR + r'\lib\icon\open_datafile.ico'
ICON_OPEN_NORDATA = SETUP_DIR + r'\lib\icon\nor_data.ico'
ICON_EXPORT = SETUP_DIR + r'\lib\icon\export.ico'
ICON_EIXT = SETUP_DIR + r'\lib\icon\exit.png'
ICON_MATHEMATICS = SETUP_DIR + r'\lib\icon\caculator.ico'
ICON_DATA_ANA = SETUP_DIR + r'\lib\icon\dataanalysis.ico'
ICON_DATA_PROC = SETUP_DIR + r'\lib\icon\data_process.ico'
ICON_DATA_SIFT = SETUP_DIR + r'\lib\icon\data_sift.ico'
ICON_DATA_MAN = SETUP_DIR + r'\lib\icon\datamanage.ico'
ICON_PARA_TEMP = SETUP_DIR + r'\lib\icon\para_temp.ico'
ICON_PARA_DICT = SETUP_DIR + r'\lib\icon\para_dict.ico'
ICON_PANELS = SETUP_DIR + r'\lib\icon\panels.ico'
ICON_SETTING = SETUP_DIR + r'\lib\icon\setting.ico'
ICON_ABOUT = SETUP_DIR + r'\lib\icon\information.png'
ICON_PLOT = SETUP_DIR + r'\lib\icon\quick_plot.ico'
ICON_PLOT_SETTING = SETUP_DIR + r'\lib\icon\plot_setting.ico'
ICON_CURVE = SETUP_DIR + r'\lib\icon\curve.ico'
ICON_TIME = SETUP_DIR + r'\lib\icon\time.ico'

ICON_FILE = SETUP_DIR + r'\lib\icon\datafile.png'
ICON_FILE_EXPORT = SETUP_DIR + r'\lib\icon\file_export.ico'
ICON_PARA = SETUP_DIR + r'\lib\icon\parameter.png'
ICON_MATH_RESULT = SETUP_DIR + r'\lib\icon\math_result.ico'
ICON_ANA_RESULT = SETUP_DIR + r'\lib\icon\ana_result.ico'

ICON_ADD = SETUP_DIR + r'\lib\icon\add.ico'
ICON_DEL = SETUP_DIR + r'\lib\icon\delete.ico'
ICON_COPY = SETUP_DIR + r'\lib\icon\copy.ico'
ICON_SEL_TEMP = SETUP_DIR + r'\lib\icon\use_template.ico'
ICON_SAVE_TEMP = SETUP_DIR + r'\lib\icon\save_template.ico'
ICON_DATA_ABSTRACT = SETUP_DIR + r'\lib\icon\data_abstract.ico'
ICON_UP = SETUP_DIR + r'\lib\icon\up.ico'
ICON_DOWN = SETUP_DIR + r'\lib\icon\down.ico'

ICON_HOME = SETUP_DIR + r'\lib\icon\home.ico'
ICON_PAN = SETUP_DIR + r'\lib\icon\pan.png'
ICON_ZOOM = SETUP_DIR + r'\lib\icon\zoom.ico'
ICON_EDIT = SETUP_DIR + r'\lib\icon\edit.png'
ICON_CONFIG = SETUP_DIR + r'\lib\icon\config.ico'
ICON_BACK = SETUP_DIR + r'\lib\icon\back.ico'
ICON_FORWARD = SETUP_DIR + r'\lib\icon\forward.ico'
ICON_SAVE = SETUP_DIR + r'\lib\icon\save.ico'
ICON_ADD_LINE_MARK = SETUP_DIR + r'\lib\icon\line_marker.ico'
ICON_TEXT = SETUP_DIR + r'\lib\icon\text.ico'
ICON_CLEAR = SETUP_DIR + r'\lib\icon\clear.ico'
ICON_PARA_VALUE = SETUP_DIR + r'\lib\icon\para_value.ico'

ICON_TEMPLATE = SETUP_DIR + r'\lib\icon\template.ico'