# pool the simulated W matrix
library(MASS)

argv <- commandArgs(TRUE)

file.name <- argv[1]
print(basename(file.name))

# now pool all W together
w.mat.ds <- data.frame(read.table(file.name, sep="\t", header=T))
w.mat <- w.mat.ds[,-1]
w.pool <- c()

for(j in 1:dim(w.mat)[2]) {
	w <- w.mat[, j]
	w.pool <- rbind(w.pool, w)
}

dW <-  density(w.pool, bw=0.05)
dW.x <- dW$x
dW.y <- dW$y * 0.05
rate <- round(fitdistr(w.pool, 'exponential')$estimate)
w.fit <- rexp(length(w.pool), rate=rate)
dsW <- density(w.fit, bw=0.05)
dsW.x <- dsW$x
dsW.y <- dsW$y * 0.05

dname <- dirname(file.name)
bname <- basename(file.name)
of.name <- file.path(dname, sub(".txt", "w.mat.pdf", bname))

pdf(of.name)

plot(dW.x, dW.y, lty=2, xlim=c(0, 14), ylim=c(0, 0.5), main=paste("Density plot of pooled W matrix"), xlab="Coefficient", ylab='Probability', type="l")
lines(dsW.x, dsW.y, lty=2, col='red')
legend("topright", legend=c("Pooled W", "Fitted Exponential Distr"), col=c('black', 'red'), pch="-")


plot(dW.x, dW.y, lty=2, xlim=c(0, 14), ylim=c(0, 0.2), main=paste("Zoomed Density plot of pooled W matrix"), xlab="Coefficient", ylab='Probability', type="l")
lines(dsW.x, dsW.y, lty=2, col='red')
legend("topright", legend=c("Pooled W", "Fitted Exponential Distr"), col=c('black', 'red'), pch="-")

for(i in 1:dim(w.mat)[2]) {
	plot(ecdf(w), cex=0, lty=2, main=paste("CDF of factor", i), xlab="Coefficient", ylab="Probability", xlim=c(0,14)) 
	lines(ecdf(w.fit), cex=0, col='red', lty=2)
	abline(h=0.95, lty=2, col='gray')
	legend("topright", legend=c(paste("factor", i), "Fitted Exponential Distr"), col=c('black', 'red'), pch="-")
	legend("center", legend=c(paste("rate:", rate), paste("p-value 0.05:", round(qexp(0.95, rate), 2))))	
}

dev.off() 
