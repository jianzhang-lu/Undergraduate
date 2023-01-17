g_l <- read.table('D:/python 文件/lab/gencode.v19.gene.length.txt',sep='\t', head=T)
# normal
gene <- read.table('D:/系统默认/桌面/lung_normal.txt',sep='\t',head=TRUE)

# get the length for genes in the bed file
ng1 = intersect(gene$Geneid, g_l$ensembl_id)
# length of each gene
lengths1 = g_l[match(ng1, g_l$ensembl_id), 3]
names(lengths1) <- g_l[match(ng1, g_l$ensembl_id), 1]
gene_name <- g_l[match(ng1,g_l$ensembl_id), 2]

# only take the gene showed in the reference, 
# so filter some gene that are not common, 
# bed is still the raw counts information
# common information for the gene
g1 <- gene[,c(1:5)]
# raw count for each cells only
bed1 <- gene[,c(7)]
length(bed1)
# total raw counts found in the cell for all genes
# total_count1 <- colSums(bed1)
total_count1 <- sum(bed1)
#nm_fpkm1 <- t(do.call(rbind,lapply(1:length(total_count1),function(i){10^9*bed1[,i]/lengths1/total_count1[i]})))
nm_fpkm1 <- 10^9*bed1/lengths1/total_count1
length(nm_fpkm1)
# fpkm for all cells
#dim(nm_fpkm1)
#nm_fpkm1 <- nm_fpkm1[which((rowSums(nm_fpkm1)/(length(colname)-2)) > 1),]
#g1 <- g1[which(g1$Geneid%in%rownames(nm_fpkm1)),]
g1 <- g1[which(g1$Geneid %in% names(nm_fpkm1)),]
b1 <- cbind(gene_name, as.data.frame(g1), nm_fpkm1)
b1 <- b1[which(b1$nm_fpkm1 > 0),]
#DEG.gene <- gsub("\\..*", "",  b1$Geneid)
# calculate duplicated gene
t <- b1$gene_name
t <- t[duplicated(t)]
length(t)
t <- t[which(t != 'NA')]
length(t)
print(t)
dim(gene)
dim(b1)

#DEG.resdata <- apply(DEG.resdata,2,as.character)
write.table(b1, file='D:/系统默认/桌面/lung_normal.tsv',col.names=T, row.names=F, quote=F,sep='\t')

