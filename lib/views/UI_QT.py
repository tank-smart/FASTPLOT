# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 15:11:48 2018

@author: Yan Hua
"""
from PyQt5 import QtWidgets  
#from ReadTree import *  
from MainUI import *
from input_function import *
from PyQt5.QtWidgets import QFileDialog, QAbstractItemView
from plot import *  
      
class MyWindow(QtWidgets.QMainWindow,Ui_MainWindow):  
    def __init__(self):  
        super(MyWindow,self).__init__()  
        self.setupUi(self)
       # self.filename=None
        self.dict_select={}
       # self.para=None
        self.dict_root={}
        self.dict_timename={}
        self.createRightMenu()
    def read_one(self):  #optional [read(),read_one()]
        file_name, ok=QFileDialog.getOpenFileName(self,'读取','D:/')
        if file_name:
            para_name=header_input(file_name,sep='\s+') #DataFrame: input the first row of data file
            pos=file_name.rindex('/')
            root_name=file_name[pos+1:]  #select filename without path
            self.treeWidget.setSelectionMode(QAbstractItemView.ExtendedSelection) #set multi select mode
            root=QtWidgets.QTreeWidgetItem(self.treeWidget) #QTreeWidgetItem object: root
            root.setText(0,root_name) #set text of treewidget
            para_list=para_name.values.tolist()[0] #ndarray to list
            for i in range(len(para_list)):
                child=QtWidgets.QTreeWidgetItem(root)  #child of root
                child.setText(0,para_list[i])
#            self.filename=file_name  #property filename for other function use
#            self.name_time=para_list[0] #name of time column
            #self.dict_timename[root]=para_list[0]    
            self.dict_root[root]=file_name #a root vs a file_name
            self.dict_timename[file_name]=para_list[0]
            
    def read(self):  #read multifiles
        file_name, ok=QFileDialog.getOpenFileNames(self,'Load','D:/')  #multi files input
        if file_name:  #file_name is a list
            for each_file in file_name:
                para_name=header_input(each_file,sep='\s+') #DataFrame: input the first row of data file
                pos=each_file.rindex('/')
                root_name=each_file[pos+1:]  #select filename without path
                self.treeWidget.setSelectionMode(QAbstractItemView.ExtendedSelection) #set multi select mode
                root=QtWidgets.QTreeWidgetItem(self.treeWidget) #QTreeWidgetItem object: root
                root.setText(0,root_name) #set text of treewidget
                para_list=para_name.values.tolist()[0] #ndarray to list
                for i in range(len(para_list)):
                    child=QtWidgets.QTreeWidgetItem(root)  #child of root
                    child.setText(0,para_list[i])
    #            self.filename=file_name  #property filename for other function use
    #            self.name_time=para_list[0] #name of time column
                #self.dict_timename[root]=para_list[0]    
                self.dict_root[root]=each_file #a root vs a file_name 
                self.dict_timename[each_file]=para_list[0]
            
    def createRightMenu(self):  
  
        # Create right menu for treewidget 
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  
        self.treeWidget.customContextMenuRequested.connect(self.showRightMenu)    
        self.rightMenu = QtWidgets.QMenu(self.treeWidget)  
  
        self.action1=self.rightMenu.addAction("Plot")  
        self.action2=self.rightMenu.addAction("Subplot")  
        self.action3=self.rightMenu.addAction("delete")  
        self.action4=self.rightMenu.addAction("save")  
  
        self.rightMenu.addSeparator()  
        self.action1.triggered.connect(self.plot)
        self.action2.triggered.connect(self.subplot)
        self.action4.triggered.connect(self.save)
        # self.rightMenu.addAction(self.RenameAct)  
        
    def showRightMenu(self, pos):    
          
        self.rightMenu.exec_(QtGui.QCursor.pos()) #在鼠标位置显示  
            
    def getitem(self, item,column):
#        pos=self.filename.rindex('/')
#        root_name=self.filename[pos+1:]
        Item_list=self.treeWidget.selectedItems()  #return the selected item as a list
        #self.select_list=[]
        self.dict_select={}  #empty in each getitem
        for ii in Item_list:
            if not self.dict_root.has_key(ii): #root item select won't have ii.parent() 
                filename=self.dict_root[ii.parent()]  #QTreeWidgetItem.parent(): parent node
                pos=filename.rindex('/')
                root_name=filename[pos+1:]
                if ii.text(0)!=root_name:
    #          filename=self.dict_root[ii.parent()] #QTreeWidgetItem.parent(): parent node
                    if not self.dict_select.has_key(filename):
                        self.dict_select[filename]=[]
                    self.dict_select[filename].append(ii.text(0).encode())  #all use str here(py2
               # self.select_list.append(ii.text(0).encode())  #all use str here(py2)
        #self.select_list.insert(0,self.name_time)  #insert the "time" column
            
    #        if item.text(0)!=root_name:
    #            self.para=[item.text(0).encode()]  #self.para for plot all use str here
    #        else:
    #            self.para=None
    
    def display(self):
        if len(self.dict_select)>0:
            horizontalHeader=[]
            df_list=[]        
            for key in self.dict_select:
                horizontalHeader +=self.dict_select[key]
                df_key=cols_input(key,self.dict_select[key],sep='\s+')
                df_list.append(df_key)
            df_all=pd.concat(df_list,axis=1,join='outer',ignore_index=False)
            
            print df_all.columns
#            print len(df_all.columns.values)
#            print '{0}'.format(df_all.iat[0,0])
            table_model=TableModel(self)
            table_model.update(df_all)
            self.tableView.setModel(table_model)
        
        
    def plot(self):
#   for now different file has different time series, para from different file..
#   is not allowed plot together
        if len(self.dict_select)>0:
            for key in self.dict_select:
#/may optimize/ # place time to the list[0]:remove it and insert it to the list[0]
                para_select=list(self.dict_select[key])  #to avoid change self.dict_select
                if self.dict_timename[key] in para_select:   
                    para_select.remove(self.dict_timename[key])
                para_select.insert(0,self.dict_timename[key])
                plot_para(key,para_select)
#        
#        if len(self.select_list)>1:
#            plot_para(self.filename,self.select_list)
    #self.textBrowser.append(df) 
        #else:
            #self.textBrowser.append("fail") 
    
    def subplot(self):
        if len(self.dict_select)>0:
            for key in self.dict_select:   #for now different file has different time series
                para_select=list(self.dict_select[key])
                if self.dict_timename[key] in para_select:
                    para_select.remove(self.dict_timename[key])
                para_select.insert(0,self.dict_timename[key])
                subplot_para(key,para_select)
#        if len(self.select_list)>1:
#            subplot_para(self.filename,self.select_list)
                
    def save(self):
        if self.dict_select:
            fileName2, ok2 = QFileDialog.getSaveFileName(self,"Save", "D:/", \
                                    "All Files (*);;Text Files (*.txt);;Text Files (*.csv)") 
            if fileName2:
                df_list=[]
                for key in self.dict_select:
                    cols=self.dict_select[key]
                    df=cols_input(key,cols,sep='\s+')
                    df_list.append(df)
                df_all=pd.concat(df_list,axis=1,join='outer',ignore_index=False) #merge different dataframe
                save_file(fileName2,df_all,sep='\t') #/update for more sep/
                
class TableModel(QtCore.QAbstractTableModel): 
    def __init__(self, parent=None, *args): 
        super(TableModel, self).__init__()
        self.datatable = None

    def update(self, dataIn):
       # print 'Updating Model'
        self.datatable = dataIn
       # print 'Datatable : {0}'.format(self.datatable)

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.datatable.index) 

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.datatable.columns.values) 

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            i = index.row()
            j = index.column()
            return '{0}'.format(self.datatable.iat[i, j])
        else:
            return QtCore.QVariant()
        
    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.datatable.columns[col]
        return QtCore.QVariant()

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled
                
if __name__=="__main__":  
    import sys  
    app=QtWidgets.QApplication(sys.argv)  
    myshow=MyWindow()  
    myshow.show()  
    sys.exit(app.exec_())  