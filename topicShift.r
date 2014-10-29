#install required libraries;
install.packages("tm", lib="http://cran.r-project.org/web/packages/tm/");
install.packages("cluster", lib="http://cran.r-project.org/web/packages/cluster/index.html");
install.packages("plyr", lib ="http://cran.r-project.org/web/packages/plyr/index.html");
install.packages("SnowballC", lib ="http://cran.r-project.org/web/packages/SnowballC/index.html");

libs<- c("tm", "plyr", "cluster", "SnowballC");
lapply(libs, require, character.only= TRUE);

#read txt files'
file <-file("/Users/pengli/Desktop/workplace/WebDataMining/Data/TS1989.no.braces.txt",open="r");
tweets <- readLines(file);
close(file)

corpus  <-Corpus(VectorSource(tweets), readerControl = list(blank.lines.skip=TRUE));
#some preprocessing
corpus <- tm_map(corpus, stemDocument)
corpus <- tm_map(corpus, removeWords, c(stopwords("smart"), "amp"))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, stripWhitespace)



#creating term matrix with TF-IDF weighting
#tf_idf <-TermDocumentMatrix(corpus,control = list(weighting = function(x)
#  weightTfIdf(x, normalize = FALSE), stopwords = TRUE))
#
dtm <-DocumentTermMatrix(corpus,control = list(weighting = function(x)
  weightTfIdf(x), stopwords = TRUE))

# remove sparse terms < 1%
dtm2 <- removeSparseTerms(dtm, sparse=0.99)

doc_m<-as.matrix(inspect(dtm))
doc_dm<-dist(scale(doc_m),method="euclidean")


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



