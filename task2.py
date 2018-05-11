'''
GEOM90042
Assignment 2 Task 2
Author: JIE PU, CHANGJIAN MA
Student Number: 765316, 653909
'''

import arcpy
import csv
import os
# This sets the workspace to the current folder.
arcpy.env.workspace = './'
# This sets the output mode into overwrite mode.
arcpy.env.overwriteOutput = True


# This function processes the three input list and combine them into one list with information required.
def input_process(accident, location, vehicle):
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
                day_of_week = accident[i][6]
                lat = row[9]
                lon = row[10]

                # This decides whether an accident is severe.
                if int(accident[i][18]) >= 3:
                    is_severe = 1
                else:
                    is_severe = 0
                accident_location.append([accident_id, day_of_week, is_severe, [lat, lon], []])
                i += 1

    j = 0
    # This loop combines the list above with vehicle list to add vehicle type information.
    for row in vehicle:
        if len(accident_location[j]) and len(row):
            if int(row[0][1:12]) > int(accident_location[j][0][1:12]):
                j += 1
            if row[0] == accident_location[j][0]:
                vehicle_type = row[13]
                if vehicle_type not in accident_location[j][4]:
                    accident_location[j][4].append(vehicle_type)

    return accident_location


# This function creates the three shapefiles.
def createShp(location):
    workspace = "./"
    shapeCursor = 'AccidentLocations.shp'
    shapeCursor_weekday = 'SevereAccidentsWeekday.shp'
    shapeCursor_weekend = 'SevereAccidentsWeekend.shp'

    # These delete the shapefiles if they exist before carrying out the shapefile creation.
    arcpy.Delete_management(workspace + '/' + shapeCursor)
    arcpy.Delete_management(workspace + '/' + shapeCursor_weekday)
    arcpy.Delete_management(workspace + '/' + shapeCursor_weekend)

    # These create the feature classes of shapefiles.
    arcpy.CreateFeatureclass_management(workspace, shapeCursor_weekday, "POINT", "", "DISABLED", "DISABLED")
    arcpy.CreateFeatureclass_management(workspace, shapeCursor_weekend, "POINT", "", "DISABLED", "DISABLED")
    arcpy.CreateFeatureclass_management(workspace, shapeCursor, "POINT", "", "DISABLED", "DISABLED")

    # These set the projection to WGS_84.
    sr = arcpy.SpatialReference(4326)
    arcpy.DefineProjection_management(workspace + '/' + shapeCursor, sr)
    arcpy.DefineProjection_management(workspace + '/' + shapeCursor_weekday, sr)
    arcpy.DefineProjection_management(workspace + '/' + shapeCursor_weekend, sr)

    # These add the attribute of AccidentLocations.shp.
    arcpy.AddField_management(shapeCursor, "A_ID", "TEXT")
    arcpy.AddField_management(shapeCursor, "Vehicles", "TEXT")
    arcpy.AddField_management(shapeCursor, "Day", "TEXT")
    arcpy.AddField_management(shapeCursor, "Severe", "TEXT")

    # These add the attribute of AccidentLocationsWeekday.shp.
    arcpy.AddField_management(shapeCursor_weekday, "A_ID", "TEXT")
    arcpy.AddField_management(shapeCursor_weekday, "Vehicles", "TEXT")
    arcpy.AddField_management(shapeCursor_weekday, "Day", "TEXT")
    arcpy.AddField_management(shapeCursor_weekday, "Severe", "TEXT")

    # These add the attribute of AccidentLocationsWeekend.shp.
    arcpy.AddField_management(shapeCursor_weekend, "A_ID", "TEXT")
    arcpy.AddField_management(shapeCursor_weekend, "Vehicles", "TEXT")
    arcpy.AddField_management(shapeCursor_weekend, "Day", "TEXT")
    arcpy.AddField_management(shapeCursor_weekend, "Severe", "TEXT")
    
    # These set up the cursors for insertion of information into the shapefiles.
    cursor = arcpy.da.InsertCursor(shapeCursor, ["A_Id", "Vehicles", "Day", "Severe", "SHAPE@"])
    cursor_weekday = arcpy.da.InsertCursor(shapeCursor_weekday, ["A_Id", "Vehicles", "Day", "Severe", "SHAPE@"])
    cursor_weekend = arcpy.da.InsertCursor(shapeCursor_weekend, ["A_Id", "Vehicles", "Day", "Severe", "SHAPE@"])

    # This loop inserts the points into shapefiles row by row.
    for p in location:
        # This extracts the longitude and latitude of the point.
        point = arcpy.Point(float(p[3][1]), float(p[3][0]))
        cursor.insertRow([p[0], str(p[4]), p[1], p[2], point])
        if p[2] == 1:
            if p[1] in ['Saturday', 'Sunday']:
                cursor_weekend.insertRow([p[0], str(p[4]), p[1], p[2], point])
            else:
                cursor_weekday.insertRow([p[0], str(p[4]), p[1], p[2], point])
    del cursor
    del cursor_weekday
    del cursor_weekend


# This function adds the statistical area 2 name into accidentsLocations.shp and outputs it into accidentsLocations_with_SA2.shp.
def addSA2():
    shapeCursor = 'AccidentLocations.shp'
    workspace = "./"
    sa2 = 'SA2_2016_AUST.shp'
    output = 'AccidentLocation_with_SA2.shp'
    
    # This deletes the AccidentLocations_with_SA2.shp if it exists already.
    arcpy.Delete_management(workspace + '/' + output)

    # This defines the fieldmappings of the new shapefile.
    fieldmappings = arcpy.FieldMappings()
    fieldmappings.addTable(workspace + shapeCursor)
    fieldmappings.addTable(workspace + sa2)

    # This defines the fields that we need.
    to_keep = ['A_ID', 'Vehicles', 'Day', 'Severe', 'SA2_NAME16']

    # This loop deletes the fields that we do not need.
    for field in fieldmappings.fields:
        if field.name not in to_keep:
            fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(field.name))

    # This spatial joins the two shapefiles and adds the SA2 information into the file.
    arcpy.AddField_management(shapeCursor, "SA2", "TEXT")
    arcpy.SpatialJoin_analysis(workspace + shapeCursor, workspace + sa2, workspace + output, "#", "#", fieldmappings)


def main():
    accident = "./ACCIDENT.csv"
    location = "./NODE.csv"
    vehicle = "./VEHICLE.csv"

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

    # This reads vehicle.csv and stores the data into a nested list.
    with open(vehicle, 'rt') as file:
        reader = csv.reader(file)
        vehicle = list(reader)
    del vehicle[0]

    # This calls the funtion that processes the data in the three lists.
    accident_location = input_process(accident, location, vehicle)

    # This calls the function that create the three shapefiles.
    createShp(accident_location)

    # This calls the function that adds the SA2 information into the shapefile.
    addSA2()


# This calls the main function.
if __name__ == '__main__':
    main()
