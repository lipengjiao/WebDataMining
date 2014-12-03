#install required libraries, 
# uncomment these line for the first time to run this script
#install.packages("tm", lib="http://cran.r-project.org/web/packages/tm/");
#install.packages("cluster", lib="http://cran.r-project.org/web/packages/cluster/index.html");
#install.packages("plyr", lib ="http://cran.r-project.org/web/packages/plyr/index.html");
#install.packages("SnowballC", lib ="http://cran.r-project.org/web/packages/SnowballC/index.html");
#install.packages("fpc", lib = "http://cran.r-project.org/web/packages/fpc/index.html");
#install.packages("proxy", lib = "http://cran.r-project.org/web/packages/proxy/index.html")

libs<- c("tm", "plyr", "cluster", "SnowballC", "fpc", "proxy", "Matrix");
lapply(libs, require, character.only= TRUE);

# function to clean text
cleanText <- function(x) {
  # replace at people with UserID
  x = gsub("@\\w+", "", x);
  # remove html links
  x = gsub("(\\w+:\\/\\/\\S+)", "", x);
  return (x);
}


# read reply files

replies1_raw<-read.table(file= "/Users/pengli/Desktop/workplace/WebDataMining/Data/obama.veterans.day.remarks.collected.nov13/trees.leve1.txt", sep="\t", header=F, quote = "");
replies2_raw<-read.table(file= "/Users/pengli/Desktop/workplace/WebDataMining/Data/obama.veterans.day.remarks.collected.nov13/trees.leve2.txt", sep="\t", header=F, quote = "");
replies3_raw<-read.table(file= "/Users/pengli/Desktop/workplace/WebDataMining/Data/obama.veterans.day.remarks.collected.nov13/trees.leve3.txt", sep="\t", header=F, quote = "");

reply1<-cleanText(replies1_raw[,2])
reply2<-cleanText(replies2_raw[,2])
reply3<-cleanText(replies3_raw[,2])

# read topic files:
topicFile = file("/Users/pengli/Desktop/workplace/WebDataMining/Data/obama.veterans.day.remarks.collected.nov13/obama.remarks.nov8.txt", open = "r")
topicString<-paste(readLines(topicFile), collapse=" ")
close(topicFile)



corpus<-Corpus(VectorSource(c(topicString, reply1, reply2, reply3)))
corpus <- tm_map(corpus, removeWords, stopwords("smart"))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, stripWhitespace)
corpus <- tm_map(corpus, stemDocument)

#creating term matrix with TF-IDF weighting
dtm <-DocumentTermMatrix(corpus,control = list(weighting = function(x)
  weightTfIdf(x), stopwords = TRUE))


# remove sparse terms < 1%
# dtm2 <- removeSparseTerms(dtm, sparse=0.99)

#compute jaccard similarity matrix
sim<-simil(as.matrix(dtm), method="fJaccard", pairwise = TRUE)




#doc_m<-as.matrix(inspect(dtm))
#doc_dm<-dist(scale(doc_m),method="euclidean")


#write.csv(inspect(dtm2), file = "/Users/pengli/Desktop/workplace/WebDataMining/Data/TS1989.csv")

fit = hclust(doc_dm, method="ward.D")

plot(fit, xlab= "term frequencies", ylab="Height")

rect.hclust(fit, k=2)

# estimate the number of cluster
wss <-(nrow(dtm)-1)*sum(apply(dtm, 2, var))


for (i in 2:15) wss[i] <- sum(kmeans(dtm,
                                     centers=i)$withinss)

plot(1:15, wss, type="b", xlab="Number of Clusters",
     ylab="Within groups sum of squares")

dtm_clu <-kmeans(x=dtm, centers=2, iter.max=40,nstart=10)



