# -*- coding: utf-8 -*-
import re
from models.datafile_model import Normal_DataFile
class DataAnalysis(object):
    def __init__(self):
        pass
    def condition_sift(self,file_list=[], condition="",search_para=[]):
        dict_result={}
        for filedir in file_list:
            df_result=[]
            file_search=Normal_DataFile(filedir)
            para_list=[item for item in search_para if item in file_search.paras_in_file]
            if not para_list:
                df_result
            para_list.insert(0,file_search.paras_in_file[0])
            df_sift=file_search.cols_input(filedir,para_list)
#           df_result=df_sift[eval("df_sift."+condition)]
            try:
                index=condition.replace("(","(df_sift.")
                df_result=df_sift[eval(index)]
                dict_result[filedir]=df_result
            except:
                return None
#            dict_result[filedir]=df_result
        return dict_result

#solution1: 任何语法不正确，搜索参数不在文件中（只要有一个参数不在文件中）都会使得字典值为None
#           而参数搜索条件结果为空时，字典值为Empty DataFrame。
#           不适用于 参数1 | 参数2条件 ，且只有其中部分参数存在文件中的情况
    def condition_sift_1(self,file_list=[], condition="",search_para=[]):
        dict_result={}
#        cond_list=re.split(r"&|\|",condition)
#        for s in cond_list:
#            para_parse=re.split(r">|<|=",s.strip())[0]
#            if para_parse not in search_para:
#                search_para.append(para_parse)
        for filedir in file_list:
            try:
                para_list=search_para
                file_search=Normal_DataFile(filedir)                
                para_list.insert(0,file_search.paras_in_file[0])
                df_sift=file_search.cols_input(filedir,para_list)
#                df_result=df_sift[eval("df_sift."+condition)]
                index=condition.replace("(","(df_sift.")
                df_result=df_sift[eval(index)]
                dict_result[filedir]=df_result
            except:
                dict_result[filedir]=None
#            dict_result[filedir]=df_result
        return dict_result
    
    def condition_sift_2(self,file_list=[], condition="",search_para=[]):
        dict_result={}
        cond_list=re.split(r"&|\|",condition)
        for s in cond_list:
            para_parse=re.split(r">|<|=",s.strip())[0]
            if para_parse not in search_para:
                search_para.append(para_parse)
        condition.split("&")
        for filedir in file_list:
            df_result=[]
            file_search=Normal_DataFile(filedir)
            para_list=[item for item in search_para if item in file_search.paras_in_file]
            if not para_list:
                df_result
            para_list.insert(0,file_search.paras_in_file[0])
            df_sift=file_search.cols_input(filedir,para_list)
#           df_result=df_sift[eval("df_sift."+condition)]
            try:
                index=condition.replace("(","(df_sift.")
                df_result=df_sift[eval(index)]
                dict_result[filedir]=df_result
            except:
                return None
#            dict_result[filedir]=df_result
        return dict_result
    
def condition_sift(file_list=[], condition="",display_para=[]):
    dict_result={}
    for filedir in file_list:
        para_list=display_para
        file_search=Normal_DataFile(filedir)
        para_list.insert(0,file_search.paras_in_file[0])
        df_sift=file_search.cols_input(filedir,para_list)
#        df_result=df_sift[eval("df_sift."+condition)]
        index=condition.replace("(","(df_sift.")
        df_result=df_sift[eval(index)]
        dict_result[filedir]=df_result
    return dict_result

if __name__ == "__main__":
    filename=u"D:\\flightdata\\FTPD-C919-10101-PD-170318-G-02-CAOWEN-664002-16.txt"
    file_list=[filename]
    da=DataAnalysis()
    condition="(FADEC_LA_Corrected_N1_Speed>=31) & (FADEC_LA_Corrected_N1_Speed<30.01)"
    condition="(FADEC_LA_Corrected_N1_Speed)"
    result=da.condition_sift_1(file_list,condition,["FADEC_LA_Corrected_N1_Speed"])
    print(result)