#!/usr/bin/python3
# module to get raw numbers

import requests
import json
import chart
import sys
import time

base_url = "https://services.arcgis.com/pDAi2YK0L0QxVJHj/arcgis/rest/services/AirQuality_Monitors_and_Data_(public_view)/FeatureServer/1/query"
outstats = [{"onStatisticField":"ReportValue","outStatisticFieldName":"value","statisticType":"avg"}]

# PM2.5 and PM10 require SiteName in request
#pollutant_types = ["SO2", "OZONE", "PM2.5", "PM25LC", "PM10", "NO", "CO"]

# holdes site names
pollutant_types = {
    "SO2": ['WHITMORE', 'NCORE'],
    "OZONE": ['NCORE'],
    "PM2.5": ['Blair BAM Direct', 'GHills BAM direct', 'NCORE'],
    "PM10": ['74DODGE', 'OPPD', 'WHITMORE', '24THO', 'NCORE', '30THFORT', 'GHILLS'],
    "NO": ['NCORE'],
    "CO": ['NCORE'],
}
site_names = ['WHITMORE', '24THO', '74DODGE', 'OPPD', 'NCORE', '30THFORT', 'GHILLS']

# gets readings by pollutant type
def getLevels(pollutant_type, interval_count, interval_type):
    sensor_values = {"pollutant":pollutant_type, "interval_count":interval_count, "interval_type":interval_type, "values":[]}
    # add other sitenames for other pollutants 

    sites = ""
    #build sitenames string
    if len(pollutant_types[pollutant_type]) == 1:
        sites = "'"+pollutant_types[pollutant_type][0]+"'"
    else:
        sites = "'"+pollutant_types[pollutant_type][0]+"'"
        for s in range(1, len(pollutant_types[pollutant_type])):
            sites += ",'"+pollutant_types[pollutant_type][s]+"'"

    #print(sites)
    query = "TimeInterval='001h' AND SiteName IN("+sites+") AND ParameterName='"+pollutant_type+"' AND SystemStandardizedDate BETWEEN (CURRENT_TIMESTAMP - INTERVAL '"+str(interval_count)+"' "+interval_type+") AND CURRENT_TIMESTAMP AND ModifiedOn IS NOT NULL"
    #print(query)
    if pollutant_type == "PM10":
        query = "TimeInterval='001h' AND SiteName IN('74DODGE', 'OPPD', 'WHITMORE', '24THO', 'NCORE', '30THFORT', 'GHILLS') AND ParameterAlias='PM10' AND SystemStandardizedDate BETWEEN (CURRENT_TIMESTAMP - INTERVAL '24' HOUR) AND CURRENT_TIMESTAMP AND FinalValue<300 AND ModifiedOn IS NOT NULL"
    elif pollutant_type == "PM2.5":
        query = "TimeInterval='001h' AND SiteName IN('Blair BAM Direct', 'GHills BAM direct', 'NCORE') AND ParameterAlias IN('PM2.5', 'PM25LC') AND SystemStandardizedDate BETWEEN (CURRENT_TIMESTAMP - INTERVAL '24' HOUR) AND CURRENT_TIMESTAMP AND FinalValue<200 AND ModifiedOn IS NOT NULL"

    p = {
        "f":"json",
        "groupByFieldsForStatistics":"SiteName,EXTRACT(YEAR FROM ModifiedOn -INTERVAL '4:59:59' HOUR TO SECOND),EXTRACT(MONTH FROM ModifiedOn -INTERVAL '4:59:59' HOUR TO SECOND),EXTRACT(DAY FROM ModifiedOn -INTERVAL '4:59:59' HOUR TO SECOND),EXTRACT(HOUR FROM ModifiedOn -INTERVAL '4:59:59' HOUR TO SECOND)",
        "outFields":"OBJECTID,ReportValue,ModifiedOn,SiteName",
        "outStatistics": json.dumps(outstats),
        "where": query
    }
    req = requests.get(base_url, params=p)
    resp = json.loads(req.text)
    #print(resp)
    
    all_values = resp['features']
    for a in all_values:
        reading = a['attributes']
        if reading['value'] != None:
            time_str = str(reading['EXPR_2'])+"-"+str(reading['EXPR_3'])+"-"+str(reading['EXPR_1'])+"-"+str(reading['EXPR_4'])+"hr"# month/day/year hour
            # hours given in 24-hour format
            sensor_values['values'].append({"source":reading['SiteName'], "value":reading['value'], "hour":reading['EXPR_4'], "month":reading['EXPR_2'], "day":reading['EXPR_3']})
        #print(reading['value'], reading['SiteName'])        
    #print(sensor_values)
    return sensor_values

if __name__ == "__main__":
    if(len(sys.argv) == 1):
        print("Help menu")
        print("_____________________________________________________________")
        print("--pollutant | -p [pollutant type]: specify pollutant type")
        print("--all | -a : print data for all pollutants")
        print("Pollutant types: "+str(list(pollutant_types.keys())))
        print("_____________________________________________________________")
    elif(sys.argv[1] in ['--pollutant', '-p'] and sys.argv[2] in list(pollutant_types.keys())):
        # print specified pollutant
        # keep at 24 hour max interval now, longer intervals may not fit as cleanly in terminal
        # (depends on display size)
        data = getLevels(sys.argv[2], 24, "HOUR")
        chart.combineValues(data)
        chart.displayGraph(data)
    elif(sys.argv[1] in ['--all', '-a']):
        for p in list(pollutant_types.keys()):
            data = getLevels(p, 24, "HOUR")
            chart.combineValues(data)
            chart.displayGraph(data)
            # keep for rate limit?
            time.sleep(0.5)

    
    #print(data)
