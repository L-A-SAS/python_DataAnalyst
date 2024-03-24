# Project 3 - Lee Saar
# Table of contents:
# Part 1: Are trees in need of a good night sleep?
    # imports
    # load data set & configurate 
    # dataset information & statistics
    # A. Establish a normal stomal conductance behivor 
    # B. Establish human behivor- population/gas emmessions/light pulotion
    # C. Conclusion 
    # biographys
# Part 2: Diamonds dataset


# imports
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import pandasql as psql
import seaborn as sb
import xlrd as xl
import openpyxl
import pyodbc as pyb
from matplotlib import pyplot
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
from random import randint
import numpy
from IPython.display import display


# load data set & configurate 
# import the csv to a df & delete all commas from numbers and rename columms with many 

# *****************change the path *****************
# the first data set is per city 
df=pd.read_csv("C:\\Users\\Lisaa\\python\\datasets\\co2_light_botanic.csv", thousands=',')
# the secound dataset has info on the countries
dfCountry=pd.read_csv("C:\\Users\\Lisaa\\python\\datasets\\country_co2.csv", thousands=',')
# change columns names to shorter names


print('Part 1: Does Light polution affect Stomatal Conductance in trees and are there \n fluctations in the tree\'s behivor corilating to the disturbences? \n')
print('I would like to analyze if trees need to "sleep" properly in order')
print('to function at their best as "air cleaners". \n ')

print('The potential impact of light pollution on air quality is complex and depends on ')
print('various factors, including tree species, canopy cover, local weather patterns, ')
print('and existing air pollution sources, the question has been confirmed ')
print('in diffrent researches- light has been used to control plants for industry ')
print('of flowers the the polution of intense indusries is known.\n')

# count countries in df
dfCountryUniq=dfCountry.Country_Name.nunique()

print('***Dataset information:***')
print('   The dataset is divided by',dfCountryUniq,'countries, it has information about')
print('   population, big factories, air pollution, light pollution, ')
print('   forestry cover, stomatal conductance processes and the variables that affect ')
print('   them as night tempeture humedity and common tree species. \n')
print('   There are many reaserches and databaises for the subjects but not one combiened,')
print('   due to the time frame I used AI to extract the data in to one table I have designed')


print('   Additional information about the dataset:')
print('   1. Stomatal Conductance-Trees have tiny pores on their leaves called stomata. ')
print('      These stomata act as gateways for gas exchange, allowing trees to take in CO2 ')
print('      from the atmosphere during photosynthesis (mmol CO2 m^-2 s^-1). \n')
print('      According to common stoma messuring system the scale is 0-4.')
print('   2. The count for popolation, CO2 emmisions & GHG emmissions is in Millions \n ')
print('   3. Light pollution is measured in LUX, with higher values indicating greater intensity.')
print('      the diffrances between city and roral area are significant.')

# df statistics of pupulation, lux and emmissions
dfStats=pd.DataFrame(dfCountry[['Country_Name','Population','Major_city_LUX','Rural_LUX','CO2Emissions']])
dfStats1=pd.DataFrame(df[['Other_GHGs']])
dfStats=dfStats.join(dfStats1)
display(round(dfStats.describe()))


print('   4. The data in the Forest Cover column refers to the percentage of the total land ')
print('      area within the city or location that is covered by tree canopy. ')
print('      This doesn\'t necessarily imply continuous forest but rather the cumulative tree ')
print('      canopy coverage across the designated area. \n')


# give each country a color for easy navigation in graphs
# automate color asign for each country
# empty list of colors
color=[]
# save the number of unique countries
nCountries=dfCountry.Country_Name.nunique()  
# asign a color for each country by geneating a random number with RGB string- i found it on pandas documentetions 
for i in range(nCountries):
    color.append('#%06X' % randint(0, 0xFFFFFF))
# save a df colors and countries
dfC=pd.DataFrame({'Country_Name': dfCountry.Country_Name.unique(), 'Color': color})
# merge the color df to the main df- 
# df=pd.merge(df, dfC, on='Country_Name', how='outer')
# the merge works but when i try to call the color from the df table it doesnt work good so i will use the dfc


# A. Establish a normal stomal conductance behivor 
# First I wish to check the relations between Forest Cover and Stomatal Conductance and create a base line.
print('Part A. locate a representative groug of stomatal conductance \n')
print('Shown in 2 pie charts: \n The relations between Stomatal Conductance and Forest Cover. \n       1. The Forest Cover has some corilation to the  Stomatal Conductance pie but not definete. \n ')


# 1
# stomatal conductance top 12
pyplot.figure(figsize=(20,10))
pyplot.subplot(1,2,1)
# group by country and mean the total stomatal conductance
df1=dfCountry.groupby(by='Country_Name')['Stomatal_Conductance'].agg(['mean'])
# sort values in df and get first 12
df1=df1.sort_values("mean", ascending=False).head(12)
# add the labels to a list 
labels1=df1.index.to_list()
# 1st pie chart
dfPar1=pyplot.pie(data=df1,x="mean",autopct='%.1f%%',pctdistance=.8, labeldistance=1.04,labels=labels1,colors=df1.index.map(dfC.set_index('Country_Name')['Color']))
# pie chart title
pyplot.title('\n                                                                1.\n Stomatal Conductance - Top 12',fontsize=28)

# Forest_Cover top 12 plot- same as above
pyplot.subplot(1,2,2)
df2=dfCountry.groupby(by='Country_Name')['Forest_Cover'].agg(['mean'])
df2=df2.sort_values("mean", ascending=False).head(12)
labels2=df2.index.to_list()
dfPar2=pyplot.pie(data=df2,x="mean",autopct='%.1f%%',pctdistance=.8,labeldistance=1.04,\
                  labels=labels2,colors=df2.index.map(dfC.set_index('Country_Name')['Color']))
pyplot.title('\n \n Forest Cover % - Top 12',fontsize=28)
pyplot.show()
print('To my knowledge the exceptions that are shown in the graphs \n Japan, South Korea, Finland, Norway represents regions \n with type of flora of Pinaceae (Pine Family) or Cupressaceae \n that have small surfece area leafs as a mechanizem to handle \n the cold temp & cloudy weather, \n')


#2
# latitude & avg tempetures
# show the lattitude, no time to get a map, in the bar plot it works ok with 2 y axes, 
# i tried a loop to asign negative values to south but it did not work proprly.
fig, ax = pyplot.subplots(figsize=(20,10)) 
dfmap = dfCountry[["Country_Name", "Latitude_Lines1", "Latitude_Lines11", "Latitude_Lines2",\
                    "Latitude_Lines21", 'Stomatal_Conductance']].sort_values(['Stomatal_Conductance'], ascending=False)
latHigh=dfmap.head(10)
latLow=dfmap.tail(10)
dfMapLat= pd.concat([latHigh, latLow], axis=0)
dfMapLat.plot(x = 'Country_Name', y = 'Latitude_Lines1', ax = ax, kind="bar",alpha=.3) 
dfMapLat.plot(x = 'Country_Name', y = 'Latitude_Lines2', ax = ax, secondary_y = True,kind="bar",
              stacked=True,rot=-55,fontsize=13,alpha=.3,color='k')
pyplot.xlabel('Country_Name',fontsize=28)
pyplot.ylabel('',rotation=0,fontsize=28)
pyplot.title('\n. 2 \n Countries latitude lines & Stomatal conductance \n              high & low Stomatal conductance \n \n Top 15 & Tail 15 \n ',fontsize=26)
pyplot.grid(True)
print('\n 2. Below Latitude lines show that the forest cover in countries with grater distance from the equateal line \n have less stamatal conductance.')
print('On the right')
print('\n',latLow.Country_Name.sort_values().unique(),'\n are in a grater distance from the equatial or have low precipitation/rainfall ')
print('\n On the left')
print( latHigh.Country_Name.sort_values().unique(),' \n that have high stoma conductance and are all have equetial latitude ')
pyplot.show()


# 3
print('\n3. Next it is shown that the forest cover in cold tempetures yield less \n       then subtropical forests with broad leaves\n ')
pyplot.figure(figsize=(20,10))
# new df
df3=dfCountry[["Country_Name","Nighttime_Temp","Stomatal_Conductance"]].sort_values('Nighttime_Temp', ascending=False)
df31=df3.head(15)
df32=df3.tail(15)
# combin df tail and head
df3= pd.concat([df31, df32], axis=0)
# heatmap
nightTemp = pd.pivot(data=df3,index="Country_Name", columns="Stomatal_Conductance", values="Nighttime_Temp")
sb.heatmap(nightTemp, annot=True)
# style
pyplot.title('\n. 3 \n Nighttime Temp vs Stomatal Conductance \n  AVG coldest & hotest nights \n              \n Top 15 & Tail 15 \n ',fontsize=26)
pyplot.tick_params(axis='x', which='major', size=18)
pyplot.tick_params(axis='y', which='major', size=18)
pyplot.xlabel('Stomatal_Conductance',fontsize=18)
pyplot.ylabel('')
pyplot.grid(True)
pyplot.show()

#4
# botanic family
# check for the exceptions in botanic family
# 3th barplot- botanic tree family/stomal conductance
print('\n 4. Botanic family Stomatal conductance')
pyplot.figure(figsize=(25,135))
pyplot.subplot(7,1,1)
df42=sb.pointplot(x='Stomatal_Conductance',y='Botanic_Family',hue='Botanic_Family',data=dfCountry,linewidth=5.5)
pyplot.title('\n 4. \n Botanic Family Stomatal Conductance \n',fontsize=28)
pyplot.xlabel('Stomatal Conductance \n',fontsize=26)
pyplot.ylabel('')
pyplot.legend(prop={'size': 18},title='Botanic Family',title_fontsize='xx-large',              loc='upper left', bbox_to_anchor=(1, 1))
pyplot.grid(True)
# Set font size for xtick labels to 14
pyplot.tick_params(axis='x', which='major', labelsize=16)
pyplot.tick_params(axis='y', which='major', labelsize=16)
pyplot.show()


# part A. conclusion, save a representative group
dfRepHighStom=psql.sqldf("select * from dfCountry where Stomatal_Conductance>=3 and Nighttime_Temp>=20  and Latitude_Lines1<=15 and Latitude_Lines2<=20;",globals())
dfRep=dfRepHighStom[['Country_Name','Stomatal_Conductance','Botanic_Family','Forest_Cover', 'Nighttime_Temp','Nighttime_Humid']]
print('accounding to the theory diveloped above I have cleand the data \n to get a representative group of',dfRep.Country_Name.nunique(),' countries \n with high stomal proceses, high night temp and equatial lines.')
display(round(dfRep.describe()))



# 5
# B. establish human behivor in the representative countries- population/gas emmessions/co2 emissions/factories
print('\n B. This part will focus on the human variables in the representative countries ')
print('      The population, Lux, factories, CO2 emissions & other gases are higher with population')
# 4th barplot -population, factories, CO2 emissions & other gases
pyplot.figure(figsize=(20,10))
df5=dfRepHighStom[['Country_Name','Population','Major_city_LUX']]
df5=pd.DataFrame({'Country_Name': df5.Country_Name, 'Population': df5.Population,'Major_city_LUX': df5.Major_city_LUX})
df5=df5.sort_values('Major_city_LUX',ascending=False)
df5=sb.barplot(data=df5,x='Major_city_LUX',y='Country_Name',hue='Population')
#add the 1st plot labels and title
pyplot.xlabel('LUX',fontsize=18)
pyplot.ylabel('')
sb.set_style('darkgrid')
pyplot.title('\n 5. \n Population & Light Pollution-Major CityLUX \n Top 20 \n',fontsize=26)
pyplot.legend(prop={'size': 18},title='Population',title_fontsize='xx-large',loc=4)
pyplot.show()

# 6
print('Above are the representative stoma countries with Major city light pulotion \n Below are the representative stoma countries with Rural light polution \n There are 3 corilation representative groups in both and \n I have divieded the Stoma group to 3 Lux . ')
print(' The 3 Lux groups are called: High Lux, Medium Lux and Low Lux.')
# 4th barplot -population, factories, CO2 emissions & other gases
pyplot.figure(figsize=(20,10))
df6=dfRepHighStom[['Country_Name','Population','Rural_LUX']]
df6=pd.DataFrame({'Country_Name': df6.Country_Name, 'Population': df6.Population,'Rural_LUX': df6.Rural_LUX})
df6=df6.sort_values('Rural_LUX',ascending=False)
df6=sb.barplot(data=df6,x='Rural_LUX',y='Country_Name',hue='Population')
#add the 1st plot labels and title
pyplot.xlabel('LUX',fontsize=18)
pyplot.ylabel('')
sb.set_style('darkgrid')
pyplot.title('\n 6. \n Population & Light Pollution-Rural LUX \n Top 20 \n',fontsize=26)
pyplot.legend(prop={'size': 18},title='Population',title_fontsize='xx-large',loc=4)
pyplot.show()


# 7
# factories &  CO2Emissions
print('The 3 Lux Stoma representative groups with the variables: Factories, Co2 Emissions, Population & Area.')
print(' There is corelation between the the Lux, Factories, Co2 Emissions, Population & Area.')
print(' Yet in the 3 Lux groups there are sub groups that corelate even better.')

dfRepHighStomLUX=psql.sqldf("select * from dfRepHighStom;",globals())

# change the factories str values to int
def func(x):
    if x=="Very High":
        return 10000
    if x=="High":
        return 5000
    if x=="Medium":
        return 1000
    else :
        return 100
dfRepHighStomLUX['Factories']=dfRepHighStomLUX['Factories'].apply(func)

# divide the rep group to 3 groups of lux 
dfRepLuxHigh=psql.sqldf("select * from dfRepHighStomLUX where Major_city_LUX>=21;",globals())
dfRepLuxMed=psql.sqldf("select * from dfRepHighStomLUX where Major_city_LUX>=16 and Major_city_LUX<=20;",globals())
dfRepLuxLow=psql.sqldf("select * from dfRepHighStomLUX where Major_city_LUX<=15;",globals())


# factories
pyplot.figure(figsize=(20,10))
pyplot.subplot(2,2,1)
df8=psql.sqldf("select Country_Name,Factories,Population,Major_city_LUX from dfRepLuxHigh;",globals())
df8=pd.DataFrame({'Country_Name': df8.Country_Name, 'Population': df8.Population, 'Factories':df8.Factories,'Major_city_LUX':df8.Major_city_LUX})
df8=df8.sort_values('Factories', ascending=False).head(10)
df8=sb.histplot(data=df8, x='Country_Name', y='Factories',hue='Major_city_LUX') 
pyplot.title('\n                                                              7. \n                                                            Factories in the 3 Stoma LUX representative groups \n',fontsize=26)
pyplot.ylabel('Factories                  \n High Lux                   ', fontsize=18, rotation=0)

pyplot.subplot(2,2,2)
df9=psql.sqldf("select Country_Name,Factories,Population,Major_city_LUX from dfRepLuxMed;",globals())
df9=pd.DataFrame({'Country_Name': df9.Country_Name, 'Population': df9.Population, 'Factories':df9.Factories,'Major_city_LUX':df9.Major_city_LUX})
df9=df9.sort_values('Factories', ascending=False).head(10)
df9=sb.histplot(data=df9, x='Country_Name', y='Factories',hue='Major_city_LUX') 
pyplot.ylabel('')

pyplot.subplot(2,2,3)
df10=psql.sqldf("select Country_Name,Factories,Population,Major_city_LUX from dfRepLuxLow;",globals())
df10=pd.DataFrame({'Country_Name': df10.Country_Name, 'Population': df10.Population, 'Factories':df10.Factories,'Major_city_LUX':df10.Major_city_LUX})
df10=df10.sort_values('Factories', ascending=False).head(10)
df10=sb.barplot(data=df10, x='Country_Name', y='Factories',hue='Major_city_LUX') 
pyplot.ylabel('Factories                  \n Low Lux                   ', fontsize=18, rotation=0)
pyplot.show()


#8
# CO2Emissions
pyplot.figure(figsize=(20,10))
pyplot.subplot(2,2,1)
df8=psql.sqldf("select Country_Name,CO2Emissions,Population,Major_city_LUX from dfRepLuxHigh;",globals())
df8=pd.DataFrame({'Country_Name': df8.Country_Name, 'Population': df8.Population, 'CO2Emissions':df8.CO2Emissions,'Major_city_LUX':df8.Major_city_LUX})
df8=df8.sort_values('CO2Emissions', ascending=False).head(10)
df8=sb.histplot(data=df8, x='Country_Name', y='CO2Emissions',hue='Major_city_LUX') 
pyplot.title('\n                                                              8. \n                                                            CO2Emissions(million tons) in the 3 Stoma LUX representative groups \n ',fontsize=26)
pyplot.ylabel('CO2 Emissions                      \n High Lux                    ', fontsize=18, rotation=0)

pyplot.subplot(2,2,2)
df8=psql.sqldf("select Country_Name,CO2Emissions,Population,Major_city_LUX from dfRepLuxMed;",globals())
df8=pd.DataFrame({'Country_Name': df8.Country_Name, 'Population': df8.Population, 'CO2Emissions':df8.CO2Emissions,'Major_city_LUX':df8.Major_city_LUX})
df8=df8.sort_values('CO2Emissions', ascending=False).head(10)
df8=sb.histplot(data=df8, x='Country_Name', y='CO2Emissions',hue='Major_city_LUX') 
pyplot.ylabel('', fontsize=18, rotation=0)

pyplot.subplot(2,2,3)
df8=psql.sqldf("select Country_Name,CO2Emissions,Population,Major_city_LUX from dfRepLuxLow;",globals())
df8=pd.DataFrame({'Country_Name': df8.Country_Name, 'Population': df8.Population, 'CO2Emissions':df8.CO2Emissions,'Major_city_LUX':df8.Major_city_LUX})
df8=df8.sort_values('CO2Emissions', ascending=False).head(10)
df8=sb.histplot(data=df8, x='Country_Name', y='CO2Emissions',hue='Major_city_LUX') 
pyplot.ylabel('CO2 Emissions                      \n Lox Lux                      ', fontsize=18, rotation=0)
pyplot.show()

# 9
# Population
pyplot.figure(figsize=(20,10))
pyplot.subplot(2,2,1)
df8=psql.sqldf("select Country_Name,Factories,Population,Major_city_LUX from dfRepLuxHigh;",globals())
df8=pd.DataFrame({'Country_Name': df8.Country_Name, 'Population': df8.Population, 'Factories':df8.Factories,'Major_city_LUX':df8.Major_city_LUX})
df8=df8.sort_values('Population', ascending=False).head(10)
df8=sb.histplot(data=df8, x='Country_Name', y='Population',hue='Major_city_LUX') 
pyplot.title('\n                                                              9. \n                                                            Population(million) in the 3 Stoma LUX representative groups \n ',fontsize=26)
pyplot.ylabel('Population                  \n High Lux                   ', fontsize=18, rotation=0)

pyplot.subplot(2,2,2)
df8=psql.sqldf("select Country_Name,Factories,Population,Major_city_LUX from dfRepLuxMed;",globals())
df8=pd.DataFrame({'Country_Name': df8.Country_Name, 'Population': df8.Population, 'Factories':df8.Factories,'Major_city_LUX':df8.Major_city_LUX})
df8=df8.sort_values('Population', ascending=False).head(10)
df8=sb.histplot(data=df8, x='Country_Name', y='Population',hue='Major_city_LUX') 
pyplot.ylabel('')

pyplot.subplot(2,2,3)
df8=psql.sqldf("select Country_Name,Factories,Population,Major_city_LUX from dfRepLuxLow;",globals())
df8=pd.DataFrame({'Country_Name': df8.Country_Name, 'Population': df8.Population, 'Factories':df8.Factories,'Major_city_LUX':df8.Major_city_LUX})
df8=df8.sort_values('Population', ascending=False).head(10)
df8=sb.barplot(data=df8, x='Country_Name', y='Population',hue='Major_city_LUX') 
pyplot.ylabel('Population                  \n Low Lux                   ', fontsize=18, rotation=0)
pyplot.show()

# 10
# area
pyplot.figure(figsize=(20,10))
pyplot.subplot(2,2,1)
df8=psql.sqldf("select Country_Name,Approx_Area,Major_city_LUX from dfRepLuxHigh;",globals())
df8=pd.DataFrame({'Country_Name': df8.Country_Name, 'Approx_Area': df8.Approx_Area,'Major_city_LUX':df8.Major_city_LUX})
df8=df8.sort_values('Approx_Area', ascending=False).head(10)
df8=sb.histplot(data=df8, x='Country_Name', y='Approx_Area',hue='Major_city_LUX') 
pyplot.title('\n                                                              10. \n                                                            Approx_Area sqKm in the 3 Stoma LUX representative groups \n ',fontsize=26)
pyplot.ylabel('Approx_Area                  \n High Lux                   ', fontsize=18, rotation=0)

pyplot.subplot(2,2,2)
df8=psql.sqldf("select Country_Name,Approx_Area,Major_city_LUX from dfRepLuxMed;",globals())
df8=pd.DataFrame({'Country_Name': df8.Country_Name, 'Approx_Area': df8.Approx_Area,'Major_city_LUX':df8.Major_city_LUX})
df8=df8.sort_values('Approx_Area', ascending=False).head(10)
df8=sb.histplot(data=df8, x='Country_Name', y='Approx_Area',hue='Major_city_LUX') 
pyplot.ylabel('')

pyplot.subplot(2,2,3)
df8=psql.sqldf("select Country_Name,Approx_Area,Major_city_LUX from dfRepLuxLow;",globals())
df8=pd.DataFrame({'Country_Name': df8.Country_Name, 'Approx_Area': df8.Approx_Area,'Major_city_LUX':df8.Major_city_LUX})
df8=df8.sort_values('Approx_Area', ascending=False).head(10)
df8=sb.barplot(data=df8, x='Country_Name', y='Approx_Area',hue='Major_city_LUX') 
pyplot.ylabel('Approx_Area                  \n Low Lux                   ', fontsize=18, rotation=0)
pyplot.show()

print('\n C. Conclusion: For a better visualizations of the disturbance of \n Factories, Co2 Emissions, Population & Area on the Stomatal conductance performances')
print('I have adjusted the stomal scale by awarding & deducting points for each disturbance level according to the sub groups above.')
print('Previous studies support this approach, as they found lower stomatal density in areas with higher pollution levels.')

# 10
dfRepSLP=psql.sqldf("select * from dfRepHighStomLUX;",globals())
# give a scale to factories effect
def func2(x):
    if x==10000:
        return 0.8
    if x==5000:
        return 0.5
    if x==1000:
        return 0.3
    else :
        return (-10)
dfRepSLP['FaStomaAdj']=dfRepSLP['Factories'].apply(func2)

# give a scale to Co2 emission effect
def func3(x):
    if x>=600:
        return 1.5
    if x>=200 and x<=600:
        return 1.3
    if x>=100 and x<=200:
        return 1.2
    if x>=50 and x<=100:
        return 1.1
    if x>=10 and x<=50:
        return 1
    if x>=5 and x<=10:
        return 0.8
    if x>=1 and x<=5:
        return 0.5
    else :
        return (-10)
dfRepSLP['co2StomaAdj']=dfRepSLP['CO2Emissions'].apply(func3)

# give a scale to POPULATION effect
def func4(x):
    if x>=5000:
        return 1.2
    if x>=1000 and x<=5000:
        return 1.1
    if x>=500 and x<=1000:
        return 0.9
    if x>=100 and x<=500:
        return 0.7
    if x>=50 and x<=100:
        return 0.5
    if x>=10 and x<=50:
        return 0.3
    if x>=5 and x<=10:
        return 0.1
    if x>=1 and x<=5:
        return 0.
    if x>=0.5 and x<=1:
        return 0.3    
    else :
        return (-10)
dfRepSLP['popStomaAdj']=dfRepSLP['Population'].apply(func4)

# give a scale to area effect
def func5(x):
    if x>=1000000:
        return 25
    if x>=500000 and x<=1000000:
        return 20
    if x>=100000 and x<=500000:
        return 15
    if x>=50000 and x<=100000:
        return 10
    if x>=1000 and x<=50000:
        return 5
    else :
        return (-10)
dfRepSLP['areaStomaAdj']=dfRepSLP['Approx_Area'].apply(func5)

# save to df
dfRepSLP=pd.DataFrame({'Country_Name': dfRepSLP.Country_Name, 'Stomatal_Conductance': dfRepSLP.Stomatal_Conductance, 'FaStomaAdj':dfRepSLP.FaStomaAdj,'co2StomaAdj':dfRepSLP.co2StomaAdj,'Major_city_LUX':dfRepSLP.Major_city_LUX,'popStomaAdj':dfRepSLP.popStomaAdj,'areaStomaAdj':dfRepSLP.areaStomaAdj})
# adjust the stoma with new variables
dfRepSLP['NSoma']=dfRepSLP.Stomatal_Conductance-dfRepSLP.co2StomaAdj-dfRepSLP.FaStomaAdj-dfRepSLP.popStomaAdj
dfRepSLP['NLux']=dfRepSLP.Major_city_LUX+dfRepSLP.areaStomaAdj
dfRepSLP['SNLux']=dfRepSLP.NLux+dfRepSLP.popStomaAdj

pyplot.figure(figsize=(29,10))
dfRepSL1 = pd.pivot(data=dfRepSLP,index="Country_Name", columns="NSoma", values="SNLux")
dfRepSL1P=sb.heatmap(dfRepSL1, annot=True)
sb.set_style('darkgrid')
pyplot.title('\n. 11 \n Lux & Stomatal Conductance \n  High Lux Group \n ',fontsize=26)
pyplot.xlabel('Stomal Conductance ', fontsize=18, rotation=0)
pyplot.ylabel(' ')
pyplot.show()



#[1] General Country Information:
#The World Factbook by the CIA: https://www.cia.gov/the-world-factbook/
#The World Bank: https://data.worldbank.org/ ([Data catalog])
#The United Nations: [invalid URL removed] (Population data)

#[2] Environmental Data:
#The World Resources Institute: https://www.wri.org/data
#The Food and Agriculture Organization (FAO): [invalid URL removed] (Forestry data)
#NASA Earth Observatory: https://earthobservatory.nasa.gov/ (Environmental data visualizations)

#[3] Light Pollution Data:
#Light Pollution Science and Technology (LPST) website: [invalid URL removed]
#The International Dark-Sky Association: https://www.darksky.org/

#[4] Forest Cover: https://www.fs.usda.gov/

#[5] Most Common Tree Species: https://www.arborday.org/trees/

# suportting citations 
#Irma Estefanía García-Sánchez, Víctor L. Barradas, Claudia A. Ponce de León Hill, Manuel Esperón-Rodríguez, Irma Rosas Pérez, Mónica Ballinas,
#Effect of heavy metals and environmental variables on the assimilation of CO2 and stomatal conductance of Ligustrum lucidum, an urban tree from Mexico City,
#Urban Forestry & Urban Greening,
#Volume 42,
#2019,
#Pages 72-81,
#ISSN 1618-8667,
#https://doi.org/10.1016/j.ufug.2019.05.002.
#(https://www.sciencedirect.com/science/article/pii/S1618866718303170)
#Abstract: Urban trees reduce CO2 and pollutants that represent a risk for human health in cities. In this work, we assessed the potential effect of heavy metals and environmental variables on the CO2 assimilation (A) and the stomatal conductace (gS) of Ligustrum lucidum, a common urban tree in Mexico City. We compared two sites with contrasting pollution levels: 1) city centre (PPI-C, high pollution level); and 2) south of the city (CU-SW; low pollution level). At each site, we measured 1) phsysiological traits (A and gS); 2) environmental variables (photosynthetically active radiation, PAR; air temperature, TA; vapor pressure deficit, VPD; concentration of atmospheric CO2); and 3) morphological leaf characteristics (stomatal size and density). Concentration of the heavy metals Pb, Cd, Cr, Cu, Mn, Fe, and Zn was determined in washed (internal metals) and unwashed (external plus internal metal) leaves at both sites. CO2 assimilation at CU-SW was higher than at PPI-C. PAR had the greatest effect on A; whereas TA and VPD had the greatest effect on gS. Regarding heavy metals, although we found no significant differences in internal concentrations between sites, we found a lower stomatal density at PPI-C, which may indicate a response of the species to the local pollution conditions. This characteristic might be benefitial for the species, allowing it to maintain optimal physiological conditions by reducing the assimilation of pollutants. Our results suggest that L. lucidum is a well adapted species for the urban environment.
#Keywords: Air temperature; CO2 concentration; Physiological responses; Photosynthetically active radiation; Pollutants; Urban vegetation
#Yu, W., Wang, Y., Wang, Y. et al. Application of a coupled model of photosynthesis and stomatal conductance for estimating plant physiological response to pollution by fine particulate matter (PM2.5). Environ Sci Pollut Res 25, 19826–19835 (2018). https://doi.org/10.1007/s11356-018-2128-6

#
#https://datascientyst.com/get-list-of-n-different-colors-names-python-pandas/
#https://proclusacademy.com/blog/customize_matplotlib_piechart/
#https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.pie.html
#https://www.w3schools.com/python/matplotlib_scatter.asp
#https://seaborn.pydata.org/tutorial/introduction
#https://seaborn.pydata.org/generated/seaborn.relplot.html
#https://seaborn.pydata.org/tutorial/axis_grids.html
#https://seaborn.pydata.org/tutorial/relational.html
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
#https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
#https://stackoverflow.com/questions/41088236/how-to-have-actual-values-in-matplotlib-pie-chart-displayed
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.size.html
#https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html
#https://stackoverflow.com/questions/15777951/how-to-suppress-pandas-future-warning
#https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html
#https://www.geeksforgeeks.org/display-the-pandas-dataframe-in-table-style/


print('\n \n ***Part 2- Diamonds*** \n')
#Part 2- Diamonds stock
#import diamonds dataset and save in df
# **adjust location if necessary**
df=sb.load_dataset('datasets\\diamonds')

#Q1 max rate for a diamond?
#save max price to df1
df1=df.price.max()
#format number with comma
df1="{:,}".format(df1)
#print answer
print('A1-The maximum rate for a diamond is','$'+df1,'\n')

#Q2 avg rate for a diamond?
#save avg price to df2
df2=int(df.price.mean())
#format number with comma
df2="{:,}".format(df2)
#print answer
print('A2-The avg rate for a diamond is','$'+df2,'\n')

#Q3 how many diamods in cut Ideal
#save len of ideal cut to df3
df3=len(df.query("cut=='Ideal'"))
#format number with comma
df3="{:,}".format(df3)
#print answer
print('A3-There are',df3,'Ideal cut diamonds','\n')

#Q4 how many diamonds colors and what are their names?
#save the number of unique colors to df4
df4=df.color.nunique()
#save & sort the names of unique colors to df41
df41=df.color.sort_values().unique()
#print answer
print('A4-There are',df4,'colors of diamonds and they are called:',df41,'\n')

#Q5 what is the avg of premium diamonds
#save premium sut to df
df5=df.query("cut=='Premium'")
# save sum and count
s=df5['carat'].sum()
c=df5['carat'].count()
# divide sum and count for avg
avg=s/c
#print answer
print('A5-The avg Carat size for a Premium diamond is',round(avg,2),'carat','\n')
#df5.groupby('cut')['carat'].mean()   # test
#df5.groupby('cut')['carat'].median() # test

#Q6 what is the average carat for each cut?
# print anwer
print('A6- The Avg Carat size for each diamond Cut \n')
# save columns carat & cut to df6
df6=df[["carat","cut","price"]].sort_values('cut')
# create sub-plot
pyplot.figure(figsize=(15,5))
# add 1st subplot
pyplot.subplot(1,2,1)
# add 1st boxplot
df6Bar=sb.boxplot(y='carat',x='cut',data=df6,palette="Set3",hue='cut')
# save & round  mean labels
lab=round(df6.groupby('cut')['carat'].agg('mean'),2)
 # for some reason it gives me a future warning and asks me to pass False in mean..
# display the labels above boxes
ver=df6['carat'].agg('mean')*0.01
for xtick in df6Bar.get_xticks():
    df6Bar.text(xtick,lab.iloc[(xtick)]+ver,lab.iloc[(xtick)],horizontalalignment='center',size=10,color='b')
# add the 1st plot labels & title to plot
pyplot.ylabel('Carat',fontsize=12,rotation=0,loc="top")
pyplot.xlabel('Cut',fontsize=12)
pyplot.title('\n A6-1. \n Avg Carat size for each diamond\'s Cut \n',fontsize=16)
# print answer
print('\n A6-1.  The avg Carat size of each Cut is represented with numbers,\n The grey line in the boxes represents the median Carat size for each Cut \n')

# select diamonds with less than 1.8 carat doesn't affect results but gives better graphics
df61=df6.query("carat<1.8")
countBig=df6[df6['carat'] > 1.8]['cut'].count()
countSmall=df6[df6['carat'] < 1.8]['cut'].count()
# add 2nd barplot to answer
pyplot.subplot(1,2,2)
df62Bar=sb.violinplot(y='carat',x='cut',data=df61,linewidth=1.5, linecolor="k",palette="Set3",hue='cut')
# add the 2st plot labels & title to plot
pyplot.ylabel('Carat',fontsize=12,rotation=0,loc="top")
pyplot.xlabel('Cut',fontsize=12)
df62Bar.set_xticks(['Ideal','Premium','Very Good','Good','Fair'])
pyplot.title('\nA6-2. \n Median Carat size distribution for each Cut \n',fontsize=16)
# add grid to 2nd plot
pyplot.grid(True)
print(' A6-2.  The distribution each Cut and Carat,\n The white line represents the median Carat size for each Cut')
print("*I have cleand the data from diamonds above 1.8 Carat, the subtraction affect on the mean and median is minor \n Number of with Carat size greater than 1.8 is->",countBig,"\n Number of with Carat size smaller than 1.8 is->",countSmall,'\n')
pyplot.show()

#Q7 what is the average price for each color
print('\n A7-1. The Avg Price for each Color in numbers,\n The Median Price is the grey line')
df7=df[["price","color","cut","carat","clarity"]].sort_values(['color','cut','clarity'],ascending=False)
pyplot.figure(figsize=(25,9))
df7Bar=sb.barplot(x='color',y='price',data=df7, fill=False,linewidth=0)
#add the bar values
df7Bar.bar_label(df7Bar.containers[0],fontsize=17)
#add the boxen plot on top off bar plot- apperntly it works 
df7Bar=sb.boxenplot(x='color',y='price',data=df7,palette="Set3",hue='color')
#add the 1st plot labels and title
pyplot.title('\n A7-1. \n The Avg Price for each Color \n',fontsize=16)
pyplot.xlabel('Color',fontsize=18)
pyplot.ylabel('')
pyplot.title('\n A7-1. Avg price for each diamond\'s color',fontsize=28)
pyplot.show()

#create 2rd plot 
print('\n A7-2. The Avg Price for each Color % ,\n')
pyplot.figure(figsize=(25,9))
sb.displot(df7, x="price", hue="color", stat="percent",common_norm=False,bins=7,fill=False)
#'count', 'density', 'percent', 'probability' or 'frequency'
pyplot.title('\n A7-2. \n The Avg Price for each Color % \n',fontsize=16)
pyplot.show()

#create 3rd plot- The 4C'- Cut, Carat, Color & Clarity 
print('\n A7-3. As shown below- Though Color, Cut and Carat affect the diamonds price the Clarity is crutial \n and can be the diffrance of thousends of dollars from VVS-Very very slightly included to Il-Included')
print('Conclusion 1-Color D is the most valuable Color, then E,F,G,H,I,J.')
print('Conclusion 2- Color, Clarity & Cut affects the price rather then Carat size')
df7=df[["price","color","cut","carat","clarity"]].sort_values(['color','cut','clarity'],ascending=True)
df7=psql.sqldf("select * from df7 where carat<=1.8;",globals())
df7Bar = sb.relplot(data=df7,x='carat', y='price', hue='color', size='clarity',style="cut",sizes=(20,60), palette='muted',height=7)
pyplot.grid(True,linestyle='--',color='grey', alpha=.25)
pyplot.ylabel('Price',rotation=0,loc="top")
pyplot.title('\n Just for fun :) \n The 4 C\'s of diamonds \n Color, Cut, Clarity & Carat \n ',fontsize=14)
pyplot.show()




#test
#df72=round(df7.groupby('color')['price'].agg(['mean','median','std']),0)
#df72