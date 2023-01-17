#import all needed packages.
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

#change to the directory
os.chdir("D:\python 文件")

#import the file
covid_data=pd.read_csv("full_data.csv")

#show all columns.
print(covid_data.info())

#show every second row between 0 and 10
print(covid_data.iloc[0:11:2,:])

#use a Boolean to show "total_cases" for all rows corresponding to Afghanistan
def x(country):
    my_columns = []
    for i in covid_data.iloc[:,1]:
        if i== country:
            a=True
        else:
            a=False
        my_columns.append(a)
    return my_columns
print(covid_data.loc[x("Afghanistan"),"total_cases"])

#compute the mean and median of new cases for the entire word
world_new_cases= covid_data.loc[x("World"),"new_cases"]
mean=np.mean(world_new_cases)
median=np.median(world_new_cases)
print("mean=",mean)
print("median=", median)

#creat a boxplot of new cases worldwide.
plt.boxplot(world_new_cases,whis=1.5,patch_artist=True,meanline=True)
plt.title("new cases worldwide")
plt.show()

#plot both new cases and new deaths worldwide
world_dates=covid_data.loc[x("World"),"date"]
world_new_deaths=covid_data.loc[x("World"),"new_deaths"]
plt.figure(1)
plt.plot(world_dates,world_new_cases,label="new_cases")
plt.figure(1)
plt.plot(world_dates,world_new_deaths,label="new_deaths")
plt.xticks(world_dates.iloc[0:len(world_dates):4],rotation=-90)
plt.legend()
plt.show()

#pursue a question that interests me.(the question is in File question.txt)
conlumns=[]
n=0
for y in covid_data.loc[:,"date"]:
    if y == "2020-03-31":
        conlumns.append(True)
    else:
        conlumns.append(False)
p_list_bool=list(covid_data.loc[conlumns,"total_cases"])
country_list=list(covid_data.loc[conlumns,"location"])
dictionary= dict(zip(country_list,p_list_bool))

for item in dictionary:
    if dictionary[item]<=10:
        print(item)
        n+=1
    else:
        continue
print("The number of countries is",n)





