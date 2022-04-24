import pandas as pd
import app

# 初期設定
g_values = ""
g_sa = ""

# 応答コマンドテーブル
doip_cmd_tbl_send = \
[   #"REQUEST"                                        ,"REQTYPE"    ,"RESPONCE"                                    ,"PROTCOL","CMN" ,"TYPE","LEN"     ,"VALUE1"     ,"VALUE2"      ,"VALUE3"        ,"VALUE4"
    ["Vehicle identification request message"         ,"0001"       ,"vehicle identification response message"    ,"UDP"     ,"02FD","0004","00000021","-VIN_GW-"   ,"-LOGI_ADDR-","-EID_GW-"       ,"-GID_GW-"  ],
    ["Vehicle identification request message with EID","0002"       ,"vehicle identification response message"    ,"UDP"     ,"02FD","0004","00000021","-VIN_GW-"   ,"-LOGI_ADDR-","-EID_GW-"       ,"-GID_GW-"  ],
    ["Vehicle identification request message with VIN","0003"       ,"vehicle identification response message"    ,"UDP"     ,"02FD","0004","00000021","-VIN_GW-"   ,"-LOGI_ADDR-","-EID_GW-"       ,"-GID_GW-"  ],
    ["DoIP entity status request"                     ,"4001"       ,"DoIP entity status response"                ,"UDP"     ,"02FD","4002","00000007","-NODE_TYPE-","-CONN_NUM-" ,"-CONN_NOW_NUM-" ,"-MAX_LEN-" ],
    ["Diagnostic power mode information request"      ,"4003"       ,"Diagnostic power mode information response" ,"UDP"     ,"02FD","4004","00000001","-DIAG_ST-"  ,None         ,None             ,None        ],
    ["Routing activation request"                     ,"0005"       ,"Routing activation response"                ,"TCP"     ,"02FD","0006","00000009","-LOGI_ADDR-","-LOGI_ADDR-",None             ,None        ],
    ["Alive check request"                            ,"0007"       ,"Alive check response"                       ,"TCP"     ,"02FD","0008","00000002","-LOGI_ADDR-","-LOGI_ADDR-",None             ,None        ],
    ["Diagnostic message"                             ,"8001"       ,"Diagnostic message positive acknowledgement","TCP"     ,"02FD","8002","00000005","-LOGI_ADDR-","-LOGI_ADDR-",None             ,None        ],
    ["Diagnostic message positive acknowledgement"    ,"8002"       ,None                                         ,"TCP"     ,None  ,None   ,None     ,None         ,None         ,None             ,None        ],]

doip_recv_df = pd.DataFrame((doip_cmd_tbl_send), columns=["REQ","REQTYPE","RES","PROTCOL","CMN","TYPE","LEN","VALUE1","VALUE2","VALUE3","VALUE4"])


# 初期化関数
def doip_init(values):
    global g_values
    g_values = values
    return


# 送信データ作成関数
def doip_make_msg(row,data):
    global g_sa
    send_data = None
    send_msg = row["RES"]
    payload_data = ""
    # ペイロード部分作成
    if row["PROTCOL"] == "UDP":
        if row["VALUE1"] != None:
            payload_data += g_values[row["VALUE1"]]
        if row["VALUE2"] != None:
            payload_data += g_values[row["VALUE2"]]
        if row["VALUE3"] != None:
            payload_data += g_values[row["VALUE3"]]
        if row["VALUE4"] != None:
            payload_data += g_values[row["VALUE4"]]
        if row["RES"] == "vehicle identification response message":
            payload_data += "0000"
    else:
        if row["RES"] == "Routing activation response":
            g_sa = data[16:20]
            payload_data += g_sa + g_values[row["VALUE2"]] + "1000000000"
        if row["RES"] == "Alive check response":
            payload_data += g_values[row["VALUE1"]]
        if row["RES"] == "Diagnostic message positive acknowledgement":
            if "" != g_sa:
                payload_data += g_values[row["VALUE1"]] + g_sa + "00"
    # ぺーロード長作成
    payload_len = hex(int(len(payload_data)/2))[2:]
    payload_len = payload_len.zfill(8)
    # 送信データ作成
    if None != payload_data:
        send_data = row["CMN"] + row["TYPE"] + payload_len + payload_data
    return send_msg ,send_data


# 受信データ判定関数
def doip_recv_msg(data,protocol):
    recv_msg = ""
    send_msg = ""
    send_data = None
    type = data[4:8]
    for index, row in doip_recv_df.iterrows():
        # 受信データ種別を判定
        if type == row["REQTYPE"] and protocol == row["PROTCOL"] :
            recv_msg = row["REQ"]
            if row["REQ"] != "Diagnostic message positive acknowledgement":
                send_msg , send_data = doip_make_msg(row,data)
    return protocol,recv_msg,data,send_msg,send_data


# ACK送信データ作成関数
def doip_make_msg_ack(values):
    send_msg = "02FD800200000005" + values["-TXT_SA2-"] + "00"
    return send_msg







