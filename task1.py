'''
GEOM90042
Assignment 2 Task 1
Author: JIE PU, CHANGJIAN MA
Student Number: 765316, 653909
'''


import csv
import math
import operator
import numpy as np
import matplotlib.pyplot as plt


# This function computes the average number of accidents per year.
def compute_avg(accident):
    # This dictionary stores the average number of accidents in each year.
    count_by_year = {}

    # The loop iterates in the list to computer number of accidents in each year.
    for row in accident:
        if len(row):
            # This extracts the year information from the list.
            year = row[1].split('/')[2]
            
            # This accumulates when an accident happened in a year.
            if year in count_by_year.keys():
                count_by_year[year] += 1
            else:
                count_by_year[year] = 1

    # i is used to keep track of number of years.
    i = 0
    # total is used to keep track of total accident numbers.
    total = 0

    # This loop is used to computer number of years and number of accidents each year.
    for key in count_by_year:
        i+=1
        total += count_by_year[key]

    # This returns the average number of accidents per year.
    return total/i


# This function is used to return the second most common type of accident.
def secCom(accident):
    count_all = 0
    # This dictionary is used to record the number of each type of accidents.
    count = {}

    # The loop works to count number of each type of accidents.
    for row in accident:
        if len(row):
            # This extracts type information from the accident list.
            type = row[4]
            if type in count.keys():
                count[type] += 1
                count_all += 1
            else:
                count[type] = 1
                count_all += 1

    # This breaks the dictionary into two lists for calculating max values.
    k = list(count.keys())
    v = list(count.values())

    # This removes the most common type of accidents.
    k.remove(k[v.index(max(v))])
    v.remove(max(v))

    # This gives the index of the second most common type of accidents.
    col_type = k[v.index(max(v))]
    col_num = max(v)

    # This returns the type and percentage of the second most common type of accidents.
    output = toStringSec(col_type,float(col_num)/count_all*100)
    return output


# This function computes numbers of accidents for each type of vehicle.
def numByType(vehicle,accident):
    # This dictionary keeps track of number of accidents for each vehicle type.
    count_by_type = {}
    # This set keeps track of types of vehicles involved in each accident.
    accident_type = set()

    i = 0
    # This loop accumulates number of accidents for each vehicle type.
    for row in vehicle:
        if len(row):
            if len(accident[i]):
                # This decides whether the row and the current accident matches.
                if row[0] != accident[i][0]:
                    # This extracts the year information from the list.
                    year = accident[i][1].split('/')[2]

                    # The loop is used to accumulates cound of each type.
                    for type in accident_type:
                        if year in count_by_type.keys():
                            if type in count_by_type[year].keys():
                                count_by_type[year][type] += 1
                            else:
                                count_by_type[year][type] = 1
                        else:
                            count_by_type[year] = {}
                            count_by_type[year][type] = 1
                            
                    # If accident is not found in the vehicle table, ignore that accident.
                    if len(accident[i+1]):
                        if accident[i+1][0] == row[0]:
                            i += 1
                            
                    # This restores the set into a new set when we come with a new accident.
                    accident_type = set()
                    
            # This adds the type into the set that records types of vehicles involved.
            if accident[i][0] == row[0]:
                accident_type.add(row[13])

    return count_by_type


# This function returns LGAs with number of accidents happened each year.
def topTenLGA(location,accident):
    # The dictionary keeps track of counts of accidents in each LGA in each year.
    count_by_LGA = {}
    i = 0

    # This loop accumulates counts of accidents in each LGA in each year.
    for row in location:
        if len(row):
            if len(accident[i]):
                # If one accident cannot match a location, ignore it.
                if (int(row[0][1:12]) > int(accident[i][0][1:12])):
                    i+=1

                # This decides whether the location information matches a accident.
                if row[0] == accident[i][0]:
                    # This extracts the year information from the list.
                    year = accident[i][1].split('/')[2]
                    # This extracts the LGA name of the accident.
                    LGA = row[5]

                    # This accumulates counts of accidents in each LGA each year.
                    if year in count_by_LGA.keys():
                        if LGA in count_by_LGA[year].keys():
                            count_by_LGA[year][LGA] += 1
                        else:
                            count_by_LGA[year][LGA] = 1
                    else:
                        count_by_LGA[year] = {}
                        count_by_LGA[year][LGA] = 1
                    i += 1

    return count_by_LGA


# This function generates the output string for question 1 in task 1.
def toStringAvg(avg):
    output = "1. The average number of accidents per year is %6.2f." % (avg)
    return output


# This function generates the output string for question 2 in task 1.
def toStringSec(type,percentage):
    output = "2. The second most common type of accident in all the recorded years is %s, " %(type)
    output += "and the percentage of the accidents that belong to this type is %4.2f%%." %(percentage)
    return output


# This function generates the HTML that output the number of accidents by vehicle type.
def byTypeHTML(count_by_type):
    output = "<table border = '1' cellpadding = '0' cellspacing = '0' width='500px' height = '200px'>"

    # This list keeps track of the order in number of accidents in 2006.
    type_order = sorted(count_by_type["2006"].items(), key=operator.itemgetter(1), reverse = True)
    # This list stores the order of year.
    year_order = ["2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016"]

    # These loops are used to add the types that do not exist in a certain year.
    by_type = []
    for item in type_order:
        by_type.append(item[0])

    for year in count_by_type.keys():
        for type in count_by_type[year].keys():
            if type not in by_type:
                by_type.append(type)

    output += "3.<tr><td>'Vehicle Type'</td>"

    # This loop is used to show the first column in the HTML.
    for item in year_order:
        output += "<td>" + item + "</td>"
    output += "</tr>"

    # This loop stores the number information into the HTML.
    for item in by_type:
        output += "<tr><td>"
        output += item
        output += "</td>"
        for year in year_order:
            output += "<td>"
            output += str(count_by_type[year][item])
            output += "</td>"
        output += "</tr>"
    output += "</table>"

    return output


# This function generates the HTML that output the number of accidents by LGA name.
def byLGAHTML(count_by_LGA):
    output = "<table border = '1' cellpadding = '0' cellspacing = '0' width='500px' height = '200px'>"

    # This list keeps track of the sorted list of count by LGA.
    order_2006 = sorted(count_by_LGA["2006"].items(), key=operator.itemgetter(1), reverse = True)
    # This selects the first ten LGAs in 2006.
    order_2006 = order_2006[0:10]

    by_LGA = []
    for item in order_2006:
        by_LGA.append(item[0])

    # This outputs the first row into HTML.
    output += "4.<tr><td>LGA</td><td>No. 2006</td><td>No. 2016</td><td>Difference</td><td>Change</td></tr>"

    # This loop outputs the number of accidents in each LGA in top 10 LGAS in 2006 and 2016.
    for item in by_LGA:
        output += "<tr><td>"
        output += item
        output += "</td><td>"
        output += str(count_by_LGA["2006"][item])
        output += "</td><td>"
        output += str(count_by_LGA["2016"][item])
        output += "</td><td>"
        output += str(count_by_LGA["2016"][item]-count_by_LGA["2006"][item])
        output += "</td><td>"
        percentage = (count_by_LGA["2016"][item]-count_by_LGA["2006"][item])/float(count_by_LGA["2006"][item]) * 100
        output += "%0.2f" % percentage
        output += "%</td></tr>"
    output += "</table>"

    return output


# This function outputs the results of task 1 into an HTML file.
def toHTML(output):
    output_string = "<!DOCTYPE html>"
    output_string = "<html>\n<body>"
    output_string += "<p>" + output[0] + "</p>"
    output_string += "<p>" + output[1] + "</p>"
    output_string += "<p>" + byTypeHTML(output[2]) + "</p>"
    output_string += "<p>" + byLGAHTML(output[3]) + "</p>"
    output_string += "<p> 5. </br><img src='fig1.png' alt='Accident Numbers by Days of the Week'></p>"
    output_string += "<p> 6. </br><img src='fig2.png' alt='Yearly Change by Severity'></p>"
    output += "</body>\n</html>"

    with open('task1_765316.html', 'w') as outfile:
        outfile.write(output_string)


# This function writes question 3 of task 1 into a csv file.
def write_by_type(count_by_type):
    # This list keeps track of the order in number of accidents in 2006.
    type_order = sorted(count_by_type["2006"].items(), key=operator.itemgetter(1), reverse=True)
    # This list stores the order of year.
    year_order = ["2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016"]

    # These loops are used to add the types that do not exist in a certain year.
    by_type = []
    for item in type_order:
        by_type.append(item[0])

    for year in count_by_type.keys():
        for type in count_by_type[year].keys():
            if type not in by_type:
                by_type.append(type)

    # If a type does not exist in a certain year, mark it as '0'.
    for item in by_type:
        for year in year_order:
            if item not in count_by_type[year].keys():
                count_by_type[year][item] = 0

    # This writes the data into a csv file row by row.
    with open('AccidentByYear.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Vehicle Type"]+year_order)
        for item in by_type:
            writer.writerow([item,str(count_by_type[year_order[0]][item]),str(count_by_type[year_order[1]][item])
                            ,str(count_by_type[year_order[2]][item]),str(count_by_type[year_order[3]][item])
                            ,str(count_by_type[year_order[4]][item]),str(count_by_type[year_order[5]][item])
                            ,str(count_by_type[year_order[6]][item]),str(count_by_type[year_order[7]][item])
                            ,str(count_by_type[year_order[8]][item]),str(count_by_type[year_order[9]][item])
                            ,str(count_by_type[year_order[10]][item])])


# This function writes the result of question 4 into a csv file.
def write_by_LGA(count_by_LGA):
    # This list keeps track of the sorted list of count by LGA.
    order_2006 = sorted(count_by_LGA["2006"].items(), key=operator.itemgetter(1), reverse=True)
    # This selects the first ten LGAs in 2006.
    order_2006 = order_2006[0:10]

    by_LGA = []
    for item in order_2006:
        by_LGA.append(item[0])

    # This outputs the data row by row into a csv file.        
    with open('AccidentByLGA.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['LGA','No. 2006','No. 2016','Difference','Change'])
        for item in by_LGA:
            writer.writerow([item,str(count_by_LGA["2006"][item]),str(count_by_LGA["2016"][item]),
                             str(count_by_LGA["2016"][item]-count_by_LGA["2006"][item]),
                             str((count_by_LGA["2016"][item]-count_by_LGA["2006"][item])/
                             float(count_by_LGA["2006"][item])*100)+"%"])


# This calls the funtions that outputs question 3 and 4 into csv files.
def write_into_csv(num_by_type,top_ten_LGA):
    write_by_type(num_by_type)
    write_by_LGA(top_ten_LGA)
    return


# This function generates a bar chart of accident number by days of the week in 2006 and 2016.
def drawByDays(accident):
    # This dictionary keeps track of accident number by days of the week in 2006 and 2016.
    count_by_days = {}

    # This loop counts the number by days of the week.
    for row in accident:
        if len(row):
            # This extracts the year information from the list.
            year = row[1].split('/')[2]
            # This extracts the day of week information from the list.
            day = row[6]

            # This accumulates the numbers of accidents by day of week and store them into the dictionary.
            if year in count_by_days.keys():
                if day in count_by_days[year].keys():
                    count_by_days[year][day] += 1
                else:
                    count_by_days[year][day] = 1
            else:
                count_by_days[year] = {}
                count_by_days[year][day] = 1

    # This stores the count in the dictionary into two lists for generating the bar chart.
    list_2006 = []
    list_2016 = []
    list_2006.append(count_by_days['2006']['Monday'])
    list_2006.append(count_by_days['2006']['Tuesday'])
    list_2006.append(count_by_days['2006']['Wednesday'])
    list_2006.append(count_by_days['2006']['Thursday'])
    list_2006.append(count_by_days['2006']['Friday'])
    list_2006.append(count_by_days['2006']['Saturday'])
    list_2006.append(count_by_days['2006']['Sunday'])
    list_2016.append(count_by_days['2016']['Monday'])
    list_2016.append(count_by_days['2016']['Tuesday'])
    list_2016.append(count_by_days['2016']['Wednesday'])
    list_2016.append(count_by_days['2016']['Thursday'])
    list_2016.append(count_by_days['2016']['Friday'])
    list_2016.append(count_by_days['2016']['Saturday'])
    list_2016.append(count_by_days['2016']['Sunday'])

    # This sets the number of fields.
    N = 7
    ind = np.arange(N)
    # This sets the width of each bar.
    width = 0.35

    fig, ax = plt.subplots()
    # This draws the bars in 2006 in red.
    rect1 = ax.bar(ind, list_2006, width, color='r')
    # This draws the bars in 2016 in yellow.
    rect2 = ax.bar(ind+width, list_2016, width, color='y')

    # Titles and legends are added here.
    ax.set_title("Accident Numbers by Days of the Week")
    ax.set_xticks(ind + width/2)
    ax.set_xticklabels(("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"))
    ax.legend((rect1[0],rect2[0]),("2006","2016"))
    ax.yaxis.set_units("Number")
    ax.autoscale_view()
    
    # This stores the bar chart into a png file.
    fig.savefig('fig1.png')
    plt.close(fig)


# This function generates a line chart of accident number by severity from 2006 to 2016.
def drawBySeverity(accident):
    # This dictionary keeps track of accident number by severity from 2006 to 2016.
    count_by_severity = {}

    # This loop accumulates the number of accidents by severity.
    for row in accident:
        if len(row):
            # This extracts the year information from the list.
            year = row[1].split('/')[2]
            # This extracts the severity information from the list.
            severity = row[26]

            # This accumulates the accident numbers by severity and year.
            if year in count_by_severity.keys():
                if severity in count_by_severity[year].keys():
                    count_by_severity[year][severity] += 1
                else:
                    count_by_severity[year][severity] = 1
            else:
                count_by_severity[year] = {}
                count_by_severity[year][severity] = 1

    # This defines the order of years.
    year_order = ["2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016"]
    # This defines the order of severities.
    severity_order = ["1","2","3"]

    # This copy the count information from the dictionary into three lists for chart output.
    severe_1 = []
    severe_2 = []
    severe_3 = []
    for year in year_order:
        severe_1.append(count_by_severity[year]["1"])
        severe_2.append(count_by_severity[year]["2"])
        severe_3.append(count_by_severity[year]["3"])

    fig, ax = plt.subplots()
    # This draws the tree lines with different severities.
    ax.plot(year_order, severe_1,label='Severity: 1', color='g', marker='o')
    ax.plot(year_order, severe_2,label='Severity: 2', color='y', marker='o')
    ax.plot(year_order, severe_3,label='Severity: 3', color='r', marker='o')

    # These set the title and legend of the chart.
    ax.set_title("Yearly Change by Severity")
    plt.ylabel("Number")
    plt.xlabel("Year")
    ax.set_xticklabels(year_order)
    plt.ylim(0,15000)
    plt.legend()

    # This outputs the chart into a png file.
    fig.savefig('fig2.png')
    plt.close(fig)


# This is the main function that reads the csv files and calls the other functions.
def main():
    accident = "./ACCIDENT.csv"
    vehicle = "./VEHICLE.csv"
    location = "./NODE.csv"
    output_sets = []

    # This reads accident.csv and stores the data into a nested list.
    with open(accident, 'rt') as file:
        reader = csv.reader(file)
        accident = list(reader)
    # This deletes the title row.
    del accident[0]

    # This removes the data for 2017 because it is not complete.
    for element in list(accident):
        if len(element):
            if element[1].split('/')[2] == "2017":
                accident.remove(element)

    # This reads vehicle.csv and stores the data into a nested list.
    with open (vehicle, 'rt') as file:
        reader = csv.reader(file)
        vehicle = list(reader)
    # This deletes the title row.
    del vehicle[0]

    # This reads node.csv and stores the data into a nested list.
    with open (location, 'rt') as file:
        reader = csv.reader(file)
        location = list(reader)
    # This deletes the title row.
    del location[0]

    # This calls the function that computes average number of accidents per year and output it.
    avg = compute_avg(accident)
    output_sets.append(toStringAvg(avg))

    # This calls the function that gets the second most common type of accident and output it.
    sec_com = secCom(accident)
    output_sets.append(sec_com)

    # This calls the function that counts number of accidents by vehicle type and output it.
    num_by_type = numByType(vehicle,accident)
    output_sets.append(num_by_type)

    # This calls the function that gets the top ten LGAs and their accident numbers and output it.
    top_ten_LGA = topTenLGA(location,accident)
    output_sets.append(top_ten_LGA)
    
    # This writes the results of question 3 and 4 into two csv files.
    write_into_csv(num_by_type,top_ten_LGA)

    # This calls the funtion that produces a bar chart of accident numbers by day of week.
    drawByDays(accident)
    # This calls the funtion that produces a bar chart of accident numbers by severity from 2006 to 2016.
    drawBySeverity(accident)

    # This calls the funtion that outputs everything above into an HTML file.
    toHTML(output_sets)


# This function calls the main funtion.
if __name__ == '__main__':
    main()
