library(ggplot2)

setwd("put your wd here")
xy<-read.csv("input file name  here.csv",sep=",")
x<-as.matrix(xy[,1]) # select column where the data is
nrow(x)
summary(x)

plot<-ggplot(data = xy,aes(x=xy$x1))+
  geom_histogram(bins = 15,fill="lightgreen")
plot

n<-nrow(x)
n
k=60 ;

dx<-as.matrix(dist(x,p=2))
head(dx)

fx<-0

for(i in 1:n) {
  zz <- dx[,i]
  dv<-sort(t(zz))
  fx[i]<-1/(dv[k]^2)
}

#xfx
xfx = cbind(1:n,x,fx) 

nm=cbind("n","x","fx")

colnames(xfx) <- nm
#  xfx


pointval<-0
ii<-c("**********")
#  ii

for(i in 1:n) {
  flag<-0 
  nn<-i
  kk<-0
  obs<-1
  while (flag==0) {    
    kk<-kk+1   
    zz <- cbind(dx[,nn],xfx) 
    colnames(zz)<- c("d","nr","x","fx")
    dv<-zz[order(zz[,1]),]
    dvc <-  t(dv[1:k,4])
    ss<-which.max(dvc)
    nn<-dv[ss,2]
    if(nn==obs){flag<-1}
    if(kk==n){flag<-1}
    obs<-nn
  }
  pointval[i] <- dv[ss,2]
}


pval<-as.matrix(pointval)
# pval

fres <- cbind(x,pval,1:n) 
colnames(fres)<-c("x","pointto" ,"obs");
#  fres
summary(fres)
dd=as.data.frame(fres)
table(dd$pointto)

pmodes<-unique(fres[,2])
View(pmodes)
modes<-cbind(pmodes,x[pmodes]) 
modes  

# plot(xfx[,2],xfx[,3])


plotx<-as.data.frame(cbind(xfx,fres[,2]))
#plotx



p <- ggplot(plotx, aes(x, fx)) + geom_point() + geom_vline(xintercept = modes[,2], col="brown2") +labs(title="knn density plot + modes")
p




