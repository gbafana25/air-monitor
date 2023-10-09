# plots data in terminal
import math
import numpy

# NOTE: data is already ordered chronologically in api response (don't use time data to  calculate position)

# parts per x * 100 for array indexes, # of decimal places to round, decrement level, unit, conversion factor, list divisor
interval_ranges = {
    "CO":(40, 2, -0.01, "ppm", 100, 100), # ppm
    "NO":(500, 3, -0.001, "ppb", 100, 100), # ppb
    "SO2":(800, 3, -0.001, "ppb", 1000, 1000), # ppb
    "OZONE":(40, 3, -0.001, "ppb", 1000, 100), # ppb
    "PM2.5": (40, 1, -1, "ug/m3", 1, 1), # ug/m3
    "PM10": (50, 1, -1, "ug/m3", 1, 1)
}

def dataInRow(row):
    if 1 in row:
        return True
    return False

def displayGraph(data):
    #print(data)
    #print(data['values'][len(data['values'])-1])

    pollutant_int = interval_ranges[data['pollutant']][0]
    round_places = interval_ranges[data['pollutant']][1]
    decr = interval_ranges[data['pollutant']][2]
    conv_factor = interval_ranges[data['pollutant']][4]
    divisor = interval_ranges[data['pollutant']][5]

    rows = interval_ranges[data['pollutant']][0]
    columns = 0
    if(data['interval_type'] == "HOUR"):
        columns = data['interval_count']
    elif(data['interval_type'] == "DAY"):
        columns = data['interval_count'] * 24
    plot_matrix = numpy.empty((rows, columns))
    #print(len(plot_matrix))
    print(data['pollutant']+" over "+str(data['interval_count']), data['interval_type'].lower()+" period ("+interval_ranges[data['pollutant']][3]+")")
    print("-"*(columns+5)*3)
    
    # add function to convert time into a 'space distance' based on given time and interval specified
    # arranges values into plotting matrix
    for i in numpy.arange(start=pollutant_int/divisor, stop=0, step=decr):
        j=0
        while(j < len(data['values'])):
            #print(str(numpy.round(data['values'][j]['value'], 2))) 
            curr_val = numpy.round(data['values'][j]['value'], round_places)
            #print(numpy.round(i, 3)*100-1)
            if curr_val == numpy.round(i, round_places):
                factor = int(1/abs(decr))
                plot_matrix[int((numpy.round(i, 3)*conv_factor)-1)][j] = 1

            j+=1
            
        #print()
    #print(plot_matrix)

    # go backwards through list, cuz it gets mirrored when read into the numpy array
    # data spanning multiple days works w/ this method

    # add more space to output
    for i in range(len(plot_matrix)-1, 0, -1):
        exists = dataInRow(plot_matrix[i])
        if(exists):
            print("{:.3f}".format((i+1)/100)+" | ", end="")
        for j in range(len(plot_matrix[i])):
            try:
                if(int(plot_matrix[i][j]) == 1):
                    #data_start = True
                    print(" * ", end="")
                else:
                    if(exists):
                        print(" "*3, end="")
            except:
                pass
        #if(data_start)
        if(exists):
            print()


    print("-"*(columns+5)*3)
    
def findValue(data, site_name, month, day, hour):
    for f in range(len(data['values'])):
        #print(time_str, data['values'][f]['time'])
        if data['values'][f]['source'] != site_name and data['values'][f]['day'] == day and data['values'][f]['hour'] == hour and data['values'][f]['month'] == month:
            return f

# still work in progress, doesn't work as required
def combineValues(data):
    alen = 0
    condensed = []
    #print(len(data['values']))
    curr_time = [data['values'][0]['hour'], data['values'][0]['day'], data['values'][0]['month'], data['values'][0]['value']]
    while(alen < len(data['values'])-1):
        if data['values'][alen]['hour'] == curr_time[0] and data['values'][alen]['day'] == curr_time[1] and data['values'][alen]['month'] == curr_time[2]:
            # average, then delete
            comb = {
                'source': 'combined',
                'value': (data['values'][alen]['value']+curr_time[3])/2,
                'hour': curr_time[0],
                'day': curr_time[1],
                'month': curr_time[2]
            } 
            condensed.append(comb)
            data['values'].pop(alen)
        #else:
            # append to condensed
            #condensed.append(data['values'][alen])
            #data['values'].pop(alen)
        alen += 1
        curr_time[0] = data['values'][alen]['hour']
        curr_time[1] = data['values'][alen]['day']
        curr_time[2] = data['values'][alen]['month']
        curr_time[3] = data['values'][alen]['value']
    #print(condensed)
    
    # insert leftover values 

    for i in range(len(data['values'])):
        curr = data['values'][i]
        for j in range(len(condensed)):
            if condensed[j]['day'] == curr['day'] and condensed[j]['month'] == curr['month'] and condensed[j]['hour']+1 == curr['hour']:
                condensed.append(curr)
    
    for s in condensed:
        print(s)
    #print(len(data['values']))
