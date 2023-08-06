import socket
import binascii
import time
import random
import string
import re
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

    botCall = str(prefixA + prefixB + dist + suffix)

    return botCall


def main():
    rxBuffer = ""
    state = "idle"
    botCall = ""
    clientCall = ""
    lastRxTime = int(time.time())

    while True:
        payload, client_address = sock.recvfrom(64)
        b = bytearray(payload)
        hexstr  = binascii.hexlify(b)
        morsecode = translator.mopptotxt(hexstr)

        log('<'+morsecode+'>')


        # If it's been more than 8 seconds since the last RX lets clear the buffer. 
        now = int(time.time())
        lastRxAge = now - lastRxTime
        if lastRxAge > 8:
            rxBuffer = ""
            print("Buffer cleared due to timeout")

        # If it's been more than 60 seconds lets reset state to idle and drop any QSOs. 
        if lastRxAge > 60:
            state = "idle"
            botCall = ""
            print("State cleared to idle")
        

        # Add the last recieved character or characters from the M32 to a buffer.
        rxBuffer = rxBuffer + str(morsecode.strip() + " ")
        print("Buffer: " + rxBuffer)


        # If we send the word ping send back the word pong to verify everything is working.  
        pingRex = r'^ping'
        if re.match(pingRex, rxBuffer.replace(" ", "")):
            print("TX: pong")
            sendmoppstr(client_address, 'pong')
            rxBuffer = ""


        # If we get the word test send back a random US call. 
        testRex = r'^test'
        if re.match(testRex, rxBuffer.replace(" ", "")):
            sendmoppstr(client_address, makeCall())
            print("TX: Bot Call")
            rxBuffer = ""


        # If we think we hear an error lets clear the buffer
        errorRex = r'.*eeee'
        if re.match(errorRex, rxBuffer.replace(" ", "")):
            print("Got Error from sender, Buffer Cleared")
            rxBuffer = ""


        # If the bot hears a CQ lets gen a call and reply.  
        cqRex = r'(?:cq){1,3}(?P<event>.*?)de(?P<cqCaller>.*?)k$'
        cqMatch = re.match(cqRex, rxBuffer.replace(" ", ""))
        if cqMatch and state=="idle":
            print("CQ Found from " + cqMatch.group('cqCaller'))
            state = "QSO"
            print("State set to QSO")
            botCall = makeCall()
            clientCall = cqMatch.group('cqCaller')
            sendmoppstr(client_address, botCall)


        # if the bot hears agn lets repeat the bots call.
        agnRex = r'^agn'
        agnMatch = re.match(agnRex, rxBuffer.replace(" ", ""))
        if agnMatch and state=="QSO":
            sendmoppstr(client_address, botCall)
            print("Bot is resending it's call")


        # If the client is answering bot reply to CQ
        cqAnsRex = r'(?P<botCall>.*?)de(?P<clientCall>.*?)k'
        cqAnsMatch = re.match(cqAnsRex, rxBuffer.replace(" ", ""))
        if cqAnsMatch and state=="QSO":
            if cqAnsMatch.group('botCall')==botCall:
                QSOReply = clientCall + " de " + botCall + " GA UR 5nn 5nn BK"
                sendmoppstr(client_address, QSOReply)


        # If the bot hears 73 sk then it will end the QSO and return state to idle"
        endQSORex = r'.*73sk'
        endQSOMatch = re.match(endQSORex, rxBuffer.replace(" ", ""))
        if endQSOMatch and state=="QSO":
            endReply = clientCall + " de " + botCall + " 73 sk"
            sendmoppstr(client_address, endReply)
            state = "idle"
            botCall = ""


        lastRxTime = int(time.time())
        print("")


if __name__=="__main__":
    main()