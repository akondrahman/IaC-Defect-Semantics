library(ggplot2)
cat("\014") 
options(max.print=1000000)

t1 <- Sys.time()

file_to_read      <- "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Topics/results/LOCKED_3_TM_WIKI_DATASET.csv"
pred_dataset      <- read.csv(file_to_read, header=FALSE)
#dimension         <- dim(pred_dataset)
rowCnt            <- nrow(pred_dataset)
colCnt            <- ncol(pred_dataset)
defects           <- pred_dataset[, 72]
defects           <- as.factor(defects)
print("*************************")
summary(defects)
topMetIndexStart  <- 2   ## this is where the topic metric starts  
topMetIndexEnd    <- 52  ## this is where the topic metric end
for (index_ in topMetIndexStart:topMetIndexEnd)
{  
   topic_data <- pred_dataset[, index_]
   #print(topic_data)
   thePlot <- ggplot(pred_dataset, aes(x=factor(defects), y=topic_data)) +  geom_boxplot(aes(fill=defects)) + labs(x='Defect Status', y=index_)
   thePlot <- thePlot + theme_bw() + stat_summary(fun.y=mean, colour="black", geom="point", shape=18, size=3, show.legend = FALSE)
   print(thePlot)
}



# Basic box plot


# churnday_per_SLOC_plot_       <- ggplot(pred_dataset, aes(x=factor(defects), y=churnday_per_SLOC)) + geom_boxplot(aes(fill=defects))
# churn_del_per_SLOC_plot_      <- ggplot(pred_dataset, aes(x=factor(defects), y=churn_del_per_SLOC)) + geom_boxplot(aes(fill=defects))




t2 <- Sys.time()
print(t2 - t1)  # 
rm(list = setdiff(ls(), lsf.str()))