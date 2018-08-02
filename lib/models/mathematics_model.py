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
import re
import pandas as pd
# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtWidgets import (QPlainTextEdit, QMessageBox, QAction, QDialog,
                             QMenu)
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QTextCursor
from PyQt5.QtCore import Qt, QRegExp, QCoreApplication, pyqtSignal

# =============================================================================
# Package views imports
# =============================================================================
from models.datafile_model import Normal_DataFile
from views.custom_dialog import SelParasDialog

#用于将特定字符加高亮
class Highlighter(QSyntaxHighlighter):
   
    def __init__(self, parent = None, paras : list = None):
        
        super().__init__(parent)
        
#        定义参数这类字符的高亮格式
        self.para_format = QTextCharFormat()
        self.para_format.setForeground(Qt.blue)
#        self.para_format.setFontItalic(True)
        
        self.highlight_rules = []
#        定义需要高亮的参数字符
        for para in paras:
            pattern = QRegExp(r'\b' + para + r'\b')
            self.highlight_rules.append((pattern, self.para_format))

#    重载函数  
    def highlightBlock(self, text : str):

        for rule in self.highlight_rules:
            expr = QRegExp(rule[0])
            index = expr.indexIn(text)
            while index >= 0:
                length = expr.matchedLength()
                self.setFormat(index, length, rule[1])
                index = expr.indexIn(text, index + length)

class MathematicsEditor(QPlainTextEdit):

    signal_compute_result = pyqtSignal(pd.DataFrame)
    
    def __init__(self, parent = None):
        
        super().__init__(parent)

        self._current_files = []
#        存储上一条语句
        self.pre_exper = ''
        self.RESERVED = 'RESERVED'
        self.PARA = 'PARA'
        self.VAR = 'VAR'
        self.INT = 'INT'
        self.FLOAT = 'FLOAT'
#        目前，只允许进行四则运算
        self.token_exprs = [
#                前两个表达式匹配空格和注释
                ('\s+', None),
                ('\=', self.RESERVED),
                ('\(', self.RESERVED),
                ('\)', self.RESERVED),
                ('\+', self.RESERVED),
                ('\-', self.RESERVED),
                ('\*', self.RESERVED),
                ('\/', self.RESERVED),
                ('[0-9]+\.[0-9]+', self.FLOAT),
                ('[0-9]+', self.INT),
                (r'[A-Za-z][A-Za-z0-9_]*', self.VAR)]
#        为以后开发解释器时使用
#        self.expression_consist_of_tokens = []
        self.paras_on_expr = []
        
        self.setup()
    
    def setup(self):
        
#        添加输入标志，并把光标移动到最后
        self.setPlainText('>>')
        text_cursor = self.textCursor()
        text_cursor.movePosition(QTextCursor.End)
        self.setTextCursor(text_cursor)
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)
#        添加右键动作
        self.action_add_para = QAction(self)
        self.action_add_para.setText(QCoreApplication.
                                   translate('MathematicsEditor', '添加参数'))
        self.action_pre_exper = QAction(self)
        self.action_pre_exper.setText(QCoreApplication.
                                      translate('MathematicsEditor', '上一条表达式'))
        self.action_clear_editor = QAction(self)
        self.action_clear_editor.setText(QCoreApplication.
                                         translate('MathematicsEditor', '清空所有输入'))
        
        self.customContextMenuRequested.connect(self.conmandline_context_menu)
        self.action_add_para.triggered.connect(self.slot_add_para)
        self.action_clear_editor.triggered.connect(self.slot_clear)
        self.action_pre_exper.triggered.connect(self.slot_insert_pre_exper)
        
#        判断用户是在哪里输入文字，只有在当前textblock内才能输入
        self.cursorPositionChanged.connect(self.slot_cursor_pos)
        self.blockCountChanged.connect(self.slot_exec_block)

# =============================================================================
# slots模块
# =============================================================================        
    def keyPressEvent(self, event):
        
#        Qt的enter与事件的enter不知道为什么差了个1
#        之所以要重写按下enter后的事件，是为了保证用户在表达式中使用enter也能执行整行代码
        if event.key() + 1 == Qt.Key_Enter:
            text_cursor = self.textCursor()
            text_cursor.movePosition(QTextCursor.End)
            self.setTextCursor(text_cursor)
        QPlainTextEdit.keyPressEvent(self, event)
    
    def slot_cursor_pos(self):
        
        document = self.document()
#        文档最后的textblock
        block_on_doc_last = document.lastBlock()        
        text_cursor = self.textCursor()
#        光标所在的textblock
        block_on_cursor = text_cursor.block()
#        如果两个block不一样则将光标移到文档最后
        if block_on_doc_last != block_on_cursor:
            text_cursor.movePosition(QTextCursor.End)
#            不允许光标移动到输入标志'>>'里
        elif text_cursor.positionInBlock() < 2:
            text = block_on_cursor.text()
            if (len(text) >= 2):
                if(text[1] == '>'):
                    text_cursor.setPosition(block_on_cursor.position() + 2)
#                为避免删除输入标志
                else:
                    text_cursor.setPosition(block_on_cursor.position() + 1)
                    text_cursor.insertText('>')
#            回车后创建输入标志
            else:
                text_cursor.insertText('>')
        self.setTextCursor(text_cursor)
        
    def slot_exec_block(self, count):
        
#        经过slot_cursor_pos和keyPressEvent函数，已保证了MATLAB那种代码交互效果
#        所以当blockcount变化时，当前的block是新输入block，前一个block是需要执行的代码
        document = self.document()
        current_block = document.lastBlock()
        exec_block = current_block.previous()
        exec_text = exec_block.text()
        if (len(exec_text) > 2):
#            剔除输入标志'>>'
            exec_text = exec_text[2 : ]
            self.pre_exper = exec_text
#            解析exec_text，如果满足要求，则执行运算
            if self.lex(exec_text) and self.paras_on_expr:
                reg_df = self.pretreat_paras()
#                将参数的数据读入内存
                for paraname in self.paras_on_expr:
                    exper = paraname + ' = reg_df[\'' + paraname + '\']'
                    exec(exper)
                try:
#                    注意此时result是series对象
                    result = eval(exec_text)
#                    判断结果是否仍然是时间序列
                    if len(result) == len(reg_df):
                        df_result = pd.DataFrame({'Time' : reg_df.iloc[:, 0], 
                                                  'Result': result}, columns = ['Time', 'Result'])
#                    否则认为是一个数
                    else:
                        df_result = pd.DataFrame({'Label' : 1,
                                                  'Result': result}, columns = ['Label', 'Result'])
                    self.signal_compute_result.emit(df_result)
                except:
                    QMessageBox.information(self,
                            QCoreApplication.translate("MathematicsEditor", "提示"),
                            QCoreApplication.translate("MathematicsEditor", '无法执行这条语句'))
            else:
                QMessageBox.information(self,
                        QCoreApplication.translate("MathematicsEditor", "提示"),
                        QCoreApplication.translate("MathematicsEditor", '无法执行这条语句'))

    def conmandline_context_menu(self, pos):
        
        menu = QMenu(self)
        menu.addActions([self.action_add_para,
                         self.action_pre_exper,
                         self.action_clear_editor])
        if self.pre_exper:
            self.action_pre_exper.setEnabled(True)
        else:
            self.action_pre_exper.setEnabled(False)
        menu.exec_(self.mapToGlobal(pos))

    def slot_add_para(self):
        
#        采用单选模式
        dialog = SelParasDialog(self, self._current_files, 0)
        return_signal = dialog.exec_()
        if (return_signal == QDialog.Accepted):
            paras = dialog.get_list_sel_paras()
            if paras:
                self.insertPlainText(paras[0])
                    
    def slot_clear(self):
        
        self.clear()
        
    def slot_insert_pre_exper(self):
        
        if self.pre_exper:
            text_cursor = self.textCursor()
            text_cursor.insertText(self.pre_exper)
            self.setTextCursor(text_cursor)
            
    def slot_update_current_files(self, files : list):
        
        self._current_files = files
        paras = []
        for file in files:
            normal_file = Normal_DataFile(file)
            paras += normal_file.paras_in_file
        if paras:
#            更新需要高亮的参数
            self.highlighter = Highlighter(self.document(), paras)
            token_exprs = [
    #                前两个表达式匹配空格和注释
                    ('\s+', None),
                    ('\=', self.RESERVED),
                    ('\(', self.RESERVED),
                    ('\)', self.RESERVED),
                    ('\+', self.RESERVED),
                    ('\-', self.RESERVED),
                    ('\*', self.RESERVED),
                    ('\/', self.RESERVED),
                    ('[0-9]+\.[0-9]+', self.FLOAT),
                    ('[0-9]+', self.INT)]
            
            for para in paras:
                token_exprs.append((para, self.PARA))
    #        先匹配参数名，如果不是参数再认为是变量
            token_exprs.append((r'[A-Za-z][A-Za-z0-9_]*', self.VAR))
            self.token_exprs = token_exprs
                    
# =============================================================================
# 功能函数模块   
# =============================================================================            
#    需要保证charaters非空，找到这个charaters中包含的参数并且保证只执行taoken_exprs限制的运算
    def lex(self, charaters):
        
        pos = 0
        paranames = []
        while pos < len(charaters):
            match = None
            for token_expr in self.token_exprs:
                pattern, tag = token_expr
                regex = re.compile(pattern)
                match = regex.match(charaters, pos)
                if match:
                    text = match.group(0)
#                    if tag:
                    if (tag == 'PARA') and not(text in paranames):
                        paranames.append(text)
                    break
            if not match:
                QMessageBox.information(self,
                        QCoreApplication.translate("MathematicsEditor", "提示"),
                        QCoreApplication.translate("MathematicsEditor", '非法字符: %s' % charaters[pos]))
#                self.expression_consist_of_tokens = []
                self.paras_on_expr = []
                return False
            else:
                pos = match.end(0)
#        self.expression_consist_of_tokens = tokens
        self.paras_on_expr = paranames
        return True
    
    def dict_current_files(self):
            
        dict_files = {}
        if self._current_files:
            for file_dir in self._current_files:
                normal_file = Normal_DataFile(file_dir)
                dict_files[file_dir]= normal_file.paras_in_file
        return dict_files
    
#    将参数读入内存中，并进行时间同步处理，返回一个dataframe
    def pretreat_paras(self):
        
        df_list = []
        dict_files = self.dict_current_files()
#        因为self.paras_on_expr只是一个参数列表，所以要先将其规整下，方便按文件读取
        dict_paras = {}
        for para in self.paras_on_expr:
            for file_dir in dict_files:
                if para in dict_files[file_dir]:
                    if file_dir in dict_paras:
                        dict_paras[file_dir].append(para)
                    else:
                        dict_paras[file_dir] = []
                        dict_paras[file_dir].append(para)
                    break
#        从文件中读取参数数据，并在不同文件读出来的dataframe中第一列加入时间
        for file_dir in dict_paras:
            file = Normal_DataFile(file_dir)
            dict_paras[file_dir].insert(0, file.paras_in_file[0])
            df = file.cols_input(file_dir, dict_paras[file_dir], '\s+')
            df_list.append(df)
            
        df_all = pd.concat(df_list,axis = 1,join = 'outer',
                           ignore_index = False)
        return df_all