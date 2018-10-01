import re

def framedSend(sock, file, debug=0):
    # if debug: print("framedSend: sending %d byte message" % len(payload))
    with open(file, 'rb') as f:
        messages = f.readlines()
        messages = [line.strip() for line in messages]
        for payload in messages:
            msg = str(len(payload)).encode() + b':' + payload
            while len(msg):
                nsent = sock.send(msg)
                msg = msg[nsent:]
    f.close()

rbuf = b""                      # static receive buffer

def framedReceive(sock, debug=0):
    global rbuf
    state = "getLength"
    msgLength = -1
    with open("FileFromClient.txt", "wb") as f:
        while True:
         if (state == "getLength"):
             match = re.match(b'([^:]+):(.*)', rbuf) # look for colon
             if match:
                  lengthStr, rbuf = match.groups()
                  try:
                       msgLength = int(lengthStr)
                  except:
                       if len(rbuf):
                            print("badly formed message length:", lengthStr)
                            return None
                  state = "getPayload"
         if state == "getPayload":
             if len(rbuf) >= msgLength:
                 payload = rbuf[0:msgLength]
                 rbuf = rbuf[msgLength:]
                 f.write(payload)
         r = sock.recv(100)
         print('received')
         rbuf += r
         if len(r) == 0:
             if len(rbuf) != 0:
                 print("FramedReceive: incomplete message. \n  state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
             return None
         if debug: print("FramedReceive: state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
    f.close()
