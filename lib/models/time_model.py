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
from datetime import datetime as Pytime
import pandas as pd

#将datatime格式或符合标准的时间字符串转换成列表，如果不满足则抛出异常
def to_intlist(time):
    
    result_time = to_datetime(time)
    
    return [result_time.hour, result_time.minute, result_time.second, result_time.microsecond]

#可计算datatime类型或时间字符串，若计算不成功则抛出异常
#起始若为采样点，那么计数到以最靠近且小于终止时间的那个采样点结束
def count_between_time(start_time, stop_time, fre):
    
    start = to_datetime(start_time)
    stop = to_datetime(stop_time)

    abs_delta = ((stop.hour - start.hour) * 3600 +
                 (stop.minute - start.minute) * 60 +
                 (stop.second - start.second) +
                 (stop.microsecond - start.microsecond) / 1000000) * fre

    if abs_delta >= 0:
        return int(abs_delta)
    else:
        return -1

#可判断datatime类型或时间字符串
#比较两个时间的大小，time1大于time2返回1，等于返回0，小于返回-1
#当函数返回是一个bool值时切忌出现返回None的情况，因为None与False在判断时是一致的
def compare(time1, time2):
    
    try:
        t1 = to_intlist(time1)
        t2 = to_intlist(time2)
    except:
#        此时应抛出异常，因为时间转换不成功
        raise
    finally:
        pass
    
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

#可判断datatime类型或时间字符串
def is_in_range(start, stop, time):
    
    try:
        st1 = compare(start, time)
        st2 = compare(time, stop)
    except:
        raise
    finally:
        pass
    
    if st1 != 1 and st2 != 1:
        return True
    else:
        return False
    
def is_std_format(time : str):
    
    tran_format = ['%H:%M:%S:%f', '%H:%M:%S.%f', '%H', '%H:%M', '%H:%M:%S', '%H-%M-%S.%f', '%H-%M-%S-%f', '%H-%M-%S']
    for format_time in tran_format:
        try:
            Pytime.strptime(time, format_time)
            return True
        except:
            pass
        finally:
            pass
    return False

def time_format(time : str):
    
    tran_format = ['%H:%M:%S:%f', '%H:%M:%S.%f', '%H', '%H:%M', '%H:%M:%S', '%H-%M-%S.%f', '%H-%M-%S-%f', '%H-%M-%S']
    for format_time in tran_format:
        try:
#            Pytime.strptime(time, format_time)
            pd.to_datetime(time, format = format_time)
            return format_time
        except:
            pass
        finally:
            pass
    return None

def str_to_datetime(time : str):
    
    tran_format = ['%H:%M:%S:%f', '%H:%M:%S.%f', '%H', '%H:%M', '%H:%M:%S', '%H-%M-%S.%f', '%H-%M-%S-%f', '%H-%M-%S']
    for format_time in tran_format:
        try:
            return Pytime.strptime(time, format_time)
        except:
            pass
        finally:
            pass
#    此时应抛出异常，因为时间转换不成功
    raise ValueError('Unsupported str-time format(FastPlot).')
    
def to_datetime(time):
    
    result_time = None
    if type(time) == Pytime:
        result_time = time
    elif type(time) == str:
        result_time = str_to_datetime(time)
    else:
        pass
    
    if result_time:
        return result_time
    else:
        raise ValueError('Unsupported time object(FastPlot).')

def datetime_to_timestr(dt : Pytime):
    
    if dt:
        re = dt.microsecond % 1000
        if re == 0:
            return dt.time().isoformat(timespec = 'milliseconds')
        else:
            return dt.time().isoformat(timespec = 'microseconds')
    else:
        return None
    
def timestr_to_stdtimestr(time : str):
    
    return datetime_to_timestr(str_to_datetime(time))

#两个时间段求交集
def and_time_intervals(tar_t : tuple, scr_t : tuple):

    stime, etime = scr_t
    lim_stime, lim_etime = tar_t
    result_st = stime
    result_et = etime
    if compare(stime, lim_stime) == -1:
        result_st = lim_stime
        if compare(etime, lim_stime) == -1:
            return None
        else:
            if compare(etime, lim_etime) == 1:
                result_et = lim_etime
    else:
        if compare(stime, lim_etime) == 1:
            return None
        else:
            if compare(etime, lim_etime) == 1:
                result_et = lim_etime
    return (result_st, result_et)

def datetime_to_origintime(dt : Pytime):
    if dt:
        strtime = dt.time().isoformat(timespec='milliseconds')
        strtime = strtime.replace('.', ':')
        return strtime
    else:
        return None
    
def str_time_delta(time2, time1):
    
    if compare(time1, time2) == 1:
        t = time1
        time1 = time2
        time2 = t
    td = to_datetime(time2) - to_datetime(time1)
    h = int(td.seconds / 3600)
    m = int((td.seconds % 3600) / 60)
    s = td.seconds % 60
    i = 0
    temp = td.microseconds
    while temp:
        temp = int(temp / 10)
        i += 1
    insert = ''
    if i != 0:
        for j in range(6 - i):
            insert += '0'
    ms = insert + str(td.microseconds)
    str_td = str(h) + ':' + str(m) + ':' + str(s) + '.' + ms
    return timestr_to_stdtimestr(str_td)
    
if __name__ == '__main__':
#    print(is_in_range('6:13','12:13:47.291','6:14:47.291'))
#    print(is_std_format('12:13:47*'))
#    t = str_to_datetime('6:13')
#    print(is_in_range(t,'12 13:47.291','6:14:47.291'))
#    print(count_between_time(t, '12:13:47.291', 16))
#    print(datetime_to_timestr(t))
#    print(and_time_intervals(('6:13','12:13:47.291'),('14:13','16:13')))
#    print(time_format('5:57:15'))
    print(str_time_delta('7:13:12:12', '6:13:12:120'))

    
    
    