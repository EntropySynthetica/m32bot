# m32bot
Virtual QSO bot for the Morserino 32

Based on https://github.com/pavian57/qsosrv

## Building the App

Docker Build
```
docker build -t m32bot:dev .
```

Docker Run
```
docker run -d --name m32bot -p 7373:7373/udp m32bot:dev
```