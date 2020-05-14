"""
We want to compare badge group to control group:
Mean and Standard deviation of: number of discussion, comments, Total
Histogram: x axis is number of dis/com/tot, y axis is amount of people
"""
import pandas as pd
import numpy as np
import re


def MakeChosenAndNotChosen():
    UsersWithId = pd.read_csv('data/NameIdAndMoodleId.csv')
    ChosenStudent = pd.read_csv('data/ChosenStudentsWithId.csv')
    NotChosenList = ChosenList = pd.DataFrame(columns=UsersWithId.columns)
    for index, row in UsersWithId.iterrows():
        if ((row['id'] == ChosenStudent['id']).any()):
            ChosenList=ChosenList.append(row, ignore_index=True, sort=False)
        else:
            NotChosenList=NotChosenList.append(row, ignore_index=True, sort=False)

    NotChosenList.to_csv('data/NotChosenList.csv', index=False,  encoding='utf-8-sig')
    ChosenList.to_csv('data/ChosenList.csv', index=False, encoding='utf-8-sig')
MakeChosenAndNotChosen()
"""

#Make File With Student name, Id and moodle Id:
data=pd.read_csv('C:/Users/Amir/PycharmProjects/badges_moodle/data/03.05.csv')
def MakeListWithMoodleId():
    CompleteList=pd.DataFrame(columns=data.columns)
    for index, row in data.iterrows():
        if (not((row['User full name'] == CompleteList["User full name"]).any()) and (row['User full name']!="דור לוי")):
            moodle_id = re.search("The user with id '(.+?)'", row['Event name']).group(1)
            if not (moodle_id == CompleteList["Component"]).any():
                CompleteList=CompleteList.append(row,ignore_index=True, sort=False)
                CompleteList["Component"].iloc[-1]=moodle_id
        elif (row['User full name']=="דור לוי"):
            moodle_id = re.search("The user with id '(.+?)'", row['Event name']).group(1)
            if not(moodle_id==CompleteList["Component"]).any():
                CompleteList=CompleteList.append(row, ignore_index=True, sort=False)
                CompleteList["Component"].iloc[-1] = moodle_id
    CompleteList.to_csv('data/CompleteList.csv', index=False, encoding='utf-8-sig')


def MakeListWithNameIdMoodleID():
    MoodleId = pd.read_csv('data/CompleteList.csv')
    UsersID = pd.read_csv('data/NameAndId.csv')
    MoodleId = pd.read_csv('data/CompleteList.csv')
    UsersID = pd.read_csv('data/NameAndId.csv')
    UsersID["User full name"] = UsersID["First name"] + " " + UsersID["Surname"]
    NewFile = pd.merge(UsersID, MoodleId, on="User full name")
    NewFile.to_csv("data/NameIdAndMoodleId.csv", index=False, encoding='utf-8-sig')
"""
