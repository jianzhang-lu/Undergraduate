library(tidyverse)
library(Seurat)
library(patchwork)
library(Matrix)
library(SingleR)
library(celldex)
library(SeuratDisk)
library(patchwork)
library(data.table)
library(hdf5r)

setwd("Lab/scRNA-seq/Data")

# 1. Liver cancer
lc_barcode <- read.csv("Liver cancer GSE151530/information.txt", 
                       sep = '\t')

lc_matrix <- Read10X("Liver cancer GSE151530/")
liver_cancer <-  CreateSeuratObject(counts = lc_matrix,
                                    project = "liver_cancer",
                                    min.cells = 3,
                                    min.features = 200)

fwrite(x = as.data.frame(liver_cancer@assays[["RNA"]]@counts), 
       row.names=T, file = "Liver cancer GSE151530/raw_counts.csv")

lc_counts <- fread(input = "Liver cancer GSE151530/raw_counts.csv")


# 2. Liver normal
ln_barcode <- read.csv("Liver normal GSM4648565/information.csv",
                       sep = ',', header = F)
colnames(ln_barcode)[1] = 'barcode'
ln_barcode <- separate(ln_barcode, 2, sep = ' \\(', into = c('big', 'small'))
ln_barcode$small <- gsub('[)]', '', ln_barcode$small)

Convert('Liver normal GSM4648565/raw_counts.h5ad', "h5seurat",
        overwrite = TRUE, assay = "RNA")

ln_matrix <- LoadH5Seurat("Liver normal GSM4648565/raw_counts.h5seurat")
fwrite(x = as.data.frame(ln_matrix@assays[["RNA"]]@counts), 
       row.names=T, file = "Liver normal GSM4648565/raw_counts.csv")

ln_counts <- fread(input = "Liver normal GSM4648565/raw_counts.csv")



# 3. Neuron cancer
nc <-  Read10X_h5("Neuron cancer GSM4186968/raw_count.h5")
nc_matrix <- CreateSeuratObject(counts = nc, 
                                project = "nc", 
                                min.cells = 3, 
                                min.features = 200)

fwrite(x = as.data.frame(nc_matrix@assays[["RNA"]]@counts), 
       row.names=T, file = "Neuron cancer GSM4186968/raw_counts.csv")

nc_counts <- fread(input = "Neuron cancer GSM4186968/raw_counts.csv")
nc_barcode <- fread(input = 'Neuron cancer GSM4186968/metadata.csv')[,1:2]
nc_barcode$V1 <- gsub('.+\\-', '', nc_barcode$V1, fixed = F)



# liver_normal <- Read10X("Lab/scRNA-seq/GSM4955422_liver_normal/")
# liver_normal[1:6,1:6]
# normal <-  CreateSeuratObject(counts = liver_normal, 
#                               project = "liver_normal", 
#                               min.cells = 3, 
#                               min.features = 200)
# normal[["percent.mt"]] <-  PercentageFeatureSet(normal, pattern = "^MT-")
# normal <-  subset(normal, nFeature_RNA > 200 & 
#                   nFeature_RNA < 6000 & 
#                   percent.mt < 10)
# 
# # 单细胞注释
# hpca.se <- celldex::HumanPrimaryCellAtlasData()
# normal_for_SingleR <- GetAssayData(normal, slot="data")
# normal.hesc <- SingleR(test = normal_for_SingleR, 
#                        ref = hpca.se, 
#                        labels = hpca.se$label.main)
# 
# length(normal.hesc@rownames)
# 
# length(normal.hesc$labels)
