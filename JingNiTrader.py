# -*- coding: utf-8 -*-

"""
项目名称：JingNiTrader
项目版本：v0.1.1
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

# 交易策略函数
def jingni_trade_strategy(trade_mode, context_data):
    print('今天当前的交易日日期是：', jingni_trading_dates(trade_mode, context_data, 0))
    print('今天前面的交易日日期是：', jingni_trading_dates(trade_mode, context_data, -1))
    print('今天后面的交易日日期是：', jingni_trading_dates(trade_mode, context_data, 1))

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