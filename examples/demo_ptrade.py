# encoding: utf-8


def initialize(context):
    # 设定每天10:00执行新股申购函数(关闭该功能请在下一行代码run_daily前加#)
    run_daily(context, jingni_subscribe_new_stock, time='10:00')
    # 设定每天10:10执行新债申购函数(关闭该功能请在下一行代码run_daily前加#)
    run_daily(context, jingni_subscribe_new_bond, time='10:10')
    # 设定每天14:50执行国债逆回购函数(关闭该功能请在下一行代码run_daily前加#)
    run_daily(context, jingni_participate_reverse_repo, time='14:50')
    pass

def handle_data(context, data):
    # 新建空策略后复制这一行示例代码到空策略里
    jingni_trade_strategy(trade_mode, context)
    pass


###################################
# 以下为JingniTrader量化交易系统代码#
# 将JingNiTrader.py的代码复制到尾部#
###################################
