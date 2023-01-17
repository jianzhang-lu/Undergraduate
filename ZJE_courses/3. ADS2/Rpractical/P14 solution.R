#### generate 50 data spreadsheets
library(tidyverse)
# what is the minimum sample size required
# typical min power for clinical trails is 0.8
# set sd=1 as we also want small sd for the week3 check data
power.t.test(delta=3,sd=1,sig.level=0.05,power=0.8,type='paired',
             alternative='one.sided') # n = 2.552324
pateint_list=lapply(1:50,function(i)
        data.frame('Name'=sample(LETTERS,3,replace=F) %>% rep(2),
                   'Pain_rate'=c(rnorm(3,6,1),rnorm(3,2.5,1)) %>% round,
                   'Timepoint'=rep(c('Post-op','Week_3'),each=3),
                   'Phone_No'=sample(1:6,6),
                   'Gender'=sample(c('M','F'),3,replace=T) %>% rep(2),
                   'Province'=sample(letters,3,replace=T) %>% rep(2),
                   'Batch'=rep(i,6)))






#### Do you have enough information to create your synthetic dataset, or are there things you need to check with Dr. Hu?

# No enough info, we need to know the desirable statistical power of his study in order to generate enough samples. 
# Also province, gender, age, health condition, medicine dosage and diet do matter for recovery process. 
# Dr. Hu has not considered the effects except province and gender.






#### Plan out a data analysis pipeline

## How will you handle having the data in several spreadsheets?
# read all the data and save to a list of data frames then combine the list
pateint_data=bind_rows(pateint_list)


## How can you protect a patient's privacy, while also making sure that you can match a person's
## pain level at their 3-week checkup to their original pain level?

# set a batch number to each batch of observed patients, or set patient 1, 2, 3...


## How are you going to deal with ambiguous or missing data? What kinds of data problems are
## likely to occur?

# Based on how much is missing. Dr. Hu must make sure he has the full data of the first few batches.
# Then based on these data sets we might use simulation to fill the upcoming missing part.
# Also there are iterative algorithms for estimating missing data. You can have a look online.
# One of them is called EM algorithm.


## Of all the information recorded in the spreadsheet, what information does the data analyst need?
## What information should be hidden from the data analyst? Should somebody else have that information?

# Need: Gender, painess rate, time-ponit, province, batch
# Names, phone numbers should be hidden from anyone.


## What would be a good way of visualising the data?
library(ggsignif)
# boxplot
ggplot(pateint_data,aes(x=Timepoint,y=Pain_rate))+theme_classic()+labs(x='Time Point',y='Pain rate')+
        geom_boxplot(size=1,outlier.size=2,outlier.colour='red')+
        geom_signif(comparisons=list(c('Post-op','Week_3')),annotations='*')+
        theme(axis.title=element_text(size=15,face='bold'),axis.text=element_text(size=12,face='bold'))
# boxplot with different batches
pateint_data$Batch=factor(pateint_data$Batch)
ggplot(pateint_data,aes(x=Batch,y=Pain_rate,colour=Timepoint))+theme_classic()+labs(x='Patient Batch',y='Pain rate')+
        geom_boxplot()+scale_colour_manual(values=c('black','red'))+
        theme(axis.title=element_text(size=15,face='bold'),axis.text=element_text(size=10,face='bold'))
        

## What kind of data analysis will you likely be using?

# Maybe anova, t-test and linear model.
pateint_data$Timepoint=factor(pateint_data$Timepoint)
p_list=group_by(pateint_data,Batch) %>% group_split(Batch) %>%
        lapply(function(x) anova(lm(x$Pain_rate~x$Timepoint))$`Pr(>F)`[1]) %>%
        unlist() %>% {data.frame('Batch'=as.factor(1:50),'pval'=.)}
ggplot(p_list,aes(Batch,pval))+theme_classic()+
        labs(x='Patient Batch',y='P-value for the same batch \n pain level difference')+
        geom_point(size=2,alpha=0.5)+geom_hline(size=1,yintercept=0.05,colour='red',linetype='dashed')+
        theme(axis.title=element_text(size=15,face='bold'),axis.text=element_text(size=10,face='bold'))


## Are there any other problems you notice or things you may need to pay attention to?

# emm...maybe how to deal with missing data