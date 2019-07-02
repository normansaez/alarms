#from influxdb import InfluxDBClient
from time import sleep
#from threading import Thread
from concurrent.futures import ThreadPoolExecutor


def
query_count(monitor='Sealand2/FF2/Biofiltros/Biofiltro1/CO2/CO2',database='blumar'):
query_count(monitor='Sealand2/FF2/Biofiltros/Biofiltro1/CO2/CO2',da    print monitor
query_count(monitor='Sealand2/FF2/Biofiltros/Biofiltro1/CO2/CO2',da    client = InfluxDBClient('localhost', 8086, 'root', 'root', database)
query_count(monitor='Sealand2/FF2/Biofiltros/Biofiltro1/CO2/CO2',da    result = client.query('SELECT count("value") FROM "%s"'%monitor)
    return list(result.get_points())[0]['count']
#    return 1 
    
def is_stuck(monitor1='Sealand2/FF2/Biofiltros/Biofiltro1/CO2/CO2', monitor2='Sealand2/FF2/Biofiltros/Biofiltro1/CO2/CO2'):
#    print monitor
    amount1_1 = query_count(monitor1) 
    amount2_1 = query_count(monitor2) 
#    print amount_1
    sleep(1)
    amount1_2 = query_count(monitor1)
    amount2_2 = query_count(monitor2) 
#    print amount_2
    diff1 = abs(amount1_2 - amount1_1)
    diff2 = abs(amount2_2 - amount2_1)
    

    if diff1 == 0:
        stuck1 = True
    else:
        stuck1 =False

    if diff2 == 0:
        stuck2 = True
    else:
        stuck2 =False

    return (stuck1 and stuck2)
        
        
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
   
