# coding: utf -8
import PySimpleGUI as sg # ライブラリの読み込み
import doip
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM

# テーマの設定
sg.theme("SystemDefault ")

# 事前設定
L1 = [
	# 診断機設定
	[sg.Text("・IPアドレス "),
	sg.InputText(default_text="127.0.0.1" , text_color = "#000000",background_color ="#ffffff",		size=(15,1),	key="-IP_EQP-" ),
	sg.Text("     ")],
	[sg.Text("・ポート番号 "),
	sg.InputText(default_text="13401" ,	text_color = "#000000",background_color ="#ffffff" ,		size=(8,1),		key="-PORT_EQP-" )]]

	# ＧＷ設定
L2 = [
	[sg.Text("・IPアドレス "),
	sg.InputText(default_text="127.0.0.2" , text_color = "#000000",background_color ="#ffffff" ,	size=(15,1),	key="-IP_GW-" ),
	sg.Text("     ")],
	[sg.Text("・ポート番号 "),
	sg.InputText(default_text="13400" ,	text_color = "#000000",background_color ="#ffffff" ,		size=(8,1),		key="-PORT_GW-" )]]
L3 = [
	[sg.Multiline(default_text="", border_width=1,	size=(130,8),autoscroll=True,	key="-COM_ST-")]]

# UDP
L4 = [[sg.Button("送信", border_width=4 ,												size =(15,1),	key="-BTN_SEND_UDP-")],			# ボタン
	## Vehicle identification request message
	[sg.Radio(text='Vehicle identification request message',							size=(50,1) ,	key="-CMD_UDP_VI_REQ-"	,	group_id='CMD_UDP') ],
	## Vehicle identification request message with EID
	[sg.Radio(text='Vehicle identification request message with EID',					size=(35,1) ,	key="-CMD_UDP_VI_REQ_EID-" ,	group_id='CMD_UDP') ],
	[sg.Text("・EID", size=(10,1)) , sg.InputText(default_text="112233445566" ,			size=(23,1) ,	key="-TXT_EID-")],
	## Vehicle identification request message with VIN
	[sg.Radio(text='Vehicle identification request message with VIN',					size=(35,1) ,	key="-CMD_UDP_VI_REQ_VIN-" ,	group_id='CMD_UDP')],
	[sg.Text("・VIN", size=(10,1)) , sg.InputText(default_text="446f697054657374546f6f6c2056494e2e" ,	size=(40,1) ,	key="-TXT_VIN-")],
	## DoIP entity status request
	[sg.Radio(text='DoIP entity status request',										size=(35,1) ,	key="-CMD_UDP_DES_REQ-" ,	group_id='CMD_UDP')],
	## Diagnostic power mode information request
	[sg.Radio(text='Diagnostic power mode information request',							size=(35,1) ,	key="-CMD_UDP_DPMI_REQ-" ,	group_id='CMD_UDP')],
#	## UDP FREE Message
#	[sg.Radio(text='FREE MESSAGE',														size=(15,1) ,	key="-CMD_UDP_FREE-"	,	group_id='CMD_UDP')],
#	[sg.Multiline(default_text="" , border_width=2,										size=(63,8),	key="-TXT_UDP_FREE-")]
]

# TCP
L5 = [[sg.Button("接続", border_width=4 , 												size =(15,1),	key="btn_connect_tcp"),				# ボタン
	sg.Button("切断", border_width=4 , 													size =(15,1),	key="btn_close_tcp"),				# ボタン
	sg.Button("送信", border_width=4 , 													size =(15,1),	key="btn_send_tcp")],				# ボタン
	## Routing activation request
	[sg.Radio(text='Routing activation request',										size=(52,1) ,	key="-CMD_TCP_RA_REQ-"	,	group_id='CMD_TCP') ],
	[sg.Text("・SA", size=(10,1)) , sg.InputText(default_text="1111" ,					size=(7,1) ,	key="-TXT_SA1-")],
	## Alive check request
	[sg.Radio(text='Alive check request',												size=(35,1) ,	key="-CMD_TCP_AC_REQ-"	,	group_id='CMD_TCP') ],
	## Diagnostic message
	[sg.Radio(text='Diagnostic message',												size=(35,1) ,	key="-CMD_TCP_DM-"	,	group_id='CMD_TCP')],
	[sg.Text("・SA", size=(10,1)) , sg.InputText(default_text="1111" ,					size=(7,1) ,	key="-TXT_SA2-"),
	sg.Text("・TA", size=(7,1)) , sg.InputText(default_text="2222" ,					size=(7,1) ,	key="-TXT_TA-")],
	[sg.Text("・User data", size=(10,1)),sg.Multiline(default_text="", border_width=2,	size=(50,3),	key="-TXT_DIAG-")],
#	## FREE Message
#	[sg.Radio(text='FREE MESSAGE',														size=(15,1) ,	key="-CMD_TCP_FREE-"	,	group_id='CMD_TCP')],
#	[sg.Multiline(default_text="" , border_width=2,										size=(63,8),	key="-TXT_TCP_FREE-")]
]


L = [[sg.Frame("DoIPクライアント（診断機）",L1),sg.Frame("DoIPサーバ（ゲートウェイ）",L2)],
	[sg.Frame("UDP",L4),sg.Frame("TCP",L5)],
	[sg.Frame("通信ステータス",L3)]]

# ウィンドウ作成
window = sg.Window ("DoIP cliant tool", L)
values = ""

def main():
	global values
	# イベントループ
	while True:
		# イベントの読み取り（イベント待ち）
		event , values = window.read()
		window_txt = ""
		# 確認表示
		# print(" イベント:",event ,", 値:",values)
		# 終了条件（ None: クローズボタン）
		if event == "-BTN_SEND_UDP-":
			window_txt += "----------UDPコマンド送信----------\n"
			window_txt += main_udp_send_cmd(values)
		# TCP接続
		elif event == "btn_connect_tcp":
			tcp_connect( values['-IP_EQP-'] , values['-IP_GW-'] , int(values['-PORT_EQP-']) , int(values['-PORT_GW-']) )
			window_txt +=  "----------TCP接続----------\n"
		# TCP切断
		elif event == "btn_close_tcp":
			tcp_close()
			window_txt +=  "----------TCP切断----------\n"
		elif event == "btn_send_tcp":
			window_txt += "----------TCPコマンド送信----------\n"
			window_txt += main_tcp_send_cmd(values)
		elif event == None:
			print(" 終了します． ")
			break
		window["-COM_ST-"].Update(window_txt.replace("\n\n\n","\n\n"))
		print(window_txt.replace("\n\n\n","\n\n"))
	# 終了処理
	window.close()


def main_udp_send_cmd(values):
	rtn = ""
	send_msg , send_data = doip.doip_make_msg(values,"UDP")
	if None != send_msg:
		rtn = send_msg + "\n" + send_data + "\n\n"
		rtn += udp_send( values['-IP_EQP-'] , values['-IP_GW-'] , int(values['-PORT_EQP-']) , int(values['-PORT_GW-']) , bytes.fromhex(send_data) )
	return rtn

def udp_send( src_ip , dst_ip , src_port , dst_port , data ):
	rtn = ""
	# 送信側アドレスをtupleに格納
	SrcAddr = ( src_ip , src_port )
	# 受信側アドレスをtupleに格納
	DstAddr = ( dst_ip , dst_port )
	# ソケット作成
	udpClntSock = socket(AF_INET, SOCK_DGRAM)
	# 送信側アドレスでソケットを設定
	udpClntSock.bind(SrcAddr)
	# 受信側アドレスに送信
	udpClntSock.sendto(data,DstAddr)
	# バッファサイズ指定
	BUFSIZE = 1024

	# While文を使用して常に受信待ちのループを実行
	while True:
		# ソケットにデータを受信した場合の処理
		# 受信データを変数に設定
		data, addr = udpClntSock.recvfrom(BUFSIZE)
		rtn = main_recv_cmd(data.hex(),"UDP")
		break
	return rtn


def tcp_connect( src_ip , dst_ip , src_port , dst_port ):
	global tcpClntSock
	# ソケット作成
	tcpClntSock = socket(AF_INET, SOCK_STREAM)
	tcpClntSock.settimeout(0.5)
	# 送信側アドレスをtupleに格納
	SrcAddr = ( src_ip , src_port )
	# 送信側アドレスでソケットを設定
	tcpClntSock.bind(SrcAddr)
	# サーバーに接続
	tcpClntSock.connect((dst_ip, dst_port))


def tcp_close():
	global tcpClntSock
	# ソケットクローズ
	tcpClntSock.close()
	print("TCP切断",tcpClntSock)


def main_tcp_send_cmd(values):
	rtn = ""
	send_msg , send_data = doip.doip_make_msg(values,"TCP")
	if None != send_msg:
		rtn = send_msg + "\n" + send_data + "\n\n"
		print(rtn)
		rtn += tcp_send( bytes.fromhex(send_data) )
		print(rtn)
	return rtn


def tcp_send( data ):
	global tcpClntSock
	rtn = ""
	try:
		tcpClntSock.send(data)
		response = tcpClntSock.recv(4096)
		rtn = main_recv_cmd(response.hex(),"TCP")
	except ConnectionResetError:
		# ソケットクローズ
		tcpClntSock.close()
	return rtn


def main_recv_cmd(data,protcol):
	global values
	global window
	window_txt = ""
	recv_msg = doip.doip_recv_msg(data,protcol)
	if None != recv_msg:
		#rtn = udp.udp_send( values['-IP_EQP-'] , values['-IP_GW-'] , int(values['-PORT_EQP-']) , int(values['-PORT_GW-']) , data )
		window_txt = "----------{}コマンド受信----------\n".format(protcol) + recv_msg + "\n" + data.upper()
	return window_txt


if __name__ == '__main__':
	main()