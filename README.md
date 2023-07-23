# m32bot
Virtual QSO bot for the Morserino 32

Based on https://github.com/pavian57/qsosrv

## Prereq

* The app binds to UDP port 7373.  That port must be available and reachable on the server that runs this app.  

## Running the App Local
This requires Python 3.10 or higher.  
```
python3 main.py
```

## Building and Running the app in Docker (Optional)

Docker Build
```
docker build -t m32bot:dev .
```

Docker Run
```
docker run -d --name m32bot -p 7373:7373/udp m32bot:dev
```

## Usage

### Setup Moresino 

1. Go to the Wifi Functions Modulus
2. Select Config Wifi
3. Using a computer with wireless connect to the SSID morserino
4. Go to m32.local or 192.168.4.1
5. Set the SSID and Password of your Wifi
6. Set the Wifi Peer to the IP of the server running this bot
7. Save and the Morserino will reboot.  

### Connecting to the bot

1. Start the bot via the above instructions for running local or thru docker.  
2. On the Morserino go to the Modulus Transceiver
3. Select Wifi Trx, The Morserino will now connect to the bot.  
4. Run a test by sending the word hi in CW.  The bot will reply with hello if all is ok.  
