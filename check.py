#from influxdb import InfluxDBClient
from time import sleep
#from threading import Thread
from concurrent.futures import ThreadPoolExecutor

def query_count(monitor='Sealand2/FF2/Biofiltros/Biofiltro1/CO2/CO2',database='blumar'):
    print monitor
    return None
#    client = InfluxDBClient('localhost', 8086, 'root', 'root', database)
#    result = client.query('SELECT count("value") FROM "%s"'%monitor)
#    return list(result.get_points())[0]['count']
    
def is_stuck(monitors):
#    print monitors
#   print len(monitors)

    for i in range(0,len(monitors)+1,2):
#        print i
#        try:
         print monitors[i].split(":")[1]
         print monitors[i+1].split(":")[1]
         m1 = query_count(monitors[i].split(":")[1],monitors[i].split(":")[2]) 
         print m1
         mi = query_count(monitor[i+1].split(":")[1],monitor[i+1].split(":")[2]) 
         sleep(30)
         m2 = query_count(monitors[i].split(":")[1],monitors[i].split(":")[2]) 
         mii = query_count(monitor[i+1].split(":")[1],monitor[i+1].split(":")[2]) 
         diff1 = abs(m2 - m1)
         diff2 = abs(mii - mi)
#         print diff1 
         if diff1 == 0:
             stuck1 = True
         else:
             stuck1 =False

         if diff2 == 0:
             stuck2 = True
         else:
             stuck2 =False
#         print diff1    
#        except IndexError:
#            return False
    return (stuck1 and stuck2)
        
        
def monitor_points():
    '''
    '''
    filename = 'monitors.ctl'
    fpt = open(filename,'rw')
    lines = fpt.readlines()
    all_threads = []
    temp = []
    d_temp = {}
    for data in lines:
        if data.__contains__('ROOM'):
            if len(temp) != 0:
                all_threads.append()
                temp = []
                d_temp.clear()
        elif not data.__contains__('#'):
            try:
                monitor = data.split('Blumar/')[1].rsplit('\n')[0]
                database = 'blumar'
            except:
                monitor = data.split('Chayahue/')[1].rsplit('\n')[0]
                database = 'chayahue'
                temp.append(database+":"+monitor)
            temp.append(database+":"+monitor)
        
#        else:
#            print "data comented"
#    print all_threads
#    executor = ThreadPoolExecutor(max_workers=len(all_threads))
    for points in all_threads:
#        task = executor.submit(is_stuck,(points))
        print is_stuck(points)
#    executor.shutdown()

if '__main__' == __name__:
    monitor_points()
   
