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
WEB = 'http//your_website'
HOSTING_PROVIDER ='http://your_provider_website'
#Path for logs - Default is the folder where you saved the script
LOG = os.getcwd()+'/conections.txt'
#Telegram username to send notifications
USER = 'User'
##########

#####
REPOSITORY= "https://github.com/vysheng/tg.git"
#####

parser = argparse.ArgumentParser(description = "Script to check websites status")
parser.add_argument("-a", "--autostart",action="store_true", help="Run demonized at startup")
parser.add_argument("-n", "--noinstall", action="store_true", help="Use it to start without Telegram installation")
args = parser.parse_args()

if (args.autostart):
     for line in fileinput.input('/etc/rc.local', inplace=True):
          if not line.strip() == "python " + os.getcwd() + '/checkurl.py -an':
               if line.strip() == 'exit 0':
                    print "python " +  os.getcwd() + '/checkurl.py -an'
               print line,

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
       try:
          provider_f = urllib2.urlopen(HOSTING_PROVIDER)
          provider_code = provider_f.getcode()
       except:
          provider_code= "provider error"

       if code != 200:
          with open(LOG,'a') as log:
               MSG = time.strftime("%H:%M:%S - %d/%m/%Y - ")+str(code)+" in "+WEB+" ; provedor code = "+str(provider_code)+"\n"
               log.write(MSG)
               subprocess.call('telegram-cli -WR -e "msg ' + USER + ' ' +  MSG + ' " ',shell=True)               
            
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
