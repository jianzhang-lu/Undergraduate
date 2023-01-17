library(NormalyzerDE)
## Example dataset
outDir <- tempdir("D:/R_document/GP_practical/P8/sumExpRun")
designFp <- system.file(package="NormalyzerDE", "extdata",
                        "tiny_design.tsv")

dataFp <- system.file(package="NormalyzerDE", "extdata",
                      "tiny_data.tsv")

normalyzer(jobName="vignette_run", designPath=designFp,
           dataPath=dataFp,outputDir=outDir)


## Real dataset
outDir <- tempdir("D:/R_document/GP_practical/P8/sumExpRun")
dataMatrix <- read.table(file = "GP_practical/P8/proteinGroups.txt", 
                         sep = "\t", header = TRUE)

designMatrix <- read.table(file = "GP_practical/P8/experiment_design.txt", 
                           sep = "\t", header = TRUE)

designMatrix$sample <- as.character(designMatrix$sample)

dataOnly <- dataMatrix[, designMatrix$sample]
annotOnly <- dataMatrix[, !(colnames(dataMatrix) %in%
                              designMatrix$sample)]

sumExpObj <- SummarizedExperiment::SummarizedExperiment(
  as.matrix(dataOnly), colData=designMatrix, rowData = annotOnly)

normalyzer(jobName = "sumExpRun", experimentObj = sumExpObj,
           outputDir = outDir)

## Other dataset
outDir <- tempdir("D:/R_document/GP_practical/P8/sumExpRun")
dataMatrix <- read.table(file = "GP_practical/P8/phosphopeptideSites.txt", 
                         sep = "\t", header = TRUE)

designMatrix <- read.table(file = "GP_practical/P8/experiment_design.txt", 
                           sep = "\t", header = TRUE)

designMatrix$sample <- as.character(designMatrix$sample)

dataOnly <- dataMatrix[, designMatrix$sample]
annotOnly <- dataMatrix[, !(colnames(dataMatrix) %in%
                              designMatrix$sample)]

sumExpObj <- SummarizedExperiment::SummarizedExperiment(
  as.matrix(dataOnly), colData=designMatrix, rowData = annotOnly)

normalyzer(jobName = "sumExpRun2", experimentObj = sumExpObj,
           outputDir = outDir)



