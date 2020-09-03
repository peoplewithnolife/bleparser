class BgRecord:
    def __init__(self):
        self.msgTimeStamp = 0.0
        self.msgFormat = '?'
        self.msgType = 0
        self.msgPayloadLen = 0
        self.msgClass = 0
        self.msgMethod = 0
        self.msgPayload = bytearray(b'')

    def dump(self):
        print("**********************Phil Sux********************")

class LogicDump:
    def __init__(self, handshake):
        self.handshake = handshake
        self.resetState()

    def resetState(self):
        self.bgRec = BgRecord()
        if self.handshake:
            self.status = "handshake"
            self.bgRec.msgFormat = 'H'
        else:
            self.status = "head"
            self.bgRec.msgFormat = 'X'
        self.frmCount = 0
        self.frmLen = 0
        self.headCount = 0
        self.payloadCount = 0
        self.payloadLen = 0

    def add(self, timestamp, datum, recCb):
        if self.status == "handshake":
            self.frmCount = 0
            self.frmLen = datum
            self.headCount = 0
            self.status = "head"
        elif self.status == "head":
            if self.headCount == 0:
                self.bgRec.msgTimeStamp = timestamp
                self.bgRec.msgType = datum
            if self.headCount == 1:
                self.payloadLen = datum
                self.bgRec.msgPayloadLen = datum
            if self.headCount == 2:
                self.bgRec.msgClass = datum
            if self.headCount == 3:
                self.bgRec.msgMethod = datum
            self.headCount += 1
            if self.headCount >= 4:
                self.payloadCount = 0
                self.status = "payload"
            if self.headCount == 1:
                # Check for error
                if self.bgRec.msgType != 0 and self.bgRec.msgType != 128:
                    self.resetState()    
                
        elif self.status == "payload":
            self.bgRec.msgPayload.append(datum)
            self.payloadCount += 1
            if self.payloadCount >= self.payloadLen:
                recCb(self.bgRec)
                if self.bgRec.msgType != 0 and self.bgRec.msgType != 128:
                    print("Bad Message Type: %d" %(self.bgRec.msgType))
                    exit()
                self.resetState()
        else:
            self.resetState()
        #self.dump()

    def dump(self):
        print(self.status + " " + str(self.payloadCount))
"""
No Handshake
33.895713999999998,'0' (0x00),, Type = 0
33.895904999999999,'2' (0x02),, PLLen = 2 
33.896096000000000,'6' (0x06),, Class = 6
33.896287000000001,\t (0x09),,  Method = 9
33.896478000000002,'0' (0x00),, PL 0
33.896669000000003,'0' (0x00),, PL 1

0.172356500000000,'128' (0x80),, Type = 128
0.172547500000000,'3' (0x03),,   PLLen = 3
0.172738500000000,'4' (0x04),,   Class = 4
0.172929500000000,'0' (0x00),,   Method = 0
0.173120500000000,'0' (0x00),,   PL 0
0.173311500000000,'5' (0x05),,   PL 1
0.173502000000000,'0' (0x00),,   PL 2

0.173693000000000,'128' (0x80),, Type = 128
0.173884000000000,'27' (0x1B),,  PLLen = 27
0.174075000000000,'2' (0x02),,   Class = 2
0.174266000000000,'0' (0x00),,   Method = 0
0.174960000000000,'0' (0x00),,   PL 0
0.175151000000000,'0' (0x00),,   PL 1
0.175342000000000,'8' (0x08),,   PL 2
0.175533000000000,'0' (0x00),,   PL 3
0.175724000000000,'0' (0x00),,   PL 4
0.175914500000000,'0' (0x00),,   PL 5
0.176105500000000,'20' (0x14),,  PL 6
0.176296500000000,~ (0x7E),,     PL 7
0.176487500000000,'0' (0x00),,   PL 8
0.176678500000000,'0' (0x00),,   PL 9
0.176869500000000,H (0x48),,     PL 10
0.177060000000000,'0' (0x00),,   PL 11
0.177251000000000,5 (0x35),,     PL 12
0.177442000000000,'0' (0x00),,   PL 13
0.177633000000000,^ (0x5E),,     PL 14
0.177824000000000,'7' (0x07),,   PL 15
0.178015000000000,'128' (0x80),, PL 16
0.178205500000000,'215' (0xD7),, PL 17
0.178396500000000,'1' (0x01),,   PL 18
0.178587500000000,'0' (0x00),,   PL 19
0.178778500000000,'255' (0xFF),, PL 20
0.178969500000000,'255' (0xFF),, PL 21
0.179160500000000,'255' (0xFF),, PL 22
0.179351500000000,'255' (0xFF),, PL 23
0.179542000000000,'255' (0xFF),, PL 24
0.179733000000000,'255' (0xFF),, PL 25
0.179924000000000,'255' (0xFF),, PL 27

Handshake
0.134240000000000,'28' (0x1C),, HSLen = 28
0.134413500000000,'0' (0x00),,  Frm 0 Type = Cmd
0.134587000000000,'24' (0x18),, Frm 1 PLLen = 24
0.134760000000000,'2' (0x02),,  Frm 2 Class = 2
0.134933500000000,'0' (0x00),,  Frm 3 Method = 0 
0.135106500000000,'5' (0x05),,  Frm 4  PL 0
0.135280000000000,'0' (0x00),,  Frm 5  PL 1
0.135453000000000,'0' (0x00),,  Frm 6  PL 2
0.135626500000000,'20' (0x14),, Frm 7  PL 3
0.135800000000000,~ (0x7E),,    Frm 8  PL 4
0.135973500000000,'4' (0x04),,  Frm 9  PL 5
0.136147000000000,'0' (0x00),,  Frm 10 PL 6
0.136320500000000,'2' (0x02),,  Frm 11 PL 7
0.136494000000000,'0' (0x00),,  Frm 12 PL 8
0.136667000000000,5 (0x35),,    Frm 13 PL 9
0.136840000000000,'0' (0x00),,  Frm 14 PL 10
0.137013500000000,O (0x4F),,    Frm 15 PL 11
0.137187000000000,'22' (0x16),, Frm 16 PL 12
0.137360500000000,~ (0x7E),,    Frm 17 PL 13
0.137534000000000,'0' (0x00),,  Frm 18 PL 14
0.137707500000000,'0' (0x00),,  Frm 19 PL 15
0.137880500000000,'0' (0x00),,  Frm 20 PL 16
0.138054000000000,'0' (0x00),,  Frm 21 PL 17
0.138227000000000,'0' (0x00),,  Frm 22 PL 18
0.138400000000000,'0' (0x00),,  Frm 23 PL 19
0.138573500000000,'0' (0x00),,  Frm 24 PL 20
0.138747000000000,'0' (0x00),,  Frm 25 PL 21
0.138920000000000,'0' (0x00),,  Frm 26 PL 22
0.139093500000000,'0' (0x00),,  Frm 27 PL 23

33.901234000000002,\t (0x09),,   HSLen = 9
33.901406999999999,'0' (0x00),,  FRM 0   Type = 0 (Command)
33.901580500000001,'5' (0x05),,  FRM 1   PLLen = 5
33.901753999999997,'6' (0x06),,  FRM 2   Class = 6
33.901927499999999,'8' (0x08),,  FRM 3   Method = 8
33.902101000000002,2 (0x32),,    FRM 4   PL 0
33.902273999999998,'0' (0x00),,  FRM 5   PL 1
33.902447500000001,COMMA (0x2C),,FRM 6   PL 2
33.902620499999998,'1' (0x01),,  FRM 7   PL 3
33.902794000000000,'3' (0x03),,  FRM 8   PL 4

"""