#!/usr/bin/env python
# -*- coding: utf8 -*-
#--------------------------------------
# ソケット通信でメッセージ送信
# 
#　前提：
#　　受信側の処理「server.py」を起動しておく必要があります。
#　　開放するポートの設定やユーザのIPアドレスの設定は「config.ini」に設定済みであること
#　概要：
# 　入力したメッセージを「config.ini」に設定されている「users」（複数選択可能）に
# 　メッセージを送信する。
#　実行例：
# 　python3 client.py
#--------------------------------------
import socket
import sys
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import configparser
from tkinter import messagebox
import time
 
#設定ファイル 
conf = configparser.ConfigParser()
conf.read('./config.ini', 'UTF-8')

root = tk.Tk()
root.title(conf.get('clientsetting','title'))
root.geometry(conf.get('clientsetting','size'))

#IPアドレス取得
localhostIP =(([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
#接続先リスト
connectlist=[]

#ボタン１のイベント　送信
def btEvent1():
    #リストボックスで選択された個数分送信する
    for sending in connectlist:
        print('Connect!:{}'.format(sending))
        print("Event1 %s::%s" %( "送信" , "001"))
        sockExec(sending,tx.get('1.0', tk.END))
    #テスト用LocalHostのみ送信
    #print("Event1 %s::%s" %( "送信" , "001"))
    #sockExec(localhostIP,tx.get('1.0', tk.END))

#ボタン２のイベント　クリア
def btEvent2():
    print("Event2 %s::%s" %( "クリア" , "002"))
    tx.delete('1.0', tk.END) 

#リストボックスを押した時のイベント
def select_listbox(event):
    connectlist.clear()
    for i in listbox.curselection():
        print(str(i)+"番目を選択中 " + listbox.get(i))
        #IPアドレスを取得
        connip=listbox.get(i).split(':')
        print('ConnectIP:{}'.format(connip[1]))
        #接続先リストに追加
        connectlist.append(connip[1])
    print('')

#ソケット通信
def sockExec( host,msg ):
    #IPv4/socket.AF_INET
    #TCP/socket.SOCK_STREAM
    #UDP/socket.SOCK_DGRAM
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(3)
        try:
            #サーバ側に接続
            s.connect((host,int(conf.get('settings','port'))))
            # サーバにメッセージを送る
            s.send(msg.encode(conf.get('environ','charset')))
            while True:
                try:
                    data = s.recv(int(conf.get('settings','clientdatasize')))
                    #print(repr(data))
                #戻りデータを受信し終わったらタイムアウトになるのでBreakして処理を抜ける
                except socket.timeout:
                    data=''
                if not data:
                    print('Break!')
                    break
            #テキストエリアに表示
            #tx.insert('end','\n->Send [{}] OK!'.format(host))
            messagebox.showinfo(conf.get('clientsetting','normsg'), conf.get('clientsetting','normagsnd') + '\nIP:' + host)
        except socket.timeout:
            #接続タイムアウト
            messagebox.showwarning(conf.get('clientsetting','erms'),conf.get('clientsetting','ermsgtimeout') + '\nIP:' + host)
        except Exception as e:
            #テキストエリアに表示
            #tx.insert('end','\n->Send [{}] NG!'.format(host))
            print(e)
            #メッセージダイアログを表示 : 送信エラー
            messagebox.showwarning(conf.get('clientsetting','erms'),conf.get('clientsetting','ermssnd')  + '\nIP:' + host)

#Label
lb = tk.Label(text=conf.get('clientsetting','labeltitle') + '(' + localhostIP + ')')
lb.pack()
#TextBox(スクロール)
tx = ScrolledText(root, width=40, height=20)
tx.insert('1.0','')
tx.pack()
#ボタン１
bt_snd = tk.Button(text=conf.get('clientsetting','bt1name') ,command=btEvent1, width=40)
bt_snd.pack()
#ボタン２
bt_cls = tk.Button(text=conf.get('clientsetting','bt2name'),command=btEvent2,width=40)
bt_cls.pack()
#Labe2
lb2 = tk.Label(text=conf.get('clientsetting','label2'))
lb2.pack()

#リストボックスのプロパティ―ファイルからユーザ名とIPアドレスを取得
listarray=[]
for connuser,addre in conf['users'].items():
    listarray.append('{}  :{}'.format(connuser,addre))
#リストボックス
list_value=tk.StringVar(value=listarray)
listbox=tk.Listbox(root,listvariable=list_value,selectmode="extended",width=40)
listbox.bind('<<ListboxSelect>>', select_listbox)
listbox.pack()

root.mainloop()
