import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import nimfa
import sys
import os

def read_data(filename):
	data_array = []
	with open(filename, 'r') as f:
		# skip first two rows
		for i in range(3):
			f.readline()
		
		for line in f:
			data = line.strip().split("\t")[2:]
			data_array.append(data)
	return np.array(data_array, dtype=float)

def get_gene_names(filename):
        gene_names = []
        with open(filename, 'r') as f:
                # skip first two rows
                for i in range(2):
                        f.readline()
                gene_names = f.readline().strip().split("\t")[2:]
        return gene_names

def save_data(data, gene_names, filename):
   dim = data.shape
   with open(filename, 'w') as f:
      # write header
      #f.write("#1.2\n")
      #f.write("%s\t%s\n" % dim)
      #f.write("Name\tfactor1\tfactor2\tfactor3\tfactor4\tfactor5\n")
      f.write("Name")
      for i in range(dim[1]):
         f.write("\t"+"factor"+str(i+1))
      f.write("\n")
#      f.write("Name\tfactor1\tfactor2\tfactor3\n")
      for i in range(dim[0]):
         #f.write(gene_names[i] + "\t")
         f.write(gene_names[i] + "\t")
         f.write("\t".join(map(lambda x: str(x), data[i, :])))
         f.write("\n")
 
def factor_eval(data, ranks, nrun=40, method="nmf", max_iter=2000):
    coefs = []
    for rank in ranks:
        fctr = nimfa.mf(data, method = method, max_iter = max_iter, rank = rank, n_run = nrun, track_factor = True)
        fctr_res = nimfa.mf_run(fctr)
        sm = fctr_res.summary()
        coef = sm['cophenetic']
        print coef
        coefs.append(coef)
    return coefs

def compute_w(data, rank, method="nmf", max_iter=2000):
   fctr = nimfa.mf(data, method=method, max_iter=max_iter, rank=rank)
   fctr_res = nimfa.mf_run(fctr)
   print "Sparseness, W: %5.4f, H: %5.4f" % fctr_res.fit.sparseness()
   return np.array(fctr_res.basis())

if __name__ == "__main__":
   parser = OptionParser()
   parser.add_option("-f", "--file", dest="filename",
                help="gct file used for rank estimation", metavar="FILE")
   parser.add_option("-r", "--rank", dest="rank",
                  help="number of columns for W matrix", metavar="NRUN")

   (options, args) = parser.parse_args()

   file_name = options.filename
   rank = options.rank

   data = read_data(file_name)
   print data.shape

   dirname = os.path.split(file_name)[0]
   parent_dir = os.path.split(dirname)[0]
   parent_dir = os.path.split(parent_dir)[0]
   sub_folder = os.path.split(dirname)[1]

   res = compute_w(data.T, rank=rank, method="nmf", max_iter=1000)
   gene_names = get_gene_names(file_name)
   save_data(res, gene_names, os.path.join(parent_dir, "Result", sub_folder) + "/" + os.path.basename(file_name) +  '.rank.' + str(rank) + '.W.txt') 
