#! /usr/bin/python2.7
# -*- coding:utf-8 -*-
# hackaffeine.com - Santi

import subprocess
import time
import urllib2
import argparse
import re
import os
import fileinput

##########
#Time among checks
CHECK_TIME = 60
#Websites to check
WEB = 'http://your_website'
#Telegram username to send notifications
USER = 'User'
##########

#####
REPOSITORY= "https://github.com/vysheng/tg.git"
#####

parser = argparse.ArgumentParser(description = "Script to check websites status and send notifications with Telegram", epilog="Please report any bugs or suggestions to santisjb@gmail.com")
parser.add_argument("-n", "--noinstall", action="store_true", help="Use it to start without Telegram installation")
args = parser.parse_args()

def installTelegram(path,repository):

     subprocess.call("git clone --recursive " + repository + " " + path, shell = True)
     subprocess.call("cd /"+path+" && bash "+path+"/configure ;make", shell = True)
     subprocess.call("ln -s " + path + "/bin/telegram-cli /usr/bin/telegram-cli", shell = True)
     subprocess.call("mkdir /etc/telegram-cli", shell = True)
     subprocess.call("cp "+path+"/tg-server.pub /etc/telegram-cli/server.pub", shell = True)
    
def installDependencies():
     
     subprocess.call('apt-get update', shell = True)
     subprocess.call('apt-get -y install libreadline-dev libconfig-dev libssl-dev lua5.2 liblua5.2-dev libevent-dev libjansson-dev make git', shell = True)

def main():
    
    while True:
       try:
          f = urllib2.urlopen(WEB)
          code = f.getcode()
       except:
          code = "error"
       
       if code != 200:
            MSG = time.strftime("%H:%M:%S - %d/%m/%Y - ")+str(code)+" in "+WEB+" \n"
               
            subprocess.call('telegram-cli -WR -U root -e "msg ' + USER + ' ' +  MSG + ' " ',shell=True)
               
       time.sleep(CHECK_TIME)


if __name__ == '__main__':
  
    if(args.noinstall == False):
    
        telegram = raw_input("Do you want to install Telegram?(yes/no): ")
    
        if (telegram == "yes"):
        
            path = raw_input("Where do you want to install Telegram?(path): ")
            path += "/tg"
            Dependencies = raw_input("some dependencies needed, install?(yes/no): ")
        
            if (Dependencies == "yes"):
            
                installDependencies()
            
            installTelegram(path, REPOSITORY)
            
            main()
            
        
        elif (telegram == "no"):
        
            main()
        
        else:
        
           print ("something wrong!")
    else:
       main()
