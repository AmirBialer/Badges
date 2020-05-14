import pandas as pd
import numpy as np
import re

Newlogs = pd.read_csv('../17.04_2.csv')#need to change manually!!!!!
AllData = pd.read_csv('../allCommentsData.csv')
UsersWithId = pd.read_csv('../UsersWithId.csv')
last_update = pd.read_csv('../lastUpdate_Comments.csv')
Hero = 8
Champion = 30
Guro = 50
weekNo = 'week1'#need to change menualy!!!!!
Newlogs['datetime']= pd.to_datetime(Newlogs['Time'], format="%d/%m/%y, %H:%M")

def Deletedcomments(data):
    Deletedcommentss = pd.DataFrame()
    for index, row in data.iterrows():
        if  (row['Component'] =='Post deleted'):
            CommentId = re.search('has deleted the post with id (.+?) in ', row['Event name'])
            if CommentId:
                found = CommentId.group(1)
                Deletedcommentss = Deletedcommentss.append({'CommentId': found},ignore_index=True)
    return Deletedcommentss

Deletedcomments = Deletedcomments(Newlogs)


def IsDeleted(row):
    CommentId = re.search('has created the post with id (.+?) in', row['Event name'])
    if CommentId:
        found = CommentId.group(1)
        return pd.Series(Deletedcomments['CommentId']).str.contains(found, regex=False).any()


def calculateOutput(data) : # adding 1 if the row is a Comment
    last_update_Date =pd.to_datetime(last_update.iloc[0].TimeStamp)
    for index, row in data.iterrows():
        name =  row['User full name']
        rowTime = row['datetime']
        if np.logical_and(row['Component'] =='Post created' , rowTime > last_update_Date):
        # if  (row['Component'] =='Post created'):
            if (not IsDeleted(row)):
                data.loc[index,weekNo] = 1
            else :
                data.loc[index,weekNo] = 0
        else :
            data.loc[index,weekNo] = 0
    return data.reset_index()

UpdateData = calculateOutput(Newlogs)


def Summarizer(UpdateData):
    sume = np.sum(UpdateData[weekNo])
    s2 = pd.Series(sume, name=weekNo)

    return pd.concat([s2], axis=1)

UpdateData = UpdateData.groupby('User full name').apply(lambda x: Summarizer(x)).reset_index()

UpdateData = UpdateData[UpdateData[weekNo] >0 ]
# UpdateData.to_csv('data/output_29_03_21_comments.csv')

UpdateData = UpdateData.drop(['level_1'], axis=1)

result = pd.merge(AllData, UpdateData, how='outer', on=['User full name'])

result['Sum']= result.drop(['Hero','Champion','Guro','Sum'], axis=1).sum(axis=1) #summing all weeks

def IssueBadges(result):
    IssueToUsers = pd.DataFrame()
    for index, row in result.iterrows():
        B1 = 0
        B2 = 0
        B3 = 0
        if  (np.logical_and(row['Sum'] >= Hero  , row.Hero != 1)):
            result.loc[index,'Hero'] = 1
            B1=1
        if  np.logical_and(row['Sum'] >= Champion , row.Champion != 1):
            result.loc[index,'Champion'] = 1
            B2=1
        if  np.logical_and(row['Sum'] >= Guro , row.Guro != 1):
            result.loc[index,'Guro'] = 1
            B3=1
        IssueToUsers =  IssueToUsers.append({'User full name': row['User full name'],'Hero' :B1,'Champion' :B2,'Guro' :B3}, ignore_index=True)
    return IssueToUsers

AllData = result
ToIssueToday = IssueBadges(result)

UsersWithId = UsersWithId.rename(columns={UsersWithId.columns[0]: "User full name",UsersWithId.columns[1]: "id"})
ToIssueToday = pd.merge(ToIssueToday, UsersWithId, how='left', on=['User full name'])

ToIssueToday = ToIssueToday[ToIssueToday['id'].notna()]

#updating the Last update date :
last_date = Newlogs.datetime.max()
last_date = pd.Series(last_date, name='TimeStamp')
last_date = pd.DataFrame(last_date)
last_date.to_csv('data/lastUpdate_Comments.csv', index=False)
result.to_csv('data/allCommentsData.csv', index=False)
ToIssueToday.to_csv('data/ToIssueToday_Comments.csv', index=False)
