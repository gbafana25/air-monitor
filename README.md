# dc-air

Frontend app/script for Douglas County Air Quality

- look into android studio alternatives

## Modules
- `dc_airq`: gets air quality data
- `chart`: plots data in terminal

## Data sources

- Pollutant data
    - https://services.arcgis.com/pDAi2YK0L0QxVJHj/arcgis/rest/services/AirQuality_Monitors_and_Data_(public_view)/FeatureServer/1/query 
    - f=json
    - groupByFieldsForStatistics: `SiteName,EXTRACT(YEAR FROM ModifiedOn -INTERVAL '4:59:59' HOUR TO SECOND),EXTRACT(MONTH FROM ModifiedOn -INTERVAL '4:59:59' HOUR TO SECOND),EXTRACT(DAY FROM ModifiedOn -INTERVAL '4:59:59' HOUR TO SECOND),EXTRACT(HOUR FROM ModifiedOn -INTERVAL '4:59:59' HOUR TO SECOND)`
    - outFields: `OBJECTID,ReportValue,ModifiedOn,SiteName`
    - outStatistics: `[{"onStatisticField":"ReportValue","outStatisticFieldName":"value","statisticType":"avg"}]`
    - resultType: `standard`
    - returnGeometry: `false`
    - spatialRel: `esriSpatialRelIntersects`
    - where: `TimeInterval='001h' AND SiteName IN('NCORE', 'WHITMORE', 'OPPD') AND ParameterAlias='SO2' AND SystemStandardizedDate BETWEEN (CURRENT_TIMESTAMP - INTERVAL '24' HOUR) AND CURRENT_TIMESTAMP AND ModifiedOn IS NOT NULL`

- Pollutant names (for request variables): SO2, PM2.5, PM25LC, OZONE, PM10, NO, CO 
- no headers needed
- sitename in `where` not needed (avg numbers from all sources)
- in `where`, between specifier can be changed `(CURRENT_TIMESTAMP - INTERVAL '2' DAY)`

# TODO
- fix chart output/formatting