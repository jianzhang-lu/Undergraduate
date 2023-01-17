library(tidyverse)
library(fgsea)
library(DOSE)
library(org.Mm.eg.db)
library(topGO)
library(clusterProfiler)
library(pathview)
library(RColorBrewer)
library(enrichplot)
library(R.utils)
library(DO.db)
library(msigdf)
library(ggstance)
library(ggrepel)

genes <- read.csv("D:/R_document/实验室+BMS/Pathway/Double_KO.csv")
genes$FC <- log10(genes$FC)
colnames(genes)[3] = 'logFC'
genes <- arrange(genes, desc(logFC))

gene_list <- genes$logFC
names(gene_list) <- as.character(genes$Gene)

myGSEA <- function(c){
  class <- msigdf.mouse %>%
    filter(category_code == c) %>% 
    select(geneset, mouse.symbol) %>% 
    as.data.frame
  Class_GSEA <- GSEA(gene_list,
                     TERM2GENE = class,
                     minGSSize = 10,
                     maxGSSize = 500,
                     pvalueCutoff = 0.05,
                     pAdjustMethod = "BH",
                     verbose = FALSE,
                     eps = 0)
  
  result <- Class_GSEA@result
  Class_GSEA@result$Description <- 
    str_trunc(Class_GSEA@result$Description, width = 30, side = "right")
  return(list(result, Class_GSEA))
}

c5_result_list <- myGSEA("c5")
ddd <- c5_result_list[[1]]
ddd$sign <- case_when(
  ddd$NES < 0 ~ 'down',
  ddd$NES >= 0 ~ 'up'
)

down <- filter(ddd, sign == 'down')
up <- filter(ddd, sign == 'up')
down_top <- arrange(down, NES)[1:20,]
up_top <- arrange(up, desc(NES))[1:20,]
y <- bind_rows(down_top, up_top)
ggplot(y, aes(NES, fct_reorder(Description, NES), fill = qvalues)) +
  geom_barh(stat = 'identity') +
  scale_fill_continuous(low = 'red', high = 'blue') +
  ylab(NULL)
  
ggsave("D:/系统默认/桌面/double_KO.pdf", width = 10, height = 8, dpi = 500)
write.csv(c5_result_list[[1]], 'D:/系统默认/桌面/double_KO.pathway.csv')

# DEG
DEG_up <- genes %>% filter(logFC>0, FDR <= 0.05) 
DEG <- DEG_up %>% arrange(desc(logFC))
DEG$rank = 1:nrow(DEG)
DEG_20 <- DEG[1:20,]
rownames(DEG_20) <- DEG_20$Gene

ggplot(DEG) +
  geom_point(aes(x = rank, y = logFC, color = FDR)) +
  geom_text_repel(data = DEG_20, 
                  aes(x = rank, 
                      y = logFC, 
                      label = DEG_20$Gene)) +
  scale_color_continuous(low = 'blue', high = 'red') +
  theme_classic()

ggsave("D:/系统默认/桌面/double_KO_DEG.pdf", width = 10, height = 8, dpi = 500)
write.csv(DEG_20, 'D:/系统默认/桌面/double_KO_DEGUP_20.csv')

