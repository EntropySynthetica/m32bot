import socket
import binascii
import time
from mopp import Moppm32

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

SERVER_IP = "0.0.0.0"
UDP_PORT = 7373
DEBUG = True


server = (SERVER_IP, UDP_PORT)
sock.bind(server)
print("Listening on " + SERVER_IP + ":" + str(UDP_PORT))
translator = Moppm32()

print('M32Bot Ready:')

def log(s):
    if DEBUG:
        print("log: " + s)

def sendmoppstr(adr, txtstr):
        log(txtstr)
        sendstr = translator.txttomopp(txtstr)
        splits = [sendstr[x:x + 8] for x in range(0, len(sendstr), 8)]
        frame = bytearray()
        for split in splits:
                value = 0
                t = len(split)
                for i in range (t): 
                        value *= 2   # // double the result so far
                        if split[i] == '1':
                                value +=1 #++; //add 1 if needed
                frame.append(value)  #
        time.sleep(0.2)
        sock.sendto(frame,adr)

def main():
    while True:
        payload, client_address = sock.recvfrom(64)
        b = bytearray(payload)
        hexstr  = binascii.hexlify(b)
        morsecode = translator.mopptotxt(hexstr)
        tlg = morsecode.strip()
        log('<'+morsecode+'>')

        if morsecode.strip() == 'hi':
              sendmoppstr(client_address, 'hello')
              print("TX: hello")


if __name__=="__main__":
    main()