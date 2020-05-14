import pandas as pd
import numpy as np
import re
UsersWithId = pd.read_csv('data/UsersWithId.csv')
ChosenStudentList=pd.read_csv('data/ChosenStudentsWithId.csv')
#Comments
OldFileComments=pd.read_csv('data/ChosenStudentsStatusOLD.csv')
NewFileComments=pd.read_csv('data/ChosenStudentsStatusNEW.csv')
#Views
OldFileViews=pd.read_csv('data/ChosenStudentsStatusOLD.csv')
NewFileViews=pd.read_csv('data/ChosenStudentsStatusNEW.csv')
MakeBadgesComments=pd.DataFrame(columns={'name','id','NewPosts','DiscussionBadge','Comments','CommentsBadge'})
for index, row in NewFileComments.iterrows():
    if ((row['DiscussionBadge'!=""])or (row['CommentsBadge'!=""])):
        ind = row['id'] == OldFileComments['id']
        if (ind.any()):
            if ((OldFileComments.loc[ind,'DiscussionBadge']!=row['DiscussionBadge'])or(OldFileComments.loc[ind,'CommentsBadge']!=row['CommentsBadge'])):
                MakeBadgesComments=MakeBadgesComments.append(row,ignore_index=True, sort=False)
        else:
            MakeBadges = MakeBadges.append(row, ignore_index=True, sort=False)
MakeBadgesViews=pd.DataFrame(columns={'name','id','views','badge status'})
for index, row in NewFileComments.iterrows():
    if ((row['DiscussionBadge'!=""])or (row['CommentsBadge'!=""])):
        ind = row['id'] == OldFileComments['id']
        if (ind.any()):
            if ((OldFileComments.loc[ind,'DiscussionBadge']!=row['DiscussionBadge'])or(OldFileComments.loc[ind,'CommentsBadge']!=row['CommentsBadge'])):
                MakeBadgesViews=MakeBadgesViews.append(row,ignore_index=True, sort=False)
        else:
            MakeBadgesViews = MakeBadgesViews.append(row, ignore_index=True, sort=False)

UpdateData=pd.merge(MakeBadgesComments,MakeBadgesViews,on=['name','id'],how='left')
UpdateData.to_csv('Data/UpdateBadges.csv', index=False)




