"""
We want to compare badge group to control group:
Mean and Standard deviation of: number of discussion, comments, Total
Histogram: x axis is number of dis/com/tot, y axis is amount of people
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import math
import pickle
import datetime
from datetime import date
TodaysDate = date.today()
TodaysDayNumber=TodaysDate.timetuple().tm_yday
TodaysWeek=TodaysDate.isocalendar()[1]
StartDay=date(2020, 3, 8)
StartDayNumber=StartDay.timetuple().tm_yday
StartWeek=StartDay.isocalendar()[1]
NumberOfDays=1+(TodaysDate - StartDay).days


UsersWithId = pd.read_csv('data/NameIdAndMoodleId.csv')
Chosen=pd.read_csv('data/ChosenList.csv')
NotChosen=pd.read_csv('data/NotChosenList.csv')
Newlogs=pd.read_csv('C:/Users/Amir/PycharmProjects/My_Badges/data/17.05.csv')
Newlogs['Time'] = pd.to_datetime(Newlogs['Time'], format="%d/%m/%y, %H:%M")
data=pd.read_csv('data/allStudentsStatus.csv')
data["NewPosts"]=pd.to_numeric(data["NewPosts"], downcast="float")
data["Comments"]=pd.to_numeric(data["Comments"], downcast="float")

def LookingForMoodleId(x):
    m=re.search("The user with id '(.+?)'", x)
    if m:
        return int(m.group(1))
    else:
        return int(0)
Newlogs["MoodleId"]=Newlogs["Event name"].apply(lambda x: LookingForMoodleId(x))


class PersonalActivity:
    def __init__(self, MoodleId, name, NumberOfDays):
        self.MoodleId= MoodleId
        self.name=name
        self.Array=np.zeros(NumberOfDays)#CumulatingArray
        self.DayMedian=0
        self.WeekMedian=0
        self.BadgeDays=[]
        self.BadgeIndex=[]
        self.Badges=[]

def SplitChosenAndNot(data):
    ChosenData=pd.DataFrame(columns=data.columns)
    NotChosenData = pd.DataFrame(columns=data.columns)
    for index, row in data.iterrows():
        if ((row['MoodleId'] == Chosen['MoodleId']).any()):
            ChosenData=ChosenData.append(row,ignore_index=True, sort=False)
        elif ((row['MoodleId'] == NotChosen['MoodleId']).any()):
            NotChosenData=NotChosenData.append(row,ignore_index=True, sort=False)
    return  ChosenData,NotChosenData


def CalcAvrageAndStd(Data):
    Data=Data.fillna(0)
    Acom=np.mean(Data["Comments"])
    Adis=np.mean(Data["NewPosts"])
    Atot=np.mean(Data["Total"])
    Scom=np.sqrt(np.sum(np.power(Acom-Data["Comments"],2))/Data.shape[0])
    Sdis = np.sqrt(np.sum(np.power(Adis - Data["NewPosts"], 2)) /Data.shape[0])
    Stot = np.sqrt(np.sum(np.power(Atot - Data["Total"], 2)) / Data.shape[0])
    return {"Average Comments": Acom, "Average Discussions": Adis, "Average Total": Atot, "Standard Deviation Comments": Scom, "Standard Deviation Discussions": Sdis, "Standard Deviation Total": Stot}

ChosenData, NotChosenData=SplitChosenAndNot(data)
ChosenStat=CalcAvrageAndStd(ChosenData)
NotChosenStat=CalcAvrageAndStd(NotChosenData)

def MakeHistogram(ChosenData,NotChosenData, object):
    ChosenData = ChosenData.fillna(0)
    NotChosenData = NotChosenData.fillna(0)
    plt.hist(ChosenData[object], label="Badge Group", alpha= 0.5)
    plt.hist(NotChosenData[object], label="Contorl Group", alpha= 0.5)
    plt.xlabel("Number of "+object)
    plt.ylabel("Counts")
    plt.title("Histogram of "+object)
    plt.legend()
    plt.savefig('graphs/histogram'+object+'.png')
    plt.show()
    plt.hist(ChosenData[object], weights=np.ones(len(ChosenData)) / len(ChosenData), label="Badge Group", alpha= 0.5)
    plt.hist(NotChosenData[object], weights=np.ones(len(NotChosenData)) / len(NotChosenData), label="Contorl Group", alpha= 0.5)
    plt.xlabel("Number of " + object)
    plt.ylabel("Normalized Counts")
    plt.title("Normalized Histogram of "+object)
    plt.legend()
    plt.savefig('graphs/histogramNormalized' + object + '.png')
    plt.show()



#MakeHistogram(ChosenData,NotChosenData, "Comments")
#MakeHistogram(ChosenData,NotChosenData, "NewPosts")
#MakeHistogram(ChosenData,NotChosenData, "Total")

def getPeopleWithAtleastOne(data, object):
    data["DiscussionBadge"] = data["DiscussionBadge"].astype(str)
    data["CommentsBadge"] = data["CommentsBadge"].astype(str)
    data.replace(0, "")
    if (object == "Discussion"):
        data= data[data["NewPosts"].apply(lambda x: x != "" )]
        data = data[data["NewPosts"].apply(lambda x: x !=0)]
        return data[data["NewPosts"].notna()]
    if (object == "Post"):
        data= data[data["Comments"].apply(lambda x: x != "" )]
        data= data[data["Comments"].apply(lambda x: x != 0 )]
        return data[data["Comments"].notna()]


def GetPeopleWithBadges(data, object):
    data["DiscussionBadge"]=data["DiscussionBadge"].astype(str)
    data["CommentsBadge"] = data["CommentsBadge"].astype(str)
    if (object=="Discussion"):
        return data[data["DiscussionBadge"].apply(lambda x: x!="nan")]
    if (object=="Post"):
        return data[data["CommentsBadge"].apply(lambda x: x!="nan")]

def GotBadge(numberOfActivities,object):
    if (object=="Post"):
        if (numberOfActivities==50):
            return 'Guro'
        elif (numberOfActivities==30):
            return'Champion'
        elif (numberOfActivities == 8):
            return 'Hero'

    elif (object=="Discussion"):
        if (numberOfActivities == 40):
            return 'Socrates'
        elif (numberOfActivities == 20):
            return 'curious'
        elif (numberOfActivities == 5):
            return 'inquisitive'
    return False


"""
I want a function that gets a group: chosen with discussion badge/chosen with comments badge/
not chosen with discussion badge/not chosen with comments badge.
it runs over each person in the group, and produces a table for his activity related to the object over all days 
from start to today.
"""
def MedianOfIntensityAndConsistency(MoodleId, object,PersonalNewLogs, NumberOfDays):
    DaysIndex=np.arange(StartDayNumber,TodaysDayNumber+1,1)
    WeeksIndex=np.arange(StartWeek,TodaysWeek+1,1)
    PersonalNewLogs["WeekNumber"] = PersonalNewLogs["Time"].apply(lambda x: x.date().isocalendar()[1])
    PersonalNewLogs["DayNumber"] = PersonalNewLogs["Time"].apply(lambda x: x.timetuple().tm_yday)
    ActivitiesPerWeek = pd.DataFrame(PersonalNewLogs.groupby("WeekNumber").size())
    WeeksDataFrame=pd.DataFrame(np.zeros(len(WeeksIndex)), index=WeeksIndex)
    WeeksDataFrame.loc[ActivitiesPerWeek.index]=ActivitiesPerWeek
    ActivitiesPerDay = pd.DataFrame(PersonalNewLogs.groupby("DayNumber").size())
    DaysDataFrame = pd.DataFrame(np.zeros(len(DaysIndex)), index=DaysIndex)
    DaysDataFrame.loc[ActivitiesPerDay.index] = ActivitiesPerDay
    return WeeksDataFrame.mean()[0], DaysDataFrame.mean()[0]

def GetActivitiesOfUser(MoodleId, object,PersonalNewLogs, NumberOfDays):
    PersonalNewLogs=PersonalNewLogs[PersonalNewLogs["Component"].apply(lambda x: x==object+' created')]#only looking at created posts/discussions
    PersonalNewLogs=PersonalNewLogs.sort_values(by=["Time"])#aranging by time
    WeekMedian,DayMedian=MedianOfIntensityAndConsistency(MoodleId, object,PersonalNewLogs, NumberOfDays)
    p=PersonalActivity(MoodleId,PersonalNewLogs["User full name"].iloc[0], NumberOfDays)
    p.DayMedian=DayMedian
    p.WeekMedian=WeekMedian
    #Making DaysArray
    LastRowDay=StartDay
    LastRowIndex=0
    for index, row in PersonalNewLogs.iterrows():
        RowDay=row["Time"].date()
        RowIndex=(RowDay-StartDay).days
        p.Array[LastRowIndex:RowIndex]=p.Array[LastRowIndex]
        p.Array[RowIndex]=p.Array[LastRowIndex]+1
        badge=GotBadge(p.Array[RowIndex],object)
        if (badge!=False):
            p.BadgeDays=p.BadgeDays+[RowDay]
            p.BadgeIndex=p.BadgeIndex+[RowIndex]
            p.Badges=p.Badges+[badge]
        LastRowDay=RowDay
        LastRowIndex=RowIndex
    #continuing the last activity until the end:
    p.Array[LastRowIndex:NumberOfDays]=p.Array[LastRowIndex]
    return p


def LookForBadgeOwnersActivity(group, object,Newlogs):
    TableOfActivities= pd.DataFrame(columns={"MoodleId", "name", "Array", "Badges","BadgesDays", "BadgeIndex", "DaysMedian", "WeeksMedian"})
    for index, row in group.iterrows():
        h=GetActivitiesOfUser(row["MoodleId"],object,Newlogs[Newlogs["MoodleId"].apply(lambda x: x==row["MoodleId"])],NumberOfDays)
        TableOfActivities =TableOfActivities.append({"MoodleId": h.MoodleId, "name": h.name, "Array": h.Array, "Badges": h.Badges, "BadgesDays": h.BadgeDays, "BadgeIndex": h.BadgeIndex, "DaysMedian": h.DayMedian, "WeeksMedian": h.WeekMedian}, ignore_index=True, sort=False)
    return TableOfActivities

def NormalizeByFirstBadge(table,DaysBefore,DaysAfter):
    DaysTable=pd.DataFrame()
    MoodleIdColumn=pd.DataFrame(columns={"MoodleId"})
    Array = pd.DataFrame(table.Array.tolist(), dtype=int)
    for index, row in table.iterrows():
        BadgeIndex=table.loc[index,"BadgeIndex"][0]
        if ((BadgeIndex-DaysBefore>=0)and (BadgeIndex+DaysAfter<NumberOfDays)):
            DaysTable=DaysTable.append(Array.iloc[index,BadgeIndex-DaysBefore:BadgeIndex+DaysAfter+1].reset_index(drop=True), sort=False,ignore_index=True)
            MoodleIdColumn=MoodleIdColumn.append({"MoodleId": table.loc[index,"MoodleId"]} ,sort=False,ignore_index=True)
    DaysTable["MoodleId"]=MoodleIdColumn
    return DaysTable

def MakeFigure3(table,DaysBefore,DaysAfter, object):
    # PeopleWithCommentsBadge=GetPeopleWithBadges(data,"Post")
    # PeopleWithCommentsBadge_Activities=LookForBadgeOwnersActivity(PeopleWithCommentsBadge, "Post", Newlogs)
    # PeopleWithCommentsBadge_Activities.to_pickle('PeopleWithCommentsBadge_Activities.pkl')

    # PeopleWithDiscussionBadge=GetPeopleWithBadges(data,"Discussion")
    # PeopleWithDiscussionBadge_Activities =LookForBadgeOwnersActivity(PeopleWithDiscussionBadge, "Discussion", Newlogs)
    # PeopleWithDiscussionBadge_Activities.to_pickle('PeopleWithDiscussionBadge_Activities.pkl')
    # PeopleWithDiscussionBadge_Activities=pd.read_pickle('PeopleWithDiscussionBadge_Activities.pkl')

    DaysBefore = 10
    DaysAfter = 4
    DaysTable = NormalizeByFirstBadge(PeopleWithDiscussionBadge_Activities, DaysBefore, DaysAfter)
    ChosenGroupidx=table["MoodleId"].apply(lambda x: (x==Chosen["MoodleId"]).any(axis=0))
    NumberOfChosen=np.sum(ChosenGroupidx)
    NotChosenGroupidx = table["MoodleId"].apply(lambda x: (x == NotChosen["MoodleId"]).any(axis=0))
    NumberOfControl=np.sum(NotChosenGroupidx)

    x=np.arange(-DaysBefore,DaysAfter+1,1)
    table=table.iloc[:,:DaysBefore+DaysAfter+1]#forget Moodle Id
    yChosen=table.loc[ChosenGroupidx].mean(axis=0)
    yNotChosen=table.loc[NotChosenGroupidx].mean(axis=0)
    plt.plot(x, yChosen, label="Badge Group- Averaged on "+str(NumberOfChosen)+" Students")
    plt.plot(x, yNotChosen, label="Control Group- Averaged on "+str(NumberOfControl)+" Students")
    plt.xlabel("Days since First badge of "+ object)
    plt.ylabel("Number of activities until day x")
    plt.title("Number Of activities for "+object+" Badge")
    plt.legend()
    plt.savefig('graphs/'+object+'BadgeAnalysis.png')
    plt.show()


def MakeFigure4(table, object):
    ChosenGroupidx = table["MoodleId"].apply(lambda x: (x == Chosen["MoodleId"]).any(axis=0))
    NumberOfChosen = np.sum(ChosenGroupidx)
    NotChosenGroupidx = table["MoodleId"].apply(lambda x: (x == NotChosen["MoodleId"]).any(axis=0))
    NumberOfControl = np.sum(NotChosenGroupidx)
    xChosen=table.loc[ChosenGroupidx,"WeeksMedian"]
    yChosen = table.loc[ChosenGroupidx,"DaysMedian"]
    xNotChosen = table.loc[NotChosenGroupidx, "WeeksMedian"]
    yNotChosen = table.loc[NotChosenGroupidx, "DaysMedian"]
    plt.scatter(xChosen, yChosen, label="Badge Group")
    plt.scatter(xNotChosen, yNotChosen, label="Control Group")
    plt.xlabel("Consistency (Days of Work per Week) on " + object+"s")
    plt.ylabel("Intensity (edits/working day)")
    plt.title("Intensity/Consistency graph for " + object + " activity")
    plt.legend()
    plt.savefig('graphs/' + object + 'Graph4.png')
    plt.show()

def MakeNicksGraph():
    ChosenGroupidx = table["MoodleId"].apply(lambda x: (x == Chosen["MoodleId"]).any(axis=0))
    NumberOfChosen = np.sum(ChosenGroupidx)
    NotChosenGroupidx = table["MoodleId"].apply(lambda x: (x == NotChosen["MoodleId"]).any(axis=0))
    NumberOfControl = np.sum(NotChosenGroupidx)
    xChosen = table.loc[ChosenGroupidx, "WeeksMedian"]
    yChosen = table.loc[ChosenGroupidx, "DaysMedian"]
    xNotChosen = table.loc[NotChosenGroupidx, "WeeksMedian"]
    yNotChosen = table.loc[NotChosenGroupidx, "DaysMedian"]
    plt.scatter(xChosen, yChosen, label="Badge Group")
    plt.scatter(xNotChosen, yNotChosen, label="Control Group")
    plt.xlabel("Consistency (Days of Work per Week) on " + object + "s")
    plt.ylabel("Intensity (edits/working day)")
    plt.title("Intensity/Consistency graph for " + object + " activity")
    plt.legend()
    plt.savefig('graphs/' + object + 'DailyActivity.png')
    plt.show()



#Make Figure 3

#MakeFigure3(DaysTable,DaysBefore, DaysAfter, "Discussion")


"""
Clearifying for myself: Figure 3 only analysis people with Badge
While Figure 4 analysis people with 1 activity or more.
"""
#MakeFigure 4
"""
PeopleWithActivity=getPeopleWithAtleastOne(data, "Post")
PeopleWithActivity1=LookForBadgeOwnersActivity(PeopleWithActivity,"Post", Newlogs)
PeopleWithActivity1.to_pickle("PeopleWithActivity1.pkl")
print("Saved!")
#PeopleWithActivity1=pd.read_pickle("PeopleWithActivity1.pkl")
MakeFigure4(PeopleWithActivity1,"Post")
"""



