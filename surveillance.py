from time import sleep,time
import imagecompare, takepicture
import os
import email_settings
from email.mime.text import MIMEText
import smtplib
import datetime


def at_home():
    hostnames = ["192.168.1.13","192.168.1.15"]

    found = False
    for host in hostnames:
        cmd = "ping -c 1 " + host
        response = os.popen(cmd).read()
        if "64 bytes from" in response:
            found = True
    return found

    
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

def main():
    gone_since = 0
    last_alert = 0
    while 1:
        while gone_since < 4:
            if at_home():
                print datetime.datetime.now().isoformat(" ") + " " + "Still home"
                gone_since = 0
            else:
                gone_since += 1
                print "Couldn't reach phone, trying again. Try: %d" % gone_since
        
        gone_since = 0
        i = 1
        os.system("python takepicture.py pics/pic%d.jpg" % i)
        i = 2
        while 1:
            os.system("python takepicture.py pics/pic%d.jpg" % i)
            sleep(1)
            _,a,b,_ = imagecompare.compare("pics/pic1.jpg","pics/pic2.jpg")
            print datetime.datetime.now().isoformat(" ") + " " + "%d %d" % (a,b)
            if a >= 4 and b >= 10:
                print "Movement!"
                if not at_home():
                    gone_since = 4
                    print "ALERT"
                    os.rename("pics/pic1.jpg", "pics/save1%s.jpg" % str(int(time())))
                    os.rename("pics/pic2.jpg", "pics/save2%s.jpg" % str(int(time())))
                    if time() - last_alert > 3600:
                        last_alert = time()
                        print "Sent email"
                        mail(email_settings.username, "Movement detected", "Detected movement at home")
                break
            
            i = 3 - i



if __name__ == "__main__":
    main()
