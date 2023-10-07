# plots data in terminal
import math
import numpy

# NOTE: data is already ordered chronologically in api response (don't use time data to  calculate position)

# (start, end, distance between intervals, physical space left on chart)
interval_ranges = {
    "CO":(0.0, .5, .1, 4)
}

def displayGraph(data):
    #print(data)
    print(data['values'][1])
    print("----------------------------------------")
    plot_matrix = numpy.empty((30, 24))
    #averages = averageValues(data)
    
    # add function to convert time into a 'space distance' based on given time and interval specified

    # arranges values into plotting matrix
    for i in numpy.arange(start=0.3, stop=0, step=-0.01):
        #print(str(numpy.round(i, 3))+" |", end="")
        j=0
        while(j < len(data['values'])):
            #print(str(numpy.round(data['values'][j]['value'], 2)))
            upper_bound = i+0.02
            lower_bound = i-0.02
            curr_val = numpy.round(data['values'][j]['value'], 2)
            #print(numpy.round(i, 3)*100-1)
            if curr_val == numpy.round(i, 2):
                plot_matrix[int(numpy.round(i, 3)*100-1)][j] = 1

            j+=1
            """
            if(numpy.round(data['values'][j]['value'], 3) == numpy.round(i, 3)):
                print(" "*(data['values'][j]['day']+data['values'][j]['hour'])+"*", end="")
            j+=1
            """
        #print()
    #print(plot_matrix)

    # go backwards through list, cuz it gets mirrored when read into the numpy array
    # TODO: figure out how to stop it from printing if no data exists on that line, print axes
    # TODO: check if data spanning multiple days works w/ this method
    for i in range(len(plot_matrix)-1, 0, -1):
        for j in range(len(plot_matrix[i])):
            try:
                if(int(plot_matrix[i][j]) == 1):
                    print("*", end="")
                else:
                    print(" ", end="")
            except:
                pass
        print()

    
def findValue(data, site_name, month, day, hour):
    for f in range(len(data['values'])):
        #print(time_str, data['values'][f]['time'])
        if data['values'][f]['source'] != site_name and data['values'][f]['day'] == day and data['values'][f]['hour'] == hour and data['values'][f]['month'] == month:
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

