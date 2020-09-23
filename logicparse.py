from logicdump import *
from logicDigiApi import *
import binascii
import sys

"""
folder name:
logicfiles

filenames:
SerExam_END_Pass_TX_to_Module.csv
SerExam_END_Pass_RX_from_Module.csv
Kdex_Pass_RX_from_Module.csv
Kdex_Pass_TX_to_Module.csv
Link_Fail_RX_from_Module.csv
Link_Fail_TX_to_Module.csv
SerExam_Pass_RX_from_Module.csv
SerExam_Pass_TX_to_Module.csv
"""

#### Some K5 Bg Files
#dumptype = "BlueGiga"
# rxfname = "frx.txt"
###rxfname = "logicfiles/SerExam_END_Pass_RX_from_Module.csv"
### rxfname = "logicfiles/SerExam_Pass_RX_from_Module.csv"
### rxfname = "logicfiles/Kdex_Pass_RX_from_Module.csv"
#rxfname = "SerRx.csv"
#rxfname = "ShortRx.txt"

###txfname = "ftx.txt"
###txfname = "logicfiles/Kdex_Pass_TX_to_Module.csv"
# txfname = "SerTx.csv"
#txfname = "ShortTx.txt"

### Some Digi XB files
dumptype = "DigiXb"
#txfname = "NormalTx.csv"
#rxfname = "NormalRx.csv"
txfname = "Mk4LogicCapt/TxFailuresTX.csv"
rxfname = "Mk4LogicCapt/TxFailuresRX.csv"
### txfname = "ShortDigiTx.csv"
### rxfname = "ShortDigiRx.csv"

linesParsed = 0
showPayload = False

rxBgrecs = []
txBgrecs = []
txrxBgRecs = []

# class LogicDump:
#     def __init__(self, handshake):
#         self.handshake = handshake
#         self.status = "none"
#         self.bytecount = 0
    
#     def add(self, timestamp, datum):
#         if self.status == "none":
#             self.status = "header"

def openfile(fname):
    print("Opening ...")
    try:
        fo = open(fname,"r")
    except:
        print("Cant open: ",fname)
        exit()
    return fo

def gotARecord(r):
    #print(dumpRec(r,showPayload))
    if r.msgFormat == 'H':
         txBgrecs.append(r)
    else:
         rxBgrecs.append(r)        

def dumpRec(r,p):
        rStr = "%09.5f %s <%02X %03d %02X %02X> %s" % (r.msgTimeStamp, r.msgFormat, r.msgType, r.msgPayloadLen, r.msgClass, r.msgMethod, r.message)
        if dumptype == "DigiXb":
            rStr += dumpDigiXPFrame(r)
        if showPayload == True:
            rStr += str(binascii.hexlify(r.msgPayload,'-'))
        return rStr

def dumpRecs(rV):
    global showPayload
    for r in rV:
        rStr = dumpRec(r,showPayload)
        print(rStr)
        if dumptype == "BlueGiga":
            if r.msgType != 0 and r.msgType != 128:
                print("Bad message type")
                exit()

def mergeRecs():
    txCnt = 0
    rxCnt = 0
    txrxCnt = 0
    txLen = len(txBgrecs)
    rxLen = len(rxBgrecs)
    print("%d %d" % (txLen,rxLen))
    while txCnt < txLen or rxCnt < rxLen:
        if rxCnt >= rxLen:
            #txrxRecs[txrxCnt] = txBgrecs[txCnt]
            txrxBgRecs.append(txBgrecs[txCnt])
            txCnt += 1
        elif txCnt >= txLen:
            #txrxRecs[txrxCnt] = rxBgrecs[rxCnt]
            txrxBgRecs.append(rxBgrecs[rxCnt])
            rxCnt += 1
        elif txBgrecs[txCnt].msgTimeStamp < rxBgrecs[rxCnt].msgTimeStamp:
            #txrxRecs[txrxCnt] = txBgrecs[txCnt]
            txrxBgRecs.append(txBgrecs[txCnt])
            txCnt += 1
        else:
            #txrxRecs[txrxCnt] = rxBgrecs[rxCnt]
            txrxBgRecs.append(rxBgrecs[rxCnt])
            rxCnt += 1
        txrxCnt += 1

def parsefile(fo,ld):
    global linesParsed
    for line in fo:
        #print(line, end='')
        ### get the float and the NxXX out of a string like this
        ### 0.025667000000000,'255' (0xFF),,
        ### But ignore a string like this
        ### Time [s],Value,Parity Error,Framing Error
        ### print("Line: " + str(len(line)))
        l = line.split(",")
        if l[0][0] != 'T' and len(line) > 10:
            ### print(float(l[0]))  ### The float is just the first list entry
            timestamp = float(l[0])  ### The float is just the first list entry
            try:
                ll = l[1].split('x')
                lll = ll[-1].split(')') ### use the last x as a delimiter ("16.337589999999999,x (0x78),,")
                datum = int(lll[0],16)
            except:
                print("Err: " + l[1])
                print(ll[-1])
                print(line)
                exit()
            ### print("Timestamp:" + str(timestamp) + " data:" + str(datum))
            ld.add(timestamp,datum,gotARecord)
            linesParsed += 1

def main():
    global showPayload
    global linesParsed

    print("Starting ...")
    nArgs = len(sys.argv)
    print("%d arguments" % (nArgs))
    print(sys.argv[0:])

    if 'p' in sys.argv:
        showPayload = True

    frx = openfile(rxfname)
    ftx = openfile(txfname)

    ldRx = LogicDump(False,dumptype)    
    ldTx = LogicDump(True,dumptype)

    print("Parsing Rx...")
    parsefile(frx,ldRx)
    print(str(linesParsed) + " Lines Parsed")

    linesParsed = 0
    print("Parsing Tx ...")
    parsefile(ftx,ldTx)
    print(str(linesParsed) + " Lines Parsed")

    frx.close()
    ftx.close()

    #dumpRecs(rxBgrecs)
    #dumpRecs(txBgrecs)
    mergeRecs()

    dumpRecs(txrxBgRecs)

    print("RxbufLen:%d" % (len(rxBgrecs)))
    print("TxbufLen:%d" % (len(txBgrecs)))
    print("RxTxbufLen:%d" % (len(txrxBgRecs)))

    print("End Program")

if __name__ == "__main__":
    main()
