#!/usr/bin/env python3
# _*_coding:utf-8_*_
# Auth by raysuen
# version v8.2


import datetime
import time
import calendar
import sys
import re


# 时间计算的类
class DateColculation(object):
    rdate = {
        "time_tuple": time.localtime(),
        "time_format": "%Y-%m-%d %H:%M:%S %A",
        "colculation_string": None,
        "last_day": False,
        "input_time": None,
        "input_format": None
    }
    def __init__(self,time_tuple=None,out_format=None,col_string=None,isLastday=None,in_time=None,in_format=None):
        if time_tuple != None:
            self.rdate["time_tuple"] = time_tuple
        if out_format != None:
            self.rdate["time_format"] = out_format
        if col_string != None:
            self.rdate["colculation_string"] = col_string
        if isLastday != None:
            self.rdate["last_day"] = isLastday
        if in_time != None:
            self.rdate["input_time"] = in_time
        if in_format != None:
            self.rdate["input_format"] = in_format
    # 月计算的具体实现函数
    def __R_MonthAdd(self, col_num, add_minus, lastday, time_truct):
        R_MA_num = 0  # 记录计算的月的数字
        R_ret_tuple = None  # 返回值，None或者时间元组
        R_MA_datetime = None  # 临时使用的datetime类型
        if type(col_num) != int:  # 判断传入的参数是否为数字
            print("the parameter type is wrong!")
            exit(5)
        if time_truct == None:
            R_MA_datetime = datetime.datetime.now()  # 获取当前时间
        else:
            R_MA_datetime = datetime.datetime.fromtimestamp(time.mktime(time_truct))

        if add_minus.lower() == "add":  # 判断是否为+
            R_MA_num = R_MA_datetime.month + col_num
            if R_MA_num > 12:  # 判断相加后的月份数是否大于12，如果大于12，需要在年+1
                while R_MA_num > 12:
                    R_MA_datetime = R_MA_datetime.replace(year=R_MA_datetime.year + 1)
                    R_MA_num = R_MA_num - 12
                R_ret_tuple = self.__days_add(R_MA_datetime, R_MA_num, lastday).timetuple()
            else:
                R_ret_tuple = self.__days_add(R_MA_datetime, R_MA_num, lastday).timetuple()
        elif add_minus.lower() == "minus":  # 判断是否为-
            while col_num >= 12:  # 判断传入的参数是否大于12，如果大于12则对年做处理
                R_MA_datetime = R_MA_datetime.replace(year=R_MA_datetime.year - 1)
                col_num = col_num - 12
            # R_MA_num = 12 + (R_MA_datetime.month - col_num)  # 获取将要替换的月份的数字

            if R_MA_datetime.month - col_num < 0:  # 判断当前月份数字是否大于传入参数(取模后的)，小于0表示，年需要减1，并对月份做处理
                if R_MA_datetime.day > calendar.monthrange(R_MA_datetime.year - 1, R_MA_datetime.month)[
                    1]:  # 如果年减一后，当前日期的天数大于年减一后的天数，则在月份加1，天变更为当前日期天数减变更后的月份天数
                    R_MA_datetime = R_MA_datetime.replace(year=R_MA_datetime.year - 1, month=R_MA_datetime.month + 1,
                                                          day=(R_MA_datetime.day >
                                                               calendar.monthrange(R_MA_datetime.year - 1,
                                                                                   R_MA_datetime.month)[1]))  # 年减1
                else:
                    R_MA_datetime = R_MA_datetime.replace(year=R_MA_datetime.year - 1)  # 年减1
                R_MA_datetime = self.__days_add(R_MA_datetime, 12 - abs(R_MA_datetime.month - col_num), lastday)
            elif R_MA_datetime.month - col_num == 0:  # 判断当前月份数字是否等于传入参数(取模后的)，等于0表示，年减1，月份替换为12，天数不变(12月为31天，不可能会存在比31大的天数)
                R_MA_datetime = R_MA_datetime.replace(year=R_MA_datetime.year - 1, month=12)
            elif R_MA_datetime.month - col_num > 0:  # 默认表示当前月份-传入参数(需要减去的月数字)大于0，不需要处理年
                R_MA_datetime = self.__days_add(R_MA_datetime, R_MA_datetime.month - col_num, lastday)
            R_ret_tuple = R_MA_datetime.timetuple()
        return R_ret_tuple  # 返回时间元组

    def __days_add(self, formal_MA_datetime, formal_MA_num, lastday):
        R_MA_datetime = formal_MA_datetime
        R_MA_num = formal_MA_num
        if lastday:  # 如果计算月最后一天，则直接把月份替换，天数为月份替换后的最后一天
            R_MA_datetime = R_MA_datetime.replace(month=R_MA_num,
                                                  day=calendar.monthrange(R_MA_datetime.year, R_MA_num)[
                                                      1])  # 月份替换，天数为替换月的最后一天
        else:
            if R_MA_datetime.day > \
                    calendar.monthrange(R_MA_datetime.year, R_MA_num)[
                        1]:  # 判断当前日期的天数是否大于替换后的月份天数，如果大于，月份在替换后的基础上再加1，天数替换为当前月份天数减替换月份天数
                R_MA_datetime = R_MA_datetime.replace(month=R_MA_num + 1,
                                                      day=R_MA_datetime.day -
                                                          calendar.monthrange(R_MA_datetime.year, R_MA_num)[
                                                              1])  # 月份在替换月的数字上再加1，天数替换为当前月份天数减替换月份天数
            else:
                R_MA_datetime = R_MA_datetime.replace(month=R_MA_num)  # 获取替换月份，day不变

        return R_MA_datetime

    # 月计算的入口函数
    def R_Month_Colculation(self, R_ColStr, lastday, time_truct):
        R_ret_tuple = None

        if R_ColStr.find("-") != -1:  # 判断-是否存在字符串
            col_num = R_ColStr.split("-")[-1].strip()  # 获取需要计算的数字
            if col_num.strip().isdigit():  # 判断获取的数字是否为正整数
                R_ret_tuple = self.__R_MonthAdd(int(col_num.strip()), "minus", lastday, time_truct)  # 获取tuple time时间格式
            else:  # 如果获取的数字不为正整数，则退出程序
                print("Please enter right format symbol!!")
                print("If you don't kown what values is avalable,please use -h to get help!")
                exit(4)
        elif R_ColStr.find("+") != -1:  # 判断+是否存在字符串
            col_num = R_ColStr.split("+")[-1].strip()  # 获取需要计算的数字
            if col_num.strip().isdigit():  # 判断获取的数字是否为正整数
                R_ret_tuple = self.__R_MonthAdd(int(col_num.strip()), "add", lastday, time_truct)  # 获取tuple time时间格式
            else:
                print("Please enter right format symbol!!")
                print("If you don't kown what values is avalable,please use -h to get help!")
                exit(4)
        return R_ret_tuple


    # 秒，分，时，日，周计算的实现函数
    # def R_General_Colculation(self, R_ColStr, time_truct, cal_parm):
    def R_General_Colculation(self, R_ColStr, time_truct):
        R_ret_tuple = None

        if time_truct == None:  # 判断是否指定了输入时间，没指定则获取当前时间，否则使用指定的输入时间
            R_Datatime = datetime.datetime.now()
        else:
            R_Datatime = datetime.datetime.fromtimestamp(time.mktime(time_truct))

        if R_ColStr.find("-") != -1:  # 判断-是否存在字符串
            col_num = R_ColStr.split("-")[-1].strip()  # 获取需要计算的数字
            if col_num.strip().isdigit():  # 判断获取的数字是否为正整数
                if R_ColStr.strip().lower().find("second") != -1:
                    R_ret_tuple = (R_Datatime + datetime.timedelta(
                        seconds=-int(col_num.strip()))).timetuple()  # 获取tuple time时间格式
                elif R_ColStr.strip().lower().find("minute") != -1:
                    R_ret_tuple = (R_Datatime + datetime.timedelta(
                        minutes=-int(col_num.strip()))).timetuple()  # 获取tuple time时间格式
                elif R_ColStr.strip().lower().find("hour") != -1:
                    R_ret_tuple = (R_Datatime + datetime.timedelta(
                        hours=-int(col_num.strip()))).timetuple()  # 获取tuple time时间格式
                elif R_ColStr.strip().lower().find("day") != -1:
                    R_ret_tuple = (R_Datatime + datetime.timedelta(
                        days=-int(col_num.strip()))).timetuple()  # 获取tuple time时间格式
                elif R_ColStr.strip().lower().find("week") != -1:
                    R_ret_tuple = (R_Datatime + datetime.timedelta(
                        weeks=-int(col_num.strip()))).timetuple()  # 获取tuple time时间格式
                # R_ret_tuple = (R_Datatime + datetime.timedelta(cal_parm=-int(col_num.strip()))).timetuple()  # 获取tuple time时间格式
            else:  # 如果获取的数字不为正整数，则退出程序
                print("Please enter right format symbol!!")
                print("If you don't kown what values is avalable,please use -h to get help!")
                exit(4)
        elif R_ColStr.find("+") != -1:  # 判断+是否存在字符串
            col_num = R_ColStr.split("+")[-1].strip()  # 获取需要计算的数字
            if col_num.strip().isdigit():  # 判断获取的数字是否为正整数
                if R_ColStr.strip().lower().find("second") != -1:
                    R_ret_tuple = (R_Datatime + datetime.timedelta(
                        seconds=int(col_num.strip()))).timetuple()  # 获取tuple time时间格式
                elif R_ColStr.strip().lower().find("minute") != -1:
                    R_ret_tuple = (R_Datatime + datetime.timedelta(
                        minutes=int(col_num.strip()))).timetuple()  # 获取tuple time时间格式
                elif R_ColStr.strip().lower().find("hour") != -1:
                    R_ret_tuple = (R_Datatime + datetime.timedelta(
                        hours=int(col_num.strip()))).timetuple()  # 获取tuple time时间格式
                elif R_ColStr.strip().lower().find("day") != -1:
                    R_ret_tuple = (R_Datatime + datetime.timedelta(
                        days=int(col_num.strip()))).timetuple()  # 获取tuple time时间格式
                elif R_ColStr.strip().lower().find("week") != -1:
                    R_ret_tuple = (R_Datatime + datetime.timedelta(
                        weeks=int(col_num.strip()))).timetuple()  # 获取tuple time时间格式
            else:
                print("Please enter right format symbol!!")
                print("If you don't kown what values is avalable,please use -h to get help!")
                exit(4)
        return R_ret_tuple

    # 年计算的实现函数
    def R_Year_Colculation(self, R_ColStr, time_truct):
        R_ret_tuple = None

        if time_truct == None:  # 判断是否指定了输入时间，没指定则获取当前时间，否则使用指定的输入时间
            R_Y_Datatime = datetime.datetime.now()
        else:
            R_Y_Datatime = datetime.datetime.fromtimestamp(time.mktime(time_truct))

        if R_ColStr.find("-") != -1:  # 判断-是否存在字符串
            col_num = R_ColStr.split("-")[-1].strip()  # 获取需要计算的数字
            if col_num.strip().isdigit():  # 判断获取的数字是否为正整数
                # 判断当前时间是否为闰年并且为二月29日，如果是相加/减后不为闰年则在月份加1，日期加1
                if calendar.isleap(
                        R_Y_Datatime.year) and R_Y_Datatime.month == 2 and R_Y_Datatime.day == 29 and calendar.isleap(
                        R_Y_Datatime.year - int(col_num.strip())) == False:
                    R_ret_tuple = (
                    R_Y_Datatime.replace(year=R_Y_Datatime.year - int(col_num.strip()), month=R_Y_Datatime.month + 1,
                                         day=1)).timetuple()  # 获取tuple time时间格式
                else:
                    R_ret_tuple = (
                        R_Y_Datatime.replace(
                            year=R_Y_Datatime.year - int(col_num.strip()))).timetuple()  # 获取tuple time时间格式
            else:  # 如果获取的数字不为正整数，则退出程序
                print("Please enter right format symbol!!")
                print("If you don't kown what values is avalable,please use -h to get help!")
                exit(4)
        elif R_ColStr.find("+") != -1:  # 判断+是否存在字符串
            col_num = R_ColStr.split("+")[-1].strip()  # 获取需要计算的数字
            if col_num.strip().isdigit():  # 判断获取的数字是否为正整数
                # 判断当前时间是否为闰年并且为二月29日，如果是相加/减后不为闰年则在月份加1，日期加1
                if calendar.isleap(
                        R_Y_Datatime.year) and R_Y_Datatime.month == 2 and R_Y_Datatime.day == 29 and calendar.isleap(
                    R_Y_Datatime.year + col_num.strip()) == False:
                    R_ret_tuple = (
                        R_Y_Datatime.replace(year=R_Y_Datatime.year - int(col_num.strip()),
                                             month=R_Y_Datatime.month + 1, day=1)).timetuple()  # 获取tuple time时间格式
                else:
                    R_ret_tuple = (
                        R_Y_Datatime.replace(
                            year=R_Y_Datatime.year + int(col_num.strip()))).timetuple()  # 获取tuple time时间格式
            else:
                print("Please enter right format symbol!!")
                print("If you don't kown what values is avalable,please use -h to get help!")
                exit(4)
        return R_ret_tuple

    # 获取月的最后一天
    def R_Month_lastday(self, time_tuple):
        R_MA_datetime = datetime.datetime.fromtimestamp(time.mktime(time_tuple))  # time_tuple
        R_MA_datetime = R_MA_datetime.replace(day=(calendar.monthrange(R_MA_datetime.year, R_MA_datetime.month)[1]))
        return R_MA_datetime.timetuple()


    def R_colculation(self):
        ret_tupletime = None
        ColStr = self.rdate["colculation_string"]
        lastday = self.rdate["last_day"]
        input_time = None

        if ColStr != None:
            if type(ColStr) != str:
                print("Please enter right format symbol!!")
                print("If you don't kown what values is avalable,please use -h to get help!")
                exit(3)
            if (ColStr.find("-") != -1) and (ColStr.find("+") != -1):
                print("Please enter right format symbol!!")
                print("If you don't kown what values is avalable,please use -h to get help!")
                exit(3)

        if self.rdate["input_time"] != None:
            if self.rdate["input_format"] == None:
                i = 1
                while 1:
                    try:
                        if i < 2:
                            input_time = time.strptime(self.rdate["input_time"], "%Y%m%d")
                        else:
                            input_time = time.strptime(self.rdate["input_time"], "%Y-%m-%d")
                        break
                    except ValueError as e:
                        if i < 2:
                            i+=1
                            continue
                        print("The input time and format do not match.")
                        exit(98)

            elif self.rdate["input_format"] == "%s":
                if self.rdate["input_time"].isdigit():
                    input_time = time.localtime(int(self.rdate["input_time"]))
                else:
                    print("The input time must be number.")
                    exit(97)
            else:
                try:
                    input_time = time.strptime(self.rdate["input_time"], self.rdate["input_format"])
                except ValueError as e:
                    print("The input time and format do not match.")
                    exit(98)

        if lastday:
            if ColStr == None:
                if input_time != None:
                    ret_tupletime = self.R_Month_lastday(input_time)
                else:
                    ret_tupletime = self.R_Month_lastday(time.localtime())
            # second,minute,hour,day和week的计算
            elif ColStr.strip().lower().find("second") != -1 or ColStr.strip().lower().find("minute") != -1 or ColStr.strip().lower().find("hour") != -1 or ColStr.strip().lower().find("day") != -1 or ColStr.strip().lower().find("week") != -1:
                if input_time != None:
                    ret_tupletime = self.R_General_Colculation(ColStr.strip().lower(), self.R_Month_lastday(input_time))
                else:
                    ret_tupletime = self.R_General_Colculation(ColStr.strip().lower(), self.R_Month_lastday(time.localtime()))
            # month的计算
            elif ColStr.strip().lower().find("month") != -1:  # 判断是否传入的字符串中是否存在day关键字
                ret_tupletime = self.R_Month_lastday(self.R_Month_Colculation(ColStr.strip().lower(), lastday, ret_tupletime))
            # year的计算
            elif ColStr.strip().lower().find("year") != -1:  # 判断是否传入的字符串中是否存在day关键字
                ret_tupletime = self.R_Month_lastday(self.R_Year_Colculation(ColStr.strip().lower(), ret_tupletime))

            else:
                print("Please enter right format symbol of -c.")
                print("If you don't kown what values is avalable,please use -h to get help!")
                exit(3)
        else:
            if ColStr == None:
                if self.rdate["input_time"] != None:
                    ret_tupletime = input_time
                else:
                    ret_tupletime = time.localtime()
            # second,minute,hour,day和week的计算
            elif ColStr.strip().lower().find("second") != -1 or ColStr.strip().lower().find(
                    "minute") != -1 or ColStr.strip().lower().find("hour") != -1 or ColStr.strip().lower().find(
                    "day") != -1 or ColStr.strip().lower().find("week") != -1:
                ret_tupletime = self.R_General_Colculation(ColStr.strip().lower(), input_time)
            # month的计算
            elif ColStr.strip().lower().find("month") != -1:  # 判断是否传入的字符串中是否存在day关键字
                ret_tupletime = self.R_Month_Colculation(ColStr.strip().lower(), lastday, input_time)
            # # year的计算
            elif ColStr.strip().lower().find("year") != -1:  # 判断是否传入的字符串中是否存在day关键字
                ret_tupletime = self.R_Year_Colculation(ColStr.strip().lower(), input_time)

            else:
                print("Please enter right format symbol of -c.")
                print("If you don't kown what values is avalable,please use -h to get help!")
                exit(3)

        return ret_tupletime


def func_help():
    print("""
    NAME:
        rdate  --display date and time
    SYNOPSIS:
        rdate [-f] [time format] [-c] [colculation format] [-d] [input_time] [input_time_format]
    DESCRIPTION:

        -c: value is second/minute/hour/day/week/month/year,plus +/-,plus a number which is number to colculate

        -l: obtain a number which is last day of month

        -d:
            input_time: enter a time string
            input_time_format: enter a time format for input time,default %Y%m%d or %Y-%m-%d

        -f:

         %A    is replaced by national representation of the full weekday name.
         %a    is replaced by national representation of the abbreviated weekday name.
         %B    is replaced by national representation of the full month name.
         %b    is replaced by national representation of the abbreviated month name.
         %C    is replaced by (year / 100) as decimal number; single digits are preceded by a zero.
         %c    is replaced by national representation of time and date.
         %D    is equivalent to ``%m/%d/%y''.
         %d    is replaced by the day of the month as a decimal number (01-31).
         %E* %O*
                POSIX locale extensions.  The sequences %Ec %EC %Ex %EX %Ey %EY %Od %Oe %OH %OI %Om %OM %OS %Ou %OU %OV %Ow %OW %Oy are supposed to provide alternate
                representations.
                Additionally %OB implemented to represent alternative months names (used standalone, without day mentioned).
         %e    is replaced by the day of the month as a decimal number (1-31); single digits are preceded by a blank.
         %F    is equivalent to ``%Y-%m-%d''.
         %G    is replaced by a year as a decimal number with century.  This year is the one that contains the greater part of the week (Monday as the first day of
                the week).
         %g    is replaced by the same year as in ``%G'', but as a decimal number without century (00-99).
         %H    is replaced by the hour (24-hour clock) as a decimal number (00-23).
         %h    the same as %b.
         %I    is replaced by the hour (12-hour clock) as a decimal number (01-12).
         %j    is replaced by the day of the year as a decimal number (001-366).
         %k    is replaced by the hour (24-hour clock) as a decimal number (0-23); single digits are preceded by a blank.
         %l    is replaced by the hour (12-hour clock) as a decimal number (1-12); single digits are preceded by a blank.
         %M    is replaced by the minute as a decimal number (00-59).
         %m    is replaced by the month as a decimal number (01-12).
         %n    is replaced by a newline.
         %O*   the same as %E*.
         %p    is replaced by national representation of either ante meridiem (a.m.)  or post meridiem (p.m.)  as appropriate.
         %R    is equivalent to ``%H:%M''.
         %r    is equivalent to ``%I:%M:%S %p''.
         %S    is replaced by the second as a decimal number (00-60).
         %s    is replaced by the number of seconds since the Epoch, UTC (see mktime(3)).
         %T    is equivalent to ``%H:%M:%S''.
         %t    is replaced by a tab.
         %U    is replaced by the week number of the year (Sunday as the first day of the week) as a decimal number (00-53).
         %u    is replaced by the weekday (Monday as the first day of the week) as a decimal number (1-7).
         %V    is replaced by the week number of the year (Monday as the first day of the week) as a decimal number (01-53).  If the week containing January 1 has
                four or more days in the new year, then it is week 1; otherwise it is the last week of the previous year, and the next week is week 1.
         %v    is equivalent to ``%e-%b-%Y''.
         %W    is replaced by the week number of the year (Monday as the first day of the week) as a decimal number (00-53).
         %w    is replaced by the weekday (Sunday as the first day of the week) as a decimal number (0-6).
         %X    is replaced by national representation of the time.
         %x    is replaced by national representation of the date.
         %Y    is replaced by the year with century as a decimal number.
         %y    is replaced by the year without century as a decimal number (00-99).
         %Z    is replaced by the time zone name.
         %z    is replaced by the time zone offset from UTC; a leading plus sign stands for east of UTC, a minus sign for west of UTC, hours and minutes follow with
                two digits each and no delimiter between them (common form for RFC 822 date headers).
         %+    is replaced by national representation of the date and time (the format is similar to that produced by date(1)).
         %-*   GNU libc extension.  Do not do any padding when performing numerical outputs.
         %_*   GNU libc extension.  Explicitly specify space for padding.
         %0*   GNU libc extension.  Explicitly specify zero for padding.
         %%    is replaced by `%'.

    EXAMPLE:
         rdate                                              --2017-10-23 11:04:51 Monday
         rdate -f "%Y-%m_%d"                                --2017-10-23
         rdate -f "%Y-%m_%d" -c "day-3"                     --2017-10-20
         rdate -f "%Y-%m_%d" -c "day+3"                     --2017-10-26
         rdate -f "%Y-%m_%d" -c "month+3"                   --2017-7-23
         rdate -f "%Y-%m_%d" -c "year+3"                    --2020-7-23
         rdate -c "week - 1" -f "%Y-%m-%d %V"               --2018-02-15 07
         rdate -c "day - 30" -f "%Y-%m-%d" -l               --2018-01-31
         rdate -d "1972-01-31" "%Y-%m-%d"                   --1972-01-31 00:00:00 Monday
    """)


if __name__ == "__main__":
    d1 = DateColculation()
    if len(sys.argv) > 1:
        i = 1
        while i < len(sys.argv):
            if sys.argv[i] == "-h":  # 判断输入的参数是否为-h,既获取帮助
                func_help()
                exit(0)
            elif sys.argv[i] == "-f":  # -f表示format,表示指定的输出时间格式
                i = i + 1
                if i >= len(sys.argv):  # 判断-f的值的下标是否大于等于参数个数，如果为真则表示没有指定-f的值
                    print("The value of -f must be specified!!!")
                    exit(1)
                elif sys.argv[i] == "-c":
                    print("The value of -f must be specified!!!")
                    exit(1)
                elif re.match("^-", sys.argv[i]) != None:  # 判断-f的值，如果-f的下个参数以-开头，表示没有指定-f值
                    print("The value of -f must be specified!!!")
                    exit(1)
                d1.rdate["time_format"] = sys.argv[i]  # 获取输出时间格式
            elif sys.argv[i] == "-c":  # -c表示colculation,计算
                i = i + 1
                if i >= len(sys.argv):  # 判断-f的值的下标是否大于等于参数个数，如果为真则表示没有指定-f的值
                    print("The value of -c must be specified!!!")
                    exit(2)
                elif sys.argv[i] == "-f":
                    print("The value of -c must be specified!!!")
                    exit(2)
                elif (re.match("^-", sys.argv[i]) != None):  # 判断-f的值，如果-f的下个参数以-开头，表示没有指定-f值
                    print("The value of -c must be specified!!!")
                    exit(2)
                d1.rdate["colculation_string"] = sys.argv[i]  # 获取需要计算的字符串参数内容
            elif sys.argv[i] == "-d":  # -d date 表示指定输入的时间和输入的时间格式
                i += 1
                if i >= len(sys.argv):  # 判断-d的值的下标是否大于等于参数个数，如果为真则表示没有指定-的值
                    print("The value of -d must be specified!!!")
                    exit(3)
                elif (re.match("^-", sys.argv[i]) != None):  # 判断-d的值，如果-df的下个参数以-开头，表示没有指定-df值
                    print("The value of -c must be specified!!!")
                    exit(3)
                d1.rdate["input_time"] = sys.argv[i]
                if (i+1 < len(sys.argv) and re.match("^-", sys.argv[(i+1)]) == None):
                    d1.rdate["input_format"] = sys.argv[i+1]
                    i+=1
            elif sys.argv[i] == "-l":  # -l表示获取月份的最后一天
                d1.rdate["last_day"] = True
            else:
                print("You must enter right parametr.")
                print("If you don't kown what values is avalable,please use -h to get help!")
                exit(3)
            i = i + 1
        d1.rdate["time_tuple"] = d1.R_colculation()  # 获取时间的元组，通过R_colculation函数，R_colculation参数为传入一个需要计算的时间字符串
        print(time.strftime(d1.rdate["time_format"], d1.rdate["time_tuple"]))
        exit(0)
    else:  # 如果不输入参数，则输出默认格式化的本地时间
        print(time.strftime(d1.rdate["time_format"], d1.rdate["time_tuple"]))
        exit(0)

