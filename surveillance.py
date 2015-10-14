#!/usr/bin/python -u
from time import sleep,time
import imagecompare, takepicture
import os, shutil
import email_settings
from email.mime.text import MIMEText
import smtplib
import datetime
import socket

TIME_THRESHOLD = 1000
LIGHT_THRESHOLD = 60000000

def at_home():
    with open("%s/.home" % os.environ["HOME"]) as f:
        content = f.read()
        if content:
            last_time = float(content)
            return time() - last_time < TIME_THRESHOLD
    return False
            

    
def mail(email, subject, message):
    gmail_username = email_settings.username
    recipients = email
    
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = gmail_username
    msg['To'] = recipients
    msg = msg.as_string()
    
    session = smtplib.SMTP(email_settings.server, email_settings.port, timeout=10)
    session.ehlo()
    session.starttls()
    session.login(gmail_username, email_settings.password)
    session.sendmail(gmail_username, recipients, msg)
    session.quit()

def came_home():
    print "Came home"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost",5432))
    sock.send("on")
    sock.close()

def left_home():
    print "Left home"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost",5432))
    sock.send("off")
    sock.close()

def main():
    gone_since = 0
    last_alert = 0
    i = 1
    while 1:
        sleep(1)
        if at_home():
            if gone_since > 0:
                came_home()
            gone_since = 0
            print datetime.datetime.now().isoformat(" ") + " " + "Still home"
        else:
            if gone_since < 4:
                print "Couldn't reach phone, trying again. Try: %d" % gone_since
                gone_since += 1
            else:
                if gone_since == 4:
                    left_home()
                    gone_since += 1
                os.system("python takepicture.py pics/pic%d.jpg" % i)
                _,a,b,sums = imagecompare.compare("pics/pic1.jpg","pics/pic2.jpg")
                print datetime.datetime.now().isoformat(" ") + " " + "%d %d" % (a,b)
                if a >= 5 and b >= 11 and b < 33 and sums[0] < LIGHT_THRESHOLD and sums[1] < LIGHT_THRESHOLD:
                    print "Movement!"
                    if not at_home():
                        gone_since = 4
                        print "ALERT"
                        shutil.copyfile("pics/pic1.jpg", "pics/save1%s.jpg" % str(int(time())))
                        shutil.copyfile("pics/pic2.jpg", "pics/save2%s.jpg" % str(int(time())))
                        if time() - last_alert > 600:
                            last_alert = time()
                            print "Sent email"
                            mail(email_settings.username, "Movement detected", "Detected movement at home: %d %d" % (a,b))
                        os.system('espeak "Movement detected"')
                i = 3 - i



if __name__ == "__main__":
    main()
