#install required libraries, 
#uncomment these line for the first time to run this script
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



ln1 = nrow(replies1_raw);
ln2 = nrow(replies2_raw);
ln3 = nrow(replies3_raw);

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
simJacard<-simil(as.matrix(dtm), method="Jaccard", pairwise = TRUE)
#compute the cosine similarity matrix
simCos<-simil(as.matrix(dtm), method = "cosine", pairwise = TRUE)

jacard<-as.matrix(simJacard)[,1]
cos<-as.matrix(simCos)[,1]

reply1_jacard<-jacard[2:(2+ln1-1)]
reply2_jacard<-jacard[(2+ln1):(2+ln1+ln2-1)]
reply3_jacard<-jacard[(2+ln1+ln2):(2+ln1+ln2+ln3-1)]

reply1_cos<-cos[2:(2+ln1-1)]
reply2_cos<-cos[(2+ln1):(2+ln1+ln2-1)]
reply3_cos<-cos[(2+ln1+ln2):(2+ln1+ln2+ln3-1)]

result1<-cbind(replies1_raw, reply1_jacard, reply1_cos)
result2<-cbind(replies2_raw, reply2_jacard, reply2_cos)
result3<-cbind(replies3_raw, reply3_jacard, reply3_cos)

# output result 
write.table(result1, "/Users/pengli/Desktop/workplace/WebDataMining/Data/obama.veterans.day.remarks.collected.nov13/result.reply1.txt", sep="\t", row.names= F, col.names = F, quote = F)
write.table(result2, "/Users/pengli/Desktop/workplace/WebDataMining/Data/obama.veterans.day.remarks.collected.nov13/result.reply2.txt", sep="\t", row.names= F, col.names = F, quote = F)
write.table(result3, "/Users/pengli/Desktop/workplace/WebDataMining/Data/obama.veterans.day.remarks.collected.nov13/result.reply3.txt", sep="\t", row.names= F, col.names = F, quote = F)

most_shifted1<-as.matrix(result1[result1[,4] == 0, 2])

freq_level1<-hist(reply1_cos, breaks = c(0.000, 0.00000001, 0.01, 0.02, 0.050, 0.1, 1))
freq_level2<-hist(reply2_cos, breaks = c(0.000, 0.00000001, 0.01, 0.02, 0.050, 0.1, 1))
freq_level3<-hist(reply3_cos, breaks = c(0.000, 0.00000001, 0.01, 0.02, 0.050, 0.1, 1))
freq<-NULL
freq<-rbind(freq_level1$counts, freq_level2$counts,freq_level3$counts)

sum(freq[,1])/sum(freq)
#write.table(freq, "/Users/pengli/Desktop/workplace/WebDataMining/Data/obama.veterans.day.remarks.collected.nov13/result.freq.txt", sep="\t", row.names= c("level1", "level2", "level3"), col.names = c("<0.01", "<0.05", "<0.1", "<0.2", "<0.4"), quote = F)



averaged_results<-c(mean(reply1_jacard), mean(reply1_cos))
averaged_results<-rbind(averaged_results, c(mean(reply2_jacard), mean(reply2_cos)))
averaged_results<-rbind(averaged_results,c(mean(reply3_jacard), mean(reply3_cos)))

write.table(averaged_results, "/Users/pengli/Desktop/workplace/WebDataMining/Data/obama.veterans.day.remarks.collected.nov13/mean.txt", sep="\t", row.names= c("level1", "level2", "level3"), col.names = c("Jaccard", "Cosine"), quote = F);

subtree_h11<-read.table(file= "/Users/pengli/Desktop/workplace/WebDataMining/Data/obama.veterans.day.remarks.collected.nov13/subtree.level11.txt", sep="\t", header=F, quote = "");
h11<-cleanText(subtree_h11[,2])
ln11= nrow(subtree_h11)

corpus<-Corpus(VectorSource(c(topicString,h11)))
corpus <- tm_map(corpus, removeWords, stopwords("smart"))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, stripWhitespace)
corpus <- tm_map(corpus, stemDocument)

dtm <-DocumentTermMatrix(corpus,control = list(weighting = function(x)
  weightTfIdf(x), stopwords = TRUE))


#compute jaccard similarity matrix
simJacard<-simil(as.matrix(dtm), method="Jaccard", pairwise = TRUE)
#compute the cosine similarity matrix
simCos<-simil(as.matrix(dtm), method = "cosine", pairwise = TRUE)

jacard<-as.matrix(simJacard)[,1]
cos<-as.matrix(simCos)[,1]

h11_jacard<-jacard[2:12]
h11_cos<-cos[2:12]

h11_result<-cbind(subtree_h11, h11_jacard, h11_cos)
write.table(h11_result, "/Users/pengli/Desktop/workplace/WebDataMining/Data/obama.veterans.day.remarks.collected.nov13/result_subtree.reply3.txt", sep="\t", row.names= F, col.names = F, quote = F)



x<-c(1, 2, 3)
y1<-c(0.0418, 0.034, 0.0293)
y2<-c(0.0509, 0.0306, 0.0324)
y3<-c(0.0615, 0.0253, 0.0284)

plot( x, y1, type="b", col="red" , ylim= c(0.02, 0.065), ylab = 'Cosine Similarity', xlab = 'Level', main = "Similarity - Level", xaxt="n")
axis(1, at = c(1, 2, 3))
lines( x, y2, type = "b", col="green" )
lines( x, y3, type = "b", col="blue" )

legend('topright',c('Politics','Sports', 'Pop Music'),
       fill = c("red", "green", "blue"), bty = 'n',
       border = NA)


j1<-c(0.2, 0.166, 0.201)
j2<-c(0.374, 0.158, 0.177)
j3<-c(0.487, 0.415, 0.430)

plot( x, j1, type="b", col="red" , ylim= c(0, 0.5), ylab = 'MJaccard Similarity', xlab = 'Level', xaxt="n")
axis(1, at = c(1, 2, 3))
lines( x, j2, type = "b", col="green" )
lines( x, j3, type = "b", col="blue" )
