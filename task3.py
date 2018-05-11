'''
GEOM90042
Assignment 2 Task 3
Author: JIE PU, CHANGJIAN MA
Student Number: 765316, 653909
'''


import arcpy
import csv

# This sets the workspace to the current folder.
arcpy.env.workspace = './'
# This sets the output mode into overwrite mode.
arcpy.env.overwriteOutput = True


# This function processes the three input list and combine them into one list with information required.
def inputProcess(accident, location):
    # This is the list that stores information required.
    accident_location = []

    i = 0
    # This loop combines accident list with location list to add location information.
    for row in location:
        if len(row) and len(accident[i]):
            # This decides whether the accident number exists in the location information.
            if int(row[0][1:12]) > int(accident[i][0][1:12]):
                i += 1
            
            # This decides whether the accident number matches the row in location information.
            if row[0] == accident[i][0]:
                accident_id = row[0]
                year = accident[i][1].split('/')[2]
                lat = row[9]
                lon = row[10]
                if int(accident[i][18]) >= 3:
                    accident_location.append([accident_id, year, [lat, lon]])
                i += 1

    return accident_location


# This function creates the three shapefile of severe accidents in a certain year.
def createShape(year, accident_location):
    workspace = "./"
    shapeCursor = 'AccidentLocations_' + year + '.shp'

    # This deletes the shapefile if it exists before carrying out the shapefile creation.
    arcpy.Delete_management(workspace + '/' + shapeCursor)
    
    # This creates the feature classes of the shapefile.
    arcpy.CreateFeatureclass_management(workspace, shapeCursor, "POINT", "", "DISABLED", "DISABLED")
    
    # This sets the projection to WGS_84.
    sr = arcpy.SpatialReference(4326)
    arcpy.DefineProjection_management(workspace + '/' + shapeCursor, sr)
    
    # This adds the attribute names into the shapefile.
    arcpy.AddField_management(shapeCursor, "A_ID", "TEXT")
    arcpy.AddField_management(shapeCursor, "YEAR", "TEXT")

    # This creates the cursor that writes points.
    cursor = arcpy.da.InsertCursor(shapeCursor, ["A_Id", "YEAR", "SHAPE@"])
    
    # This loop writes the points row by row into the shapefile.
    for p in accident_location:
        if p[1] == year:
            # This extracts the longitude and latitude of the point.
            point = arcpy.Point(float(p[2][1]), float(p[2][0]))
            cursor.insertRow([p[0], p[1], point])
    del cursor


# This function carries out optimized hot spot analysis with severe accidents in each year.
def hotspot(year):
    arcpy.OptimizedHotSpotAnalysis_stats('AccidentLocations_' + year +'.shp', 'HotSpot_' + year + '.shp', '#', 'COUNT_INCIDENTS_WITHIN_AGGREGATION_POLYGONS', '#', 'SA2_2016_AUST.shp', '#')


# This is the main function that calls the other functions.
def main():
    # These variables store the years to be analyzed.
    year1 = "2006"
    year2 = "2016"

    accident = "./ACCIDENT.csv"
    location = "./NODE.csv"

    # This reads accident.csv and stores the data into a nested list.
    with open(accident, 'rt') as file:
        reader = csv.reader(file)
        accident = list(reader)
    del accident[0]

    # This reads node.csv and stores the data into a nested list.
    with open(location, 'rt') as file:
        reader = csv.reader(file)
        location = list(reader)
    del location[0]

    # This calls the funtion that processes the data in the two lists.
    accident_location = inputProcess(accident, location)

    # These call the function that create shapefiles for severe accidents in 2006 and 2016.
    createShape(year1, accident_location)
    createShape(year2, accident_location)

    # These call the function that carry out optimized hot spot analysis for severe accidents in 2006 and 2016.
    hotspot(year1)
    hotspot(year2)


# This calls the main function.
if __name__ == '__main__':
        main()
