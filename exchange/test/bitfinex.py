# -*- coding: utf-8 -*-
# author: hzy(306679711@qq.com)

from websocket import create_connection
import time
import json

if __name__ == '__main__':
    while True:
        try:
            ws = create_connection(
                "wss://api.bitfinex.com/ws/2",
                http_proxy_host="127.0.0.1",
                http_proxy_port=1087)
            break
        except Exception as ex:
            print('connect ws error,retry...{}'.format(ex))
            time.sleep(5)

    print('connect is started.')

    # 订阅 KLine 数据
    tradeStr = json.dumps({
        "event": "subscribe",
        "channel": "candles",
        "key": "trade:1m:tETHUSD"
        # "key": "trade:1m:tETHUSD"
    })

    ws.send(tradeStr)

    while (True):
        res = ws.recv()
        print(res)
        # res = gzip.decompress(compressData).decode('utf-8')

        # print(res)

        # if res[:7] == '{"ping"':
        #     ts = res[8:21]
        #     pong = '{"pong":' + ts + '}'
        #     ws.send(pong)
#
