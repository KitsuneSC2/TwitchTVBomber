import socks
import threading
import random
from time import sleep
 
accounts = open("accounts.txt", "r").readlines()
proxies = open("proxies.txt", "r").readlines()
channel = raw_input("channel> ")
message = raw_input("message> ")
 
def listenForData(socket):
    while True:
        data = socket.recv(1024)
        data = data.strip()
        splitData = data.split()
        try:
            if splitData[0] == "PING":
                socket.send("PONG %s\n" % splitData[1])
        except:
            continue
        
def connectToChat(account, proxy, channel, message):
    username = account[0]
    password = "%s:%s" % (account[1], account[2])
    socket = socks.socksocket()
    socket.setproxy(socks.PROXY_TYPE_HTTP, proxy[0], int(proxy[1]))
    socket.connect(("irc.twitch.tv", 6667))
    socket.send("PASS %s\n" % password)
    socket.send("NICK %s\n" % username)
    socket.send("USER %s %s %s :%s\n" % (username, username, username, username))
    socket.send("JOIN #%s\n" % channel)
    threading.Thread(target=listenForData, args=[socket]).start()
    sleep(11)
    while True:
                socket.send("PRIVMSG #%s :%s %d\n" % (channel, message, random.randrange(10000, 99999)))
                sleep(2.5)
 
for account in range(len(accounts)):                
    threading.Thread(target=connectToChat, args=[accounts[account].strip().split(":"),
                                           proxies[account].strip().split(":"),
                                           channel,
                                           message]).start()
    #connectToChat(accounts[0].split(":"), proxies[0].strip().split(":"), channel, message)