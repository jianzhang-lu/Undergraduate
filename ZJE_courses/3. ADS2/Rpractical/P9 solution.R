###### Practical solution by Simon (Jingyuan)

library(tidyverse)

### Q1 (bigger sample size is better)
stu.26=replicate(10000,mean(runif(26,0,100))) 
mean(stu.26<40)

stu.5=replicate(10000,mean(runif(5,0,100)))
mean(stu.5<40)

data.frame('score'=c(stu.26,stu.5),'Student_number'=rep(c('26','5'),each=10000)) %>%
 ggplot()+theme_classic()+geom_histogram(aes(x=score,y=..density..,fill=Student_number),bins=40,alpha=0.5,
                                                                       colour='black',position='identity')+
 geom_density(aes(x=score,y=..density..,colour=Student_number),size=1.5,alpha=0.2)+labs(x='Normative Scores',y='Frequency')



### Q2
uni.80=replicate(10000,mean(runif(26,0,80)))
uni.100=replicate(10000,mean(runif(26,0,100)))
mean(uni.80>uni.100)
data.frame('score'=c(uni.80,uni.100),'Student'=rep(c('unlucky','lucky'),each=10000)) %>%
 ggplot()+theme_classic()+geom_histogram(aes(x=score,y=..density..,fill=Student),bins=40,alpha=0.2,colour='black',position='identity')+
        geom_density(aes(x=score,y=..density..,colour=Student),size=1.5,alpha=0.2)+labs(x='Uniform distributed normative scores',y='Frequency')



### Q3 (calculate normative score)
pnorm(64,50,10)*100
mean(pnorm(c(64,63,62,59),50,10)*100)
mean(pnorm(c(70,63,61,56),50,10)*100)



### Q4
10*(1-0.2);50*(1-0.2)
UnluckyNormScore=pnorm(rnorm(10000,40,8),50,10)*100
hist(UnluckyNormScore)

unl=replicate(10000,mean(sample(UnluckyNormScore,26,replace=T)))
luc=replicate(10000,mean(runif(26,0,100)))
mean(unl>luc)

uni.var=replicate(10000,runif(1,5,40)) %>% round(.) %>% 
        sapply(function(i) runif(i,0,100) %>% mean)
mean(unl>uni.var)



### Q5 (might not be correct)
# raw score of normal classes with varying size
RawScore_list=replicate(10000,simplify=F,runif(1,5,40) %>% round %>% 
                   rnorm(.,rnorm(1,50,5),10)) 
RawScore_list %>% unlist %>% data.frame('score'=.) %>%
 ggplot(aes(score))+theme_classic()+geom_histogram(bins=40,fill=NA,colour='black')+
 labs(x='Raw Score of varied class size')+geom_vline(aes(xintercept=mean(score)),size=2,
                                                     colour='red',linetype='dashed',alpha=0.5)
# raw score of unlucky class with varying size
Class_size=lapply(RawScore_list,function(x) length(x)) %>% unlist
UnRawScore_list=lapply(Class_size,function(i) rnorm(i,rnorm(1,40,4),8))
# normative score distribution for unlucky class
UnRawScore_list %>% lapply(function(v) pnorm(v,50,10)*100) %>% unlist %>% data.frame('score'=.) %>%
 ggplot(aes(score))+theme_classic()+geom_histogram(bins=40,fill=NA,colour='black')+
 labs(x='Normative Score of Unlucky Class with Varied Class Size')+geom_vline(aes(xintercept=mean(score)),size=2,
                                                     colour='red',linetype='dashed',alpha=0.5)
# probability unlucky class better than normal class
prob=lapply(1:10000,function(i) data.frame('Raw'=RawScore_list[[i]],'Unl_Raw'=UnRawScore_list[[i]],'Sim_order'=i)) %>%
 bind_rows %>% mutate('Raw_Nor'=pnorm(Raw,50,10)*100,'Unl_Nor'=pnorm(Unl_Raw,50,10)*100,.before=Sim_order) %>% 
 group_by(Sim_order) %>% summarise('Raw_Mean'=mean(Raw_Nor),'Unl_Mean'=mean(Unl_Nor))
mean(prob$Unl_Mean>prob$Raw_Mean)
# Leonie's team's normative scores
Nor_mean=replicate(10000,rnorm(1,50,5),simplify=F)
L=lapply(Nor_mean,function(x) pnorm(c(64,63,62,59),x,10)*100)
S=lapply(Nor_mean,function(x) pnorm(c(70,63,61,56),x,10)*100)
lapply(1:10000,function(i) mean(L[[i]])>mean(S[[i]])) %>% unlist %>% mean
