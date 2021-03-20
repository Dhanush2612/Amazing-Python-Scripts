# -*- coding: utf-8 -*-
"""Titanic.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EWpqk4k8XDOg29c5aEWUYedN-daw2ENm

# Importing Modules
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings(action='ignore')

"""## Loading Dataset"""

df = pd.read_csv('./Titanic Survival Prediction/Dataset/train.csv')
df.head()

len(df)

df.shape

"""# Cleaning of Raw Data

### Checking Null Values
"""

df.isnull().sum()

"""* As the total 891 rows , In 'Cabin' there are more than 70% data is missing , so it is irrelevant to fill it 

* Now, dropping Cabin column
"""

df.pop('Cabin')

df['Age'].plot.hist()

"""* as Curve is Bell Shaped , so fill the missing values by Mean"""

df['Age'].fillna(df['Age'].mean(), inplace= True)

"""* Embarked column is categorical so calculating the mode and filling it """

df["Embarked"].value_counts()

"""* We observe that max people are from S-southampton so we fill all with S"""

df["Embarked"].fillna(value='S',inplace=True)

"""* Now checking missing values"""

df.isnull().sum()

"""* All missing values are filled now ,

## Droping Irrelevent columns

* As the name column contain different name and the survival is not relevant to names
* passenger Id does not make any sense
"""

df.drop(['PassengerId','Name'], axis=1, inplace=True)

df.head()

"""* Ticket number doesnt provide any relevant information whether they survived or not so drop it"""

df.pop('Ticket')

"""* now data only conatin relevant columns"""

df.info()

"""* lets change all text to numeric using dummy and label encoding"""

gender=pd.get_dummies(df["Sex"], drop_first=True)
gender.head()

"""* Label Encoding it encode the value as per given instance
- Eg- columns has 3 category C/S/Q--it will form label
    suppose 0-C, 1-S, 2-Q
"""

from sklearn.preprocessing import LabelEncoder
lab = LabelEncoder()
df["Embarked"] = lab.fit_transform(df["Embarked"])
df["Embarked"].head(10)

"""* Concatinating Sex column to original dataframe """

df = pd.concat((df,gender),axis=1)
df = df.drop(["Sex"],axis=1)

df.info()

"""### Features: The titanic dataset has roughly the following types of features:

* Categorical/Nominal: Variables that can be divided into multiple categories but having no order or priority.
Eg. Embarked (C = Cherbourg; Q = Queenstown; S = Southampton)
* Binary: A subtype of categorical features, where the variable has only two categories.
Eg: Sex (Male/Female)
* Ordinal: They are similar to categorical features but they have an order(i.e can be sorted).
Eg. Pclass (1, 2, 3)
* Continuous: They can take up any value between the minimum and maximum values in a column.
Eg. Age, Fare
* Count: They represent the count of a variable.
Eg. SibSp, Parch

Useless: They don’t contribute to the final outcome of an ML model. Here, PassengerId, Name, Cabin and Ticket might fall into this category.

# EDA

* I am prefering Raw Data for EDA : (not cleaned data)
"""

# sns.catplot(x ="male", hue ="Survived", 
# kind ="count", data = df)

""" Raw Data """

eda =  pd.read_csv('./Titanic Survival Prediction/Dataset/train.csv')

eda.head()

sns.catplot(x ="Sex", hue ="Survived", kind ="count", data = eda)

"""* Just by observing the graph, it can be approximated that the survival rate of men is around 20% and that of women is around 75%. Therefore, whether a passenger is a male or a female plays an important role in determining if one is going to survive."""

# Group the dataset by Pclass and Survived and then unstack them 

group = eda.groupby(['Pclass', 'Survived']) 
pclass_survived = group.size().unstack() 

# Heatmap - Color encoded 2D representation of data. 

sns.heatmap(pclass_survived, annot = True, fmt ="d")

"""It helps in determining if higher-class passengers had more survival rate than the lower class ones or vice versa. Class 1 passengers have a higher survival chance compared to classes 2 and 3. It implies that Pclass contributes a lot to a passenger’s survival rate."""

# Adding a column Family_Size 

eda['Family_Size'] = 0
eda['Family_Size'] = eda['Parch'] + eda['SibSp'] 

# Adding a column Alone 

eda['Alone'] = 0
eda.loc[eda.Family_Size == 0, 'Alone'] = 1

# Factorplot for Family_Size 

sns.factorplot(x ='Family_Size', y ='Survived', data =eda) 

# Factorplot for Alone 

sns.factorplot(x ='Alone', y ='Survived', data = eda)

"""Family_Size denotes the number of people in a passenger’s family. It is calculated by summing the SibSp and Parch columns of a respective passenger. Also, another column Alone is added to check the chances of survival of a lone passenger against the one with a family.

Important observations –

If a passenger is alone, the survival rate is less.
If the family size is greater than 5, chances of survival decreases considerably.
"""

# Divide Fare into 4 bins 
eda['Fare_Range'] = pd.qcut(eda['Fare'], 4) 

# Barplot - Shows approximate values based 
# on the height of bars. 
sns.barplot(x ='Fare_Range', y ='Survived', 
data =eda)

"""Fare denotes the fare paid by a passenger. As the values in this column are continuous, they need to be put in separate bins(as done for Age feature) to get a clear idea. It can be concluded that if a passenger paid a higher fare, the survival rate is more.

"""

sns.catplot(x ='Embarked', hue ='Survived', 
kind ='count', col ='Pclass', data =eda)

"""## Spliting Data into Dependent Variable and Independent variable"""

y = df["Survived"]
X = df.drop(["Survived"],axis=1)

X.head()

y.head()

"""# Train the model using Logistic Regression"""

model=LogisticRegression()

model.fit(X,y)

"""## Using Test Data"""

test_data = np.load('./Titanic Survival Prediction/Dataset/test.csv')

test_data.head()

"""## Cleaning test data"""

test_data.isnull().sum()

test_data.drop(['Name','PassengerId','Ticket'],axis=1, inplace=True)

test_data.head()

test_data.drop(['Cabin'], axis=1, inplace=True)

test_data

test_data['Age'].fillna(test_data['Age'].mean(), inplace=True)

test_data['Fare'].fillna(test_data['Fare'].mean(),inplace=True)

test_data.isnull().sum()

le = LabelEncoder()
test_data["Embarked"]=le.fit_transform(test_data["Embarked"])

gender = pd.get_dummies(test_data["Sex"],drop_first=True)
gender.head()

test_data=pd.concat((test_data,gender),axis=1)
test_data=test_data.drop(["Sex"],axis=1)

test_data

"""## Prediction"""

from sklearn.linear_model import LogisticRegression
import pickle
model = LogisticRegression()
model.fit(xtrain, ytrain)
# save the model to disk
pickle.dump(model, open(model_file_path, 'wb'))

model = pickle.load(open(model_file_path, 'rb'))
y_pred = model.predict(test_data)

y_pred

len(y_pred)

#print("Accuracy of model is :",accuracy_score(ytest,y_pred))

#print(classification_report(ytest, y_pred))

#print(confusion_matrix(ytest,y_pred))

test = pd.read_csv('./Titanic Survival Prediction/Dataset/test.csv')

test.head()

pred = pd.DataFrame(y_pred, columns=['predictions'])
pred.head()

data = [test["PassengerId"], pred["predictions"]]
headers = ["PassengerId", "Survived"]
final_data = pd.concat(data, axis=1, keys=headers)

final_data

final_data.to_csv("./Titanic Survival Prediction/Dataset/titanic_pred.csv",index=False)