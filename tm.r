#install required libraries;
install.packages("tm", lib="http://cran.r-project.org/web/packages/tm/");

#install.packages("class", lib ="http://cran.r-project.org/web/packages/class/index.html");
install.packages("cluster", lib="http://cran.r-project.org/web/packages/cluster/index.html");
install.packages("plyr", lib ="http://cran.r-project.org/web/packages/plyr/index.html");

libs<- c("tm", "plyr", "cluster", "SnowballC");
lapply(libs, require, character.only= TRUE);

#read txt articles fro'
file <-file("/Users/pengli/Desktop/workplace/WebDataMining/Data/Ebola.uniq.txt",open="r");
tweets <- readLines(file);
close(file)

corpus  <-Corpus(VectorSource(tweets), readerControl = list(blank.lines.skip=TRUE));
#some preprocessing
corpus <- tm_map(corpus, removeWords, stopwords("english"))
corpus <- tm_map(corpus, stripWhitespace)
corpus <- tm_map(corpus, removePunctuation)

corpus <- tm_map(corpus, stemDocument)
#corpus <- tm_map(corpus, stemCompletion)
#creating term matrix with TF-IDF weighting
tf_idf <-TermDocumentMatrix(corpus,control = list(weighting = function(x)
  weightTfIdf(x, normalize = FALSE), stopwords = TRUE))
#
tf_idf2 <-DocumentTermMatrix(corpus,control = list(weighting = function(x)
  weightTfIdf(x, normalize = FALSE), stopwords = TRUE))
