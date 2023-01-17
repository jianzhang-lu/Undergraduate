library(DESeq2)
library(tidyverse)
# 1. Download and load the data
download.file(url = "https://raw.githubusercontent.com/hugocarlos/public_scripts/master/teaching/naive_primed_hESC_RNAseq_readcount.txt",
              destfile = "naive_primed_hESC_RNAseq_readcount.txt")
readcount <- read.delim("GP_practical/P4/naive_primed_hESC_RNAseq_readcount.txt")

# 2. Data quality control for read counts.
# Include: how many counts in total and number of genes got covered.
total.cov <- apply(readcount[,-9], 2, sum)
barplot(total.cov, las = 2, 
        ylab = "log10(total counts over genes)", cex.axis = 0.7, cex.lab = 0.9)

genecovered <- apply(readcount[ ,-9], 2, function(x) sum(x > 0))
barplot(genecovered, las = 2, ylab = "genes covered", cex.axis = 0.7, cex.lab = 0.9)

# 3. Calculating RPKM
rpk <- readcount / readcount$exonlength * 1000
rpkm <- rpk[,-9]
for (i in 1:8){
  rpkm[,i] <- rpk[,i] / total.cov[i] * 10^6
}

# 4. Load data into DESeq2
readcount <- read.table("GP_practical/naive_primed_hESC_RNAseq_readcount.txt",
                        header = TRUE, row.names = 1)
configure <- data.frame(condition = factor(rep(c("naive", "primed"), each = 4)),
                        type = rep(c("r1", "r2", "r3", "r4"), 2))

dds <- DESeqDataSetFromMatrix(countData = readcount[ ,-9],
                               colData = configure,
                               design = ~ condition)

# 5. Variance stabilizing transformation (vst) and rlog
vsd <- vst(dds, blind = FALSE)
head(assay(vsd), 3)
colData(vsd)

rld <- rlog(dds, blind = FALSE)
head(assay(rld), 3)
colData(rld)

library(dplyr)
library(hexbin)
dds <- estimateSizeFactors(dds)
df <-  bind_rows(
  as_tibble(log2(counts(dds, normalized = TRUE)[ , 1:2] + 1))
  %>% mutate(transformation = "log2(x + 1)"),
  as_tibble(assay(vsd)[ , 1:2]) %>% mutate(transformation = "vst"),
  as_tibble(assay(rld)[ , 1:2]) %>% mutate(transformation = "rlog"))
colnames(df)[1:2] = c("x", "y")

ggplot(df, aes(x = x, y = y)) + geom_hex(bins = 80) +
  coord_fixed() + facet_grid(.~ transformation)

# 6. Sample distance
sampleDists <- dist(t(assay(vsd)))

## Heatmap and PCA
library(pheatmap)
library(RColorBrewer)
sampleDistMatrix <- as.matrix(sampleDists)
colors <- colorRampPalette(rev(brewer.pal(9, "Blues")))(255)
pheatmap(sampleDistMatrix,
         clustering_distance_rows = sampleDists,
         clustering_distance_cols = sampleDists,
         col = colors,
         angle_col = 90)

plotPCA(vsd)

# 7. Differential expression analysis with DESeq2.
dim(counts(dds))
keep <- rowSums(counts(dds)) >= 10
dds <- dds[keep, ]
dds <- DESeq(dds)
res <- results(dds)
write.csv(res, file = "hESC_DESeq2_output.csv")
summary(res)

# 8. Filter the data.
res.05 <- results(dds, alpha = 0.05)
table(res$padj < 0.05)
summary(res.05)

resLFC1 <- results(dds, lfcThreshold = 2)
summary(resLFC1)

resBoth <- results(dds, lfcThreshold = 2, alpha = 0.05)
summary(resBoth)

# 9 Multiple testing
resSig <- subset(res, padj < 0.05)
head(resSig[order(resSig$log2FoldChange), ])
head(resSig[order(resSig$log2FoldChange, decreasing = TRUE), ])

# Visualization
## Count plot
topGene <- rownames(res)[which.min(res$padj)]
plotCounts(dds, gene = topGene)

d <- plotCounts(dds, gene = topGene, intgroup = "condition", returnData = TRUE)
### Plotting the MOV10 normalized counts, using the condition (rownames of d as labels)
library(ggrepel)
ggplot(d, aes(x = condition, y = count, color = condition)) +
  geom_point(position = position_jitter(w = 0.1, h = 0)) +
  geom_text_repel(aes(label = rownames(d))) +
  theme_bw() +
  ggtitle(topGene) +
  theme(plot.title = element_text(hjust = 0.5))

## MA plot
plotMA(res)

## Histogram
hist(res$pvalue[res$baseMean > 1], breaks = 0:20/20,
     col = "grey50", border = "white")

## Heatmap
library(genefilter)
topVarGenes <- head(order(rowVars(assay(vsd)), decreasing = TRUE), 20)
mat <- assay(vsd)[topVarGenes, ]
pheatmap(mat)

mat <- mat - rowMeans(mat)
pheatmap(mat)

mat <- rpkm[topVarGenes, ]
pheatmap(mat)

pheatmap(log2(mat+1))

