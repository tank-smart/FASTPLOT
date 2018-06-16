# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 简述：项目类
#
# =======使用说明
# 
#
# =======日志
# 
# =============================================================================
import time as Pytime

def str_to_intlist(time : str):
    
    return [int(x) for x in time.split(':')]

def lines_between_times(start_time : str, stop_time : str, fre : int):
    
    start = str_to_intlist(start_time)
    stop = str_to_intlist(stop_time)
    lines = ((stop[0] - start[0]) * (fre * 60 * 60) +
             (stop[1] - start[1]) * (fre * 60) +
             (stop[2] - start[2]) * fre)
    return lines

#    比较两个时间的大小，time1大于time2返回1，等于返回0，小于返回-1
def compare(time1 : str, time2 : str):
    
    t1 = str_to_intlist(time1)
    t2 = str_to_intlist(time2)
    l = len(t1)
#    当前位前边的位都是相等的
    equal = True
    for i in range(l):
#        前边的位相等，当前位大于
        if t1[i] > t2[i] and equal:
            return 1
        if t1[i] < t2[i] and equal:
            return -1
    return 0

def is_in_range(start : str, stop : str, time : str):
    st1 = compare(start, time)
    st2 = compare(time, stop)
    if st1 != 1 and st2 != 1:
        return True
    else:
        return False
    
def is_std_format(time : str):
    try:
        Pytime.strptime(time, "%H:%M:%S:%f")
        return True
    except:
        return False
    
if __name__ == '__main__':
    print(is_in_range('09:29:25:354','12:13:47:291','12:12:47:291'))