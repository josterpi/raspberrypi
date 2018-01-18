
import os
import glob
from datetime import datetime
import time
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def weekend(dt):
    if dt.weekday() in (5, 6):
        return True
    return False

def cmp(a, b):
    # Python 3 doesn't have cmp
    return (a>b) - (a<b)

def datetime_compare(a, b):
    if isinstance(a, datetime):
        a = (a.hour, a.minute)
    if isinstance(b, datetime):
        b = (b.hour, b.minute)
    if cmp(a[0], b[0]) == 0:
        return cmp(a[1], b[1])
    else:
        return cmp(a[0], b[0])

def gte(a, b):
    return datetime_compare(a, b) in (0, 1)

def lt(a, b):
    return datetime_compare(a, b) == -1

# Schedule
# MF 5:45am 70
#    9:00am 68
#   10:00pm 65
# SS 6:00am 70
#    8:00am 68
#    9:00pm 65

def scheduled_temp(dt):
    schedule = {"MF": [(0, 0, 65), (5, 45, 70), (9, 0, 68), (22, 0, 65)],
                "SS": [(0, 0, 65), (6, 0, 70), (8, 0, 68), (21, 0, 65)]}
    group = "MF"
    if weekend(dt):
        group = "SS"
    temp = 0
    for point in schedule[group]:
        if gte(dt, point):
            temp = point[2]
        if lt(dt, point):
            break
    return temp
 
def _read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = _read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f
