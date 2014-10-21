#install required libraries;
install.packages("tm", lib="http://cran.r-project.org/web/packages/tm/");

install.packages("class", lib ="http://cran.r-project.org/web/packages/class/index.html");

install.packages("plyr", lib ="http://cran.r-project.org/web/packages/plyr/index.html");

libs<- c("tm", "plyr", "class");
lapply(libs, require, character.only= TRUE);