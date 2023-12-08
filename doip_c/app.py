# coding: utf -8
import PySimpleGUI as sg # ライブラリの読み込み (Load library)
import doip
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM

# テーマの設定 (Theme setting)
sg.theme("SystemDefault ")

# 事前設定 (Pre-configuration)
L1 = [
	# 診断機設定 (Client setting)
	[sg.Text("・IPアドレス (IP address)"),
	sg.InputText(default_text="127.0.0.1" , text_color = "#000000",background_color ="#ffffff",		size=(15,1),	key="-IP_EQP-" ),
	sg.Text("     ")],
	[sg.Text("・ポート番号 (Port Number)"),
	sg.InputText(default_text="13401" ,	text_color = "#000000",background_color ="#ffffff" ,		size=(8,1),		key="-PORT_EQP-" )]]

	# ＧＷ設定 (GW setting)
L2 = [
	[sg.Text("・IPアドレス (IP address)"),
	sg.InputText(default_text="127.0.0.2" , text_color = "#000000",background_color ="#ffffff" ,	size=(15,1),	key="-IP_GW-" ),
	sg.Text("     ")],
	[sg.Text("・ポート番号 (Port number)"),
	sg.InputText(default_text="13400" ,	text_color = "#000000",background_color ="#ffffff" ,		size=(8,1),		key="-PORT_GW-" )]]
L3 = [
	[sg.Multiline(default_text="", border_width=1,	size=(130,8),autoscroll=True,	key="-COM_ST-")]]

# UDP
L4 = [[sg.Button("送信\nSend", border_width=4 ,										size =(15,2),	key="-BTN_SEND_UDP-")],			# ボタン (button)
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
L5 = [[sg.Button("接続\nConnect", border_width=4 , 									size =(15,2),	key="btn_connect_tcp"),				# ボタン (button)
	sg.Button("切断\nDisconnect", border_width=4 , 									size =(15,2),	key="btn_close_tcp"),				# ボタン
	sg.Button("送信\nSend", border_width=4 ,											size =(15,2),	key="btn_send_tcp")],			# ボタン
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


L = [[sg.Frame("DoIPクライアント（診断機） (Client)",L1),sg.Frame("DoIPサーバ（ゲートウェイ） (Server(Gateway))",L2)],
	[sg.Frame("UDP",L4),sg.Frame("TCP",L5)],
	[sg.Frame("通信ステータス (Communication status)",L3)]]

# ウィンドウ作成 (Create window)
window = sg.Window ("DoIP cliant tool", L)
values = ""

def main():
	global values
	# イベントループ (Event loop)
	while True:
		# イベントの読み取り（イベント待ち） (Read event (wait for event))
		event , values = window.read()
		window_txt = ""
		# 確認表示 (Confirmation indication)
		# print(" イベント:",event ,", 値:",values)
		# 終了条件（ None: クローズボタン） (Exit conditions(None: Close button))
		if event == "-BTN_SEND_UDP-":
			window_txt += "----------UDPコマンド送信 (UDP Send command)----------\n"
			window_txt += main_udp_send_cmd(values)
		# TCP接続 (TCP connect)
		elif event == "btn_connect_tcp":
			tcp_connect( values['-IP_EQP-'] , values['-IP_GW-'] , int(values['-PORT_EQP-']) , int(values['-PORT_GW-']) )
			window_txt +=  "----------TCP接続 (TCP Connect)----------\n"
		# TCP切断 (TCP disconnect)
		elif event == "btn_close_tcp":
			tcp_close()
			window_txt +=  "----------TCP切断 (TCP Disconnect)----------\n"
		elif event == "btn_send_tcp":
			window_txt += "----------TCPコマンド送信 (TCP Send command)----------\n"
			window_txt += main_tcp_send_cmd(values)
		elif event == None:
			print(" 終了します． (End.)")
			break
		window["-COM_ST-"].Update(window_txt.replace("\n\n\n","\n\n"))
		print(window_txt.replace("\n\n\n","\n\n"))
	# 終了処理 (End)
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
	# 送信側アドレスをtupleに格納 (Store sender address in tuple)
	SrcAddr = ( src_ip , src_port )
	# 受信側アドレスをtupleに格納 (Store the recipient address in a tuple)
	DstAddr = ( dst_ip , dst_port )
	# ソケット作成 (Create socket)
	udpClntSock = socket(AF_INET, SOCK_DGRAM)
	# 送信側アドレスでソケットを設定 (Configure socket with sender address)
	udpClntSock.bind(SrcAddr)
	# 受信側アドレスに送信 (Send to recipient address)
	udpClntSock.sendto(data,DstAddr)
	# バッファサイズ指定 (Set buffer size)
	BUFSIZE = 1024

	# While文を使用して常に受信待ちのループを実行
	while True:
		# ソケットにデータを受信した場合の処理 (Processing when receiving data on socket)
		# 受信データを変数に設定 (Save received data)
		data, addr = udpClntSock.recvfrom(BUFSIZE)
		rtn = main_recv_cmd(data.hex(),"UDP")
		break
	return rtn


def tcp_connect( src_ip , dst_ip , src_port , dst_port ):
	global tcpClntSock
	# ソケット作成 (Create socket)
	tcpClntSock = socket(AF_INET, SOCK_STREAM)
	tcpClntSock.settimeout(0.5)
	# 送信側アドレスをtupleに格納 (Store sender address in tuple)
	SrcAddr = ( src_ip , src_port )
	# 送信側アドレスでソケットを設定 (Configure socket with sender address)
	tcpClntSock.bind(SrcAddr)
	# サーバーに接続 (Connect to server)
	tcpClntSock.connect((dst_ip, dst_port))


def tcp_close():
	global tcpClntSock
	# ソケットクローズ (Close socket)
	tcpClntSock.close()
	print("TCP切断 (TCP Disconnect)",tcpClntSock)


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
		# ソケットクローズ (Close socket)
		tcpClntSock.close()
	return rtn


def main_recv_cmd(data,protcol):
	global values
	global window
	window_txt = ""
	recv_msg = doip.doip_recv_msg(data,protcol)
	if None != recv_msg:
		#rtn = udp.udp_send( values['-IP_EQP-'] , values['-IP_GW-'] , int(values['-PORT_EQP-']) , int(values['-PORT_GW-']) , data )
		window_txt = "----------{}コマンド受信 (Command reception)----------\n".format(protcol) + recv_msg + "\n" + data.upper()
	return window_txt


if __name__ == '__main__':
	main()