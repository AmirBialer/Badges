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

grades2=grades.set_index("ID")