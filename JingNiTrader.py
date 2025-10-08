# -*- coding: utf-8 -*-

"""
项目名称：JingNiTrader
项目版本：v0.1.10
项目描述：JingNiTrader是一个基于Python的量化交易开发框架，致力于提供兼容中国券商交易软件的量化解决方案。
项目版权：Copyright (c) 2024-present, Hanjun Du
项目作者：Hnjun Du (hanjun.du@outlook.com)
项目贡献：项目长期招募贡献者，有意向请邮件联系项目作者。
免责声明：本项目仅用于教育目的，不保证任何交易的成功。请自行承担风险。
关于本项目的信息和反馈，请访问GitHub存储库：https://github.com/duhanjun/JingNiTrader
关于本项目的学习和实践，请访问在线课程目录：https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MjM5MTU2NDA3OQ==&action=getalbum&album_id=4151851070626693141#wechat_redirect
"""

import time
import datetime


# 选择券商交易软件名称（ptrade、qmt、goldminer）
global trade_mode
trade_mode = '软件名称'

# 查询交易日历函数
def jingni_trading_dates(trade_mode, context_data, trading_dates_count):
    try:
        if trade_mode == 'goldminer':
            if trading_dates_count == 0:
                # 获取交易日历，0代表今天
                trading_dates_data = context_data.now.strftime('%Y%m%d')
            elif trading_dates_count > 0:
                # 获取交易日历，大于0代表今天的后n个交易日
                trading_dates_data = get_next_n_trading_dates(exchange='SHSE', date=context_data.now.strftime('%Y-%m-%d'), n=trading_dates_count)[0]
            elif trading_dates_count < 0:
                # 获取交易日历，小于0代表今天的前n个交易日
                trading_dates_data = get_previous_n_trading_dates(exchange='SHSE', date=context_data.now.strftime('%Y-%m-%d'), n=-trading_dates_count)[0]
        elif trade_mode == 'ptrade':
            if trading_dates_count == 0:
                # 获取交易日历，0代表今天
                trading_dates_data = get_trading_day(trading_dates_count).strftime('%Y%m%d')
            elif trading_dates_count > 0:
                # 获取交易日历，大于0代表今天的后n个交易日
                trading_dates_data = get_trading_day(trading_dates_count).strftime('%Y%m%d')
            elif trading_dates_count < 0:
                # 获取交易日历，小于0代表今天的前n个交易日
                trading_dates_data = get_trading_day(trading_dates_count).strftime('%Y%m%d')
        elif trade_mode == 'qmt':
            if trading_dates_count == 0:
                # 获取交易日历，0代表今天
                trading_dates_data = timetag_to_datetime(context_data.get_bar_timetag(context_data.barpos), '%Y%m%d')
            elif trading_dates_count > 0:
                # 获取交易日历，大于0代表今天的后n个交易日
                trading_dates_data = None
            elif trading_dates_count < 0:
                # 获取交易日历，小于0代表今天的前n个交易日
                trading_dates_data = None
    except Exception as e:
        print('查询交易日历未知异常：', e)
        trading_dates_data = None
    return trading_dates_data

# 查询账户信息函数
def jingni_portfolio(trade_mode, context_data, security_field):

    try:
        if trade_mode == 'goldminer':
            if security_field == 'assets_value':
                # 获取账户资产
                portfolio_data = context_data.account().cash['nav']
            elif security_field == 'market_value':
                # 获取账户市值
                portfolio_data = context_data.account().cash['market_value']
            elif security_field == 'cash':
                # 获取可用资金
                portfolio_data = context_data.account().cash['balance']
            elif security_field == 'positions':
                # 获取账户持仓
                portfolio_data = context_data.account().positions()
        elif trade_mode == 'ptrade':
            if security_field == 'assets_value':
                # 获取账户资产
                portfolio_data = context_data.portfolio.portfolio_value
            elif security_field == 'market_value':
                # 获取账户市值
                portfolio_data = context_data.portfolio.positions_value
            elif security_field == 'cash':
                # 获取可用资金
                portfolio_data = context_data.portfolio.cash
            elif security_field == 'positions':
                # 获取账户持仓
                portfolio_data = context_data.portfolio.positions
        elif trade_mode == 'qmt':
            if security_field == 'assets_value':
                # 获取账户资产
                portfolio_data = get_trade_detail_data(account, 'stock', 'account')[0].m_dBalance
            elif security_field == 'market_value':
                # 获取账户市值
                portfolio_data = get_trade_detail_data(account, 'stock', 'account')[0].m_dInstrumentValue
            elif security_field == 'cash':
                # 获取可用资金
                portfolio_data = get_trade_detail_data(account, 'stock', 'account')[0].m_dAvailable
            elif security_field == 'positions':
                # 获取账户持仓
                portfolio_data = get_trade_detail_data(account, 'stock', 'position')
    except Exception as e:
        print('查询账户信息未知异常：', e)
        portfolio_data = None

    return portfolio_data

# 证券代码转换函数
def jingni_map_security_code(security_code):

    try:
        if trade_mode == 'goldminer':
            if security_code[security_code.find('.') - 1].isdigit():
                # 获取证券代码.之前的字符串,即六位数字字符
                security_code_char_number = security_code[0:security_code.rfind('.')]
                # 获取证券代码.开始的字符串，即点和市场字符
                security_code_char_market = security_code[security_code.rfind('.'):]
                # 如果市场字符等于'.SH'则将市场字符替换成'SHSE.'
                if security_code_char_market == '.SH':
                    security_code_char_market = 'SHSE.'
                # 如果市场字符等于'.SZ'则将市场字符替换成'SZSE.'
                elif security_code_char_market == '.SZ':
                    security_code_char_market = 'SZSE.'
                # 将六位数字字符和点和市场字符重新拼接成新的证券代码
                security_code = security_code_char_market + security_code_char_number
            elif security_code[security_code.find('.') - 1].isalpha():
                # 获取证券代码.之前的字符串,即市场字符
                security_code_char_market = security_code[:security_code.rfind('.')+1]
                # 获取证券代码.开始的字符串，即点和数字字符
                security_code_char_number = security_code[security_code.rfind('.')+1:]
                # 如果市场字符等于'SHSE.'则将市场字符替换成'.SH'
                if security_code_char_market == 'SHSE.':
                    security_code_char_market = '.SH'
                # 如果市场字符等于'SZSE.'则将市场字符替换成'.SZ'
                elif security_code_char_market == 'SZSE.':
                    security_code_char_market = '.SZ'
                # 将六位数字字符和点和市场字符重新拼接成新的证券代码
                security_code = security_code_char_number + security_code_char_market

        elif trade_mode == 'ptrade':
            # 获取证券代码.之前的字符串,即六位数字字符
            security_code_char_number = security_code[0:security_code.rfind('.')]
            # 获取证券代码.开始的字符串，即点和市场字符
            security_code_char_market = security_code[security_code.rfind('.'):]
            # 如果市场字符等于'.SH'则将市场字符替换成'.SS'
            if security_code_char_market == '.SH':
                security_code_char_market = '.SS'
            # 如果市场字符等于'.SZ'则将市场字符替换成'.SZ'
            elif security_code_char_market == '.SZ':
                security_code_char_market = '.SZ'
            # 如果市场字符等于'.SS'则将市场字符替换成'.SH'
            elif security_code_char_market == '.SS':
                security_code_char_market = '.SH'
            # 如果市场字符等于'.SZ'则将市场字符替换成'.SZ'
            elif security_code_char_market == '.SZ':
                security_code_char_market = '.SZ'
            # 如果市场字符等于'.XSHG'则将市场字符替换成'.SH'
            elif securities_code_char_market == '.XSHG':
                securities_code_char_market = '.SH'
            # 如果市场字符等于'.XSHE'则将市场字符替换成'.SZ'
            elif securities_code_char_market == '.XSHE':
                securities_code_char_market = '.SZ'
            # 将六位数字字符和点和市场字符重新拼接成新的证券代码
            security_code = security_code_char_number + security_code_char_market

        elif trade_mode == 'qmt':
            # 获取证券代码.之前的字符串,即六位数字字符
            security_code_char_number = security_code[0:security_code.rfind('.')]
            # 获取证券代码.开始的字符串，即点和市场字符
            security_code_char_market = security_code[security_code.rfind('.'):]
            # 如果市场字符等于'.SH'则将市场字符替换成'.SH'
            if security_code_char_market == '.SH':
                security_code_char_market = '.SH'
            # 如果市场字符等于'.SZ'则将市场字符替换成'.SZ'
            elif security_code_char_market == '.SZ':
                security_code_char_market = '.SZ'
            # 如果市场字符等于'.SH'则将市场字符替换成'.SH'
            elif security_code_char_market == '.SH':
                security_code_char_market = '.SH'
            # 如果市场字符等于'.SZ'则将市场字符替换成'.SZ'
            elif security_code_char_market == '.SZ':
                security_code_char_market = '.SZ'
            # 将六位数字字符和点和市场字符重新拼接成新的证券代码
            security_code = security_code_char_number + security_code_char_market
    except Exception as e:
        print('证券代码转换未知异常：', e)

    return security_code

# 查询实时行情函数
def jingni_get_current(trade_mode, context_data, security_code, security_field):

    try:
        if trade_mode == 'goldminer':
            # 获取实时行情数据
            current_data = current(symbols=security_code, fields=security_field)
        elif trade_mode == 'ptrade':
            # 获取实时行情数据
            current_data = get_snapshot(security_code)
        elif trade_mode == 'qmt':
            # 将字符串参数转换成列表参数
            if isinstance(security_code, str):
                security_code = [security_code]
            # 获取实时行情数据
            current_data = context_data.get_full_tick(security_code)
    except Exception as e:
        print('查询实时行情未知异常：', e)
        current_data = None

    return current_data

# 查询历史行情函数
def jingni_get_history(trade_mode, context_data, security_code, security_frequency, security_field, security_count):

    try:
        if trade_mode == 'goldminer':
            # 获取历史行情数据
            history_data = history_n(symbol=str(security_code), frequency=str(security_frequency), count=int(-security_count), end_time=datetime.datetime.strptime(jingni_trading_dates(trade_mode, context_data, 0), "%Y%m%d").strftime("%Y-%m-%d"), fields=str(security_field), adjust=ADJUST_PREV, df=True)
        elif trade_mode == 'ptrade':
            # 获取历史行情数据
            if security_field == '':
                security_field = None
            history_data = get_history(int(-security_count), str(security_frequency), security_field, security_code, fq='pre', include=True)
        elif trade_mode == 'qmt':
            # 将字符串参数转换成列表参数
            if isinstance(security_code, str):
                security_code = [security_code]
            if security_field == '':
                security_field = []
            else:
                if isinstance(security_field, str):
                    security_field = [security_field]
            # 获取历史行情数据
            history_data = context_data.get_market_data_ex(fields=security_field, stock_code=security_code, period=str(security_frequency), end_time=str(jingni_trading_dates(trade_mode, context_data, 0)), count=int(-security_count), dividend_type='front')
    except Exception as e:
        print('查询历史行情未知异常：', e)
        history_data = None

    return history_data

# 提取单日证券行情数据
def jingni_get_field(trade_mode, context_data, security_code, security_frequency, security_field, security_count):

    security_field_data = None

    if trade_mode == 'goldminer':
        if security_count == 0:
            # 判断策略运行模式（返回1为实时模式，返回2为回测模式）
            if context_data.mode == 1:
                # 实时行情数据字段映射
                if security_field == 'open':
                    security_field = 'open'
                elif security_field == 'high':
                    security_field = 'high'
                elif security_field == 'low':
                    security_field = 'low'
                elif security_field == 'close':
                    security_field = 'price'
                # 获取实时行情数据，0代表实盘当天
                security_field_data = jingni_get_current(trade_mode, context_data, security_code, security_field)
                # 判断行情数据是否不为空
                if security_field_data is not None and len(security_field_data) > 0:
                    # 提取字段数值
                    security_field = security_field_data[0][security_field]
            elif context_data.mode == 2:
                # 获取历史行情数据，0代表回测当天
                security_field_data = jingni_get_history(trade_mode, context_data, security_code, security_frequency, security_field, security_count-1)
                # 判断行情数据是否不为空
                if security_field_data is not None and not security_field_data.empty and security_field_data.shape[0] > 0:
                    # 提取字段数值
                    security_field = security_field_data.iloc[security_count - 1][security_field]
        elif security_count < 0:
            # 获取历史行情数据，小于0代表实盘或回测当天的前n个交易日
            security_field_data = jingni_get_history(
                trade_mode, context_data, security_code, security_frequency, security_field, security_count)
            # 判断行情数据是否不为空
            if security_field_data is not None and not security_field_data.empty and security_field_data.shape[0] > 0:
                # 提取字段数值
                security_field = security_field_data.iloc[security_count][security_field]
    elif trade_mode == 'ptrade':
        if security_count == 0:
            # 判断策略运行模式（返回True为实时模式，返回False为回测模式）
            if is_trade():
                # 实时行情数据字段映射
                if security_field == 'open':
                    security_field = 'open_px'
                elif security_field == 'high':
                    security_field = 'high_px'
                elif security_field == 'low':
                    security_field = 'low_px'
                elif security_field == 'close':
                    security_field = 'last_px'
                # 获取实时行情数据，0代表实盘当天
                security_field_data = jingni_get_current(trade_mode, context_data, security_code, security_field)
                # 判断行情数据是否不为空
                if security_field_data is not None and len(security_field_data) > 0:
                    # 提取字段数值
                    security_field = security_field_data[security_code][security_field]
            else:
                # 获取历史行情数据，0代表回测当天
                security_field_data = jingni_get_history(trade_mode, context_data, security_code, security_frequency, security_field, security_count-1)
                # 判断行情数据是否不为空
                if security_field_data is not None and not security_field_data.empty and security_field_data.shape[0] > 0:
                    # 提取字段数值
                    security_field = security_field_data[security_field][security_count-1]
        elif security_count < 0:
            # 获取历史行情数据，小于0代表实盘或回测当天的前n个交易日
            security_field_data = jingni_get_history(trade_mode, context_data, security_code, security_frequency, security_field, security_count)
            # 判断行情数据是否不为空
            if security_field_data is not None and not security_field_data.empty and security_field_data.shape[0] > 0:
                # 提取字段数值
                security_field = security_field_data[security_field][security_count]
    elif trade_mode == 'qmt':
        # 将字符串参数转换成列表参数
        if isinstance(security_code, str):
            security_code = [security_code]
        if isinstance(security_field, str):
            security_field = [security_field]
        if security_count == 0:
            # 判断策略运行模式（返回False为实时模式）
            if not context_data.do_back_test:
                # 实时行情数据字段映射
                if security_field[0] == 'open':
                    security_field = ['open']
                elif security_field[0] == 'high':
                    security_field = ['high']
                elif security_field[0] == 'low':
                    security_field = ['low']
                elif security_field[0] == 'close':
                    security_field = ['lastPrice']
                # 获取实时行情数据，0代表实盘当天
                security_field_data = jingni_get_current(trade_mode, context_data, security_code, security_field)
                # 判断行情数据是否补为空
                if security_field_data is not None and len(security_field_data) > 0:
                    # 提取字段数值
                    security_field = security_field_data[security_code[0]][security_field[0]]
            else:
                # 获取历史行情数据，0代表回测当天
                security_field_data = jingni_get_history(trade_mode, context_data, security_code, security_frequency, security_field, security_count-1)
                # 判断行情数据是否不为空
                if security_field_data is not None and len(security_field_data) > 0:
                    # 提取字段数值
                    security_field = security_field_data[security_code[0]][security_field[0]][security_count-1]
        elif security_count < 0:
            # 获取历史行情数据，小于0代表实盘或回测当天的前n个交易日
            security_field_data = jingni_get_history(trade_mode, context_data, security_code, security_frequency, security_field, security_count-1)
            # 判断行情数据是否不为空
            if security_field_data is not None and len(security_field_data) > 0:
                # 提取字段数值
                security_field = security_field_data[security_code[0]][security_field[0]][security_count-1]

    # 判断行情数据是否为空
    if security_field_data is None and security_field_data.shape[0] == 0:
        # 设定字段数值的缺省值
        security_field = 0

    return security_field

# 提取多日证券行情数据
def jingni_get_field_n(trade_mode, context_data, security_code, security_frequency, security_field, security_count):

    jingni_get_field_n_data = None

    if trade_mode == 'goldminer':
        if security_count == 0:
            # 判断策略运行模式（返回1为实时模式，返回2为回测模式）
            if context_data.mode == 1:
                # 实时行情数据字段映射
                if security_field == 'open':
                    security_field = 'open'
                elif security_field == 'high':
                    security_field = 'high'
                elif security_field == 'low':
                    security_field = 'low'
                elif security_field == 'close':
                    security_field = 'price'
                # 获取实时行情数据，0代表实盘当天
                jingni_get_field_n_data = jingni_get_current(trade_mode, context_data, security_code, security_field)
                # 判断行情数据是否不为空
                if jingni_get_field_n_data is not None and len(jingni_get_field_n_data) > 0:
                    # 提取字段数值
                    security_field_n = jingni_get_field_n_data[security_field].values
            elif context_data.mode == 2:
                # 获取历史行情数据，0代表回测当天
                jingni_get_field_n_data = jingni_get_history(trade_mode, context_data, security_code, security_frequency, security_field, security_count-1)
                # 判断行情数据是否不为空
                if jingni_get_field_n_data is not None and not jingni_get_field_n_data.empty and jingni_get_field_n_data.shape[0] > 0:
                    # 提取字段数值
                    security_field_n = jingni_get_field_n_data[security_field].values
        elif security_count < 0:
            # 获取历史行情数据，小于0代表实盘或回测当天的前n个交易日
            jingni_get_field_n_data = jingni_get_history(trade_mode, context_data, security_code, security_frequency, security_field, security_count-1)
            # 判断行情数据是否不为空
            if jingni_get_field_n_data is not None and not jingni_get_field_n_data.empty and jingni_get_field_n_data.shape[0] > 0:
                # 提取字段数值
                security_field_n = jingni_get_field_n_data[security_field].values
    elif trade_mode == 'ptrade':
        if security_count == 0:
            # 判断策略运行模式（返回True为实时模式，返回False为回测模式）
            if is_trade():
                # 实时行情数据字段映射
                if security_field == 'open':
                    security_field = 'open_px'
                elif security_field == 'high':
                    security_field = 'high_px'
                elif security_field == 'low':
                    security_field = 'low_px'
                elif security_field == 'close':
                    security_field = 'last_px'
                # 获取实时行情数据，0代表实盘当天
                jingni_get_field_n_data = jingni_get_current(trade_mode, context_data, security_code, security_field)
                # 判断行情数据是否不为空
                if jingni_get_field_n_data is not None and len(jingni_get_field_n_data) > 0:
                    # 提取字段数值
                    security_field_n = jingni_get_field_n_data[security_code][security_field].values
            else:
                # 获取历史行情数据，0代表回测当天
                jingni_get_field_n_data = jingni_get_history(
                    trade_mode, context_data, security_code, security_frequency, security_field, security_count-1)
                # 判断行情数据是否不为空
                if jingni_get_field_n_data is not None and not jingni_get_field_n_data.empty and jingni_get_field_n_data.shape[0] > 0:
                    # 提取字段数值
                    security_field_n = jingni_get_field_n_data[security_field].values
        elif security_count < 0:
            # 获取历史行情数据，小于0代表实盘或回测当天的前n个交易日
            jingni_get_field_n_data = jingni_get_history(trade_mode, context_data, security_code, security_frequency, security_field, security_count)
            # 判断行情数据是否不为空
            if jingni_get_field_n_data is not None and not jingni_get_field_n_data.empty and jingni_get_field_n_data.shape[0] > 0:
                # 提取字段数值
                security_field_n = jingni_get_field_n_data[security_field].values
    elif trade_mode == 'qmt':
        # 将字符串参数转换成列表参数
        if isinstance(security_code, str):
            security_code = [security_code]
        if isinstance(security_field, str):
            security_field = [security_field]
        if security_count == 0:
            # 判断策略运行模式（返回False为实时模式）
            if not context_data.do_back_test:
                # 实时行情数据字段映射
                if security_field[0] == 'open':
                    security_field = ['open']
                elif security_field[0] == 'high':
                    security_field = ['high']
                elif security_field[0] == 'low':
                    security_field = ['low']
                elif security_field[0] == 'close':
                    security_field = ['lastPrice']
                # 获取实时行情数据，0代表实盘当天
                jingni_get_field_n_data = jingni_get_current(
                    trade_mode, context_data, security_code, security_field)
                # 判断行情数据是否补为空
                if jingni_get_field_n_data is not None and len(jingni_get_field_n_data) > 0:
                    # 提取字段数值
                    security_field_n = jingni_get_field_n_data[security_code[0]
                                                               ][security_field[0]]
            else:
                # 获取历史行情数据，0代表回测当天
                jingni_get_field_n_data = jingni_get_history(trade_mode, context_data, security_code, security_frequency, security_field, security_count-1)
                # 判断行情数据是否不为空
                if jingni_get_field_n_data is not None and len(jingni_get_field_n_data) > 0:
                    # 提取字段数值
                    security_field_n = jingni_get_field_n_data[security_code[0]][security_field[0]].values
        elif security_count < 0:
            # 获取历史行情数据，小于0代表实盘或回测当天的前n个交易日
            jingni_get_field_n_data = jingni_get_history(trade_mode, context_data, security_code, security_frequency, security_field, security_count-1)
            # 判断行情数据是否不为空
            if jingni_get_field_n_data is not None and len(jingni_get_field_n_data) > 0:
                # 提取字段数值
                security_field_n = jingni_get_field_n_data[security_code[0]][security_field[0]].values

    # 判断行情数据是否为空
    if jingni_get_field_n_data is None and jingni_get_field_n_data.shape[0] == 0:
        # 设定字段数值的缺省值
        security_field_n = 0

    return security_field_n

# 证券数量交易函数
def jingni_order_amount(trade_mode, context_data, security_code, security_amount, security_price):

    try:
        if trade_mode == 'goldminer':
            if security_amount >= 0:
                order_volume(symbol=str(security_code), volume=int(security_amount), price=float(security_price), side=OrderSide_Buy, order_type=OrderType_Limit, position_effect=PositionEffect_Open)
                print('%s元 买入证券 %s %s股' % (security_price, security_code, security_amount))
            elif security_amount < 0:
                order_volume(symbol=str(security_code), volume=int(-security_amount), price=float(security_price), side=OrderSide_Sell, order_type=OrderType_Limit, position_effect=PositionEffect_Close)
                print('%s元 卖出证券 %s %s股' % (security_price, security_code, -security_amount))
        elif trade_mode == 'ptrade':
            if security_amount >= 0:
                order(str(security_code), int(security_amount), limit_price=float(security_price))
                print('%s元 买入证券 %s %s股' % (security_price, security_code, security_amount))
            elif security_amount < 0:
                order(str(security_code), int(-security_amount), limit_price=float(security_price))
                print('%s元 卖出证券 %s %s股' % (security_price, security_code, -security_amount))
        elif trade_mode == 'qmt':
            if security_amount >= 0:
                passorder(23, 1101, str(account), str(security_code), 11, float(security_price), int(security_amount), '', 2, '', context_data)
                print('%s元 买入证券 %s %s股' % (security_price, security_code, security_amount))
            elif security_amount < 0:
                passorder(24, 1101, str(account), str(security_code), 11, float(security_price), int(-security_amount), '', 2, '', context_data)
                print('%s元 卖出证券 %s %s股' % (security_price, security_code, -security_amount))
    except Exception as e:
        print('证券数量交易未知异常：', e)

# 交易策略函数
def jingni_trade_strategy(trade_mode, context_data):
    print(jingni_order_amount(trade_mode, context_data, jingni_map_security_code('510300.SH'), 100, 4.741))

# 盘前事件函数
def jingni_before_trading_start(trade_mode, context_data):
    print(datetime.datetime.now(), '开始运行盘前函数')
    # 运行盘前函数1
    # 运行盘前函数2
    # 运行盘前函数3
    print(datetime.datetime.now(), '结束运行盘前函数')

# 盘中事件函数（开始交易时间，结束交易时间，交易时间间隔）
def jingni_handle_data(trade_mode, context_data, trade_start_time, trade_end_time, trade_seconds):
    print(datetime.datetime.now(), '开始运行盘中函数')
    while True:
        # 获取系统最新时间
        trade_now_time = datetime.datetime.now().time()
        # 如果系统最新时间大于等于程序开始交易时间，小于等于程序结束交易时间，则运行盘中所需相关函数
        if trade_start_time <= trade_now_time <= trade_end_time:
            # 运行交易策略函数
            jingni_trade_strategy(trade_mode, context_data)
        # 如果系统最新时间大于程序结束交易时间
        elif trade_now_time > trade_end_time:
            break
        # 设置交易时间间隔
        time.sleep(trade_seconds)
    print(datetime.datetime.now(), '结束运行盘中函数')

# 盘后事件函数
def jingni_after_trading_end(trade_mode, context_data):
    print(datetime.datetime.now(), '开始运行盘后函数')
    # 运行盘后函数1
    # 运行盘后函数2
    # 运行盘后函数3
    print(datetime.datetime.now(), '结束运行盘后函数')

# JingniTrade的入口函数，负责启动JingniTrade的各个组件并将它们连接起来形成一个完整的系统
def jingni_main(trade_mode, context_data):
    # 定义程序开始运行时间为09:00:00
    app_start_time = datetime.time(9, 0, 0)
    # 定义程序结束运行时间为15:00:00
    app_end_time = datetime.time(15, 00, 0)
    while True:
        # 获取系统最新时间
        app_now_time = datetime.datetime.now().time()
        print(datetime.datetime.now(), '程序等待运行')
        time.sleep(3)
        # 如果系统最新时间大于等于程序开始运行时间，小于程序结束运行时间，则程序开始交易
        if app_start_time <= app_now_time <= app_end_time:
            print(datetime.datetime.now(), '程序开始运行')
            # 运行盘前交易事件函数
            jingni_before_trading_start(trade_mode, context_data)
            # 定义交易开始时间为09:30:00
            trade_start_time = datetime.time(8, 30, 0)
            # 定义交易结束时间为15:00:00
            trade_end_time = datetime.time(15, 00, 0)
            # 定义程序交易时间间隔为3秒
            trade_seconds = 3
            while True:
                # 获取系统最新时间
                trade_now_time = datetime.datetime.now().time()
                # 如果系统最新时间大于等于交易开始时间，小于等于交易结束时间，则运行盘中交易事件函数
                if trade_start_time <= trade_now_time <= trade_end_time:
                    jingni_handle_data(
                        trade_mode, context_data, trade_start_time, trade_end_time, trade_seconds)
                # 如果系统最新时间大于程序结束交易时间
                elif trade_now_time > trade_end_time:
                    break
            # 运行盘后交易事件函数
            jingni_after_trading_end(trade_mode, context_data)

if __name__ == '__main__':
    jingni_main(trade_mode,'')