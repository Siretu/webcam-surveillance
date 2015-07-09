# Webcam Surveillance
Repo to set up webcam for home surveillance while no one's home

## What does it do?
Running surveillance.py will start regularly pinging the local ips specified in the hostnames list. These are supposed to be the smartphones static wifi ip to detect when the phones leave home. When it can't reach any of them for a certain period of time, it starts taking pictures. It keeps the last two and continuously compares the last two pictures to detect change. If the change is above a certain threshold, it activates and sends a message. 

The image comparing is done by imagecompare.py. It checks the average pixel difference and a more complex measurement to see how uniformly the picture has changed (to not trigger from uniform light changes).

## How to use?
Open surveillance.py and change hostnames list to include the local ips of your smartphone devices.

Run surveillance.py to start the script.