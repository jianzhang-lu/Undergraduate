library(tidyverse)
cell = "Dendritic_cells	Pathological_FB	Adventitial_FB	Airway_club	Tregs	Cycling_NK_T_cells	Airway_ciliated	CD4_T_cells	Systemic_venous_endothelial_cells	Plasma_cells	CD8_T_cells	Other_FB	Alveolar_macrophages	B_cells	Tuft_like	Airway_basal	Pericytes	Monocytes	Vascular_smooth_muscle	ECM_high_epithelial	Mast_cells	Arterial_endothelial_cells	AT2	Transitioning_MDM	Inflamed_endothelial_cells	Monocyte_derived_macrophages	Intermediate_pathological_FB	NK_cells	Pulmonary_venous_endothelial_cells	Cycling_epithelial	Capillary_endothelial_cells	Neuronal_cells	Airway_goblet	Airway_smooth_muscle	Activated_B_cells	Endothelial_cells_(other)	Alveolar_FB	Endothelial_cells_(general)	Mesothelial_FB	Airway_mucous	AT1"
cell2 <- str_split(cell, "\t")
cell3 <- c(unlist(cell2))

data <- read.csv("D:/系统默认/桌面/COVID_DEG_up.covid.sort.bed", sep = "\t", header = F)
data <- data[2:nrow(data),c(1,2,3,4,6,9)]
data <- separate(data, V9, sep = ',', into = cell3)
colnames(data)[1:4] = c("Chrom", "Start", "End", "Gene_name") 

zheng <- which(data$V6 == '+')
fu <- which(data$V6 == '-')
data$Start <- as.numeric(data$Start)
data$End <- as.numeric(data$End)

data[zheng, 'Start'] = data[zheng, 'Start'] - 1000
data[zheng, 'End'] = data[zheng, 'Start'] + 1003
data[fu, 'Start'] = data[fu, 'End'] - 1003
data[fu, 'End'] = data[fu, 'End'] + 1000

no <- which(data$Start < 0)
data[no, 'Start'] <- 0
data <- data[,-5]
write.table(data, "D:/系统默认/桌面/result/COVID_DEG_up.covid.bed", sep = "\t", 
            quote = F, col.names = T, row.names = F)
