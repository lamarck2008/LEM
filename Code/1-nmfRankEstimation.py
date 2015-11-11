import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import nimfa
import sys, os
from optparse import OptionParser

# Read the data file
def read_data(filename):
	data_array = []
	with open(filename, 'r') as f:
		# Skip first two rows for the gct file
		for i in range(3):
			f.readline()

		for line in f:
			data = line.strip().split("\t")[2:]
			data_array.append(data)
	return np.array(data_array, dtype=float)


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

if __name__ == "__main__":
  parser = OptionParser()
  parser.add_option("-f", "--file", dest="filename",
                  help="gct file used for rank estimation", metavar="FILE")
  parser.add_option("-n", "--nrun", dest="nrun",
                    help="number of times of NMF", metavar="NRUN")
  parser.add_option("-s", "--start", dest="start",
                    help="minmum rank of data to be estimated")
  parser.add_option("-e", "--end", dest="end",
                    help="maximum rank of data to be estimated")

  (options, args) = parser.parse_args()
  file_name = options.filename
  nrun = int(options.nrun)
  start = int(options.start)
  end = int(options.end)

  data = read_data(file_name)
  print data.shape
  print 'The dimension of data is: ' + str(data.shape[0]) + ' ' + str(data.shape[1])

  res_list = []

  # dirname = os.path.split(file_name)[0]
  # parent_dir = os.path.split(dirname)[0]
  # parent_dir = os.path.split(parent_dir)[0]
  # sub_folder = os.path.split(dirname)[1]

  for i in range(nrun):
     res = factor_eval(data.T, ranks=range(start, end+1), method="nmf", max_iter=1000, nrun=20)
     res_list.append(res)
     plt.plot(range(start , end+1), res, 'r--', range(start, end+1), res, 'bo')
     plt.ylabel("cophenetic coefficient")
     plt.xlabel("Factors")
     plt.savefig(os.path.join("..", "Result") + "/" + os.path.basename(file_name) + "." + str(i) + '.pdf') 

  with open(os.path.join("..", "Result") + "/" + os.path.basename(file_name) + "." + "cophentic" + ".txt", 'w') as f:
     for res in res_list:
        f.write("\t".join(map(lambda x : str(x), res)))
        f.write("\n")    
