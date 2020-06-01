import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import math
import pickle
import datetime
from datetime import date
#time:
TodaysDate = date.today()
TodaysDayNumber=TodaysDate.timetuple().tm_yday
TodaysWeek=TodaysDate.isocalendar()[1]
StartDay=date(2020, 3, 8)
midtermDate=date(2020,5,15)
midtermDay=(midtermDate-StartDay).days
StartDayNumber=StartDay.timetuple().tm_yday
StartWeek=StartDay.isocalendar()[1]
NumberOfDays=1+(TodaysDate - StartDay).days

#reading:
UsersWithId = pd.read_csv('data/NameIdAndMoodleId.csv')
Chosen=pd.read_csv('data/ChosenList.csv')
NotChosen=pd.read_csv('data/NotChosenList.csv')
Newlogs=pd.read_csv('C:/Users/Amir/PycharmProjects/My_Badges/data/27.05.csv')# change everytime
Newlogs['Time'] = pd.to_datetime(Newlogs['Time'], format="%d/%m/%y, %H:%M")
data=pd.read_csv('data/allStudentsStatus.csv')
grades=pd.read_csv("data/midterm.csv")
data["NewPosts"]=pd.to_numeric(data["NewPosts"], downcast="float")
data["Comments"]=pd.to_numeric(data["Comments"], downcast="float")
Date="31.05"
Newlogs=pd.read_csv('C:/Users/Amir/PycharmProjects/My_Badges/data/'+Date+'.csv')

def LookingForMoodleId(x):
    m=re.search("The user with id '(.+?)'", x)
    if m:
        return int(m.group(1))
    else:
        return int(0)


Newlogs["MoodleId"]=Newlogs["Event name"].apply(lambda x: LookingForMoodleId(x))
a=pd.DataFrame(Newlogs.groupby("MoodleId").count()["Time"])
UsersWithId["AllRows"]=0
UsersWithId["Views"]=0
UsersWithId["ZoomViews"]=0
UsersWithId["KobiViews"]=0

UsersWithId=UsersWithId.set_index("MoodleId")
#AllRows
UsersWithId.loc[UsersWithId.index,"AllRows"]=a.loc[UsersWithId.index,"Time"]
#allViews
Newlogs["Count"]=Newlogs["Component"].str.contains("view")
d=pd.DataFrame(Newlogs.groupby("MoodleId")["Count"].apply(lambda x: np.sum(x)))
UsersWithId.loc[UsersWithId.index,"Views"]=d.loc[UsersWithId.index,"Count"]
#AllZoom
Newlogs["Count"]=Newlogs["Affected user"].str.contains("ZOOM")
d=pd.DataFrame(Newlogs.groupby("MoodleId")["Count"].apply(lambda x: np.sum(x)))
UsersWithId.loc[UsersWithId.index,"ZoomViews"]=d.loc[UsersWithId.index,"Count"]
UsersWithId.to_csv("data/CountedActivity.csv",index=False, encoding='utf-8-sig')
#KobiLectures2017
Newlogs["Count"]=Newlogs["Affected user"].str.contains("2017")
d=pd.DataFrame(Newlogs.groupby("MoodleId")["Count"].apply(lambda x: np.sum(x)))
UsersWithId.loc[UsersWithId.index,"KobiViews"]=d.loc[UsersWithId.index,"Count"]
UsersWithId.to_csv("data/CountedActivity.csv",index=False, encoding='utf-8-sig')








