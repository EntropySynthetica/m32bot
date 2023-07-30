import socket
import binascii
import time
import random
import string
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

# If Debug is on print this to console
def log(s):
    if DEBUG:
        print("log: " + s)

# Func to send this text to the M32
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


# Generate a random US format Callsign
def makeCall():
    prefixA = random.choice(['a','k','w','n'])
    prefixB = ""
    if random.randint(1,2) == 1:
          prefixB = ''.join(random.choices(string.ascii_lowercase, k=1))
    dist = ''.join(random.choices(string.digits, k=1))
    suffix = ''.join(random.choices(string.ascii_lowercase, k=random.randint(1, 3)))

    botCall = prefixA + prefixB + dist + suffix
    
    return botCall


def main():
    rxBuffer = ""

    while True:
        payload, client_address = sock.recvfrom(64)
        b = bytearray(payload)
        hexstr  = binascii.hexlify(b)
        morsecode = translator.mopptotxt(hexstr)
        tlg = morsecode.strip()
        log('<'+morsecode+'>')

        rxBuffer = rxBuffer + str(morsecode.strip() + " ")
        print("Buffer: " + rxBuffer)

        # If we are sent the word hi send back hello.  This is our M32 test Ping.
        if morsecode.strip() == 'hi':
              sendmoppstr(client_address, 'hello')
              print("TX: hello")

        # If we get teh wrod test send back a random US call. 
        if morsecode.strip() == 'test':
              sendmoppstr(client_address, makeCall())
              print("TX: Bot Call")


              


if __name__=="__main__":
    main()