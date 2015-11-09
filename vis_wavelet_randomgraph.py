import math
import pdb
import networkx as nx
import numpy as np
from numpy.random import randn
import scipy.io
import matplotlib.pyplot as plt
import os
import sys

DIRECTORY='/Users/hpan/mmfc/v4/src/'

def random_laplacian(num_nodes, radius, ftype='txt'):
	r = nx.random_geometric_graph(num_nodes, radius)
	lapl = nx.laplacian_matrix(r)
	pos_dict = nx.get_node_attributes(r, 'pos')

	if ftype == 'txt':
		fname = DIRECTORY + 'examples/fiddle/rand_%d.txt' %(num_nodes)
		np.savetxt(fname, lapl.todense(), delimiter=' ', newline='\n')
	elif ftype == 'hb':
		fname = DIRECTORY + 'examples/fiddle/rand_%d.hb' %(num_nodes)
		scipy.io.hb_write(fname, lapl) # is this really what we want to use?
	else:
		print("Format must be txt or hb")

	return fname, pos_dict, r

def write_pos_dict(d, fname):
	f = open(fname, 'w')
	# position is saved as a list of length 2
	for k, p in d.items():
		x, y = p[0], p[1]
		f.write('%d,%f,%f\n' %(k, x, y))	
	f.close()
	
def read_pos_dict(fname):
	f = open(fname, 'r')
	d = {}
	for line in f.readlines():
		split = line.split(',')
		node = int(split[0])
		x = float(split[1])
		y = float(split[2])
		d[node] = [x,y]

	f.close()
	return d

def draw_graph(graph, pos_dict, func, rownum=0, vmin=None, vmax=None):
	'''
	graph - a networkx graph object
	pos_dict - dictionary mapping node(integer) to (x,y) coordinate
	func - dictionary mapping node(integer) to function value
	'''
	#fig = plt.figure(figsize=(8,8))
	fig, ax = plt.subplots()
	nx.draw_networkx_edges(graph,pos_dict,alpha=0.4)
	fmin = func[min(func, key=func.get)]
	fmax = func[max(func, key=func.get)]
	nx.draw_networkx_nodes(graph,pos_dict,nodelist=func.keys(),
												 node_size=[100 + 50*abs(i) for i in func.values()],
												 node_color=func.values(),
												 cmap=plt.cm.bwr,
												 alpha=0.4,
												 vmin=vmin,
											   vmax=vmax
												)
	'''
	plt.xlim(-1,1)
	plt.ylim(-1,1)
	'''
	plt.axis('off')
	plt.title('Zachs Karate Club - Visualizing Row %d' %rownum)
	plt.savefig('wavelets/zachs_karate_club_rotate3_%02d.png' %rownum)
	#plt.show()

def mmf_fname(fname, ftype):
	i = fname.index('.')
	q_fname = fname[:i] + '.Q.dat'
	return q_fname

if __name__ == '__main__':
	# make a random graph

	'''
	# Perform MMF Factorization
	lap_file = sys.argv[1]
	executable = '../../tools/mmffact'
	call = './%s %s -k=3 -nstages=5' %(executable, lap_file)
	os.system(call)
	'''

	#'''
	# make graph from gml file
	fname = sys.argv[1]
	q_fname = sys.argv[2]
	graph = nx.read_gml(fname)
	pos_dict = nx.spring_layout(graph, dim=2) 
	#pos_dict = nx.spectral_layout(graph, dim=2) 
	
	# Load the Q matrix into a numpy matrix
	q_matrix = np.loadtxt(q_fname)
	'''

	'''
	# do the drawing
	for row in range(q_matrix.shape[0]):
	#for row in range(1):
		mean = np.mean(q_matrix[row, :])
		wavelet_row = {j+1: 10*(q_matrix[row, j]) for j in range(q_matrix.shape[0])}
		#wavelet_col = {j+1:  10*q_matrix[j, row] for j in range(q_matrix.shape[0])}
		draw_graph(graph, pos_dict, wavelet_row, rownum=row, vmin=min(q_matrix[row, :]), vmax=max(q_matrix[row, :]))
	#'''
