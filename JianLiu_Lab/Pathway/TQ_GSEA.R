library(tidyverse)
library(fgsea)
library(DOSE)
library(org.Hs.eg.db)
library(topGO)
library(clusterProfiler)
library(pathview)
library(tidyverse)
library(RColorBrewer)
library(enrichplot)
library(R.utils)
library(DO.db)
library(msigdf)

# x <- readLines("D:/R_document/实验室+BMS/GSEA/msigdb.v7.5.1.symbols.gmt")
# res <- strsplit(x, "\t")
# names(res) <- vapply(res, function(y) y[1], character(1))
# res <- lapply(res, "[", -c(1:2))

genes <- read.csv("D:/R_document/实验室+BMS/GSEA/genes.csv")[,1:3]
colnames(genes) = c('gene_name', 'logFC', 'FDR')
genes <- arrange(genes, desc(logFC))

gene_list <- genes$logFC
names(gene_list) <- toupper(as.character(genes$gene_name))

myGSEA <- function(c){
  class <- msigdf.human %>%
    filter(category_code == c) %>% 
    select(geneset, symbol) %>% 
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
c5_result <- c5_result_list[[1]]

which(c5_result$ID == 'GOBP_CHROMATIN_ASSEMBLY_OR_DISASSEMBLY')
c5_result[106,]$p.adjust


gseaplot(c5_result_list[[2]],
         geneSetID = 109, # 取第一个pathway绘图
         by = "runningScore", # or “preranked”, “all”
         title = c5_result_list[[1]]$Description[109])

gseaplot2(c5_result_list[[2]],
          geneSetID = 106,
          color = "red",
          rel_heights = c(1.5, 0.5),# 子图高度
          subplots = 1:2, # 显示哪些子图
          pvalue_table = F, #是否显示pvalue表
          title = c5_result_list[[1]]$Description[106],
          ES_geom = "line")

gseaplot2(c5_result_list[[2]],
          geneSetID = 1:3,#或直接输入基因集ID向量名
          color = c("#003399", "#000000", "#FF6600"),
          pvalue_table = TRUE,
          ES_geom = "line")

# fgseaRes <- fgsea(pathways = res,
#                   stats = gene_list,
#                   minSize = 15,
#                   maxSize = 500)
# 
# topPathwaysUp <- fgseaRes[ES > 0][head(order(pval), n=10), pathway]
# topPathwaysDown <- fgseaRes[ES < 0][head(order(pval), n=10), pathway]
# topPathways <- c(topPathwaysUp, rev(topPathwaysDown))
# plotGseaTable(res[topPathways], gene_list, fgseaRes,
#               gseaParam = 0.5)
# 
# library(data.table)
# fwrite(fgseaRes, file = "D:/系统默认/桌面/pathways.csv")
# 
# 
# plotEnrichment(res[["BENPORATH_PROLIFERATION"]], gene_list) +
#   labs(title = "BENPORATH_PROLIFERATION")
# 
# plotEnrichment(res[["BIDUS_METASTASIS_UP"]], gene_list) +
#   labs(title = "BIDUS_METASTASIS_UP")
