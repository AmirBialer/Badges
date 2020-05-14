#views:
import pandas as pd
import numpy as np
import re
UsersWithId = pd.read_csv('data/UsersWithId.csv')
ChosenStudentList=pd.read_csv('data/ChosenList.csv')
Teachers = pd.read_csv('data/Teachers.csv')


Newlogs=pd.read_csv('C:/Users/Amir/PycharmProjects/My_Badges/data/13.05.csv')


def CountViewsToEachPost(data):
    PostViewCount = pd.DataFrame(columns = [ 'postID', 'count'])
    for index, row in data.iterrows():
        if (row['Component'] == 'Discussion viewed'):
            postID=re.search('discussion with id (.+?) in the forum', row['Event name']).group(1)
            if((PostViewCount['postID']==postID).any()):
                ind=np.array(PostViewCount['postID']==postID).nonzero()[0]
                PostViewCount.loc[ind,'count']+=1
            else:
                moodle_id = re.search("The user with id '(.+?)'", row['Event name']).group(1)
                PostViewCount = PostViewCount.append(pd.Series([postID,int(0)],index=PostViewCount.columns), ignore_index=True)
    return PostViewCount

def GetMaxViewsperPerson(data):
    ViewsPerPerson=pd.DataFrame(columns = ['name','id', 'views', 'badge status'])
    data["MoodleId"]=data["MoodleId"].astype(int)
    ChosenStudentList["MoodleId"]=ChosenStudentList["MoodleId"].astype(int)
    for index, row in ChosenStudentList.iterrows():
        ind=row['MoodleId']==data['MoodleId']
        if (ind.any()):
            maxViews=np.max(data.loc[ind,'count'].to_numpy())
            badge=''
            if (maxViews>250):
                badge='important'
            elif(maxViews>150):
                badge='popular'
            elif(maxViews>100):
                badge='famous'
            ViewsPerPerson=ViewsPerPerson.append(pd.Series([row['name'],row['id'],maxViews,badge],index=ViewsPerPerson.columns), ignore_index=True)
        else:
            ViewsPerPerson=ViewsPerPerson.append(pd.Series([row['name'],row['id'],0,''],index=ViewsPerPerson.columns), ignore_index=True)
    return ViewsPerPerson

OldFile=pd.read_csv('data/ViewsOfBadgeGroup.csv')
OldFile.to_csv('data/ViewsOfBadgeGroupOLD.csv', encoding='utf-8-sig')

CountViews=CountViewsToEachPost(Newlogs)
CountViewsPerPerson=GetMaxViewsperPerson(CountViews)
CountViewsPerPerson.to_csv('data/ViewsOfBadgeGroupNEW.csv',index=False, encoding='utf-8-sig')

