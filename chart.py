# plots data in terminal
import math
import numpy

# parts per x * 100 for array indexes, # of decimal places to round, decrement level, unit, conversion factor, list divisor
interval_ranges = {
    "CO":(40, 2, -0.01, "ppm", 100, 100, "{:.2f}", 100), # ppm
    "NO":(500, 3, -0.001, "ppb", 100, 100, "{:.2f}", 100), # ppb
    "SO2":(800, 3, -0.001, "ppb", 1000, 1000, "{:.3f}", 1000), # ppb
    "OZONE":(80, 3, -0.001, "ppb", 1000, 100, "{:.3f}", 1000), # ppb
    "PM2.5": (40, 1, -1, "ug/m3", 1, 1, "{:.0f}", 1), # ug/m3
    "PM10": (50, 1, -1, "ug/m3", 1, 1, "{:.0f}", 1)
}

def dataInRow(row):
    if 1 in row:
        return True
    return False

def showTimeAxis(count, c_type, div):
    total = 0
    if c_type == 'DAY':
        total = count*24
    else:
        total = count

    if(div == 100):
        print(" "*7, end="")
    elif(div == 1000):
        print(" "*8, end="")
    elif(div == 1):
        print(" "*6, end="")
    
    for i in range(total):
        print(" "+str(i+1)+" ", end="")

    print()
    print(" "*(total)+"Time (hr)")


def displayGraph(data):
    #print(data)
    #print(data['values'][len(data['values'])-1])
    
    pollutant_int = interval_ranges[data['pollutant']][0]
    round_places = interval_ranges[data['pollutant']][1]
    decr = interval_ranges[data['pollutant']][2]
    conv_factor = interval_ranges[data['pollutant']][4]
    divisor = interval_ranges[data['pollutant']][5]
    unit_format = interval_ranges[data['pollutant']][6]
    unit_divisor = interval_ranges[data['pollutant']][7]

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
            print(unit_format.format((i+1)/unit_divisor)+" | ", end="")
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
    showTimeAxis(data['interval_count'], data['interval_type'], unit_divisor)
    
def findValue(data, site_name, month, day, hour):
    for f in range(len(data['values'])):
        #print(time_str, data['values'][f]['time'])
        if data['values'][f]['source'] != site_name and data['values'][f]['day'] == day and data['values'][f]['hour'] == hour and data['values'][f]['month'] == month:
            return f

# still work in progress, doesn't work as required
def combineValues(data):
    combined_data = []
    # dict of timeslots (hour, day, month) as tuples
    time_slots = {}
    # create dictionary of all timeslots
    for i in range(len(data['values'])):
        curr = data['values'][i]
        t_tup = (curr['hour'], curr['day'], curr['month'])
        if t_tup not in time_slots:
            time_slots[t_tup] = []
            time_slots[t_tup].append(data['values'][i])
        else:
            time_slots[t_tup].append(data['values'][i])

    #print(time_slots)
    # average slot if multiple
    keyslots = list(time_slots.keys())
    for f in range(len(keyslots)):
        curr = time_slots[keyslots[f]]
        #print(curr)
        if(len(curr) > 1):
            sum = 0
            for c in curr:
                sum += c['value']
            avg = sum/len(curr)
            time_slots[keyslots[f]] = {'source':'average', 'value':avg, 'hour':keyslots[f][0], 'day':keyslots[f][1], 'month':keyslots[f][2]}
            combined_data.append(time_slots[keyslots[f]])
        else:
            combined_data.append(curr[0])
    #print(combined_data)
    data['values'] = combined_data
    
