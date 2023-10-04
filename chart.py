# plots data in terminal
import math
import numpy

# (start, end, distance between intervals, physical space left on chart)
interval_ranges = {
    "CO":(0.0, .5, .1, 4)
}

def displayGraph(data):
    # define chart intervals to display
    values = []
    for f in data['values']:
        values.append(f['value'])
        #print(f['value'])



    #print(max(values))
    #print(min(values))
    #print(data)
    print("----------------------------------------")
    #averages = averageValues(data)
    #print(data['values'][0]['time'])
    #print(data['values'][0]['time'][-3:-2])
    # add function to convert time into a 'space distance' based on given time and interval specified
    for s in numpy.arange(0.5, 0.0, -0.1):
        #print(str(s))
        for v in data['values']:
            #print(numpy.round(v['value'], 2))
            line = ""
            #print(v['value'], numpy.round(s, 2))
            if v['value'] >= numpy.round(s, 2) and v['value'] < numpy.round(s+0.1, 2):
                #print((v['hour'])*" "+"*", end=None)
                line += (v['hour']*5)*" "+"*"
            if line != "":
                print(line)
        #print()
    
def findValue(data, site_name, time_str):
    for f in range(len(data['values'])):
        #print(time_str, data['values'][f]['time'])
        if data['values'][f]['source'] != site_name and data['values'][f]['time'] == time_str:
            return f

# not all sites collect on same frequencies
# if matching one can't be found, just append

# maybe add later: add object with time of sample
def averageValues(data):
    avgs = []
    array_len = len(data['values'])
    for d in range(array_len):
        if(d >= len(data['values'])):
            break
        #print(str(d))
        #print(data['values'][d])
        curtime = data['values'][d]['time']
        loc = data['values'][d]['source']
        match_val = findValue(data, loc, curtime)
        #print(match_val)
        if match_val != None:
            avgs.append(((data['values'][d]['value']+data['values'][match_val]['value'])/2, data['values'][d]['time']))
            data['values'].pop(match_val)
            data['values'].pop(d)
            #array_len -= 2
        else:
            avgs.append((data['values'][d]['value'], data['values'][d]['time']))
            data['values'].pop(d)
        # look for values taken at exact same time
    
    return avgs
    #print(data)

