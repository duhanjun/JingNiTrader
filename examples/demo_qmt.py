# encoding: gbk

import time
import datetime


def init(ContextInfo):
    # 设定每天10:00执行新股申购函数(关闭该功能请在下一行代码ContextInfo.schedule_run前加#)
    ContextInfo.schedule_run(jingni_subscribe_new_stock, datetime.datetime.now().strftime('%Y%m%d') + '100000', 1, datetime.timedelta(days=1), 'jingni_subscribe_new_stock')
    # 设定每天10:10执行新债申购函数(关闭该功能请在下一行代码ContextInfo.schedule_run前加#)
    ContextInfo.schedule_run(jingni_subscribe_new_bond, datetime.datetime.now().strftime('%Y%m%d') + '101000', 1, datetime.timedelta(days=1), 'jingni_subscribe_new_bond')
    pass

def handlebar(ContextInfo):
    # 新建空策略后复制这一行示例代码到空策略里
    jingni_trade_strategy(trade_mode, ContextInfo)
    pass


###################################
# 以下为JingniTrader量化交易系统代码#
# 将JingNiTrader.py的代码复制到尾部#
###################################
