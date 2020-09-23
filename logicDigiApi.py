class DigiApiRecord:
    def __init__(self):
        self.msgTimeStamp = 0.0
        self.msgFormat = '?'

    def dump(self):
        print("**********************Phil Sux********************")

class LogicDigiApiDump:
    def __init__(self, rx):
        self.handshake = handshake
        self.resetState()

    def resetState(self):
        self.apiRec = DigiApiRecord()

    def add(self, timestamp, datum, recCb):
        pass
