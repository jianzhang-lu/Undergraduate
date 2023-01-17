library(tidyverse)
library(Seurat)
library(patchwork)
library(Matrix)

pbmc.data <- Read10X("GP_practical/P6/pbmc3k_filtered_gene_bc_matrices/filtered_gene_bc_matrices/hg19/")
class(pbmc.data)
dim(pbmc.data)
pbmc.data[1:6,1:6]

# 1 quality control
# 1.1 Set the object and filter.
pbmc <-  CreateSeuratObject(counts = pbmc.data, 
                            project = "pbmc", 
                            min.cells = 3, 
                            min.features = 200)
dim(pbmc)
class(pbmc)
slotNames(pbmc)

# 1.2 Calculate the percentage of mitochondria genome.
pbmc[["percent.mt"]] <-  PercentageFeatureSet(pbmc, pattern = "^MT-")

# 1.3 Visualize QC metrics as a violin plot.
VlnPlot(pbmc, features = c("nFeature_RNA", "nCount_RNA", "percent.mt"), 
        ncol = 3, pt.size = 0)
summary(pbmc[["nFeature_RNA"]])
summary(pbmc[["nCount_RNA"]])
summary(pbmc[["percent.mt"]])

# 1.4 Visualize feature-feature relationships.
plot1 <- FeatureScatter(pbmc, feature1 = "nCount_RNA", 
                       feature2 = "percent.mt")
plot2 <- FeatureScatter(pbmc, feature1 = "nCount_RNA", 
                       feature2 = "nFeature_RNA")
plot1 + plot2

# 1.5 Subset the data.
pbmc <-  subset(pbmc, nFeature_RNA > 200 & 
                  nFeature_RNA < 6000 & 
                  percent.mt < 10)
dim(pbmc)

# 2 Normalize the data.
pbmc <-  NormalizeData(pbmc, 
                       normalization.method = "LogNormalize", 
                       scale.factor = 10000)
pbmc[["RNA"]]@data
# 3 Identification of highly variable features (feature selection).
pbmc <- FindVariableFeatures(pbmc, 
                             selection.method = "vst",
                             nfeatures = 2000)

top10 <- head(VariableFeatures(pbmc), 10)

plot1 <- VariableFeaturePlot(pbmc)
plot2 <- LabelPoints(plot = plot1, points = top10, repel = T)
plot2

# 4 Scale the data
all.genes <- rownames(pbmc)
pbmc <- ScaleData(pbmc, features = all.genes)
p1 <- pbmc[["RNA"]]@scale.data["CST3", ]
p2 <- pbmc[["RNA"]]@scale.data["TYROBP", ]
p3 <- pbmc[["RNA"]]@scale.data["LST1", ]

n1 <- pbmc[["RNA"]]@scale.data["MALAT1", ]
n2 <- pbmc[["RNA"]]@scale.data["LTB", ]
n3 <- pbmc[["RNA"]]@scale.data["IL32", ]

hist(p1)
hist(p2)
hist(n1)
hist(n2)
hist(p3)
hist(n3)

# 5 Perform linear dimensional reduction
pbmc <- RunPCA(pbmc, features = VariableFeatures(object = pbmc))
print(pbmc[["pca"]], dims = 1:5, nfeatures = 5)

VizDimLoadings(pbmc, dims = 1:2, reduction = "pca")
DimPlot(pbmc, reduction = "pca")

DimHeatmap(pbmc, dims = 1, cells = 500, balanced = T, legend = T)
DimHeatmap(pbmc, dims = 1:15, cells = 500, balanced = T)

# 6 Determine the dimensionality.
ElbowPlot(pbmc)

# 7 Cluster the cells.
pbmc <- FindNeighbors(pbmc, dims = 1:10)
pbmc <- FindClusters(pbmc, resolution = 0.5)
head(Idents(pbmc), 5)

# 8 Run non-linear dimensional reduction (UMAP/t-SNE)
pbmc <- RunTSNE(pbmc, dims = 1:10)
DimPlot(pbmc, reduction = "tsne", label = T)

pbmc <- RunUMAP(pbmc, dims = 1:10)
DimPlot(pbmc, reduction = "umap", label = T)

# 9 CD86 expression in different clusters.
FeaturePlot(pbmc, features = c("CD86"), reduction = "umap")
VlnPlot(pbmc, features = c("CD86"), slot = "count", log = T)
VlnPlot(pbmc, features = c("CD86"), log = T)

# 10 Finding differentially expressed features (cluster biomarkers)
cluster0.markers <- FindMarkers(pbmc, ident.1 = 0, min.pct = 0.25)
cluster58.markers <- FindMarkers(pbmc, ident.1 = c(5,8), min.pct = 0.25)

head(cluster0.markers, n = 6)

FeaturePlot(pbmc, features = c("MS4A1", "GNLY", "CD3E", 
                               "CD14", "FCER1A", "FCGR3A", 
                               "LYZ", "PPBP", "CD8A"), reduction = "umap")

VlnPlot(pbmc, features = c("MS4A1", "GNLY", "CD3E", 
                           "CD14", "FCER1A", "FCGR3A", 
                           "LYZ", "PPBP","CD8A"), 
        slot = "counts", log = TRUE)
