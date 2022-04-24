import pandas as pd

# 送信コマンドテーブル
doip_cmd_tbl_send = \
[   #"cmand"                                            ,"protocol","KEY"                   ,"CMN" ,"TYPE","LEN"     ,"VALUE1"         ,"VALUE2"   ,"VALUE3"
    ["Vehicle identification request message"           ,"UDP"     ,"-CMD_UDP_VI_REQ-"      ,"02FD","0001","00000000",None             ,None       ,None           ],
    ["Vehicle identification request message with EID"  ,"UDP"     ,"-CMD_UDP_VI_REQ_EID-"  ,"02FD","0002","00000006","-TXT_EID-"      ,None       ,None           ],
    ["Vehicle identification request message with VIN"  ,"UDP"     ,"-CMD_UDP_VI_REQ_VIN-"  ,"02FD","0003","00000011","-TXT_VIN-"      ,None       ,None           ],
    ["DoIP entity status request"                       ,"UDP"     ,"-CMD_UDP_DES_REQ-"     ,"02FD","4001","00000000",None             ,None       ,None           ],
    ["Diagnostic power mode information request"        ,"UDP"     ,"-CMD_UDP_DPMI_REQ-"    ,"02FD","4003","00000000",None             ,None       ,None           ],
    ["Routing activation request"                       ,"TCP"     ,"-CMD_TCP_RA_REQ-"      ,"02FD","0005","00000007","-TXT_SA1-"      ,None       ,None           ],
    ["Alive check request"                              ,"TCP"     ,"-CMD_TCP_AC_REQ-"      ,"02FD","0007","00000000",None             ,None       ,None           ],
    ["Diagnostic message"                               ,"TCP"     ,"-CMD_TCP_DM-"          ,"02FD","8001","00000000","-TXT_SA2-"      ,"-TXT_TA-" ,"-TXT_DIAG-"   ],
    #["FREE MESSAGE"                                     ,"UDP"     ,"-CMD_UDP_FREE-"        ,None  ,None  ,None      ,"-TXT_UDP_FREE-" ,None       ,None           ],
    #["FREE MESSAGE"                                     ,"TCP"     ,"-CMD_TCP_FREE-"        ,None  ,None  ,None      ,"-TXT_TCP_FREE-" ,None       ,None           ],
    #["Diagnostic message positive acknowledgement"      ,"-CMD_TCP_DMA-"         ,"02FD","8002","00000005","-TXT_SA2-"  ,"-TXT_TA-" ,None           ],
]

# 受信コマンドテーブル
doip_cmd_tbl_recv = \
[
    ["vehicle identification response message"          ,"UDP"     ,"-CMD_UDP_VI_RES-"      ,"02FD","0004","00000021"],
    ["DoIP entity status response"                      ,"UDP"     ,"-CMD_UDP_DES_RES-"     ,"02FD","4002","00000007"],
    ["Diagnostic power mode information response"       ,"UDP"     ,"-CMD_UDP_DPMI_RES-"    ,"02FD","4004","00000001"],
    ["Routing activation response"                      ,"TCP"     ,"-CMD_TCP_RA_RES-"      ,"02FD","0006","00000009"],
    ["Alive check response"                             ,"TCP"     ,"-CMD_TCP_AC_RES-"      ,"02FD","0008","00000002"],
    ["Diagnostic message"                               ,"TCP"     ,"-CMD_TCP_DM-"          ,"02FD","8001","00000000"],
    ["Diagnostic message positive acknowledgement"      ,"TCP"     ,"-CMD_TCP_DMA-"         ,"02FD","8002","00000005"],
]

doip_send_df = pd.DataFrame((doip_cmd_tbl_send), columns=["cmand","protocol", "KEY", "CMN", "TYPE","LEN","VALUE1","VALUE2","VALUE3"])
doip_recv_df = pd.DataFrame((doip_cmd_tbl_recv), columns=["cmand","protocol", "KEY", "CMN", "TYPE","LEN"])


# 送信データ作成関数
def doip_make_msg(values,protocol):
    send_msg = None
    send_data = None
    # 送信コマンドテーブル検索
    for index, row in doip_send_df.iterrows():
        # 送信データ種別を判定
        if values[row["KEY"]] == True and protocol == row["protocol"] :
            send_msg = row["cmand"]
            payload_data = ""
            payload_len =""
            # ペイロード部分作成
            if row["cmand"] == "Routing activation request":
                payload_data += values[row["VALUE1"]]
                payload_data += "0000000000"
            else:
                if row["VALUE1"] != None:
                    payload_data += values[row["VALUE1"]]
                if row["VALUE2"] != None:
                    payload_data += values[row["VALUE2"]]
                if row["VALUE3"] != None:
                    payload_data += values[row["VALUE3"]]
            payload_len = hex(int(len(payload_data)/2))[2:]
            payload_len = payload_len.zfill(8)
            if None != payload_data:
                send_data = row["CMN"] + row["TYPE"] + payload_len + payload_data
            break
    return send_msg ,send_data


# ACK送信データ作成関数
def doip_make_msg_ack(values):
    send_msg = "02FD800200000005" + values["-TXT_SA2-"] + "00"
    return send_msg


# 受信データ判定関数
def doip_recv_msg(data,protocol):
    recv_msg = ""
    type = data[4:8]
    for index, row in doip_recv_df.iterrows():
        # 受信データ種別を判定
        if type == row["TYPE"] and protocol == row["protocol"] :
            recv_msg = row["cmand"]
    return recv_msg