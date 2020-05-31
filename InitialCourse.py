import pandas as pd
import numpy as np
import pickle
import re
import math

UsersWithId = pd.read_csv('data/NameIdAndMoodleId.csv')
ChosenStudentList=pd.read_csv('data/ChosenList.csv')
Date="31.05"
Newlogs=pd.read_csv('C:/Users/Amir/PycharmProjects/My_Badges/data/'+Date+'.csv')


def LookingForMoodleId(x):
    m=re.search("The user with id '(.+?)'", x)
    if m:
        return int(m.group(1))
    else:
        return int(0)

Newlogs["MoodleId"]=Newlogs["Event name"].apply(lambda x: LookingForMoodleId(x))

def get_deleted_object(data, object):
    deleted_objects = pd.DataFrame(columns={'object_id'})
    for index, row in data.iterrows():
        if(row['Component'] == object +' deleted'):
            object_id = re.search('has deleted the '+object.lower() + ' with id (.+?) in', row['Event name'])
            if object_id:
                found = object_id.group(1)
                deleted_objects = deleted_objects.append({'object_id': found}, ignore_index=True)
    return deleted_objects


DeletedDiscussions = get_deleted_object(Newlogs, 'Discussion')
DeletedComments = get_deleted_object(Newlogs,'Post')
DeletedDiscussions.to_csv('data/DeletedPosts.csv', encoding='utf-8-sig')

def is_deleted_object(row, object):
    object_id = re.search('has created the ' + object + ' with id (.+?) in', row['Event name'])
    if object_id:
        found = object_id.group(1)
        if object == 'Post' :
            return pd.Series(DeletedComments['object_id']).str.contains(found, regex=False).any()
        else:
            return pd.Series(DeletedDiscussions['object_id']).str.contains(found, regex=False).any()


def mark_rows(data):
    Discussions=Comments=pd.DataFrame(columns=data.columns)
    PostViewCount = pd.DataFrame(columns = ['PostID', 'count'])
    for index, row in data.iterrows():
        if (row['Component'] == 'Discussion created'):
            if not is_deleted_object(row, 'Discussion'.lower()):
                moodle_id = row["MoodleId"]
                postID = re.search('discussion with id (.+?) in the forum', row['Event name']).group(1)
                Discussions=Discussions.append(row, ignore_index=True, sort=False)
                Discussions["Description"].iloc[-1]=moodle_id
                Discussions["Origin"].iloc[-1]=1
                Discussions["IP address"].iloc[-1]=postID
        elif (row['Component'] == 'Post created'):
            if not is_deleted_object(row, 'Post'.lower()):
                moodle_id = row["MoodleId"]
                Comments = Comments.append(row, ignore_index=True, sort=False)
                Comments["Description"].iloc[-1]=moodle_id
                Comments["Origin"].iloc[-1]=1

        elif (row['Component'] == 'Discussion viewed'):
            if not is_deleted_object(row, 'Discussion'.lower()):
                postID=re.search('discussion with id (.+?) in the forum', row['Event name']).group(1)
                if((PostViewCount['PostID']==postID).any()):
                    ind=np.array(PostViewCount['PostID']==postID).nonzero()[0]
                    PostViewCount.loc[ind,'count']+=1
                else:
                    PostViewCount = PostViewCount.append(pd.Series([postID,int(0)],index=PostViewCount.columns), ignore_index=True)



    return Discussions.rename(columns={"IP address": "PostID"}),Comments,PostViewCount


Discussions,Comments,PostViewCount=mark_rows(Newlogs)
Discussions.to_pickle("Discussions.pkl")
Comments.to_pickle("Comments.pkl")
PostViewCount.to_pickle("views.pkl")
#Discussions=pd.read_pickle("Discussions.pkl")
#Comments=pd.read_pickle("Comments.pkl")
#PostViewCount=pd.read_pickle("views.pkl")

def Summarizer(UpdateData):
    sume = np.sum(UpdateData['Origin'])
    s2 = pd.Series(sume, name='Origin')
    return pd.concat([s2], axis=1)

def GetDisBadges(UpdateData_discussions):
    for index, row in UpdateData_discussions.iterrows():
        if (row['NewPosts']>40):
            UpdateData_discussions.loc[index,'DiscussionBadge']='Socrates'
        elif (row['NewPosts']>20):
            UpdateData_discussions.loc[index,'DiscussionBadge']='curious'
        elif (row['NewPosts'] > 5):
            UpdateData_discussions.loc[index, 'DiscussionBadge'] = 'מעניין'
    return UpdateData_discussions

def GetComBadges(UpdateData_comments):
    for index, row in UpdateData_comments.iterrows():
        if (row['Comments']>50):
            UpdateData_comments.loc[index,'CommentsBadge']='Guro'
        elif (row['Comments']>30):
            UpdateData_comments.loc[index,'CommentsBadge']='אלוף'
        elif (row['Comments'] > 8):
            UpdateData_comments.loc[index, 'CommentsBadge'] = 'גיבור'
    return UpdateData_comments



def FinalizeFiles(data):
    AllStudents = pd.DataFrame(columns=data.columns)
    ChosenStudents =pd.DataFrame(columns=data.columns)
    for index, row in UsersWithId.iterrows():
        ind = row['MoodleId'] == data['MoodleId']
        AllStudents=AllStudents.append(data.loc[ind], ignore_index=True, sort=False)
        if((row['MoodleId'] == ChosenStudentList['MoodleId']).any()):
            ChosenStudents = ChosenStudents.append(data.loc[ind], ignore_index=True, sort=False)
        """
        else:
            AllStudents = AllStudents.append(pd.Series([row['name'],row['id'],0,'',0,''], index=data.columns), ignore_index=True, sort=False)
            if ((row['MoodleId'] == ChosenStudentList['MoodleId']).any()):
                ChosenStudents = ChosenStudents.append(pd.Series([row['name'],row['id'], 0, '', 0, ''], index=data.columns), ignore_index=True, sort=False)
        """
    return AllStudents, ChosenStudents


def MakeCommentsReport(UsersWithId):
    UpdateData_discussions = Discussions.groupby('Description').apply(lambda x: Summarizer(x)).reset_index()
    UpdateData_discussions = UpdateData_discussions.drop(['level_1'], axis=1)
    UpdateData_discussions = UpdateData_discussions.rename(columns={"User full name": "name", 'Origin': "NewPosts", "Description": "MoodleId"})
    UpdateData_discussions = GetDisBadges(UpdateData_discussions)

    UpdateData_comments = Comments.groupby('Description').apply(lambda x: Summarizer(x)).reset_index()
    UpdateData_comments = UpdateData_comments.drop(['level_1'], axis=1)
    UpdateData_comments = UpdateData_comments.rename(columns={"User full name": "name", 'Origin': "Comments", "Description": "MoodleId"})
    UpdateData_comments = GetComBadges(UpdateData_comments)
    UpdateData = pd.merge(UpdateData_discussions, UpdateData_comments, on=['MoodleId'], how='outer')
    UpdateData["NewPosts"] = UpdateData["NewPosts"].fillna(0)
    UpdateData["Comments"] = UpdateData["Comments"].fillna(0)
    UpdateData["Total"] = UpdateData["NewPosts"] + UpdateData["Comments"]
    UsersWithId["MoodleId"] = UsersWithId["MoodleId"].astype(int)
    UsersWithId = UsersWithId[["MoodleId", "id", "name"]]
    UpdateData["MoodleId"] = UpdateData["MoodleId"].astype(int)
    UpdateData_1 = pd.merge(UpdateData, UsersWithId, on=['MoodleId'], how='outer')
    AllStudents, ChosenStudents = FinalizeFiles(UpdateData_1)

    # updating the Last update date-Comments :
    OldFile = pd.read_csv('data/ChosenStudentsStatus.csv')
    OldFile.to_csv('data/ChosenStudentsStatusOLD.csv', index=False, encoding='utf-8-sig')

    AllStudents = AllStudents[["MoodleId", "id", "name", "NewPosts", "Comments", "Total", "DiscussionBadge", "CommentsBadge"]]
    AllStudents.to_csv('data/allStudentsStatus.csv', index=False, encoding='utf-8-sig')
    ChosenStudents = ChosenStudents[["id", "name", "NewPosts", "DiscussionBadge", "Comments", "CommentsBadge"]]
    ChosenStudents.to_csv('data/ChosenStudentsStatusNEW.csv', index=False, encoding='utf-8-sig')

MakeCommentsReport(UsersWithId)



def MatchPostToPerson(data,Discussions):
    for index, row in data.iterrows():
        idx=row["PostID"]==Discussions["PostID"]
        if (idx.any()):
            data.at[index, "name"]=Discussions.loc[idx, "User full name"].values[0]
            b=Discussions.loc[idx,"Description"].values[0]
            if (pd.isna(b)):
                data.at[index,"MoodleId"]=int(0)
            else:
                data.at[index, "MoodleId"] = int(b)
    return data


def GetMaxViewsperPerson(data):
    ViewsPerPerson=pd.DataFrame(columns = ['name','id', 'views', 'badge status'])
    data["MoodleId"]=data["MoodleId"].astype('Int64')
    ChosenStudentList["MoodleId"]=ChosenStudentList["MoodleId"].astype(int)
    for index, row in ChosenStudentList.iterrows():
        ind=row['MoodleId']==data['MoodleId']
        if (ind.any()):
            maxViews=np.max(data.loc[ind,'count'].to_numpy())
            badge=''
            if (maxViews>250):
                badge='important'
            elif(maxViews>150):
                badge='הודעה פופולרית'
            elif(maxViews>100):
                badge='הודעה חשובה'
            ViewsPerPerson=ViewsPerPerson.append(pd.Series([row['name'],row['id'],maxViews,badge],index=ViewsPerPerson.columns), ignore_index=True)
        else:
            ViewsPerPerson=ViewsPerPerson.append(pd.Series([row['name'],row['id'],0,''],index=ViewsPerPerson.columns), ignore_index=True)
    return ViewsPerPerson




def MakeViewsReport():
    OldFile=pd.read_csv('data/ViewsOfBadgeGroup.csv')
    OldFile.to_csv('data/ViewsOfBadgeGroupOLD.csv', encoding='utf-8-sig')
    CountViewsWithPostOwners=MatchPostToPerson(PostViewCount,Discussions)
    CountViewsWithPostOwners.to_pickle('CountViewsWithPostOwners.pkl')
    CountViewsPerPerson=GetMaxViewsperPerson(CountViewsWithPostOwners)
    CountViewsPerPerson.to_csv('data/ViewsOfBadgeGroupNEW.csv',index=False, encoding='utf-8-sig')
# Viewscount
MakeViewsReport()


def FindPopularViewsLink(PostViewCount, NumberFfPosts):
    print(PostViewCount.sort_values(["count"], ascending=False).head(NumberFfPosts))

FindPopularViewsLink(PostViewCount,10)