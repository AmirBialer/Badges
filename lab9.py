import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold

#Read File
df=pd.read_csv("C:/Users/Amir/Desktop/Studying/BI/lab9/train_Loan.csv")
#Fill na
df = df.fillna(df.mode().iloc[0])


#Change categorial to numeric
var_mod=["Gender", "Married", "Dependents", "Education", "Self_Employed", "Property_Area", "Loan_Status"]
x=var_mod[0:6]
y=var_mod[6]
le=LabelEncoder()
for i in var_mod:
    df[i]=le.fit_transform(df[i])

#Train
kf=KFold(n_splits=10)
model=RandomForestClassifier()
accuracy=[]
for train,test in kf.split(df):
    # split data and labels:
    data_x = df[x].iloc[train,:]
    data_y=df[y].iloc[train]
    model.fit(data_x,data_y)
    accuracy.append(model.score(df[x].iloc[test],df[y].iloc[test]))

print("cv accuracy: ", np.mean(accuracy))
model.fit(df[x],df[y])
#67%
print("train accuracy: ",model.score(df[x],df[y]))
#75%