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
                             QMenu, QApplication)
from PyQt5.QtGui import (QSyntaxHighlighter, QTextCharFormat, QTextCursor)
from PyQt5.QtCore import (Qt, QRegExp, QCoreApplication, pyqtSignal)

# =============================================================================
# Package views imports
# =============================================================================
from models.datafile_model import Normal_DataFile, DataFile_Factory, DataFile
from models.data_model import DataFactory
import models.time_model as Time
import views.config_info as CONFIG
from models.analysis_model import DataAnalysis
from views.custom_dialog import SelParasDialog, MathScriptDialog, SelfuncDialog

#用于将特定字符加高亮
class Highlighter(QSyntaxHighlighter):
   
    def __init__(self, parent = None, paras : list = None, funcs : list = None):
        
        super().__init__(parent)
        
#        定义参数这类字符的高亮格式
        self.para_format = QTextCharFormat()
        self.para_format.setForeground(Qt.blue)
#        self.para_format.setFontItalic(True)
        self.func_format = QTextCharFormat()
        self.func_format.setForeground(Qt.magenta)
        
        self.highlight_rules = []
#        定义需要高亮的参数字符
        for para in paras:
            pattern = QRegExp(r'\b' + para + r'\b')
            self.highlight_rules.append((pattern, self.para_format))
 
        for func in funcs:
            pattern = QRegExp(r'\b' + func + r'\b')
            self.highlight_rules.append((pattern, self.func_format))

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
#---------yanhua加    
    signal_clc = pyqtSignal(bool)
#---------yanhua
    
    def __init__(self, parent = None):
        
        super().__init__(parent)

        self._current_files = []
        self._dict_filetype = {}
#        存储上一条语句
#---------        yanhua 加
        self.scope={}
        self.time_df=None
        self.count=0
        self.script_dialog = MathScriptDialog(self)
#----------       yanhua 加结束
        self.pre_exper = ''
        self.RESERVED = 'RESERVED'
        self.PARA = 'PARA'
        self.VAR = 'VAR'
        self.INT = 'INT'
        self.FLOAT = 'FLOAT'
#        目前，只允许进行四则运算
#        self.token_exprs = [
##                前两个表达式匹配空格和注释
#                ('\s+', None),
#                ('\=', self.RESERVED),
#                ('\(', self.RESERVED),
#                ('\)', self.RESERVED),
#                ('\+', self.RESERVED),
#                ('\-', self.RESERVED),
#                ('\*', self.RESERVED),
#                ('\/', self.RESERVED),
#                ('\.', self.RESERVED),
#                ('\,', self.RESERVED),
#                ('\^', self.RESERVED),
#                ('\'', self.RESERVED),
#                ('\:', self.RESERVED),
#                ('\[', self.RESERVED),
#                ('\]', self.RESERVED),
#                ('[0-9]+\.[0-9]+', self.FLOAT),
#                ('[0-9]+', self.INT),
#                (r'[A-Za-z][A-Za-z0-9_]*', self.VAR)]
#        为以后开发解释器时使用
        self.token_exprs = []
#        self.expression_consist_of_tokens = []
        self.paras_on_expr = []
        self.load_desc()
        self.setup()
#---------   yanhua 加
        self.scope_setup()
#---------   yanhua 加
    
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
        self.action_add_func = QAction(self)
        self.action_add_func.setText(QCoreApplication.
                                     translate('MathematicsEditor', '添加函数'))
        self.action_script = QAction(self)
        self.action_script.setText(QCoreApplication.
                                   translate('MathematicsEditor', '计算脚本'))
        self.action_pre_exper = QAction(self)
        self.action_pre_exper.setText(QCoreApplication.
                                      translate('MathematicsEditor', '上一条表达式'))
        self.action_clear_editor = QAction(self)
        self.action_clear_editor.setText(QCoreApplication.
                                         translate('MathematicsEditor', '清空所有输入'))
        
        self.customContextMenuRequested.connect(self.conmandline_context_menu)
        self.action_add_para.triggered.connect(self.slot_add_para)
        self.action_add_func.triggered.connect(self.slot_add_func)
        self.action_script.triggered.connect(self.slot_math_script)
        self.action_clear_editor.triggered.connect(self.slot_clear)
        self.action_pre_exper.triggered.connect(self.slot_insert_pre_exper)
        
#        判断用户是在哪里输入文字，只有在当前textblock内才能输入
        self.cursorPositionChanged.connect(self.slot_cursor_pos)
        self.blockCountChanged.connect(self.slot_exec_block_Test)

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
        
    def slot_exec_block_wxl(self, count):
        
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
                if type(reg_df) == pd.DataFrame:
                    try:
#                        将参数的数据读入内存
                        for paraname in self.paras_on_expr:
                            exper = paraname + ' = reg_df[\'' + paraname + '\']'
                            exec(exper)
#                        注意此时result是series对象
                        result = eval(exec_text)
#                        判断结果是否仍然是时间序列
                        if len(result) == len(reg_df):
                            df_result = pd.DataFrame({'Time' : reg_df.iloc[:, 0], 
                                                      'Result': result}, columns = ['Time', 'Result'])
#                        否则认为是一个数
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
                            QCoreApplication.translate("MathematicsEditor", '参数维度不一致'))
            else:
                QMessageBox.information(self,
                        QCoreApplication.translate("MathematicsEditor", "提示"),
                        QCoreApplication.translate("MathematicsEditor", '语法错误'))

#----------------yanhua改
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
#            if self.lex(exec_text) and self.paras_on_expr:
            flag=self.lex(exec_text)
            if flag!=-1:
                if flag==1:
                    reg_df = self.pretreat_paras()
                    self.time_df=reg_df.iloc[:, 0]#注：这边的时间其实并没有什么意义
#                    self.scope['reg_df']=reg_df
                    
    #                将参数的数据读入内存
                    for paraname in self.paras_on_expr:
                        self.scope[paraname]=reg_df[paraname]
#                        exper = paraname + ' = reg_df[\'' + paraname + '\']'
#                        exec(exper,self.scope)
                try:
                    if exec_text.find('=')!=-1:        
                        exec(exec_text,self.scope)
                        result_name=exec_text.split('=')[0]            
                        result=eval(result_name,self.scope)
#                        self.paras_on_expr.append(result_name)
#                        print(result)
                    else:
#                       注意此时result是series对象
                        result = eval(exec_text,self.scope)
                        result_name='Result'+str(self.count+1)
                        if result is not None:
                            self.count = self.count+1
#                       判断结果是否仍然是时间序列
                    if result is not None:
                        
                        if self.time_df is not None and isinstance(result, type(self.time_df)) and (len(result) == len(self.time_df)):
                            
#                            print(self.time_df)
                            df_result = pd.DataFrame({'Time' : self.time_df, 
                                                      result_name: result}, columns = ['Time', result_name])
#                        否则认为是一个数
#                            
                        else:
                            
                            df_result = pd.DataFrame({'Label' : [1],
                                                      result_name: result}, columns = ['Label', result_name])
#                            print(df_result)
                        self.signal_compute_result.emit(df_result)
                    else:
                        pass
                except:
                    QMessageBox.information(self,
                            QCoreApplication.translate("MathematicsEditor", "提示"),
                            QCoreApplication.translate("MathematicsEditor", '无法执行这条语句'))
            else:
                QMessageBox.information(self,
                        QCoreApplication.translate("MathematicsEditor", "提示"),
                        QCoreApplication.translate("MathematicsEditor", '无法执行这条语句'))

    def slot_exec_block_Test(self, count):
        
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
#            if self.lex(exec_text) and self.paras_on_expr:
            flag, exec_text=self.lex(exec_text)
            if flag!=-1:
                if flag==1:
                    self.read_paras()
                    
#                    self.time_treat(self.paras_)
#                    self.scope['reg_df']=reg_df
                    
    #                将参数的数据读入内存
#                    for paraname in self.paras_on_expr:
#                        self.time_df = paraname.index
#                        exper = paraname + ' = reg_df[\'' + paraname + '\']'
#                        exec(exper,self.scope)
                try:
                    
                    if exec_text.find('=')!=-1:        
                        exec(exec_text,self.scope)
                        result_name=exec_text.split('=')[0]            
                        result=eval(result_name,self.scope)
                        
    #                        self.paras_on_expr.append(result_name)
    #                        print(result)
                    else:
    #                       注意此时result是series对象
                        result = eval(exec_text,self.scope)
                        result_name='Result'+str(self.count+1)
                        if result is not None:
                            self.count = self.count+1
                            
    #                       判断结果是否仍然是时间序列
                    if result is not None:
                        
    #                        if self.time_df is not None and isinstance(result, type(self.time_df)) and (len(result) == len(self.time_df)):
                        if isinstance(result, pd.Series) or isinstance(result, pd.DataFrame):
    #                            print(self.time_df)
                            
                            result = result.reset_index()
                            
                            df_result = pd.DataFrame({'Time' : result.iloc[:,0], 
                                                      result_name: result.iloc[:,1]}, columns = ['Time', result_name])
    #                        否则认为是一个数
    #                            
                        else:
                            
                            df_result = pd.DataFrame({'Label' : [1],
                                                      result_name: result}, columns = ['Label', result_name])
    #                            print(df_result)
                        self.signal_compute_result.emit(df_result)
                    else:
                        pass
                except Exception as e:
                    QMessageBox.information(self,
                            QCoreApplication.translate("MathematicsEditor", "错误提示"),
                            QCoreApplication.translate("MathematicsEditor", repr(e)))
            else:
                QMessageBox.information(self,
                        QCoreApplication.translate("MathematicsEditor", "提示"),
                        QCoreApplication.translate("MathematicsEditor", '无法执行这条语句'))

    def read_paras(self):
        
        dict_files = self.dict_current_files()
#        因为self.paras_on_expr只是一个参数列表，所以要先将其规整下，方便按文件读取
        for para in self.paras_on_expr:
            for file_dir in dict_files:
                if para in dict_files[file_dir]:
                    df = DataFactory(file_dir, [para], self._dict_filetype[file_dir])
                    df = df.data.set_index(df.data.columns[0])
                    print(df)
#                    dataframe to series                   
                    para_df = df.iloc[:,0]
#                    para_df = df.data.iloc[:,1]
#                    df_time = df.data.iloc[:,0]
#                    exec('para=para_df',self.scope)
#                    print(para_df.index)
                    self.scope['a'+str(abs(hash(para)))] = para_df

                    
#                    print(para_df)
#                    self.scope[para+'time'] = df_time
                    
        

    def scope_setup(self):
        self.scope['clear']=self.clc
        self.scope['describe'] = self.describe
        self.scope['add']=self.add
        self.scope['sub']=self.sub
        self.scope['mul']=self.mul
        self.scope['div']=self.div
        self.scope['help']=self.help_me()
        self.scope['resample']=self.resample
        self.scope['sqrt']=self.sqrt
        self.scope['init_time']=self.init_time
        self.scope['output']=self.output
        self.scope['combine']=self.combine
#        函数名称列表，用于高亮显示
        self.funcs = self.df_func.iloc[:,0].tolist()
        
#        self.funcs = ['abs','add','sub','mul','div','resample','sqrt','pow',
#                      'init_time','output','.interpolate','.isna','.append']

    def clc(self):
        self.scope={}
        self.scope_setup()
        self.time_df=None
        self.count=0
        self.signal_clc.emit(True)

    def combine(self, left, right, func):
        return left.combine(right, func)
        
    def sqrt(self, series):
        result = pow(series, 0.5)
        return result
    
    def describe(self, series):
        attr = series.describe()
#        print(str(attr))
        return str(attr)

#    忽略时间序列的二元计算装饰器    
    def force_operator(func):
        def wrapper(self, left, right):
            if isinstance(left, pd.Series) and isinstance(right, pd.Series):
                if(len(left)>=len(right)):
                    index=left.index
                else:
                    index=right.index
                
                new_left=left.reset_index(drop=True)
                new_right=right.reset_index(drop=True)
                result = func(self, new_left, new_right)
                result.index = index
            else:
                result = left + right
            return result
        return wrapper

    def add(self, left, right):
        if isinstance(left, pd.Series) and isinstance(right, pd.Series):
        
            if(len(left)>=len(right)):
                index=left.index
            else:
                index=right.index
            
            new_left=left.reset_index(drop=True)
            new_right=right.reset_index(drop=True)
            result=new_left.add(new_right, fill_value=None)
            result.index=index
            
        else:
            result = left+right
        return result
    
    @force_operator
    def sub(self, left, right):
        result = left.sub(right, fill_value=None)
        return result
    
    @force_operator
    def mul(self, left, right):
        result = left.mul(right, fill_value=None)
        return result

    @force_operator    
    def div(self, left, right):
        result = left.div(right, fill_value=None)
        return result
    
    def resample(self, series, freq):
        df_series=series.reset_index()
        df=DataFactory(df_series)
        series_freq=df.sample_frequency
        analysis=DataAnalysis()
        if series_freq>=freq:
            result=analysis.downsample(df_series, freq)
        else:
            result=analysis.upsample(df_series, freq)
#        输出Series
        result=result.set_index(result.columns[0]).iloc[:,0]
        return result

#    时间初始化为从0开始
    def init_time(self, series):
        if isinstance(series, pd.Series):
            QApplication.processEvents()
            df_series = series.reset_index()
            time_format = Time.time_format(df_series.iat[0,0])
            timeseries = pd.to_datetime(df_series.iloc[:,0],format=time_format)
            index_start = Time.str_to_datetime(series.index[0])
            dtime = index_start - Time.str_to_datetime('00:00:00:000')
            timeseries = timeseries - dtime
            df_series.iloc[:,0] = timeseries.apply(lambda x: x.strftime(time_format))
            result=df_series.set_index(df_series.columns[0]).iloc[:,0]
        return result   

    def output(self, result_name = None):
        result = eval(result_name,self.scope)
        if result is not None:
#            result_name = list(dict(result = result).keys())[0]
            
#                        if self.time_df is not None and isinstance(result, type(self.time_df)) and (len(result) == len(self.time_df)):
            if isinstance(result, pd.Series) or isinstance(result, pd.DataFrame):
#                            print(self.time_df)
                
                result = result.reset_index()
                
                df_result = pd.DataFrame({'Time' : result.iloc[:,0], 
                                          result_name: result.iloc[:,1]}, columns = ['Time', result_name])
#                        否则认为是一个数
#                            
            else:
                
                df_result = pd.DataFrame({'Label' : [1],
                                          result_name: result}, columns = ['Label', result_name])
#                            print(df_result)
            self.signal_compute_result.emit(df_result)
        else:
            pass
        
    
    def help_me(self):
        tell_you = \
        """
        add(left, right)    无限制加法，会把较长参数的序列作为结果的时间序列
        parameter.between(left,right)  返回判断left<=series<=right的bool序列
        describe(series)    描述参数信息：包括count,mean,std,min,25%,50%,75%,max
        clear()             清除结果和内存
        parameter.cov(other) 求两个参数序列的协方差
        parameter.corr(other) 求两个参数序列的相关系数
        parameter.sum()       求和
        parameter.pow(other)
        resample(parameter, freq)  升降频
        """
        return tell_you
    
        
            
        
        
#------------yanhua
                
    def conmandline_context_menu(self, pos):
        
        menu = QMenu(self)
        menu.addActions([self.action_add_para,
                         self.action_add_func,
                         self.action_script,
                         self.action_pre_exper,
                         self.action_clear_editor])
        if self.pre_exper:
            self.action_pre_exper.setEnabled(True)
        else:
            self.action_pre_exper.setEnabled(False)
        menu.exec_(self.mapToGlobal(pos))

    def slot_add_para(self):
        
#        采用单选模式
        dialog = SelParasDialog(self, self._current_files, 0, self._dict_filetype)
        return_signal = dialog.exec_()
        if (return_signal == QDialog.Accepted):
            paras = dialog.get_list_sel_paras()
            if paras:
                self.insertPlainText(paras[0])
                
    def slot_add_func(self):
        dialog = SelfuncDialog(self, self.df_func, 0)
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
            
    def slot_update_current_files(self, files : list, dict_filetype : dict):
        
        self._current_files = files
        self._dict_filetype = dict_filetype
        paras = []
        for file in files:
            file_fac = DataFile_Factory(file, **dict_filetype[file])
            paras += file_fac.paras_in_file

#            normal_file = Normal_DataFile(file)
#            paras += normal_file.paras_in_file
        
        if paras:
#            更新需要高亮的参数
            self.highlighter = Highlighter(self.document(), paras, self.funcs)
            self.dialog_highlighter = Highlighter(self.script_dialog.script_edit_win.document(), paras, self.funcs)
#        if self.funcs:
#            
#            self.func_highlighter = Highlighter(self.document(), self.funcs, Qt.magenta)
#            token_exprs = [
#    #                前两个表达式匹配空格和注释
#                    ('\s+', None),
#                    ('\=', self.RESERVED),
#                    ('\(', self.RESERVED),
#                    ('\)', self.RESERVED),
#                    ('\+', self.RESERVED),
#                    ('\-', self.RESERVED),
#                    ('\*', self.RESERVED),
#                    ('\/', self.RESERVED),
#                    ('\.', self.RESERVED),
#                    ('\,', self.RESERVED),
#                    ('\^', self.RESERVED),
#                    ('\'', self.RESERVED),
#                    ('\:', self.RESERVED),
#                    ('\[', self.RESERVED),
#                    ('\]', self.RESERVED),
#                    ('\-', self.RESERVED),
#                    ('[0-9]+\.[0-9]+', self.FLOAT),
#                    ('[0-9]+', self.INT)]
            token_exprs = []
            for para in paras:
               
                token_exprs.append((para, self.PARA))
    #        先匹配参数名，如果不是参数再认为是变量
#            token_exprs.append((r'[A-Za-z][A-Za-z0-9_]*', self.VAR))
            self.token_exprs = token_exprs
    
    def slot_math_script(self):
        
#        self.script_dialog = MathScriptDialog(self)
        return_signal = self.script_dialog.exec_()
        if (return_signal == QDialog.Accepted):
            
#            self.pre_exper = exec_text
#            解析exec_text，如果满足要求，则执行运算
#            if self.lex(exec_text) and self.paras_on_expr:
            flag=self.lex(self.script_dialog.script)
            if flag!=-1:
                if flag==1:
                    self.read_paras()
                    #注：这边的时间其实并没有什么意义
#                    self.time_treat(self.paras_)
#                    self.scope['reg_df']=reg_df
                    
    #                将参数的数据读入内存
#                    for paraname in self.paras_on_expr:
#                        self.time_df = paraname.index
#                        exper = paraname + ' = reg_df[\'' + paraname + '\']'
#                        exec(exper,self.scope)
                try:
                    
                    exec(self.script_dialog.script, self.scope)
                    
                            
#                       判断结果是否仍然是时间序列

                except Exception as e:
                    QMessageBox.information(self,
                            QCoreApplication.translate("MathematicsEditor", "错误提示"),
                            QCoreApplication.translate("MathematicsEditor", repr(e)))
            else:
                QMessageBox.information(self,
                        QCoreApplication.translate("MathematicsEditor", "提示"),
                        QCoreApplication.translate("MathematicsEditor", '无法执行这条语句'))
                    
# =============================================================================
# 功能函数模块   
# =============================================================================            
#    需要保证charaters非空，找到这个charaters中包含的参数并且保证只执行taoken_exprs限制的运算
    def lex_wxl(self, charaters):
        
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

#------------yanhua改    
#    修改返回值为int，表示三种状态：1有合法可载入的参数;0无需要载入的参数;-1非法字符    
    def lex(self, charaters):
        
#        pos = 0
        paranames = []
#        while pos < len(charaters):
        match = None
        for token_expr in self.token_exprs:
            pattern, tag = token_expr
            match = charaters.find(pattern)
#                regex = re.compile(pattern)
#                match = regex.match(charaters, pos)
            if match!=-1:
#                    text = match.group(0)
                text = pattern
#                    if tag:
                if (tag == 'PARA') and not(text in paranames) and str(hash(text)) not in self.scope:
                    paranames.append(text)
                    hash_para = abs(hash(text))
                    new_charaters = charaters.replace(text, 'a'+str(hash_para))
#                        self.dict_hashpara[str(hash_para)] = text
               
#        if match==-1:
#            QMessageBox.information(self,
#                    QCoreApplication.translate("MathematicsEditor", "提示"),
#                    QCoreApplication.translate("MathematicsEditor", '非法字符: %s' % charaters[pos]))
##                self.expression_consist_of_tokens = []
#            self.paras_on_expr = []
#            return (-1,None)
#        else:
#            pos = match.end(0)
#        self.expression_consist_of_tokens = tokens
        self.paras_on_expr = paranames
        if self.paras_on_expr == []:
            return (0,charaters)
        else:
            return (1,new_charaters)
#----------yanhua改
    
    def dict_current_files(self):
            
        dict_files = {}
        if self._current_files and self._dict_filetype:
            for file_dir in self._current_files:
                fac_file = DataFile_Factory(file_dir, **self._dict_filetype[file_dir])
                dict_files[file_dir] = fac_file.paras_in_file
#                normal_file = Normal_DataFile(file_dir)
#                dict_files[file_dir]= normal_file.paras_in_file
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
        first_data = None
        for file_dir in dict_paras:
            if first_data:
                df = DataFactory(file_dir, dict_paras[file_dir], self._dict_filetype[file_dir])
                if df.is_concat(first_data):
                    
                    df_list.append(df.data[df.get_paralist()])
                else:
#                    这里进行同步处理，处理不了返回None
                    return None
            else:
                first_data = DataFactory(file_dir, dict_paras[file_dir], self._dict_filetype[file_dir])
                df_list.append(first_data.data)
            
        df_all = pd.concat(df_list,axis = 1,join = 'outer',
                           ignore_index = False)
        return df_all
    
    def load_desc(self):
        
        try:
            filedir = CONFIG.SETUP_DIR + r'\data\func_desc.txt'
            funcfile = DataFile(filedir, sep='|')
            df_func = funcfile.all_input()
            self.df_func = df_func
        except:
            pass
    
if __name__ == '__main__':
    
    file_dir = r'D:\flightdata\shoufei_AGIdata\FTPD-C919-10101-PD-170505-G-01-000FTE-664003-32_AGI.txt'
    file = Normal_DataFile(file_dir)
    df1 = DataFactory(file_dir, [file.paras_in_file[1]])
    df1 = df1.data.set_index(df1.data.columns[0])                                  
    para_df1 = df1.iloc[:,0]
    df2 = DataFactory(file_dir, [file.paras_in_file[2]])
    df2 = df2.data.set_index(df2.data.columns[0])                                  
    para_df2 = df2.iloc[:,0]
    me = MathematicsEditor()
    result = me.div(para_df1,para_df2)
    result = me.set_t0(para_df1)
    print(result)
    