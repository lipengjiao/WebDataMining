#install required libraries;
install.packages("tm", lib="http://cran.r-project.org/web/packages/tm/");

#install.packages("class", lib ="http://cran.r-project.org/web/packages/class/index.html");
install.packages("cluster", lib="http://cran.r-project.org/web/packages/cluster/index.html");
install.packages("plyr", lib ="http://cran.r-project.org/web/packages/plyr/index.html");
install.packages("SnowballC", lib ="http://cran.r-project.org/web/packages/SnowballC/index.html");

libs<- c("tm", "plyr", "cluster", "SnowballC");
lapply(libs, require, character.only= TRUE);

#read txt files'
file <-file("/Users/pengli/Desktop/workplace/WebDataMining/Data/Ebola.uniq.txt",open="r");
tweets <- readLines(file);
file2 <-file("/Users/pengli/Desktop/workplace/WebDataMining/Data/Halloween.uniq.txt",open="r");
tweet2 <- readLines(file2);
close(file)
close(file2)

corpus  <-Corpus(VectorSource(c(tweets, tweet2)), readerControl = list(blank.lines.skip=TRUE));
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
dtm2 <- removeSparseTerms(dtm, sparse=0.98)

tdm<-as.TermDocumentMatrix(dtm2)

term_m<-as.matrix(inspect(tdm))

#calculate the distance_matrix of term frequencies
term_dm<-dist(scale(term_m),method="euclidean")

fit = hclust(term_dm, method="ward.D")

plot(fit, xlab= "term frequencies", ylab="Height")

rect.hclust(fit, k=2)

# estimate the number of clusters
wss <-(nrow(dtm)-1)*sum(apply(dtm, 2, var))


for (i in 2:15) wss[i] <- sum(kmeans(dtm,
                                     centers=i)$withinss)

plot(1:15, wss, type="b", xlab="Number of Clusters",
     ylab="Within groups sum of squares")

dtm_clu <-kmeans(x=dtm, centers=2, iter.max=40,nstart=10)



