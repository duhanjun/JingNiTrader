# coding=utf-8

import datetime
import time
from __future__ import print_function, absolute_import

from gm.api import *


# 策略中必须有init方法
def init(context):
    # 新建空策略后复制这一行示例代码到空策略里
    subscribe(symbols='SHSE.600000', frequency='1d')
    # 设定每天10:00执行新股申购函数(关闭该功能请在下一行代码schedule前加#)
    schedule(schedule_func=jingni_subscribe_new_stock, date_rule='1d', time_rule='10:00:00')
    # 设定每天10:10执行新债申购函数(关闭该功能请在下一行代码schedule前加#)
    schedule(schedule_func=jingni_subscribe_new_bond, date_rule='1d', time_rule='10:10:00')
    pass

# 新建空策略后复制这两行示例代码到空策略里
def on_bar(context, bars):
    # 新建空策略后复制这一行示例代码到空策略里
    jingni_trade_strategy(trade_mode, context)

# 新建空策略后复制strategy_id和token的值分别替换示例代码里10个x和10个y
if __name__ == '__main__':
    '''
    strategy_id策略ID, 由系统生成
    filename文件名, 请与本文件名保持一致
    mode运行模式, 实时模式:MODE_LIVE回测模式:MODE_BACKTEST
    token绑定计算机的ID, 可在系统设置-密钥管理中生成
    backtest_start_time回测开始时间
    backtest_end_time回测结束时间
    backtest_adjust股票复权方式, 不复权:ADJUST_NONE前复权:ADJUST_PREV后复权:ADJUST_POST
    backtest_initial_cash回测初始资金
    backtest_commission_ratio回测佣金比例
    backtest_slippage_ratio回测滑点比例
    backtest_match_mode市价撮合模式，以下一tick/bar开盘价撮合:0，以当前tick/bar收盘价撮合：1
    '''
    run(strategy_id='xxxxxxxxxx',
        filename='main.py',
        mode=MODE_BACKTEST,
        token='yyyyyyyyyy',
        backtest_start_time='2025-09-01 08:00:00',
        backtest_end_time='2025-09-01 16:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=10000000,
        backtest_commission_ratio=0.0001,
        backtest_slippage_ratio=0.0001,
        backtest_match_mode=1)


###################################
# 以下为JingniTrader量化交易系统代码#
# 将JingNiTrader.py的代码复制到尾部#
###################################
