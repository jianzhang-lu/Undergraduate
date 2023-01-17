# 1. Pie chart about peak annotation
library(tidyverse)
data <- read.csv("POLR2A_annot.txt", sep = "\t")
data$Annotation <- gsub(" (.+)", "", data$Annotation, fixed = F)
count <- data %>% group_by(Annotation) %>% summarise(count = table(Annotation))
count <- count[order(count$count, decreasing = TRUE),]
myLabel = as.vector(count$Annotation)
myLabel = paste(myLabel, "(", round(count$count/sum(count$count)*100, 2), "%)", sep = "") 
ggplot(count, aes(x = "", y = count, fill = Annotation)) + 
  geom_bar(stat = "identity", width = 1) +    
  coord_polar(theta = "y") + 
  labs(x = "", y = "", title = "Annotation of POLR2A") +
  scale_fill_discrete(breaks = count$Annotation, labels = myLabel) +
  theme(plot.title = element_text(hjust = 0.5),
        axis.text = element_blank()) 

# 2. The normalized density of tags for 5 data
data2 <- read.csv("metaGene_profile.txt", sep = "\t")
data2 <- data2[,c(1,2,5,8,11,14)]
Chip_order <- c("pos", "H3K27ac", "H3K27me3", "H3K4me1", "H3K4me3", "POLR2A")
colnames(data2) <- Chip_order
data2_gather <- gather(data2, 
                       c("H3K27ac", "H3K27me3", "H3K4me1", "H3K4me3", "POLR2A"), 
                       key = "factor", value = "value")
ggplot(data2_gather, aes(x = pos, y = value, group = factor))+
  geom_line(aes(col = factor)) +
  labs(x = "position", y = "density", color = "Factor", 
       title = "(A) Normalized density of tags on the upstream, downstream and within the 
       gene bodies of genes from 5 data") +
  theme_classic()

# 3. The average density of tags for the other 4 data around the summits of the POLR2A peaks.
data3 <- read.csv("density_profile.txt", sep = "\t")
data3 <- data3[,c(1, 2, 5, 8, 11, 14)]
colnames(data3) <- c("position", "POLR2A", "H3K27ac", "H3K27me3", "H3K4me1", "H3K4me3")
data3 <- gather(data3, c("POLR2A", "H3K27ac", "H3K27me3", "H3K4me1", "H3K4me3"), 
                key = "Factor", value = "value")
ggplot(data3, aes(x = position, y = value, group = Factor))+
  geom_line(aes(col = Factor)) +
  labs(x = "position", y = "density", color = "Factor", 
       title = "The density of tags of other 4 data around the summits of the POLR2A peaks") +
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5)) 


## POLR2A ------ promoter

## H3K4me1 ------- active enhancer (ensure)
## H3K4me3 ------- active promoter (ensure)
## H3K27ac ------- active enhancer, active promoter (ensure)
## H3K27me3 ------ repressive enhancer, repressive promoter (ensure)

# 4. Venn diagram
library(ggvenn)
H3K4me1 <- read.csv('D:/系统默认/桌面/新建文件夹/GP report/Motif_Search/H3K4me1/knownResults.txt', sep = "\t")
H3K4me1$Motif.Name <- gsub('\\(.+', '', H3K4me1$Motif.Name, fixed = F)
H3K4me1 <- filter(H3K4me1, q.value..Benjamini. <= 0.01)

H3K4me3 <- read.csv('D:/系统默认/桌面/新建文件夹/GP report/Motif_Search/H3K4me3/knownResults.txt', sep = "\t")
H3K4me3$Motif.Name <- gsub('\\(.+', '', H3K4me3$Motif.Name, fixed = F)
H3K4me3 <- filter(H3K4me3, q.value..Benjamini. <= 0.01)

H3K27ac <- read.csv('D:/系统默认/桌面/新建文件夹/GP report/Motif_Search/H3K27ac/knownResults.txt', sep = "\t")
H3K27ac$Motif.Name <- gsub('\\(.+', '', H3K27ac$Motif.Name, fixed = F)
H3K27ac <- filter(H3K27ac, q.value..Benjamini. <= 0.01)

H3K27me3 <- read.csv('D:/系统默认/桌面/新建文件夹/GP report/Motif_Search/H3K27me3/knownResults.txt', sep = "\t")
H3K27me3$Motif.Name <- gsub('\\(.+', '', H3K27me3$Motif.Name, fixed = F)
H3K27me3 <- filter(H3K27me3, q.value..Benjamini. <= 0.01)

POLR2A <- read.csv('POLR2A/knownResults.txt', sep = "\t")
POLR2A$Motif.Name <- gsub('\\(.+', '', POLR2A$Motif.Name, fixed = F)
POLR2A <- filter(POLR2A, q.value..Benjamini. <= 0.01)

promoter <- list('H3K4me3' = H3K4me3$Motif.Name, 
                 'POLR2A' = POLR2A$Motif.Name,
                 'H3K27ac' = H3K27ac$Motif.Name,
                 'H3K27me3' = H3K27me3$Motif.Name)

ggvenn(promoter, show_percentage = T, stroke_color = "white",
       fill_color = c("#E41A1C","#1E90FF","#FF8C00","#984EA3"),
       set_name_color =c("#E41A1C","#1E90FF","#FF8C00","#984EA3"),
       set_name_size = 4) +
  labs(title = '(A) Common transcript factors found in 4 data related to promoters') +
  theme(plot.title = element_text(hjust = 0.5, size = 18))
ggsave("D:/系统默认/桌面/新建文件夹/GP report/Figure/promoters.png", width = 10, height = 6, dpi = 500)


a <- intersect(H3K4me3$Motif.Name, H3K27ac$Motif.Name)
b <- intersect(a, H3K27me3$Motif.Name)


enhancer <- list('H3K4me1' = H3K4me1$Motif.Name, 
                 'H3K27me3' = H3K27me3$Motif.Name,
                 'H3K27ac' = H3K27ac$Motif.Name)

ggvenn(enhancer, show_percentage = T, stroke_color = "white",
       fill_color = c("#4DAF4A","#984EA3","#FF8C00"),
       set_name_color =c("#4DAF4A","#984EA3","#FF8C00")) +
  labs(title = '(B) Common transcript factors found in 3 data related to enhancers') +
  theme(plot.title = element_text(hjust = 0.5, size = 18))
ggsave("D:/系统默认/桌面/新建文件夹/GP report/Figure/enhancer.png", width = 10, height = 6, dpi = 500)


c <- intersect(H3K4me1$Motif.Name, H3K27me3$Motif.Name)
d <- intersect(c, H3K27ac$Motif.Name)


motif <- select(POLR2A, c(2,5,6,7,8,9))
motif <- arrange(motif, desc(X..of.Target.Sequences.with.Motif))

# # Plot 1
# ggplot(data2_gather[data2_gather$factor == 'H3K27ac',], aes(x = pos, y = value, group = factor))+
#   geom_line() +
#   labs(x = "position", y = "density", color = "Factor") +
#   xlim(-2000,2000) +
#   geom_vline(xintercept=c(-1,1), linetype = 2, color = "red", size = 1) +
#   labs(x = "position", y = "density", color = "Factor",
#        title = "(B) Normalized density of tags around the TSS from the H3K27ac data") +
#   theme_classic()
# ggsave("D:/系统默认/桌面/新建文件夹/GP report/Figure/H3K27ac_dist.png", width = 10, height = 6, dpi = 500)
# 
# 
# # Plot 2
# ggplot(data2_gather[data2_gather$factor == 'H3K27me3',], aes(x = pos, y = value, group = factor))+
#   geom_line() +
#   labs(x = "position", y = "density", color = "Factor") +
#   xlim(-2000,2000) +
#   geom_vline(xintercept=c(-1,1), linetype = 2, color = "red", size = 1) +
#   labs(x = "position", y = "density", color = "Factor",
#        title = "(C) Normalized density of tags around the TSS from the H3K27me3 data") +
#   theme_classic()
# ggsave("D:/系统默认/桌面/新建文件夹/GP report/Figure/H3K27me3_dist.png", width = 10, height = 6, dpi = 500)
# 
# 
# # Plot 3
# ggplot(data2_gather[data2_gather$factor == 'H3K4me1',], aes(x = pos, y = value, group = factor))+
#   geom_line() +
#   labs(x = "position", y = "density", color = "Factor") +
#   xlim(-2000,2000) +
#   geom_vline(xintercept=c(-1,1), linetype = 2, color = "red", size = 1) +
#   labs(x = "position", y = "density", color = "Factor",
#        title = "(D) Normalized density of tags around the TSS from the H3K4me1 data") +
#   theme_classic()
# ggsave("D:/系统默认/桌面/新建文件夹/GP report/Figure/H3K4me1_dist.png", width = 10, height = 6, dpi = 500)
# 
# 
# # Plot 4
# ggplot(data2_gather[data2_gather$factor == 'H3K4me3',], aes(x = pos, y = value, group = factor))+
#   geom_line() +
#   labs(x = "position", y = "density", color = "Factor") +
#   xlim(-2000,2000) +
#   geom_vline(xintercept=c(-1,1), linetype = 2, color = "red", size = 1) +
#   labs(x = "position", y = "density", color = "Factor",
#        title = "(E) Normalized density of tags around the TSS from the H3K4me3 data") +
#   theme_classic()
# ggsave("D:/系统默认/桌面/新建文件夹/GP report/Figure/H3K4me3_dist.png", width = 10, height = 6, dpi = 500)
# 
# # Plot 5
# ggplot(data2_gather[data2_gather$factor == 'POLR2A',], aes(x = pos, y = value, group = factor))+
#   geom_line() +
#   labs(x = "position", y = "density", color = "Factor") +
#   xlim(-2000,2000) +
#   geom_vline(xintercept=c(-1,1), linetype = 2, color = "red", size = 1) +
#   labs(x = "position", y = "density", color = "Factor",
#        title = "(F) Normalized density of tags around the TSS from the POLR2A data") +
#   theme_classic()
# ggsave("D:/系统默认/桌面/新建文件夹/GP report/Figure/POLR2A_dist.png", width = 10, height = 6, dpi = 500)


# # heatmap
# library(pheatmap)
# library(RColorBrewer)
# data6 <- read.csv("D:/系统默认/桌面/新建文件夹/GP report/profile/tag_density_profile.txt", sep = "\t")
# 
# data_POLR2A <- data6[, 2:202]
# data_H3K27ac <- data6[, 203:403]
# data_H3K27me3 <- data6[, 404:604]
# data_H3K4me1 <- data6[, 605:805]
# data_H3K4me3 <- data6[, 806:1006]
# 
# 
# pheatmap(data_POLR2A,
#          cluster_cols = F, cluster_rows = F, 
#          show_colnames = F, show_rownames = F,
#          color = colorRampPalette(brewer.pal(n = 9, name = "Reds"))(1000),
#          main = "POLR2A")
# 
# pheatmap(data_H3K27ac,
#          cluster_cols = F, cluster_rows = F, 
#          show_colnames = F, show_rownames = F,
#          color = colorRampPalette(brewer.pal(n = 9, name = "Blues"))(1000),
#          main = "H3K27ac")
# 
# pheatmap(data_H3K27me3,
#          cluster_cols = F, cluster_rows = F, 
#          show_colnames = F, show_rownames = F,
#          color = colorRampPalette(brewer.pal(n = 9, name = "Greens"))(1000),
#          main = "H3K27me3")
# 
# pheatmap(data_H3K4me1,
#          cluster_cols = F, cluster_rows = F, 
#          show_colnames = F, show_rownames = F,
#          color = colorRampPalette(brewer.pal(n = 9, name = "Greens"))(1000),
#          main = "H3K4me1")
# 
# pheatmap(data_H3K4me3,
#          cluster_cols = F, cluster_rows = F, 
#          show_colnames = F, show_rownames = F,
#          color = colorRampPalette(brewer.pal(n = 9, name = "Greens"))(1000),
#          main = "H3K4me3")


                 