ソケット通信でメッセージの送受信をおこないます。
全てPython3で書いていますので、Python3がインストールされているWindowsとLinuxで実行可能です。
GUI(画面)部分はTkinterを使用しています。
（外部ライブラリは使用しないで作成していますのでPythonデフォルトのライブラリのみで使用できます）

ソフトは3つの構成になっています
１．server.py
　　メッセージ受信用の画面
    下記のクライアント側の処理から送信されたメッセージを受信します。
２．client.py
    メッセージ送信用の画面
    上記のサーバ側にメッセージを送信します。
３．client_cui.py
    メッセージ送信用のコマンド
    上記のサーバ側にメッセージを送信します。
    画面は使用せずにコマンドベースで実行できるので自動実行ジョブの結果送信等に使用します。
    

※注意
Windowsのネットワーク設定に
「Npcap Loopback Adapter」
がある場合は無効にしないと通信できないようです。

「Npcap Loopback Adapter」※は通常使用しないので無効にしても問題ありません。
※PC自身を表すIPアドレスでサーバを立てるときに自分自身の疎通確認のために使用するもの
