#!/usr/bin/env python
# -*- coding: utf8 -*-
#--------------------------------------
# ソケット通信でメッセージ受信
# 
#　前提：
#　　開放するポートの設定やユーザのIPアドレスの設定は「config.ini」に設定済みであること
#　概要：
#　　送信側の処理「client.py」(GUI)又は「lient_cui.py」(CUI)から送信されてくる
#　　メッセージを受信します。
#　　メッセージ表示エリアは「config.ini」で指定した「reloadtime」の間隔で更新されます。
#　実行例：
# 　python3 server.py
#--------------------------------------
import socket
import struct
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter import filedialog
import configparser
import threading
import datetime
import os
from contextlib import closing
from time import sleep
import sys

#設定ファイル 
conf = configparser.ConfigParser()
conf.read('./config.ini', 'UTF-8')

#IPアドレス取得
localhostIP =(([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
print(localhostIP)

def socketThread():
    #IPv4/socket.AF_INET
    #TCP/socket.SOCK_STREAM
    #UDP/socket.SOCK_DGRAM
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # IPアドレスとポートを指定
        s.bind((localhostIP, int(conf.get('settings','port'))))
        # 接続要求を 5 個 (通常の最大値) まで順番待
        s.listen(5)
        # connectionを待つ
        while True:
            #アクセスしてきたら、コネクションとアドレスを入れる
            conn, addr = s.accept()
            print('conn:{} addr:{}'.format(conn,addr))
            data_sum = bytes()
            with conn:
                while True:
                    try:
                        # データを受け取る
                        data = conn.recv(int(conf.get('settings','serverdatasize')))
                        data_sum = data_sum + data
                        if not data:
                            print('Break!')
                            break
                        # クライアントにデータを返す(b -> byte でないといけない)
                        #conn.sendall(b'Recebbived: ' + data)
                        conn.send(data)
                    except BrokenPipeError:
                        print('BrokenPipe Error!!')
                    except Exception as e:
                        print(e)
                        messagebox.showwarning('エラー',e)
                        #break
                    #sleep(1)
                #受信ログファイルに追記
                with open(conf.get('log','serverlog'),'a',encoding="utf-8") as f:
                    ddaattee=datetime.datetime.today().strftime("%Y/%m/%d/%H:%M:%S")#フォーマットの指定
                    f.write('---------- ' + ddaattee + ' Form:' + localhostIP + '----------\n')
                    f.write(data_sum.decode('utf-8'))
                    f.write('-------------------------------------------\n')

def updateText():
    #指定時間でテキストエリアを更新
    root.after(int(conf.get('serversetting','reloadtime')),updateText)
    if btval.get():
        #ログファイル読み込み
        with open(conf.get('log','serverlog'),'r',encoding="utf-8") as f:
            log=f.read()
        tx.delete('1.0', 'end')
        tx.insert('end',log)
        tx.see('end')

#ボタンのイベント　削除
def btEvent1():
    print("Event1 %s::%s" %( "削除" , "001"))
    # メッセージボックス（はい・いいえ） 
    ret = messagebox.askyesno(conf.get('serversetting','msg1'), conf.get('serversetting','msg2'))
    if ret == True:
        #空ファイル作成
        with open(conf.get('log','serverlog'),'w',encoding="utf-8") as f:
            f.write('')
#ボタンのイベント　読込
def btEvent2():
    print("Event1 %s::%s" %( "読込" , "002"))
    with open(conf.get('log','serverlog'),'r',encoding="utf-8") as f:
        log=f.read()
    tx.delete('1.0', 'end')
    tx.insert('end',log)
    tx.see('end')
#ボタンのイベント　保存
def btEvent3():
    print("Event1 %s::%s" %( "保存" , "003"))
    root.filename =  filedialog.asksaveasfilename(initialdir = "/",title = "Save as",filetypes =  [("text file","*.txt")])
    print (root.filename)
    with open(root.filename, 'w') as f:
        f.write(tx.get('1.0', 'end'))
#閉じるボタンのイベント
def on_closing():
    #if messagebox.askokcancel("Quit", "Do you want to quit?"):
    #
    #スレッドが終了するまで待機
    th1.join(1)
    global root
    root.destroy()
    os._exit(0)

if __name__ == "__main__":

    #スレッド処理でクライアントからメッセージを受信
    #ソケット処理をスレッド化
    th1 = threading.Thread(target=socketThread,)
    # スレッドスタート
    th1.start()

    #画面の処理
    root = tk.Tk()
    root.title(conf.get('serversetting','title'))
    root.geometry(conf.get('serversetting','size'))
    root.protocol('WM_DELETE_WINDOW', on_closing)
    #root.protocol("WM_SAVE_YOURSELF", on_closing)
    #Label
    lb = tk.Label(text=conf.get('serversetting','labeltitle'))
    lb.pack()
    #TextBox(スクロール)
    tx = ScrolledText(root, width=100, height=35)
    tx.insert('1.0',"")
    tx.see('end')
    tx.pack()
    #チェックボタン　自動読み込みの要否
    btval = tk.BooleanVar()
    btval.set(True)
    bt_aut = tk.Checkbutton(root,text=conf.get('serversetting','btauto'),variable=btval)
    bt_aut.pack(side=tk.LEFT)
    #ボタン　ログ削除
    bt_del = tk.Button(text=conf.get('serversetting','btdel'),command=btEvent1,width=10)
    bt_del.pack(side=tk.LEFT)
    #ボタン　ログ読込
    bt_read = tk.Button(text=conf.get('serversetting','btread'),command=btEvent2,width=30)
    bt_read.pack(side=tk.LEFT)
        #ボタン　ログ保存
    bt_save = tk.Button(text=conf.get('serversetting','btsave'),command=btEvent3,width=30)
    bt_save.pack(side=tk.LEFT)

    updateText()
    root.mainloop()