### This script is used to assign membership to each gene

### load library

### read W matrix
argv <- commandArgs(TRUE)
file.name <- argv[1]
thred <- as.numeric(argv[2])
w.mat.ds <- data.frame(read.table(file.name, sep="\t", header=T))
w.mat <- w.mat.ds[, -1]

### function used to threshold W matrix
thred.func <- function(v, thred){
	## v is the factor to be processed
	## thred is the threshold
	v.thred <- v
	for(i in 1:length(v)){
		#print(i)
		if(v.thred[i] < thred){
			v.thred[i] <- 0
		}
		else{
			v.thred[i] <- v[i]
		}
	}
	return(v.thred)
}

w.mat.thred <- w.mat
# threshold used to discritize W matrix
num.factors <- dim(w.mat)[2]
for(i in 1:dim(w.mat)[1]){
	w.mat.thred[i, ] <- thred.func(w.mat[i, ], thred)
}

### assign membership
genes <- w.mat.ds[,1] 
memberships <- vector('numeric', length(genes))
for(i in 1:dim(w.mat)[1]){
	d <- w.mat.thred[i, ]
	if(sum(d) == 0){
		memberships[i] <- 0
		next
	}
	ind <- which(d == max(d))
	ind <- ind[1]
	memberships[i] <- ind
}
res <- cbind(as.character(genes), memberships)
colnames(res) <- c("genes", "memberships")
res.name <- sub('txt', paste('membership', 'rank', dim(w.mat)[2], 'txt', sep='.'), file.name)
write.table(res, sep="\t", row.names=F, file=res.name)

# also write each class of genes except metagene 0
rank <- dim(w.mat)[2]
for( i in 1:rank) {
	ind <- which(memberships == i)
	g <- as.character(genes[ind])
	res.file.name <- sub('txt', paste('membership', 'rank', dim(w.mat)[2], paste('metagene', i, sep="_"), 'txt', sep='.'), file.name)
	write.table(g, sep="\t", row.names=F, col.names=F, file=res.file.name)
}

