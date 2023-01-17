##### R codes for the practical course ADS2 Week6 
##### Getting and cleaning data 
### 20211014 
### By Xianghua Li. 

# Set working directory
setwd('~/Desktop/data_Science/') # Where did you put the file? You may want to set the working directory there. 

#1. Let's load the practical data set1. 
wnv <- read.csv("WNV_mosquito_test_results.csv" ) 

#1.1. Explore our data
head(wnv)
summary(wnv)
str(wnv) # 
class(wnv)
class(wnv$TEST.DATE)
# Let's try to make it a real date/time type 
wnv$TEST.DATE <- as.POSIXct(wnv$TEST.DATE, format = "%m/%d/%Y %H:%M:%S" ,tz="America/Chicago")
class(wnv$TEST.DATE)

#Let's try to convert timezone of daytime type data
dat1 <- wnv$TEST.DATE[1]
dat1
attributes(dat1)
attributes(dat1)$tzone <- "America/Los_Angeles"
dat1

#Let's try to separate LOCATION column into LATITUDE and LONGITUDE  
wnv$LOCATION <- gsub("[()]","", wnv$LOCATION, perl = T)
wnv <- separate(wnv,LOCATION, into = c("LATITUDE", "LONGITUDE"), sep = ",", remove = F, fill = "left" ,convert = T)
summary(wnv)

#### There other useful ways to do string manipulations ###### 
library (stringr) # for example. 
#### explore other functions
# str_sub(), str_replace() , str_split()


#1.2 Screen and diagnosis. 

# Just for fun / practice purpose, let's try the functions gather and spread. 
# In order not to mess up the original dataset, Xianghua makes a new transformed dataset
# first, let's load the library for this. 
library(tidyr) # Sometimes, you may need to install a library. In that case, serach the library in the "Packages" pane and install before loading.  
? gather
wnv2<- gather(wnv)
# what is this format giving us? 
head(wnv2) 

str(wnv2)  # This data as it is too messy. We will remove it. 
rm(wnv2)

### Are the variable names informative? 
table(wnv$SEASON.YEAR)
# Looks that there is no season in it. 
# Missing values? Duplicated rows? Anything to chnage? 
anyNA(wnv) # there are, but where? 
which(!complete.cases(wnv))  # quite a lot. 
# Let's have a look at them. 
wnv[17, ] # We saw NA values and missing space. 

length(wnv[wnv$LOCATION=="", "LOCATION"]) 
# 4416 rows with these missing values. It is quite a lot. 
length(rownames(wnv[is.na(wnv$LATITUDE), ]))  
# Any duplicated values? 
which(duplicated(wnv))
# None.  
# Let's check if the datatypes are ok. 
str(wnv) # What do you think? Shall we change any of them? 

# Strange patterns? 
### We need to plot to check if there are any strange patterns. 
library(ggplot2)
library(viridis) # Color-blind friendly color 

# Let's check if the relationships between number of mosiquitoes and different factors. 
# year? 
ggplot(data= wnv,aes(x=as.factor(YEAR), y=NUMBER.OF.MOSQUITOES)) + geom_boxplot() 
# Latitute? 
ggplot(data= wnv,aes(x=LATITUDE, y=NUMBER.OF.MOSQUITOES)) + geom_point(alpha=0.3, size=1, aes(col=as.factor(YEAR))) + 
  scale_color_viridis(discrete = T) + geom_smooth()
# Longitude? 
ggplot(data= wnv,aes(x=LONGITUDE, y=NUMBER.OF.MOSQUITOES)) + geom_point(alpha=0.3, size=1, aes(col=as.factor(YEAR))) + 
  scale_color_viridis(discrete = T) + geom_smooth()
# Species & TRAP
ggplot(data= wnv,aes(x=as.factor(TRAP_TYPE), y=NUMBER.OF.MOSQUITOES, col=SPECIES)) + geom_boxplot()+ 
  scale_color_viridis(discrete = T)

#### Please explore the way you want. 
## If you want to save any figures, 
# You could click "Plots" pane & "Export"
# Or, use the function  ggsave() to export file as you wish. Play with the parameters if you want. 

# One outlier. Which is it? 
wnv[wnv$NUMBER.OF.MOSQUITOES> 70, ]


### Treatment. 
#1. Variable name for SEASON.YEAR should be changed to YEAR
names(wnv)[1] <- "YEAR"
#2. Shall we remove the NA values? If you want to remove, we could: 
wnv<- wnv[!is.na(wnv$LONGITUDE), ] 

#3. Shall we remove the outlier?  
#### If you think we should, but only with SOLID REASON. 
# Xianghua thinks that she should keep the outlier. 



#### Now, if you want, you may want to save the file as a R data or export as a file. 
save(wnv, file='wnv_modified_20201013.RData')
# if you want to export as a table, 
write.table(wnv, file = "wnv_modified_20201013.txt", sep='\t', quote=F) 
# Make sure that you document all the changes that you implemented in your electronic notebook. 
# Variable naemes changed.  
# Especially, which data point are removed & Why. 

#####
####### Practice 2 
########
# First, let's clean up the environment. 
rm(list=ls())
dev.off()

# Load the datatable. This time, it is a tab separate txt file. 
# Therefore we used read.table rather than read.csv. 
pgp3_og<-read.table("Tests_PGP3.txt", sep='\t', header = T)

# Have a look at the data and get a feeling. 
head(pgp3_og)
summary(pgp3_og)
str(pgp3_og)
table(pgp3_og$measured)
table(pgp3_og$SampleID)
##### 

which(duplicated(pgp3_og)) # ok there are duplicated rows. 
idx1= which(duplicated(pgp3_og))
idx2= which(duplicated(pgp3_og, fromLast = T))

# Since it only gives one set of index duplicated rather than both. Let's check 
pgp3_og[c(idx1, idx2),  ] # Xianghua thinks it is safe to keep only one copy.  

# We already saw that some data seems to be missing. 
anyNA(pgp3_og) 
# There are missing values. 
length(rownames(pgp3_og[complete.cases(pgp3_og), ])) 
# 2219, less than number of rows that is 2324. 

####
#### Treatment. 
#1. Xianghua think it is safe to keep only one set of duplicated rows. 
pgp3<- pgp3_og[-idx1, ]# remove one set of the duplciated rows.  
# Let's check if all the duplicated rows are removed. 
which(duplicated(pgp3)) # ok. 

#2. Xianghua will transform it to a wide format. 
pgp3<- spread (pgp3, measured, value)
head(pgp3)
summary(pgp3)
str(pgp3)
table(pgp3$sex)  # hard to understand 
table(as.character(pgp3$sex)) # 1 and 2. From the source of data we know 1 is male and 2 is female. 


#3. Data types 
#3.1 The SampleID should be factors, NOT integers. 
#3.2 The elisa od values shouldn't be factors. Xianghua thinks it is better to change them to numeric values. 
#3.3 The sex varaible is not easily interpretable. Xianghua will change them to M and F. 

#covert SampleID, age.F, sex to readable factor
pgp3$SampleID <- as.character(pgp3$SampleID)
pgp3$elisa.od <- as.numeric(as.character(pgp3$elisa.od)) # Here, we change the factor to character first. What would happen if you don't convert to character first? 
pgp3$elisa.pre.od <- as.numeric(as.character(pgp3$elisa.pre.od))

pgp3$sex <- gsub("1","M",as.character(pgp3$sex))
pgp3$sex <- gsub("2","F",as.character(pgp3$sex))
pgp3$sex <- as.factor(pgp3$sex)
summary(pgp3)

#4. Missing values. 
# Shall we remove them? Xianghua decided to drop them out. 
length(rownames(pgp3[!complete.cases(pgp3), ])) # 103, as in the summary for sex values missing. 

pgp3= pgp3[complete.cases(pgp3), ]
anyNA(pgp3)

#5. Any strange patterns? 

ggplot(data=pgp3) + geom_boxplot(aes(x=sex, y=elisa.od))
ggplot(data=pgp3) + geom_boxplot(aes(x=age.f, y=elisa.pre.od))
# What is going on? x-axis group label is missing. 
# These are not dropped since it is not recorded as NA values. 
# Xianghua thinks these should be removed, considering we are interested in the relationship between age and elisa od. 
head(pgp3[pgp3$age.f=='', ]) 
pgp3<- pgp3[pgp3$age.f!='',] 

ggplot(data=pgp3) + geom_boxplot(aes(x=age.f, y=elisa.pre.od))
ggplot(data=pgp3) + geom_boxplot(aes(x=age.f, y=elisa.od))

#6.  We want to reshape the dataframe so that we could compare ELISA od at two time points at each age group. 
# For that purpose, we should reshape the dataframe again. 

pgp3 <- gather(pgp3,key = "time.point", value = "ELISA.od", elisa.od:elisa.pre.od, factor_key = T)
summary(pgp3)
ggplot(data= pgp3, aes(age.f, ELISA.od, color=time.point)) + geom_boxplot()
ggsave(file='ELISA_od.pdf', width = 7, height = 5)

save(pgp3, file='pgp3_20201013_modified.RData') 
# Documentation
# Xianghua changed the data 
# 1) from long to wide, 
# 2) changed datatypes, 
# 3) changed how sex value is coded, 
# 4) removed missing values that occur in age range and sex
# 5) Reshaped the dataframe again by gathering the two od values with the key as time.point.  







