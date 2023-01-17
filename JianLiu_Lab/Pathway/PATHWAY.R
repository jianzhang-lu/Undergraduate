library(DOSE)
library(org.Hs.eg.db) # For Human
library(org.Mm.eg.db) # For mouse
library(topGO)
library(clusterProfiler)
library(pathview)
library(tidyverse)
library(RColorBrewer)
library(enrichplot)
library(R.utils)
library(DO.db)

# 1. GO分析
## 导入数据.
data <- read.csv('D:/系统默认/桌面/实验室/SRTP/SRTP进展/数据/pten_lkb1 VS pten.csv')
colnames(data) <- c('gene_name', 'padj', 'log2FoldChange')
data$log2FoldChange <- log2(data$log2FoldChange)


## 去重
data$sign <- case_when(
  data$log2FoldChange >= 0 ~ "+",
  data$log2FoldChange < 0 ~ "-",
)
data$log2FoldChange <- abs(data$log2FoldChange)
data <- data %>% arrange(data[,1], data[,3])
data <- data[-which(duplicated(data[, 1], fromLast = T)), ]
data[which(data$sign == '-'), 'log2FoldChange'] <- -data[which(data$sign == '-'), 'log2FoldChange']
data$sign <- NULL
  
rownames(data) <- data$gene_name
data$gene_name <- NULL
data <- na.omit(data)

## 添加上下调基因分组标签
data$group <- case_when(
  data$log2FoldChange > 1 & data$padj < 0.05 ~ "up",
  data$log2FoldChange < -1 & data$padj < 0.05 ~ "down",
  abs(data$log2FoldChange) <= 1 ~ "none",
  data$padj >= 0.05 ~ "none"
)

## 根据研究目的筛选差异基因(仅上调、下调或者全部)：
up <- rownames(data)[data$group == "up"]
down <- rownames(data)[data$group == "down"]
diff <- c(up,down)

## ID转换 (使用clusterProfiler包自带ID转换函数bitr(基于org.Hs.eg.db))
up_entrez <- bitr(up,
                  fromType = "SYMBOL",
                  toType = "ENTREZID",
                  OrgDb = "org.Mm.eg.db")

down_entrez <- bitr(down,
                    fromType = "SYMBOL",
                    toType = "ENTREZID",
                    OrgDb = "org.Mm.eg.db")

diff_entrez <- bitr(diff,
                    fromType = "SYMBOL",
                    toType = "ENTREZID",
                    OrgDb = "org.Mm.eg.db")

## Gene Ontology分析：
GO_MF_diff <- enrichGO(gene = diff_entrez$ENTREZID, 
                       OrgDb = org.Mm.eg.db, 
                       ont = "MF", 
                       pAdjustMethod = "BH",
                       pvalueCutoff = 0.05,
                       qvalueCutoff = 0.05,
                       readable = TRUE) ## 是否将gene ID映射到gene name
GO_MF_result <- GO_MF_diff@result

GO_CC_diff <- enrichGO(gene = diff_entrez$ENTREZID,
                       OrgDb = org.Mm.eg.db,
                       ont = "CC",
                       pAdjustMethod = "BH",
                       pvalueCutoff = 0.05,
                       qvalueCutoff = 0.05,
                       readable = FALSE)
GO_CC_result <- GO_CC_diff@result

GO_BP_diff <- enrichGO(gene = diff_entrez$ENTREZID,
                       OrgDb = org.Mm.eg.db,
                       ont = "BP",
                       pAdjustMethod = "BH",
                       pvalueCutoff = 0.05,
                       qvalueCutoff = 0.05,
                       readable = TRUE)
GO_BP_result <- GO_BP_diff@result

GO_all_diff <- enrichGO(gene = diff_entrez$ENTREZID,
                        OrgDb = org.Hs.eg.db,
                        ont = "ALL",
                        pAdjustMethod = "BH",
                        pvalueCutoff = 0.05,
                        qvalueCutoff = 0.05,
                        readable = TRUE)
GO_all_result <- GO_all_diff@result

write.csv(GO_BP_result, 'D:/系统默认/桌面/Pten_LKB1_KO vs Pten BP.csv')
write.csv(GO_CC_result, 'D:/系统默认/桌面/Pten_LKB1_KO vs Pten CC.csv')
write.csv(GO_MF_result, 'D:/系统默认/桌面/Pten_LKB1_KO vs Pten MF.csv')

## Figure 1
goplot(GO_MF_diff)
ggsave("D:/系统默认/桌面/GO_MF_diff.png", width = 10, height = 8, dpi = 500)
goplot(GO_CC_diff)
ggsave("D:/系统默认/桌面/GO_CC_diff.png", width = 10, height = 8, dpi = 500)
goplot(GO_BP_diff)
ggsave("D:/系统默认/桌面/GO_BP_diff.png", width = 10, height = 8, dpi = 500)

## Figure 2
barplot(
  GO_MF_diff,
  x = "Count", # "GeneRatio"
  color = "pvalue", # "pvalue" and "qvalue"
  showCategory = 20, # 显示前20(enrichResult按照p值排序)
  font.size = 12,
  title = "Molecular Function enrichment barplot",
  label_format = 30 # 超过30个字符串换行
)
ggsave("D:/系统默认/桌面/GO_MF_bar.png", width = 10, height = 8, dpi = 500)

barplot(
  GO_CC_diff,
  x = "Count", 
  color = "p.adjust",
  showCategory = 20, 
  font.size = 12,
  title = "Cellular Component enrichment barplot",
  label_format = 30
)
ggsave("D:/系统默认/桌面/GO_CC_bar.png", width = 10, height = 8, dpi = 500)

barplot(
  GO_BP_diff,
  x = "Count", 
  color = "p.adjust", 
  showCategory = 20, 
  font.size = 12,
  title = "Biology Process enrichment barplot",
  label_format = 30
)
ggsave("D:/系统默认/桌面/GO_BP_bar.png", width = 10, height = 8, dpi = 500)


barplot(
  GO_all_diff,
  x = "Count", # "GeneRatio"
  color = "pvalue", # "pvalue" and "qvalue"
  showCategory = 20, # 显示前20(enrichResult按照p值排序)
  font.size = 12,
  title = "All classes enrichment barplot",
  label_format = 30, # 超过30个字符串换行
  split='ONTOLOGY'
) + 
  facet_grid(ONTOLOGY~., scale="free")

## Figure 2 -- ggplot2
mytheme <- theme(axis.title = element_text(size = 13),
                 axis.text = element_text(size = 11),
                 plot.title = element_text(size = 14,
                                           hjust = 0.5,
                                           face = "bold"),
                 legend.title = element_text(size = 13),
                 legend.text = element_text(size = 11))

MF_top20 <- GO_MF_result[1:20, ]
ggplot(MF_top20,
       aes(x = -log10(pvalue), y = Description, fill = Count)) +
  scale_fill_distiller(palette = "RdPu",direction = 1) +
  geom_bar(stat = "identity", width = 0.8) +
  labs(x = "-log10(pvalue)", y = "Pathway", 
       title = "Molecular Function enrichment barplot") +
  theme_bw() + 
  mytheme


## Figure 2 -- pathway在柱状图里面
mytheme2 <- mytheme + theme(axis.text.y = element_blank())
MF_top20$text_x <- rep(0.03,20)
ggplot(data = MF_top20,
       aes(x = -log10(pvalue), y = Description)) +
  geom_bar(aes(fill = Count), stat = "identity", width = 0.8, alpha = 0.7) +
  scale_fill_distiller(palette = "RdPu", direction = 1) +
  labs(x = "-log10(pvalue)", y = "Pathway", 
       title = "Molecular Function enrichment barplot") +
  geom_text(aes(x = text_x, label = Description),
            hjust = 0) +
  theme_bw() + 
  mytheme2

## Figure 3
dotplot(
  GO_CC_diff,
  x = "GeneRatio",
  color = "p.adjust",
  title = "Top 20 of GO CC terms Enrichment",
  showCategory = 20,
  label_format = 30
)
ggsave("D:/系统默认/桌面/GO_CC_dot.png", width = 10, height = 8, dpi = 500)

dotplot(
  GO_MF_diff,
  x = "GeneRatio",
  color = "p.adjust",
  title = "Top 20 of GO MF terms Enrichment",
  showCategory = 20,
  label_format = 30
)
ggsave("D:/系统默认/桌面/GO_MF_dot.png", width = 10, height = 8, dpi = 500)

dotplot(
  GO_BP_diff,
  x = "GeneRatio",
  color = "p.adjust",
  title = "Top 20 of GO BP terms Enrichment",
  showCategory = 20,
  label_format = 30
)
ggsave("D:/系统默认/桌面/GO_BP_dot.png", width = 10, height = 8, dpi = 500)

# 2. KEGG分析
R.utils::setOption("clusterProfiler.download.method", "auto")
KEGG_diff <- enrichKEGG(gene = diff_entrez$ENTREZID,
                        organism = "mmu", # hsa
                        pvalueCutoff = 0.05,
                        qvalueCutoff = 0.05)

KEGG_result <- KEGG_diff@result

## 探索/调出选定的KEGG通路
## 直接跳转到对应网页，红色为富集到该通路的差异基因
browseKEGG(KEGG_diff, "hsa04610")

## Figure 1
barplot(
  KEGG_diff,
  x = "Count", 
  color = "p.adjust", 
  showCategory = 20,
  font.size = 12,
  title = "KEGG enrichment barplot",
  label_format = 30 
)

## Figure 2
dotplot(
  KEGG_diff,
  x = "GeneRatio",
  color = "p.adjust",
  title = "Top 20 of Pathway Enrichment",
  showCategory = 20,
  label_format = 30
)


# 3. GSEA
library(msigdf)
library(GseaVis)
genelist <- data$log2FoldChange
names(genelist) <- toupper(rownames(data))
genelist <- sort(genelist, decreasing = T)

myGSEA <- function(c){
  class <- msigdf.human %>%
    filter(category_code == c) %>%
    dplyr::select(geneset, symbol) %>%
    as.data.frame
  Class_GSEA <- GSEA(genelist,
                     TERM2GENE = class,
                     minGSSize = 10,
                     maxGSSize = 500,
                     pvalueCutoff = 0.05,
                     pAdjustMethod = "BH",
                     verbose = FALSE,
                     eps = 0)
  
  result <- Class_GSEA@result
  # Class_GSEA@result$Description <- 
  #   str_trunc(Class_GSEA@result$Description, width = 30, side = "right")
  return(list(result, Class_GSEA))
}

H_result_list <- myGSEA("h")
c1_result_list <- myGSEA("c1")
c2_result_list <- myGSEA("c2")
c3_result_list <- myGSEA("c3")
c4_result_list <- myGSEA("c4")
c5_result_list <- myGSEA("c5")
c6_result_list <- myGSEA("c6")
c7_result_list <- myGSEA("c7")
c8_result_list <- myGSEA("c8")

H_result <- H_result_list[[1]]
c1_result <- c1_result_list[[1]]
c2_result <- c2_result_list[[1]]
c3_result <- c3_result_list[[1]]
c4_result <- c4_result_list[[1]]
c5_result <- c5_result_list[[1]]
c6_result <- c6_result_list[[1]]
c7_result <- c7_result_list[[1]]
c8_result <- c8_result_list[[1]]


up_index <- which(c5_result$NES > 0)
down_index <- which(c5_result$NES < 0)

c5_up <- c5_result_list[[2]]@result[up_index, ]
c5_down <- c5_result_list[[2]]
## Figure 1
dotplot(c5_result_list[[2]], showCategory = 20, font.size = 10)
ggsave("D:/系统默认/桌面/GSEA_c6_dot.png", width = 10, height = 8, dpi = 500)

## Figure 2

gseaplot(c5_result_list[[2]],
         geneSetID = 1, # 取第一个pathway绘图
         by = "runningScore", # or “preranked”, “all”
         title = c5_result_list[[1]]$Description[1])


gseaplot(c5_result_list[[2]],
         geneSetID = 1,
         by = "preranked",
         title = c5_result_list[[1]]$Description[1])


gseaplot(c5_result_list[[2]],
         geneSetID = 1,
         by = "all",
         title = c5_result_list[[1]]$Description[1])
ggsave("D:/系统默认/桌面/GSEA_c5_all.png", width = 10, height = 8, dpi = 500)

# 纵坐标表示“Ranked list metric”，
# GSEA官网对此的解释是ranking metric，即signal-to-noise ratio。
# ranking metric的含义：
# 它表示基因与表型(phenotype)的关系。
# 即：这个基因与treat相关，还是与control相关，相关的度量值是多少。
# 
# positive ranking metric表示与phenotype1相关，
# negative ranking metric表示与phenotype2相关。
#
# Signal2noise：信号强度/噪声强度。
# 举例：gene A在treat组和和control组的表达量的比值。
# 上图中，对该值取log，值大于0，表示在前表型中表达量高；
# 值小于0，表示在后表型中表达量高。

gseaplot2(c5_result_list[[2]],
          geneSetID = 885,
          color = "red",
          rel_heights = c(1.5, 0.5, 1),# 子图高度
          subplots = 1:3, # 显示哪些子图
          pvalue_table = T, #是否显示pvalue表
          title = c5_result_list[[1]]$Description[885],
          ES_geom = "line") # or "dot"
ggsave("D:/系统默认/桌面/GSEA2_c5_all.png", width = 10, height = 8, dpi = 500)


gseaplot2(c5_result_list[[2]],
          geneSetID = c(772, 848),#或直接输入基因集ID向量名
          color = c("#003399", "#FF6600"),
          pvalue_table = TRUE,
          ES_geom = "line")
ggsave("D:/系统默认/桌面/GSEA2_c5_all2.png", width = 10, height = 8, dpi = 500)

# 在图上标出基因名字
gseaNb(
  object = c5_result_list[[2]],
  geneSetID = c5_result_list[[2]]@result$ID[848],
  addPval = T,
  pvalX = 0.95,
  pvalY = 0.8,
  addPoint = F,
  newCurveCol = c("#001871","#b9b4ad", "#f99f1c"),
  newHtCol = c("#001871", "white", "#f99f1c"),
  addGene = T, 
  markTopgene = T, # 是否标注Top基因
  topGeneN = 5, # 标注前多少个gene
  geneCol = 'red', # 基因名标签颜色更改
  rmSegment = T
)
ggsave("D:/系统默认/桌面/test.png", width = 10, height = 8, dpi = 500)


gseaNb(
  object = c5_result_list[[2]],
  geneSetID = c5_result_list[[2]]@result$ID[848],
  addPval = T,
  pvalX = 0.95,
  pvalY = 0.8,
  addPoint = F,
  newCurveCol = c("#001871","#b9b4ad", "#f99f1c"),
  newHtCol = c("#001871", "white", "#f99f1c"),
  addGene = c('TREX1', 'TLR9'), 
  geneCol = 'red', 
  rmSegment = F
)

# x <- readLines("D:/R_document/实验室+BMS/GSEA/c6.all.v7.5.1.symbols.gmt")
# res <- strsplit(x, "\t")
# names(res) <- vapply(res, function(y) y[1], character(1))
# res <- lapply(res, "[", -c(1:2))

# # ID转换：
# KEGG_ges_set <- setReadable(KEGG_ges,
#                             OrgDb = org.Hs.eg.db,
#                             keyType="ENTREZID")
# 
# # 转换后：
# KEGG_ges_set@result$core_enrichment[1]
