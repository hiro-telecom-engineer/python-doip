# coding: utf -8
import PySimpleGUI as sg # ライブラリの読み込み
import threading
import sys
import socket
from socket import socket, AF_INET, SOCK_DGRAM ,SOCK_STREAM
import time
import doip


# テーマの設定
sg.theme("SystemDefault ")

# 事前設定
L1 = [[sg.Text("・IPアドレス "			,size=(20,1)),
	sg.InputText(default_text="127.0.0.2" , 	text_color = "#000000",background_color ="#ffffff" ,	size=(40,1),	key="-IP_GW" )],
	[sg.Text("・ポート番号 "			,size=(20,1)),
	sg.InputText(default_text="13400" ,			text_color = "#000000",background_color ="#ffffff" ,	size=(40,1),	key="-PORT_GW-" )],
	[sg.Text("・EID "				,size=(20,1)),
	sg.InputText(default_text="112233445566" ,	text_color = "#000000",background_color ="#ffffff" ,	size=(40,1),	key="-EID_GW-" )],
	[sg.Text("・VIN "				,size=(20,1)),
	sg.InputText(default_text="446f697054657374546f6f6c2056494e2e" ,	text_color = "#000000",background_color ="#ffffff" ,		size=(40,1),		key="-VIN_GW-" )],
	[sg.Text("・GID"				,size=(20,1)),
	sg.InputText(default_text="000000000001" ,	text_color = "#000000",background_color ="#ffffff" ,	size=(40,1),	key="-GID_GW-" )],
	[sg.Text("・ロジカルアドレス "	,size=(20,1)),
	sg.InputText(default_text="2222" ,			text_color = "#000000",background_color ="#ffffff" ,	size=(40,1),	key="-LOGI_ADDR-" )],
	[sg.Text("・ノードタイプ "		,size=(20,1)),
	sg.InputText(default_text="01" ,			text_color = "#000000",background_color ="#ffffff" ,	size=(40,1),	key="-NODE_TYPE-" )],
	[sg.Text("・接続可能数 "		,size=(20,1)),
	sg.InputText(default_text="01" ,			text_color = "#000000",background_color ="#ffffff" ,	size=(40,1),	key="-CONN_NUM-" )],
	[sg.Text("・接続コネクション "	,size=(20,1)),
	sg.InputText(default_text="00" ,			text_color = "#000000",background_color ="#ffffff" ,	size=(40,1),	key="-CONN_NOW_NUM-" )],
	[sg.Text("・最大データ長 "		,size=(20,1)),
	sg.InputText(default_text="0000FFFF" ,		text_color = "#000000",background_color ="#ffffff" ,	size=(40,1),	key="-MAX_LEN-" )],
	[sg.Text("・診断状態 "			,size=(20,1)),
	sg.InputText(default_text="01" ,			text_color = "#000000",background_color ="#ffffff" ,	size=(40,1),	key="-DIAG_ST-" )]
]
# UDP
L2 = [[sg.Button("OPEN", border_width=4 ,												size =(25,1),	key="-BTN_UDP_OPEN-")]]			# ボタン

# TCP
L3 = [[sg.Button("OPEN", border_width=4 , 												size =(25,1),	key="-BTN_TCP_OPEN-")]]				# ボタン

# 通信ステータス
L4 = [[sg.Multiline(default_text="", border_width=1,	size=(62,10),	key="-COM_ST-")]]

L = [[sg.Frame("DoIPサーバ設定",L1)],
	[sg.Frame("UDP",L2),sg.Frame("TCP",L3)],
	[sg.Frame("通信ステータス",L4)]]

# ウィンドウ作成
window = sg.Window ("DoIP sever tool", L)
values = ""

def main():
	global values
	threads = []
	# イベントループ
	while True:
		# イベントの読み取り（イベント待ち）
		event , values = window.read()
		# 確認表示
		# print(" イベント:",event ,", 値:",values)
		# 終了条件（ None: クローズボタン）
		if event == "-BTN_UDP_OPEN-":
			doip.doip_init(values)
			t1 = threading.Thread(target=udp_recv, args=(values['-IP_GW'] , int(values['-PORT_GW-']),))
			threads.append(t1)
			t1.setDaemon(True)
			t1.start()
			window["-COM_ST-"].Update("UDP OPEN")

		# TCP接続
		elif event == "-BTN_TCP_OPEN-":
			doip.doip_init(values)
			t2 = threading.Thread(target=tcp_recv, args=(values['-IP_GW'] , int(values['-PORT_GW-']),))
			threads.append(t2)
			t2.setDaemon(True)
			t2.start()
			window["-COM_ST-"].Update("TCP OPEN")
		elif event == None:
			sys.exit()


def main_window_update(protocol,recv_msg,data,send_msg,send_data):
	global values
	window_txt = ""
	window_txt += "----------{}コマンド受信----------\n".format(protocol) + recv_msg + "\n" + data + "\n"
	if "" != send_msg:
		window_txt += "\n----------{}コマンド送信----------\n".format(protocol) + send_msg + "\n" + send_data + "\n"
	window["-COM_ST-"].Update(window_txt)
	return


def udp_recv( ip_addr , port ):
	# 受信側アドレスをtupleに格納
	SrcAddr = ( ip_addr , port)
	# バッファサイズ指定
	BUFSIZE = 1024
	# ソケット作成
	udpServSock = socket(AF_INET, SOCK_DGRAM)
	# 受信側アドレスでソケットを設定
	udpServSock.bind(SrcAddr)
	time.sleep(1)
	# While文を使用して常に受信待ちのループを実行
	while True:
		time.sleep(1)
		# ソケットにデータを受信した場合の処理
		# 受信データを変数に設定
		data, addr = udpServSock.recvfrom(BUFSIZE)
		# 受信データを確認
		protocol,recv_msg,data,send_msg,send_data = doip.doip_recv_msg(data.hex(),"UDP")
		main_window_update(protocol,recv_msg,data,send_msg,send_data)
		if None != send_data:
			send_data = bytes.fromhex(send_data)
			udpServSock.sendto(send_data,addr)


BUFFER_SIZE = 1024

def tcp_recv( ip_addr , port ):
	tcp_server = socket(AF_INET, SOCK_STREAM)
	tcp_server.bind(( ip_addr , port))
	tcp_server.listen()
	time.sleep(1)
	while True:
		(connection, client) = tcp_server.accept()
		while True:
			try:
				data = connection.recv(BUFFER_SIZE)
				# 受信データを確認
				protocol,recv_msg,data,send_msg,send_data = doip.doip_recv_msg(data.hex(),"TCP")
				main_window_update(protocol,recv_msg,data,send_msg,send_data)
				if None != send_data:
					connection.send(bytes.fromhex(send_data))
			except:
				pass


if __name__ == '__main__':
	main()

