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
ChosenStudentList=pd.read_csv('data/ChosenList.csv')
data=pd.read_csv('data/allStudentsStatus.csv')
grades=pd.read_csv("data/midterm.csv")
data["NewPosts"]=pd.to_numeric(data["NewPosts"], downcast="float")
data["Comments"]=pd.to_numeric(data["Comments"], downcast="float")
Date="31.05"
Newlogs=pd.read_csv('C:/Users/Amir/PycharmProjects/My_Badges/data/'+Date+'.csv')
CountViewsPerPerson=pd.read_csv('data/ViewsOfBadgeGroupNEW.csv')
PostViewCount=pd.read_pickle("views.pkl")
CountViewsWithPostOwners=pd.read_pickle("CountViewsWithPostOwners.pkl")

def GetMaxViewsperPerson(data):
    ViewsPerPerson=pd.DataFrame(columns = ['name','id', 'views', 'badge status', "postID"])
    data["MoodleId"]=data["MoodleId"].astype('Int64')
    ChosenStudentList["MoodleId"]=ChosenStudentList["MoodleId"].astype(int)
    for index, row in ChosenStudentList.iterrows():
        ind=row['MoodleId']==data['MoodleId']
        PostID=""
        if (ind.any()):
            maxViews=np.max(data.loc[ind,'count'].to_numpy())
            maxIndex=np.where(data.loc[ind,'count'].to_numpy()==maxViews)[0]
            PostID=data.loc[maxIndex,"PostID"].values[0]
            PostID=PostID[1:len(PostID)-1]
            badge=''
            if (maxViews>250):
                badge='important'
            elif(maxViews>150):
                badge='הודעה פופולרית'
            elif(maxViews>100):
                badge='הודעה חשובה'
            ViewsPerPerson=ViewsPerPerson.append(pd.Series([row['name'],row['id'],maxViews,badge,PostID],index=ViewsPerPerson.columns), ignore_index=True)
        else:
            ViewsPerPerson=ViewsPerPerson.append(pd.Series([row['name'],row['id'],0,'',PostID],index=ViewsPerPerson.columns), ignore_index=True)
    return ViewsPerPerson

CountViewsPerPerson=GetMaxViewsperPerson(CountViewsWithPostOwners)
CountViewsPerPerson["MessageLink"]=""
for index, row in CountViewsPerPerson.iterrows():
    if (row["postID"]!=""):
        CountViewsPerPerson.loc[index,"MessageLink"]="https://moodle2.bgu.ac.il/moodle/mod/forum/discuss.php?d="+str(CountViewsPerPerson.loc[index,"postID"])
CountViewsPerPerson.to_csv('data/ViewsOfBadgeGroupNEW1.csv',index=False, encoding='utf-8-sig')
