#Replication simulations about
#Grund, T. (2014). Why your friends are more important and special than you
#think, Sociological Science,1, 128-140.
library(igraph)
library(intergraph)
library(faux)
library(dplyr)
#generate a ER network
n<-243
m<-517
er<-sample_gnm(n=243, m=517)
plot(er,vertex.color="lightblue" ,vertex.size=4, vertex.label=NA,main='ER network')

#generate a Watts-strogatz small world network
ws<- sample_smallworld(1, size=243, nei=2, p=0.03)
plot(ws,vertex.color="lightblue" ,vertex.size=4, vertex.label=NA,main='Smallworld network')



#Average nearest neighbor degree
nb_degree <- knn(er)[1][[1]]
hist(nb_degree)

#degree of each node
deg <- degree(er)
degree <- degree_distribution(er)
plot(degree)
hist(deg, xlim=c(0,30))

#closeness
plot(d)
cl<- closeness(er)

#betweenness
betweenness(er)

#eigenvector_centrality
ec<-eigen_centrality(er)[[1]]
hist(ec)

# produce x based on degree of each node
x<-rnorm_pre(deg, mu = 0, sd = 1, r = 0.800)
x<-round(x,2)
d <- density(x)

V(er)$X <- x
plot(density(V(er)$X))

#correlation
corr<-seq(from = 0, to = 0.8, by = 0.4)
corr<-seq(from = 0, to = 0.8, by = 0.4)
df <- tibble(a = 1:30,b = 1:30,c = 1:30,d = 1:30,e = 1:30,f = 1:30)

for (j in 1:3){
  result<- list()
  med <- list()
  for (i in 1:30){
    k<-corr[j]
    print(i)
    # produce x based on degree of each node (deg), with correlation r 
    x<-rnorm_pre(deg, mu = 0.000, sd = 1.000, r = k)
    #round x to digits 2
    x<-round(x,2)
    V(er)$X <- x
    med<-append(med,median(x,na.rm = T))
    t=0
    while(length(unique(V(er)$X))>sum(deg==0)+1){
      one <- sample(1:n, size=1)
      #if one has at least one friend
      if(length(neighbors(er,one))!=0){
        other<-sample(neighbors(er,one),1)
        vertex_attr(er, 'X', index = one) <- vertex_attr(er, 'X', index = other)
        t=t+1
      }
    }
    converage<-vertex_attr(er, 'X', index = other)
    #collecting converage result and iteration periods
    result<-append(result,converage)
    
  }
  df[[j*2-1]]<-as_numeric(result) 
  df[[j*2]]<-as_numeric(med)
}
df2<-data.frame(lapply(df, as.character), stringsAsFactors=FALSE)
write.csv(df2, "friend_er_fd.csv")


corr<-seq(from = 0, to = 0.8, by = 0.4)
df <- tibble(a = 1:30,b = 1:30,c = 1:30,d = 1:30,e = 1:30,f = 1:30)

for (j in 1:3){
  result<- list()
  med <- list()
  for (i in 1:30){
    k<-corr[j]
    print(i)
    # produce x based on degree of each node (deg), with correlation r 
    x<-rnorm_pre(deg, mu = 0.000, sd = 1.000, r = k)
    #round x to digits 2
    x<-round(x,2)
    V(er)$X <- x
    med<-append(med,median(x,na.rm = T))
    t=0
    while(length(unique(V(ws)$X))>sum(deg==0)+1){
      two <- sample(1:n, 2)
      #"one" adapt the attribute from "other"
      one <-two[1]
      other <- two[2]
      vertex_attr(ws, 'X', index = one) <- vertex_attr(ws, 'X', index = other)
      t<- t+1
    }
    converage<-vertex_attr(ws, 'X', index = other)
    converage<-vertex_attr(er, 'X', index = other)
    #collecting converage result and iteration periods
    result<-append(result,converage)
    
  }
  df[[j*2-1]]<-as_numeric(result) 
  df[[j*2]]<-as_numeric(med)
}
df2<-data.frame(lapply(df, as.character), stringsAsFactors=FALSE)
write.csv(df2, "friend_er_ran.csv")



#boxplot(as.numeric(result3),horizontal = TRUE, col = 8, ylim=c(-3,3), main='corr=0.8  random')


# add degree to the graph
V(er)$degree <- degree(er, loops = TRUE, normalized = FALSE)
V(er)$closeness<- closeness(er)
V(er)$bt<-betweenness(er)
V(er)$ec<-eigen_centrality(er)[[1]]
# get a list of neighbours, for each node
er_ngh <- neighborhood(er, mindist = 1) 

# write a function that gets the means                       
get.mean.degree <- function(x){
  mean(V(er)$degree[x])
}


# apply the function, add result to the graph
V(er)$av_degr_nei <- sapply(er_ngh, get.mean.degree)

V(ws)$av_degr_nei <- sapply(ws_ngh, get.mean.degree)
# get data into dataframe
d_vert_attr <- as_data_frame(er, what = "vertices")
wsd_vert_attr <- as_data_frame(ws, what = "vertices")

plot(wsd_vert_attr$degree,wsd_vert_attr$av_degr_nei,xlim=c(0,15) , ylim=c(0,15),
     xlab="average", ylab="average of friends", main="degree" )
