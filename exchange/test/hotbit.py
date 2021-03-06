# -*- coding: utf-8 -*-
# author: hzy(306679711@qq.com)

from websocket import create_connection
# import gzip
import sys
import time
import json

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('USE: python bitfinex.py btc_usd,eth_usd')

    symbols = sys.argv[1] if len(sys.argv) > 1 else "eth_btc"
    symbols = symbols.split(",")

    while True:
        try:
            ws = create_connection(
                "wss://ws.hotbit.io",
                http_proxy_host="127.0.0.1",
                http_proxy_port=1087)
            break
        except Exception as ex:
            print('connect ws error,retry...{}'.format(ex))
            time.sleep(2)

    print('connect is started.')

    try:
        # 订阅  Market Kline 数据

        # tradeStr = json.dumps({
        #     "method": "kline.subscribe",
        #     "params": ["LCSBTC", 3600],
        #     "id": 100
        # })

        # ws.send(tradeStr)

        # sub_data_list = [
        #     json.dumps({
        #         "method": "kline.subscribe",
        #         "params": [symbol.replace("_", "").upper(), 60],
        #         "id": int(time.time() * 1000000)
        #     }) for symbol in symbols
        # ]
        sub_data_list = [symbol.replace("_", "").upper() for symbol in symbols]
        # subId = 10000
        # for symbol in symbols:
        #     subId += 1
        #     subData = json.dumps({
        #         "method":
        #         "kline.subscribe",
        #         "params": [symbol.replace("_", "").upper(), 60],
        #         "id":
        #         subId
        #     })
        #     sub_data_list.append(subData)

        # for sub in sub_data_list:
        #     ws.send(sub)

        ping = json.dumps({"method": "server.ping", "params": [], "id": 100})
        timeStart = time.time()
        symbolIndex = 0
        while True:
            symbol = sub_data_list[symbolIndex]
            klineQuery = json.dumps({
                "method":
                "kline.query",
                "params":
                [symbol, int(time.time()) - 60,
                 int(time.time()), 60],
                "id":
                int(time.time())
            })
            ws.send(klineQuery)
            res = ws.recv()

            timeEnd = time.time()
            if timeEnd - timeStart > 0.5:  # 2 seconds ping heartbeat
                timeStart = timeEnd
                ws.send(ping)
            print(res)

            symbolIndex += 1
            if symbolIndex >= len(sub_data_list):
                symbolIndex = 0

    except Exception as ex:
        print(ex)
