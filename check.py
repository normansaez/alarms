#from influxdb import InfluxDBClient
from time import sleep
#from threading import Thread
from concurrent.futures import ThreadPoolExecutor


def query_count(database='blumar', monitor='Sealand2/FF2/Biofiltros/Biofiltro1/CO2/CO2'):
    client = InfluxDBClient('localhost', 8086, 'root', 'root', database)
    result = client.query('SELECT count("value") FROM "%s"'%monitor)
    return list(result.get_points())[0]['count']
#    return 1 
    
def is_stuck(database='blumar', monitor='Sealand2/FF2/Biofiltros/Biofiltro1/CO2/CO2'):
    amount_ini = query_count(databse, monitor) 
    sleep(1)
    amount_fin = query_count(database, monitor) 
    diff = abs(amount_fin - amount_ini)
    if diff == 0:
        return True
    return False
    
def check_room(database, point1, point2):
    executor = ThreadPoolExecutor(max_workers=2)    
    task1 = executor.submit(is_stuck,(database, point1))
    task2 = executor.submit(is_stuck,(database, point2))
    executor.shutdown(wait=True)
    return task1.result() and task2.result()

def group_by_room(database, data):
    print len(data)
    print data
    acummulate = []
    previuos_room = ''
    first_e = True
    for monitor in data:
        namespace = monitor.split("/")
        namespace_point = namespace[0]+"/"+ namespace[1]+"/"+namespace[2]+"/"+namespace[3]+"/"+namespace[4]+"/"+namespace[5]
        room = namespace[1]
        type_ = namespace[2]
        if room != previuos_room:
            previuos_room = room
            previuos_mon = namespace_point
        else:
            if first_e is True:
                first_e = False
            else:
                acummulate.append([database, previuos_mon, namespace_point]) 
        
        print database
        print room
        print namespace_point

def inspect_data(data):
    monitors = []
    data = data.rstrip('\n')
    monitor = data.split('/')
    if len(monitor) != 7:
        print "Namespace is not correct: %s , should be 7 parameters" % data
        return None
    database = monitor[0].lower()
#    print database
    monitor_point = monitor[1]+"/"+monitor[2]+"/"+monitor[3]+"/"+monitor[4]+"/"+monitor[5]+"/"+monitor[6]
    return database , monitor_point

def go(data, database):
    executor = ThreadPoolExecutor(max_workers=len(to_be_monitored))
    for points in to_be_monitored:
        database = points[0]
        point1 = points[1]
        point2 = points[2]
        task = executor.submit(check_room,(database,point1, point2))

def read_monitor_points():
    '''
    '''
    filename = 'monitors.ctl'
    fpt = open(filename,'rw')
    lines = fpt.readlines()
    blumar_points = []
    sealand2_points = []
    for data in lines:
        if not data.__contains__('#'):
            database, monitor = inspect_data(data)
            if database == 'blumar':
                blumar_points.append(monitor)
            if database == 'chayahue':
                sealand2_points.append(monitor)

#    print len(blumar_points)
    print blumar_points
    to_be_monitored = group_by_room('blumar', blumar_points)
#    go(to_be_monitored, 'blumar')



    print len(sealand2_points) 
if '__main__' == __name__:
    read_monitor_points()
