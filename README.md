# alarms
ssh dev01.bluemonster.cl -l blue -p 6050
arrives to: 172.16.20.60
*/2 * * * * /usr/bin/env python2 /home/blue/alarms/check.py > /home/blue/alarms/check.log
