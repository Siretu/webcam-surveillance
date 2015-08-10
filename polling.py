import os
import time
import datetime

def at_home():
    hostnames = ["192.168.1.13"]

    found = False
    for host in hostnames:
        print "Polling %s" % host
        cmd = "ping -c 1 " + host
        response = os.popen(cmd).read()
        if "64 bytes from" in response:
            print "Found"
            found = True
            break
    return found

def update():
    with open("%s/.home" % os.environ["HOME"],"w") as f:
        print "Was at home at %s" % datetime.datetime.now().isoformat(" ")
        f.write(str(time.time()))

while 1:
    if at_home():
        update()
    else:
        print "Not at home"
