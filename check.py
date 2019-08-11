#!/usr/bin/env python2
from influxdb import InfluxDBClient
import smtplib
from time import sleep
#from threading import Thread
from concurrent.futures import ThreadPoolExecutor

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def send_email(send_to='norman.saez@blueshadows.cl', room=''):
    msg = MIMEMultipart()
    msg['From'] = 'sealand.alarms@gmail.com'
    msg['To'] = send_to
    msg['Subject'] = 'Alarm to %s' % room
    message = 'here is the email'
    msg.attach(MIMEText(message))
    
    mailserver = smtplib.SMTP('smtp.gmail.com:587')
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login('sealand.alarms@gmail.com', 'myalarms123!')
    
    mailserver.sendmail('sealand.alarms@gmail.com',send_to, msg.as_string())
    
    mailserver.quit()


def query_count(database='bluemar', monitor='Sealand2/FF2/Biofiltros/Biofiltro1/CO2/CO2'):
    
    client = InfluxDBClient('localhost', 8086, 'root', 'root', database)
    result = client.query('SELECT count("value") FROM "%s"'%monitor)
    if result.items().__len__() > 0:
        return list(result.get_points())[0]['count']
    return 0

def is_stuck(database, point):
#    print point
    database = database.lower()
    m1 = query_count(database, point) 
    sleep(1)
    m2 = query_count(database, point) 
    diff = abs(m2-m1)
    if diff == 0:
        return True
    return False
        
def is_room_stuck(database_room, monitors):
    print database_room
    database = database_room.split("|")[0]
    executor = ThreadPoolExecutor(max_workers=len(monitors))
    tasks_results = []
    for point in monitors:
        print point
        task = executor.submit(is_stuck,database, point)
        tasks_results.append(task.result())
    executor.shutdown(wait=True)
    print tasks_results
    result = 0
    for i in tasks_results:
        result = i + result
    print i

        
def monitor_points():
    '''
    '''
    filename = 'monitors.ctl'
    fpt = open(filename,'rw')
    lines = fpt.readlines()
    all_threads = {}
    temp = []
    
    for data in lines:
        if data.__contains__('ROOM'):
            if len(temp) != 0:
                all_threads.update({database+"|"+room:temp})
                temp = []
        elif not data.__contains__('#'):
                data = data.rsplit('\n')[0]
                namespace = data.split("/")
                database = namespace[0]
                room = namespace[2]
                monitor = namespace[1]+"/"+namespace[2]+"/"+namespace[3]+"/"+namespace[4]+"/"+namespace[5]+namespace[6]
                temp.append(monitor)
    all_threads.update({database+"|"+room:temp})

    executor = ThreadPoolExecutor(max_workers=len(all_threads))
    for k,v in all_threads.iteritems():
        is_room_stuck(k,v)
        task = executor.submit(is_room_stuck,k,v)
    executor.shutdown(wait=True)

if '__main__' == __name__:
    monitor_points()
