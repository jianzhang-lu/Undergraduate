library(DESeq2)
library(tidyverse)
library(apeglm)
data_liver <- read.table("实验室+BMS/热图/liver.txt", header = T)
ref <- read.table("D:/python 文件/lab/gencode.v19.gene.length.txt", header = T)

inforData <- data_liver[,c(1:5)]
countData <- as.matrix(data_liver[7:19])
rownames(countData) <- data_liver$Geneid

keep <- rowSums(countData) >= 1
countData <- countData[keep, ]

which(duplicated(row.names(countData)))

configure <- data.frame("condition" = factor(c(rep('cancer', 4), rep('normal', 9))),
                        "type" = c(paste0('cancer', 1:4), paste0('normal', 1:9)))

dds <- DESeqDataSetFromMatrix(countData, 
                              colData = configure, 
                              design = ~condition)

dds <- DESeq(dds)
res <- results(dds, contrast = c("condition", "cancer", "normal"))
res <- as.data.frame(res)
res <- na.omit(res)
res$Gene_id <- rownames(res)
merge_res <- merge(res, inforData, by.x = "Gene_id", by.y = "Geneid", all.x = T)

res_filter <- filter(merge_res, padj <= 0.05)
res_up <- filter(res_filter, log2FoldChange >= 1)
res_down <- filter(res_filter, log2FoldChange <= -1)
res_all <- rbind(res_up, res_down)

mean(res_up$Gene_id %in% ref$ensembl_id)
mean(res_down$Gene_id %in% ref$ensembl_id)
res_up <- as.matrix(merge(res_up, ref, by.x = 'Gene_id', by.y = 'ensembl_id'))
res_down <- as.matrix(merge(res_down, ref, by.x = 'Gene_id', by.y = 'ensembl_id'))
res_all <- as.matrix(merge(res_all, ref, by.x = 'Gene_id', by.y = 'ensembl_id'))

res_up <- as.data.frame(res_up[,c(8,9,10,11,3,7,12)])
res_down <- as.data.frame(res_down[,c(8,9,10,11,3,7,12)])
res_all <- as.data.frame(res_all[,c(8,9,10,11,3,7,12)])
res_sort <- arrange(res_all, desc(log2FoldChange))

write.table(res_up, "D:/系统默认/桌面/liver_up.bed", col.names = F, row.names = F, quote = F)
write.table(res_down, "D:/系统默认/桌面/liver_down.bed", col.names = F, row.names = F, quote = F)


##########################################################################################
# Retain the position, log2FC and p-value.
FCP <- merge_data[, c(3,7:10)]
FCP <- select(FCP, c(3,4,5,1,2))

# Group the data
n1 = 5e-2
n2 = 1e-2
n3 = 5e-3
n4 = 1e-3
n5 = 5e-4

# q < 0.05
deg_filtered <- FCP


# Sort the data
deg_filtered <- deg_filtered %>% arrange(chr, start, end, log2FoldChange)
table(deg_filtered$chr)

# Remove the duplicated scores. 
dup_index <- which(duplicated(deg_filtered[,c(1:3)], fromLast = T))
if (length(dup_index) != 0){
  deg_filtered <- deg_filtered[-dup_index, ]
}

# Fold change > 1.5:log2(FC=1.5) = 0.585
deg.large.vs.lung_up <- deg_filtered[which(deg_filtered$log2FoldChange > 0),]
deg.large.vs.lung_down <- deg_filtered[which(deg_filtered$log2FoldChange < 0),]

row_names <- as.integer(rownames(deg.large.vs.lung_up))
row_names <- c(row_names, as.integer(rownames(deg.large.vs.lung_down)))

#167,167,167
g0_up <- deg.large.vs.lung_up[which(deg.large.vs.lung_up$padj > n1),]
#167,167,167
g0_down <- deg.large.vs.lung_down[which(deg.large.vs.lung_down$padj > n1),]

#246,183,198
g1_up <- deg.large.vs.lung_up[which(deg.large.vs.lung_up$padj <= n1 & deg.large.vs.lung_up$padj > n2),]
#191,203,249
g1_down <- deg.large.vs.lung_down[which(deg.large.vs.lung_down$padj <= n1 & deg.large.vs.lung_down$padj > n2),]

#244,106,139
g2_up <- deg.large.vs.lung_up[which(deg.large.vs.lung_up$padj <= n2 & deg.large.vs.lung_up$padj > n3),]
#109,139,248
g2_down <- deg.large.vs.lung_down[which(deg.large.vs.lung_down$padj <= n2 & deg.large.vs.lung_down$padj > n3),]

#245,8,65
g3_up <- deg.large.vs.lung_up[which(deg.large.vs.lung_up$padj <= n3 & deg.large.vs.lung_up$padj > n4),]
#6,57,249
g3_down <- deg.large.vs.lung_down[which(deg.large.vs.lung_down$padj<= n3 & deg.large.vs.lung_down$padj > n4),]

#161,4,42
g4_up <- deg.large.vs.lung_up[which(deg.large.vs.lung_up$padj <= n4 & deg.large.vs.lung_up$padj > n5),]
#4,37,161
g4_down <- deg.large.vs.lung_down[which(deg.large.vs.lung_down$padj <= n4 & deg.large.vs.lung_down$padj > n5),]

#95,3,25
g5_up <- deg.large.vs.lung_up[which(deg.large.vs.lung_up$padj <= n5),]
#2,21,91
g5_down <- deg.large.vs.lung_down[which(deg.large.vs.lung_down$padj <= n5),]


