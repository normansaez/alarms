from influxdb import InfluxDBClient
from time import sleep
#from threading import Thread
from concurrent.futures import ThreadPoolExecutor


def query_count(monitor='Sealand2/FF2/Biofiltros/Biofiltro1/CO2/CO2'):
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'blumar')
    result = client.query('SELECT count("value") FROM "%s"'%monitor)
    return list(result.get_points())[0]['count']

def is_stuck(monitor='Sealand2/FF2/Biofiltros/Biofiltro1/CO2/CO2'):
    print monitor
    amount_1 = query_count(monitor) 
    print amount_1
    sleep(10)
    amount_2 = query_count(monitor)
    print amount_2
    diff = abs(amount_2 - amount_1)
    if diff == 0:
        return True
    return False

def monitor_points():
    '''
    '''
    filename = 'monitors.ctl'
    fpt = open(filename,'rw')
    lines = fpt.readlines()
    blumar_points = []

    for i in lines:
        if not i.__contains__('#'):
            monitor = i.split('Blumar/')[1].rsplit('\n')[0]
            blumar_points.append(monitor)
    executor = ThreadPoolExecutor(max_workers=len(blumar_points))
    for points in blumar_points:
        task = executor.submit(is_stuck,(points))
if '__main__' == __name__:
    monitor_points()
    
