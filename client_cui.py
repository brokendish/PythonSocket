#!/usr/bin/env python
# -*- coding: utf8 -*-
#--------------------------------------
# ソケット通信でメッセージ送信
# 
#　前提：
#　　受信側の処理「server.py」を起動しておく必要があります。
#　　開放するポートの設定やユーザのIPアドレスの設定は「config.ini」に設定済みであること
#　概要：
# 　パイプから取得したメッセージを「config.ini」に設定されている「broadcastusers」
# 　全てのアドレスに対して送信する。
#　実行例：
# 　cat config.ini | python3 client_cui.py
# 　echo "aaaaaa" | python3 client_cui.py
#--------------------------------------
import socket
import sys
import configparser
from contextlib import closing
from time import sleep
 
#設定ファイル 
conf = configparser.ConfigParser()
conf.read('./config.ini', 'UTF-8')

#ソケット通信
def sockExec( host,msg ):
    #IPv4/socket.AF_INET
    #TCP/socket.SOCK_STREAM
    #UDP/socket.SOCK_DGRAM
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(3)
        try:
            #サーバに接続
            s.connect((host,int(conf.get('settings','port'))))
            #サーバにメッセージを送る
            s.send(msg.encode(conf.get('environ','charset')))
            while True:
                try:
                    #戻りデータを受信（パケットサイズ単位で返信してくるのでループして全部受信する）
                    response = s.recv(int(conf.get('settings','clientdatasize')))
                    print('-------**-------')
                    print(response)
                #戻りデータを受信し終わったらタイムアウトになるのでBreakして処理を終了する
                except socket.timeout:
                    response=''
                if not response:
                    print('Break!')
                    break
        except socket.timeout:
            print('Error : {} IP:{}'.format('接続タイムアウト',host))
        except Exception as e:
            print('Error : {}'.format(e))
   
if __name__ == "__main__":
    msg=''
    #標準入力から送信するメッセージを取得
    for line in iter(sys.stdin.readline, ""):
        msg += line

    #リストボックスのプロパティ―ファイルからブロードキャストユーザとIPアドレスを取得
    for connuser,addre in conf['broadcastusers'].items():
        print("%s::%s" %( "送信" , "START"))
        #sockExec(addre,'{}\n'.format(u'a'*1027 + '##'))
        sockExec(addre,u'{}\n'.format(msg))
        print("%s::%s" %( "送信" , "END"))

    #----- テスト用　-----
    #IPアドレス取得
    #localhostIP =(([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
    #localhostIP='192.168.2.115'
    ipadder='192.168.2.100'
    #ipadder='169.254.100.253'
    #print("%s::%s" %( "送信" , "START"))
    #sockExec(ipadder,'{}\n'.format(u'a'*1027 + '##'))
    #print("%s::%s" %( "送信" , "END"))
    