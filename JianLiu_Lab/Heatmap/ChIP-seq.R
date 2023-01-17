# # sort
# normal <- read.csv("D:/系统默认/桌面/normal.bed", sep = '\t', header = F)
# tumor <- read.csv("D:/系统默认/桌面/tumor.bed", sep = '\t', header = F)
# normal$gap <- normal$V3 - normal$V2
# tumor$gap <- tumor$V3 - tumor$V2
# library(tidyverse)
# normal <- normal %>% arrange(desc(gap))
# tumor <- tumor %>% arrange(desc(gap))
# write.table(normal, 'D:/系统默认/桌面/normal_sort.bed', 
#           sep = '\t', quote = F, col.names = F, row.names = F)
# 
# write.table(tumor, 'D:/系统默认/桌面/tumor_sort.bed', 
#             sep = '\t', quote = F, col.names = F, row.names = F)

#http://www.360doc.com/content/19/0221/08/52645714_816465961.shtml

library(ChIPseeker)
normal <- readPeakFile('D:/系统默认/桌面/normal.bed', head=F)
#normal <- normal[,c(1,6)]
cancer <- readPeakFile('D:/系统默认/桌面/tumor.bed', head=F)
#cancer <- cancer[,c(1,6)]
peaklist <- list('normal'=normal, 'cancer'=cancer)

# promoter annotation
library(TxDb.Hsapiens.UCSC.hg19.knownGene)
promoter <- getPromoters(TxDb.Hsapiens.UCSC.hg19.knownGene)
# figure
normalMatrix <- getTagMatrix(normal, windows = promoter)
cancerMatrix <- getTagMatrix(cancer, windows = promoter)

# tagHeatmap(normalMatrix, xlim = c(-1000,1000), color = '#e79686', title = 'normal')
# tagHeatmap(cancerMatrix, xlim = c(-1000,1000), color = '#E7475E', title = 'cancer')

peakHeatmap(peaklist, TxDb = TxDb.Hsapiens.UCSC.hg19.knownGene, upstream = 4000, downstream = 4000, color = c('#4e709d','#E7475E'))


# reference generation
normalAnno <- annotatePeak(normal, tssRegion = c(-2000,2000), TxDb=TxDb.Hsapiens.UCSC.hg19.knownGene)
cancerAnno <- annotatePeak(cancer, tssRegion = c(-2000,2000), TxDb=TxDb.Hsapiens.UCSC.hg19.knownGene)
Annolist <- list('normal' = normal, 'cancer' = cancer)

# multiply annotation/peak
# vennpie(normalAnno)
# vennpie(cancerAnno)
# library(ggupset)
# library(ggimage)
upsetplot(normalAnno, vennpie = TRUE)
upsetplot(cancerAnno, vennpie = TRUE)
# plotDistToTSS(normalAnno, title = 'Distribution of transcription factor\nbinding loci relative to TSS')
# plotDistToTSS(cancerAnno, title = 'Distribution of transcription factor\nbinding loci relative to TSS')
# peakAnnoList <- lapply(peaklist, annotatePeak, TxDb = TxDb.Hsapiens.UCSC.hg19.knownGene, tssRegion = c(-1000,1000))
# plotDistToTSS(peakAnnoList)
