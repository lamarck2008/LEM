library('AnnotationFuncs')
library('org.Hs.eg.db')

argv <- commandArgs(TRUE)

file.name <- argv[1]
genes.sym <- unlist(read.table(file.name, sep="\t", header=F))

genes.entrez <- unlist(translate(genes.sym, org.Hs.egSYMBOL2EG))

res.file.name <- sub('txt$', 'entrez.txt', file.name)

write.table(as.numeric(genes.entrez), res.file.name, col.names=F, row.names=F)



