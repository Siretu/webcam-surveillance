from time import sleep,time
import imagecompare, takepicture
import os, shutil
import email_settings
from email.mime.text import MIMEText
import smtplib
import datetime

TIME_THRESHOLD = 600

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

def main():
    gone_since = 0
    last_alert = 0
    i = 1
    while 1:
        sleep(1)
        if at_home():
            gone_since = 0
            print datetime.datetime.now().isoformat(" ") + " " + "Still home"
        else:
            if gone_since < 4:
                print "Couldn't reach phone, trying again. Try: %d" % gone_since
                gone_since += 1
            else:
                os.system("python takepicture.py pics/pic%d.jpg" % i)
                _,a,b,_ = imagecompare.compare("pics/pic1.jpg","pics/pic2.jpg")
                print datetime.datetime.now().isoformat(" ") + " " + "%d %d" % (a,b)
                if a >= 4 and b >= 10:
                    print "Movement!"
                    if not at_home():
                        gone_since = 4
                        print "ALERT"
                        shutil.copyfile("pics/pic1.jpg", "pics/save1%s.jpg" % str(int(time())))
                        shutil.copyfile("pics/pic2.jpg", "pics/save2%s.jpg" % str(int(time())))
                        if time() - last_alert > 600:
                            last_alert = time()
                            print "Sent email"
                            mail(email_settings.username, "Movement detected", "Detected movement at home")
                        os.system('espeak "Movement detected"')
                i = 3 - i



if __name__ == "__main__":
    main()
