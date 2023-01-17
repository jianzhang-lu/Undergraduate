##### The first method to draw a heatmap. #####

library(tidyverse)
library(superheat)
library(gapminder)    # the gapminder data is from this library.
library(RColorBrewer)    # brewer.pal function to choose colors.
library(scales)   # show_col function to visualize colors using #code.

# the row names are used to label the left axis. 
# If the desired labels are in a column variable, 
# the variable must be converted to row names.!!!!!!!

data(mtcars)
superheat(mtcars, scale = F)
superheat(mtcars,
          scale = TRUE,
          left.label.text.size=3,
          bottom.label.text.size=3,
          bottom.label.size = 0.05,
          row.dendrogram = T)

data(gapminder)
asia_data <- gapminder %>% 
  filter(continent == "Asia") %>% 
  select(year, country, lifeExp)
wide <- spread(asia_data, key = year, value = lifeExp)
wide <- as.data.frame(wide)
row.names(wide) <- wide$country
wide <- wide[,-1]

sort_order <- order(wide$`2007`)

colors <- rev(brewer.pal(5, "Blues"))
show_col(colors)

superheat(wide,
          scale = FALSE,
          left.label.text.size=3,
          bottom.label.text.size=3,
          bottom.label.size = 0.05,
          heat.pal = colors,
          order.rows = sort_order,
          title = "Life Expectancy in Asia",
          )

length(rownames(wide))
test <- rev(c(1:33))
# order.rows must be a vector containing the row indexes of "X".
# test can be a value of order.rows.


##### The second method to draw a heatmap. #####

# the row names are used to label the right axis.

library(tidyverse)
library(pheatmap)

# 1. (标准化方向) scale argument shoud take values: 'none', 'row' or 'column'.
pheatmap(mtcars, scale = "row")

# 2. 图形外观调整
pheatmap(mtcars, scale = "row",
         border="white", # 设置边框为白色
         cluster_cols = F, # 去掉横向, 纵向聚类
         cluster_rows = F)

# 3. 设置图例范围, legend_breaks向量中所有数值将会被显示在图例上。
pheatmap(mtcars,scale="row",
         legend_breaks=c(-2,-1,0,1,2)) # 设置图例范围

# 4. 设置横向纵向字体大小。
pheatmap(mtcars, scale="row",
         fontsize_row = 12, # 分别设置横向和纵向字体大小
         fontsize_col = 16)

# 5. 设置横向纵向聚类的树高。
pheatmap(mtcars, scale="row",
         treeheight_col = 50, # 分别设置横、纵向聚类树高
         treeheight_row = 45)

# 6. 调整纵向分组标签角度。
pheatmap(mtcars, scale="row",
         angle_col = 0) # 设置显示角度

# 7. 添加图形标题
pheatmap(mtcars, scale="row",
         main = "car")

# 8. 分别调整热图方块宽度和高度。
pheatmap(mtcars, scale="row", 
         cellwidth = 30, cellheight = 15)

# 9. 划分聚类热图区块并增加边缘线。
pheatmap(mtcars, scale="row",
         cutree_cols = 6, cutree_rows =5, # 列划为6块，行为5块
         border="#8B0A50") # 边缘线颜色
         
# 10. 在热图上显示数据并调整显示字体的大小, 颜色, 格式。
pheatmap(mtcars, scale="row",
         display_numbers = T,
         fontsize_number = 10,
         number_color="red",
         number_format = "%.2f")

# 11. 标记热图区块。
pheatmap(mtcars, scale="row",
         fontsize_number = 10,
         display_numbers = matrix(ifelse(mtcars > 1, "+", "-"), nrow(mtcars)))
## 注意写法，传递的值必须是一个矩阵。

# 12. 构建横向纵向分组信息。
annotation_row = data.frame(Class = factor(rep(c("A", "B", "C", "D"),8)))
rownames(annotation_row) <- rownames(mtcars)
pheatmap(mtcars, annotation_row =annotation_row)

annotation_col = data.frame(Day=factor(c(1:11)))
rownames(annotation_col) <- colnames(mtcars)
pheatmap(mtcars, annotation_col = annotation_col)

pheatmap(mtcars, 
         scale = "row",
         annotation_col = annotation_col,
         annotation_row = annotation_row,
         angle_col = 0)

# 13. 保存图片
pheatmap(mtcars,
         filename = "热图.pdf",
         width = 10, height = 8)  # 手动设置输出文件的宽度和高度
