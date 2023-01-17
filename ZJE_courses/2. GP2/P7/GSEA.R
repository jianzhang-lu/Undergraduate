library(fgsea)
library(ggplot2)
data(examplePathways)
data(exampleRanks)

examplePathways[1]
fgseaRes <- fgsea(pathways = examplePathways,
                  stats = exampleRanks,
                  minSize = 15,
                  maxSize = 500)
data <- fgseaRes
sum(fgseaRes[, padj < 0.01])

# Plot a single pathway
plotEnrichment(examplePathways[["5991130_Programmed_Cell_Death"]], exampleRanks) + 
  labs(title="Programmed Cell Death")

# plot the most significantly enriched pathway
plotEnrichment(examplePathways[[head(fgseaRes[order(pval), ], 1)$pathway]],
               exampleRanks) + labs(title=head(fgseaRes[order(pval), ], 1)$pathway)

# Now you can make a table plot for a bunch of selected pathways
topPathwaysUp <- fgseaRes[ES > 0][head(order(pval), n=10), pathway]
topPathwaysDown <- fgseaRes[ES < 0][head(order(pval), n=10), pathway]
topPathways <- c(topPathwaysUp, rev(topPathwaysDown))
plotGseaTable(examplePathways[topPathways], exampleRanks, fgseaRes,
              gseaParam = 0.5)

# Eliminate the duplicates
collapsedPathways <- collapsePathways(fgseaRes[order(pval)][padj < 0.01],
                                      examplePathways, exampleRanks)
mainPathways <- fgseaRes[pathway %in% collapsedPathways$mainPathways][order(-NES), pathway]
plotGseaTable(examplePathways[mainPathways], exampleRanks, fgseaRes,
              gseaParam = 0.5)

# Output the data.
library(data.table)
fwrite(fgseaRes, file="fgseaRes.txt", sep="\t", sep2=c("", " ", ""))

# For the top gene set the “leading edge” genes are the following 

fgseaRes[order(pval),][1,]$leadingEdge

# You can get the number of genes in the leading edge 
length(fgseaRes[order(pval),][1,]$leadingEdge[[1]])
length(examplePathways[[fgseaRes[order(pval),][1,]$pathway]])
length(examplePathways[['5990979_Cell_Cycle,_Mitotic']])

