#!/usr/bin/python -u
import os
import time
import datetime

def at_home():
    hostnames = ["192.168.1.13", "192.168.1.15"]

    found = False
    for host in hostnames:
        print "Polling %s" % host
        cmd = "ping -c 1 " + host
        response = os.popen(cmd)
        status = response.close()
        if status == None: # None implies exit code 0 which means host is alive
            print "Poll: Successful"
            return True
        print "Poll: Unsuccessful"
    return False

def update():
    with open("%s/.home" % os.environ["HOME"],"w") as f:
        print "Was at home at %s" % datetime.datetime.now().isoformat(" ")
        f.write(str(time.time()))

while 1:
    time.sleep(0.5)
    if at_home():
        update()
    else:
        print "Not at home"

