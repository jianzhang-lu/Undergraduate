# install.packages(c('tidyverse','reshape2'))
# tidyverse packages contains 'tidyr' and 'ggplot2'
library(tidyverse);library(reshape2)

### first data set
mos.data=read.csv('C:/Users/simon/Desktop/WNV_mosquito_test_results.csv',header=T,sep=',')

mos.data$LOCATION=mos.data$LOCATION %>% str_replace_all(pattern='[()]',replacement='') 
# replace () by empty

mos.data=separate(data=mos.data,col=LOCATION,into=c('LATITUDE','LONGITUDE'),sep=',',remove=T,convert=T) 
# split the LOCATION column into 2 columns named 'LATITUDE'&'LONGITUDE', sep=',' removes the comma between the 2 numbers,
# remove=T removes the original column LOCATION

head(mos.data);tail(mos.data);nrow(mos.data);attributes(mos.data);table(mos.data$TRAP)
# first 6 rows, last 6 rows
str(mos.data);class(mos.data)

# it is a wide format
names(mos.data)[1]='YEAR'

# diagnose
anyNA(mos.data)
which(!complete.cases(mos.data))
mos.data=na.omit(mos.data)

anyDuplicated(mos.data)

mos.data$TEST.DATE=as.POSIXct(mos.data$TEST.DATE,tz='America/Chicago',format='%m/%d/%Y %H:%M:%S')

# gather and melt are similar, pivot_wider is similar to spread
xxx=gather(mos.data,key='LOCATION',value='value',LATITUDE,LONGITUDE);rm(xxx)
yyy=melt(mos.data,id.vars=1:8,measure.vars=c('LATITUDE','LONGITUDE'),value.name='value',variable.name='LOCATION')
zzz=pivot_wider(xxx,names_from=LOCATION,values_from=value)








### Second set
# messy long format file convert it right now!
Tests_PGP3=read.table('C:/Users/simon/Desktop/Tests_PGP3.txt',header=T,sep='\t')
Tests_PGP3$value=na_if(Tests_PGP3$value,'') %>% as.character()
# replace blank by NA and tranfer value column to characters

Tests_PGP3=Tests_PGP3 %>% group_by(SampleID) %>% group_split() %>% lapply(function(data) distinct(data)) %>%
  bind_rows()
# remove duplicated row by spliting the entire data frame to seperate sub data frames by SampleID, then reunite 

Tests_PGP3.wide=pivot_wider(Tests_PGP3,id_cols=SampleID,names_from=measured,values_from=value) %>% na.omit()
# transfer to wide format and remove na

Tests_PGP3.wide$sex=str_replace(Tests_PGP3.wide$sex,'1','Male') %>% str_replace('2','Female')
# replace character 1 by Male and 2 by Female

str(Tests_PGP3.wide);table(Tests_PGP3.wide$age.f)
Tests_PGP3.wide$age.f=factor(Tests_PGP3.wide$age.f,levels=c('(0,10]','(10,20]','(20,30]','(30,40]','(40,50]','(50,90]'))
# set the levels for the age.f column in order to keep the order when plot the data

Tests_PGP3.plot=Tests_PGP3.wide %>% melt(id.vars=1:3,measure.vars=c('elisa.od',"elisa.pre.od"),variable.name='Time point',value.name='ELISA.od') %>%
  mutate('ELISA.od'=as.numeric(ELISA.od)) %>% ggplot(aes(age.f,ELISA.od,colour=`Time point`))+theme_classic()+
  geom_boxplot(size=1,alpha=0.5)+scale_colour_manual(breaks=c('elisa.od',"elisa.pre.od"),limits=c('elisa.od',"elisa.pre.od"),
                                                      values=c('red','blue'))
# ...hard to explain