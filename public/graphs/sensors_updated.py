import datetime
from sets import Set
import time
import csv
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.offline as plotOffLine
import plotly.graph_objs as go
import numpy as np
import copy
import re
import sys, os
import webbrowser
import pickle


"""
Given a the path and file to a CSV file containing activity sensing data,
this function will generate a full table from that data.
The activity sensing data should have the following format per row:
{ Tag ID, Base Station ID, Date, Enter Flag }
    Data == Year-Month-Day Hour:Minute:Second
    Enter Flag == 1 when entering station, 0 when leaving

    :param fileName: path and file name of the csv file containing the activity
    data.
"""
def genTableFromCSV(fileName, today = None):
    dataItems = []
    with open(fileName, 'rb') as csvFile:
        lines = csv.reader(csvFile)
        for row in lines:
            (tag, station, enterFlag) = (row[0], row[1], row[3])
            timeString = re.search('(\d+):(\d+):(\d+)', row[2])
            secondsPastMidnight = int(timeString.group(1)) * 60 * 60 # Hours
            secondsPastMidnight += int(timeString.group(2)) * 60 # Minutes
            secondsPastMidnight += int(timeString.group(3)) # Seconds
            d = Data(tag, int(station), secondsPastMidnight, int(enterFlag))
            dataItems.append(d)

    if today == None:
        process(dataItems, days, daysMap, datetime.date.today())
    else:
        process(dataItems, days, daysMap, today)



def saveFileToLocalSystem(nameOfFile):
    # get current local system path
    path_name = os.path.realpath(__file__)
    curr_dir_path = os.path.dirname(path_name)
    graph_path = curr_dir_path + "/Graphs"
    # create a subdirectory if the one with graphs doesn't exist
    try:
        os.makedirs(graph_path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    
# with open('data_file.csv', 'rb') as csvfile:
#     raw_data = csv.reader(csvfile)
#     for row in raw_data:
#         print ', '.join(row)


class Data:
    """
    The Data class represents the raw data that is provided from the sensors group.
    As per the sensor group's example data, the data is provided as a single row
    as follows:

        :param tag_id: ID of the tag which transmits data.
        :param base_station_id: ID of the base station where children play.
        :param timestamp: Date and time formatted in seconds past midnight of the
            current day.
        :param enter_flag: 1 if the tag is entering a station, 0 if leaving.
    """
    def __init__(self, tag_id, base_station_id, timestamp, enter_flag):
        self.tag_id = tag_id 
        self.base_station_id = base_station_id 
        self.timestamp = timestamp # in seconds past midnight
        self.enter_flag = enter_flag # 1 for enter, 0 for leave

    def __repr__(self):
        return str((self.tag_id, self.base_station_id, self.timestamp, self.enter_flag))


class TimeBlock:
    """
    For a particular tag and station, a TimeBlock contains the time the tag
    entered a base station and the time the tag left.
    """
    def __init__(self, tag_id, base_station_id, enter_time, leave_time):
        self.tag_id = tag_id 
        self.base_station_id = base_station_id
        self.enter_time = enter_time # in seconds past midnight
        self.leave_time = leave_time # in seconds past midnight

    def __repr__(self):
        return str((self.tag_id, self.base_station_id, self.enter_time, self.leave_time))


class Table:
    """
    Table class stores the processed data.

        :param timeblocks: a list of all TimeBlocks.
        :param tagBlocks: Dictionary mapping each Tag ID to a list of TimeBlocks
            for that tag.
        :param tagStations: Dictionary mapping each Tag ID to dictionaries
            where the keys are stations and the values are a list of length 2
            where the 0th index is an int of the total times spent and the 1st
            is the amount of times that tag has visted that station.
        :param baseBlocks: Dictionary mapping each Base Station ID to a list of
            timeBlocks.
        :param baseStudents: Dictionary mapping each Base Station ID to a set of
            students who used that station.
        :param baseTotalTime: Dictionary with the total time spent at each station.
    """
    def __init__(self, timeblocks, tagBlocks, tagStations, baseBlocks, baseStudents, baseTotalTime):
        self.timeblocks = timeblocks
        self.tagBlocks = tagBlocks
        self.tagStations = tagStations

        self.baseBlocks = baseBlocks
        self.baseStudents = baseStudents
        self.baseTotalTime = baseTotalTime
        
    def __repr__(self):
        return "TimeBlocks: %s \n\nTagBlocks: %s \n\nTagStations: %s \n\nBaseBlocks: %s \n\nBaseStudents: %s \n\nBaseTotalTime: %s\n" % (self.timeblocks, self.tagBlocks, self.tagStations, self.baseBlocks, self.baseStudents, self.baseTotalTime)

    #str((self.timeblocks, self.tagBlocks, self.tagStations, self.baseBlocks, self.baseStudents, self.baseTotalTime))

def plotAverageTimeStations(baseStationOV, todaysDir):
    """
    Given the baseStationOV providing information about all stations as well as
    this function returns and 
    displays a bar graph showing the average amount of time spent per student who visited that station
    (each student spent x total time at station s, on average).

        :param baseStationOV see definition
        :param student
        :rtype: plt
    """
    plotDict = dict()
    
    btt = baseStationOV.baseTotalTime
    bs = baseStationOV.baseStudents
    
    for station in btt:
        plotDict[station] = btt[station] / len(bs[station]) / float(60)

    trace = go.Bar(x=plotDict.keys(), y=plotDict.values())
    data = [trace]
    layout = go.Layout(title='Average time spent per student',
        xaxis = dict(title='Station Number', type = 'category', fixedrange=True),
        yaxis = dict(title='(Minutes)', fixedrange=True))
    fig = go.Figure(data=data, layout=layout)

    htmlLink = plotOffLine.plot(fig, show_link=False, auto_open=False, filename=todaysDir + '\\avgSat.html')[7:]

    filterPlotlyHTML(htmlLink)



"""
Takes path and filename of an html file produced by Plotly.
Removes display logo and several other buttons that are normally displayed
by Plotly. Only leaves save as png button.
"""
def filterPlotlyHTML(htmlLink):
    with open(htmlLink, 'r') as file:
        tempHTML = file.read()

    tempHTML = tempHTML.replace('displaylogo:!0', 'displaylogo:!1')
    tempHTML = tempHTML.replace('modeBarButtonsToRemove:[]',
        'modeBarButtonsToRemove:["sendDataToCloud", "toggleSpikelines", \
            "toggleHover", "hoverClosestCartesian", "hoverCompareCartesian"]')

    with open(htmlLink, 'w') as file:
        file.write(tempHTML)
    del tempHTML



def plotTotalTimeStations(baseStationOV, todaysDir):
    """
    Given the baseStationOV providing information about all stations as well as
    this function returns and 
    displays a bar graph showing the total time spent at the station across all students.

        :param baseStationOV see definition
        :param student 
        :rtype: plt
    """
    plotDict = dict()
    
    btt = baseStationOV.baseTotalTime

    for station in btt:
        plotDict[station] = btt[station] / float(60)

    trace = go.Bar(x=plotDict.keys(), y=plotDict.values())
    data = [trace]
    layout = go.Layout(title='Total Time Spent at All Stations',
        xaxis = dict(title='Station Number', type = 'category', fixedrange=True),
        yaxis = dict(title='Total Time Spent (Minutes)', fixedrange=True))
    fig = go.Figure(data=data, layout=layout)

    htmlLink = plotOffLine.plot(fig, show_link=False, auto_open=False, filename=todaysDir + '\\totalTimeAtAllSats.html')[7:]

    filterPlotlyHTML(htmlLink)

    
def plotTotalTimeStationsPerStudent(tagStation, student, todaysDir):
    """
    Given the tagStation providing information about all stations as well as
    which specific student you're interested in, this function returns and 
    displays a bar graph showing all of the stations and total time spent per visit
    for that specific student.

        :param tagStation see definition
        :param student 
        :rtype: plt
    """
    
    plotDict = dict()

    for station in tagStation[student]:
        plotDict[station] = tagStation[student][station][0] / float(60)

    trace = go.Bar(x=plotDict.keys(), y=plotDict.values())
    data = [trace]
    layout = go.Layout(title='Total Time Spent at All Stations for ' + student,
        xaxis = dict(title='Station Number', type = 'category', fixedrange=True),
        yaxis = dict(title='Total Time Spent (Minutes)', fixedrange=True))
    fig = go.Figure(data=data, layout=layout)

    htmlLink = plotOffLine.plot(fig, show_link=False, auto_open=False, \
        filename=todaysDir + '\\totalTime' + str(student) + '.html')[7:]

    filterPlotlyHTML(htmlLink)



def plotAvgTimeStationsPerStudent(tagStation, student, todaysDir):
    """
    Given the tagStation providing information about all stations as well as
    which specific student you're interested in, this function returns and 
    displays a bar graph showing all of the stations and avg time spent per visit
    for that specific student.

        :param tagStation see definition
        :param student 
        :rtype: plt
    """
    avgTimesStation = avgTimeStations(tagStation)
    studAvgTimes = avgTimeStationsPerStudent(avgTimesStation, student)

    # y_pos = np.arange(len(studAvgTimes.keys()))
    # plt.bar(y_pos, studAvgTimes.values(), align='center', alpha=0.5)
    # plt.xticks(np.arange(4), studAvgTimes.keys())
    # plt.xlabel("Station Number")
    # plt.ylabel("In Minutes")
    # plt.title("Average time spent per visit for each station" + " for " + str(student))
    # plt.show()

    trace = go.Bar(x=studAvgTimes.keys(), y=studAvgTimes.values())
    data = [trace]
    layout = go.Layout(title='Average time spent per visit for each station for ' + str(student),
        xaxis = dict(title='Station Number', type = 'category', fixedrange=True),
        yaxis = dict(title='(Minutes)', fixedrange=True))
    fig = go.Figure(data=data, layout=layout)

    htmlLink = plotOffLine.plot(fig, show_link=False, auto_open=False, \
        filename=todaysDir + '\\avgTime' + str(student) + '.html')[7:]

    filterPlotlyHTML(htmlLink)
    

    
def avgTimeStationsPerStudent(avgTagStation, tag):
    """
    Returns a list of each station and the average time a student has spent there per visit

        :param avgTagStation: data structure holding all students average times per station
        :param tag: identifier for retrieval of avg times per station for specific student

            .. note:: avgTagStation is generated by the avgTimeStations function
    """
    return avgTagStation[tag]

def avgTimeStations(tagStations):
    """
    Returns data structure holding the average times spent at each station for all students

        :param tagStations: see definition in Table class

        .. note:: tagStations are generated by the studentOverview function
    """
    avgTagStation = dict()
    for tag in tagStations:
        avgTagStation[tag] = dict()
        d = tagStations[tag]
        for station in d:
            timeSpent = d[station][0]
            freqs = d[station][1]
            avgTagStation[tag][station] = timeSpent / float(freqs) / 60
    return avgTagStation


def top3Stations(tagStations):
    """
    Returns a dictionary where the keys are tags and the values are
    a list of the top three stations used by each tag provided in the
    argument.
    
        :param tagStations: see definition in Table class.
        
        .. note:: tagStations are generated by the studentOverview function.
    """
    result = dict()
    for tag in tagStations:
        d = tagStations[tag]
        stations = [x for x in tagStations[tag]]
        inAscendOrder = sorted(stations, key = lambda station: d[station][0], reverse = True)
        if len(inAscendOrder) <= 3:
            result[tag] = inAscendOrder
        else:
            result[tag] = inAscendOrder[0:3]
    return result


def studentOverview(start, end, days, daysMap, tagIds):
    """
    Generates an overview of tags (students) by aggregating multiple tables
    from a period of time into one result.

        :param start: Starting date of the data (instance of datetime.date).
        :param end: Ending data of the data (instance of datetime.date).
        :param days: 
        :param daysMap: 
        :param tagIds: 

        :return tagStation: see definition in Table class.
    """
    tables = timePeriod(start, end, days, daysMap)

    # dictionary mapping tag ids to dictionaries of total time spent at each station for that user
    tagStations = dict()
    for tag in tagIds:
        tagStations[tag] = dict()
        for table in tables:
            if tag in table.tagStations:
                for station in table.tagStations[tag]:
                    if station not in tagStations[tag]:
                        tagStations[tag][station] = table.tagStations[tag][station]
                    else:
                        tagStations[tag][station][0] += table.tagStations[tag][station][0]
                        tagStations[tag][station][1] += table.tagStations[tag][station][1]
    return tagStations
        

def baseStationOverview(start, end, days, daysMap, baseStationIds):
    """
    Provides an overview for base stations while aggregating multiple tables from
    a period of time into one Table.

        :param start: Starting date of the data (instance of datetime.date).
        :param end: Ending date of the data (instance of datetime.date).
        :param days:
        :param daysMap:
        :param baseStationIds: 

        :return: Table with the total number of students who visited, the total
            time spent, and the TimeBlocks for the underlying data.
        :rtype: Table

        :note: The Table returned does not have it's TimeBlocks, tagBlockss,
            or tagStations fields initialized.
    """
    tables = timePeriod(start, end, days, daysMap)

    # map from base station to all students who were at the base Station in that period of time
    baseStudents = dict()
    # map from base station to the total time spent by all students at that station
    baseTotalTime = dict()
    # map from base station to the TimeBlocks for that base Station
    baseBlocks = dict()
    
    for bsId in baseStationIds:
        baseStudents[bsId] = set()
        baseTotalTime[bsId] = 0
        baseBlocks[bsId] = []
        
        for table in tables:
            baseStudents[bsId].update(table.baseStudents[bsId])
            baseTotalTime[bsId] += table.baseTotalTime[bsId]
            baseBlocks[bsId] += table.baseBlocks[bsId]
            
    return Table(None, None, None, baseBlocks, baseStudents, baseTotalTime)
    

def timePeriod(start, end, days, daysMap):
    """
    :todo: Complete comments

    Generates a list of tables from days which contains data that was from
    the start to end date. Returns None if 

        :param start: Starting date of the data (instance of datetime.date).
        :param end: Ending date of the data (instance of datetime.date).
        :param days: 
        :param daysMap: 

        :return: List of 
    """
    if start > end:
        print "Error: The start date is later than the end date"
        return None
    try:
        sIndex = None
        eIndex = None
        while start <= end:
            if start in daysMap:
                sIndex = daysMap[start]
                break
            else:
                start += datetime.timedelta(days = 1)
        while start <= end:
            if end in daysMap:
                eIndex = daysMap[end]
                break
            else:
                end -= datetime.timedelta(days = 1)                         
        return days[sIndex: eIndex + 1]
    except:
        print "Error: There is no data for this date range"
        return None



def process(L, days, daysMap, test = None):
    """
    :todo: What does this do?

        :param L: List of data
        :type L: List<Data>
        :param days:
        :param daysMap:
        :param test: <any number> when testing
    """
    if test == None:
        daysMap[datetime.date.today()] = len(days)
    else:
        daysMap[test] = len(days)
    
    tables = processData(L)
    days.append(tables)
        

def processData(L):
    """
    Generates a Table given a list of data

        :param L: List of Data

        :return: Table containing all of the Data in L
        :rtype: Table class.
    """
    
    # sorts L in time order
    L.sort(key = lambda x: x.timestamp)

    # create TimeBlocks from data
    D = dict()
    timeblocks = []
    for data in L:
        key = (data.tag_id, data.base_station_id)
        if data.enter_flag == 1 and key not in D:
            D[key] = data
        elif data.enter_flag == 0 and key in D:
            enterdata = D[key]
            timeblock = TimeBlock(data.tag_id, data.base_station_id, enterdata.timestamp, data.timestamp)
            timeblocks.append(timeblock)
            del D[key]

    # create tag_id hash table
    tagD = dict()
    tagStations = dict()
    for tb in timeblocks:
        tag_id = tb.tag_id
        if tag_id not in tagD:
            tagD[tag_id] = [tb]
            tagStations[tag_id] = {tb.base_station_id: [tb.leave_time - tb.enter_time, 1]}
        else:
            tagD[tag_id].append(tb)
            if tb.base_station_id in tagStations[tag_id]:
                tagStations[tag_id][tb.base_station_id][0] += (tb.leave_time - tb.enter_time)
                tagStations[tag_id][tb.base_station_id][1] += 1
            else:
                tagStations[tag_id][tb.base_station_id] = [tb.leave_time - tb.enter_time, 1]
            
    # create base station id hash table
    bsD = dict()
    bsStudents = dict()
    bsTotalTime = dict()
    for tb in timeblocks:
        base_station_id = tb.base_station_id
        if base_station_id not in bsD:
            bsD[base_station_id] = [tb]
            bsStudents[base_station_id] = Set([tb.tag_id])
            bsTotalTime[base_station_id] = tb.leave_time - tb.enter_time
        else:
            bsD[base_station_id].append(tb) 
            bsStudents[base_station_id].add(tb.tag_id)
            bsTotalTime[base_station_id] += (tb.leave_time - tb.enter_time)
            
    return Table(timeblocks, tagD, tagStations, bsD, bsStudents, bsTotalTime)


def get_datewise_data(in_date, days, daysMap):
    """
    Station usage over different time frames: daily, weekly, monthly.

        :todo: TEST
    """
    in_date_list = in_date.split("-")
    month = in_date_list[0]
    day = in_date_list[1]
    year = in_date_list[2]
    #return table from the "days" correspnding to the date supplied
    return days[daysMap[datetime.date(int(year),int(month),int(day))]] 


def plotBaseStationVisitorCount(baseStationOV, todaysDir):
    """
    Given a Table which contains an overview of the base stations,
    this function returns and displays a bar graph showing all of the stations
    and their visitor count.

        :param baseStationOV: Table generated by the baseStationOverview
        function.
        :rtype: plt
    """
    baseStudents = copy.deepcopy(baseStationOV.baseStudents)

    for tag in baseStudents.keys():
        baseStudents[tag] = len(baseStudents[tag])

    trace = go.Bar(x=baseStudents.keys(), y=baseStudents.values())
    data = [trace]
    layout = go.Layout(title='The number of visitors at all stations',
        xaxis = dict(title='Station Number', type = 'category', fixedrange=True),
        yaxis = dict(title='# of visitors', fixedrange=True))
    fig = go.Figure(data=data, layout=layout)

    htmlLink = plotOffLine.plot(fig, show_link=False, auto_open=False, \
        filename=todaysDir + '\\visitorCount.html')[7:]

    filterPlotlyHTML(htmlLink)

def plotBaseStationUniqueVisitorCount(baseStationInfo, todaysDir):
    """
    This function accepts base station info, and outputs the number of unique
    visitors on that particular base station in the form if a graph. Info is 
    contained in the form of a dictionary.

        :param baseStationInfo: Table generated by the baseStationOverview
        function.
        :retruns: plt
    """
    baseStudents = copy.deepcopy(baseStationInfo.baseStudents)
    
    baseStudentsUnique = {}
    for key,value in baseStudents.items():
        if value not in baseStudentsUnique.values():
            baseStudentsUnique[key] = value
    
    for tag in baseStudentsUnique.keys():
        baseStudentsUnique[tag] = len(baseStudentsUnique[tag])

    trace = go.Bar(x=baseStudentsUnique.keys(), y=baseStudentsUnique.values())
    data = [trace]
    layout = go.Layout(title='The number of unique visitors at all stations',
        xaxis = dict(title='Station Number', type = 'category', fixedrange=True),
        yaxis = dict(title='# of visitors', fixedrange=True))
    fig = go.Figure(data=data, layout=layout)

    htmlLink = plotOffLine.plot(fig, show_link=False, auto_open=False, \
        filename=todaysDir + '\\visitorCount.html')[7:]

    filterPlotlyHTML(htmlLink)


# tests
def tests():
    a = Data('Charlie', 1, 36000, 1)
    b = Data('Suzie', 1, 37000, 1)
    c = Data('Charlie', 1, 38000, 0)
    d = Data('Suzie', 1, 39000, 0)
    e = Data('Suzie', 2, 40000, 1)
    f = Data('Suzie', 2, 41000, 0)
    g = Data('Charlie', 1, 44000, 1)
    h = Data('Charlie', 1, 48000, 0)
    i = Data('Suzie', 3, 50000, 1)
    j = Data('Suzie', 3, 55000, 0)
    k = Data('Suzie', 4, 50000, 1)
    l = Data('Suzie', 4, 56000, 0)
    data = [a, b, c, d, e, f, g, h, i, j, k, l]

    # processData function
    # print "processData function...", processData(data)
    processData(data)
    # process function
    days = []
    daysMap = dict()

    d2 = datetime.date.today() - datetime.timedelta(days = 5)
    d3 = datetime.date.today() - datetime.timedelta(days = 1)
    
    process(data, days, daysMap, d2)
    print days
    print daysMap
    process(data, days, daysMap, d3)
    print days
    print daysMap

    # timePeriod function
    assert(timePeriod(d2, d2, days, daysMap) == timePeriod(d2 - datetime.timedelta(days = 1), d2, days, daysMap))
    print timePeriod(d2, d2, days, daysMap)
    print timePeriod(d2, d3, days, daysMap)

    # student overview function
    print studentOverview(d2, d3, days, daysMap, ['Suzie'])
    tagStation = studentOverview(d2, d3, days, daysMap, ['Suzie', 'Charlie'])
    print tagStation

    # top 3 stations function
    print "Top 3 stations...", top3Stations(tagStation)

    # base station overview function
    print "Testing Base Station Overview"
    print baseStationOverview(d2, d2, days, daysMap, [1])
    bso = baseStationOverview(d2, d3, days, daysMap, [1, 2, 3, 4])
    print bso

    # plotBaseStationVisitorCount(bso)
    plotAverageTimeStations(bso, 'plots\\2017-5-1')
    plotTotalTimeStations(bso, 'plots\\2017-5-1')
    # Test for plot for avg times per station for Suzie
    plotAvgTimeStationsPerStudent(tagStation, "Suzie", 'plots\\2017-5-1')
    plotTotalTimeStationsPerStudent(tagStation, "Suzie", 'plots\\2017-5-1')

#tests()

##timeString = re.search('(\d+)/(\d+)/(\d+)', "5/3/2017")
##print int(timeString.group(1))
##print int(timeString.group(2))
##print int(timeString.group(3))

# example input: 5/3/2017 (must include entire year, 5/3/17 does not work)
# returns a datetime.date object
def stringToDate(s):
    try:
        timeString = re.search('(\d+)/(\d+)/(\d+)', s)
        month = int(timeString.group(1))
        day = int(timeString.group(2))
        year = int(timeString.group(3))
        return datetime.date(year, month, day)
    except:
        print "The date string could not be parsed. Example string: 2/3/2017"
        return None

if __name__ == "__main__":
    # example commands:
    # python <thisfilename> lastweek
    # python <thisfilename> lastmonth
    # python <thisfilename> daterange 4/28/2017 5/2/2017
    # python <thisFileName> <csvFileName>
    if sys.argv[1] in ["lastweek", "lastmonth", "daterange"]:
        
        try:
            days = pickle.load(open("days.p", "rb"))
            daysMap = pickle.load(open("daysMap.p", "rb"))
        except:
            days = []
            daysMap = dict()
        endDate = None
        startDate = None
        period = None
        if sys.argv[1] == "lastweek":
            endDate = datetime.date.today()
            startDate = datetime.date.today() - datetime.timedelta(days = 6)
            period = "weekof"
        elif sys.argv[1] == "lastmonth":
            endDate = datetime.date.today()
            startDate = datetime.date.today() - datetime.timedelta(days = 30)
            period = "monthof"
        else:
            endDate = stringToDate(sys.argv[3])
            startDate = stringToDate(sys.argv[2])
            period = "periodfrom"
        
        periodStr = period + str(startDate) + "to" + str(endDate)

        print periodStr
        
        todaydir = 'plots\\' + periodStr  
        if not os.path.exists(todaydir):
            os.makedirs(todaydir)
        
        tempTable = timePeriod(startDate, endDate, days, daysMap)[0]
        
        stations = tempTable.baseBlocks.keys()
        tags = tempTable.tagBlocks.keys()

        bso = baseStationOverview(startDate, endDate, days, daysMap, stations)
        tagStation = studentOverview(startDate, endDate, days, daysMap, tags)
        
        plotAverageTimeStations(bso, todaydir)
        plotTotalTimeStations(bso, todaydir)

        for tag in tags:
            plotAvgTimeStationsPerStudent(tagStation, tag, todaydir)
            plotTotalTimeStationsPerStudent(tagStation, tag, todaydir)
        
        exit()
        
    csvFileForToday = sys.argv[1]
    if ".csv" not in csvFileForToday:
        raise Exception("Please provide a CSV file to process data on")

    # load previous days and daysMap from file
    try:
        days = pickle.load(open("days.p", "rb"))
        daysMap = pickle.load(open("daysMap.p", "rb"))
    except:
        days = []
        daysMap = dict()

    today = datetime.date.today()
    todayStr = str(today)
    todaydir = 'plots\\' + todayStr

    genTableFromCSV(csvFileForToday, today)

    if not os.path.exists(todaydir):
        os.makedirs(todaydir)

    tempTable = timePeriod(today, today, days, daysMap)[0]
    stations = tempTable.baseBlocks.keys()
    tags = tempTable.tagBlocks.keys()

    bso = baseStationOverview(today, today, days, daysMap, stations)
    tagStation = studentOverview(today, today, days, daysMap, tags)

    pickle.dump(days, open( "days.p", "wb" ) )
    pickle.dump(daysMap, open( "daysMap.p", "wb" ) )

    plotAverageTimeStations(bso, todaydir)
    plotTotalTimeStations(bso, todaydir)
    plotBaseStationVisitorCount(bso, todaydir)

    for tag in tags:
        plotAvgTimeStationsPerStudent(tagStation, tag, todaydir)
        plotTotalTimeStationsPerStudent(tagStation, tag, todaydir)
