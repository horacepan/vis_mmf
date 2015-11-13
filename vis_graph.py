import pdb
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os
import sys

# Replace with location of mmf
MMFFACT='/Users/hpan/mmfc/v4/src/tools/mmffact'
DATA_DIR = 'data/'
PLOT_DIR = 'plots/'
GRAPH_FUNCS = {
  'cycle': nx.cycle_graph,
  'path': nx.path_graph,
  'complete': nx.complete_graph,
  'barbell': nx.barbell_graph,
  'grid': nx.grid_2d_graph,
  'star': nx.star_graph,
  'wheel': nx.wheel_graph,
} 

LAYOUT_FUNCS = {
  'spring': nx.spring_layout,
  'circular': nx.circular_layout,
  'spectral': nx.spectral_layout,
  'random': nx.random_layout,
}

def draw_graph(graph, pos_dict, func, rownum=0, vmin=None, vmax=None, title=''):
	'''
	@param{networkx.graph} graph - a networkx graph object
	@param{dict} pos_dict - dictionary mapping node(integer) to (x,y) coordinate
	@param{dict} func - dictionary mapping node(integer) to function value
  
  Draws the graph via matplotlib and saves the figure.
	'''
	fig, ax = plt.subplots()
	nx.draw_networkx_edges(graph,pos_dict,alpha=0.4)
	nx.draw_networkx_nodes(graph,pos_dict,nodelist=func.keys(),
												 node_size=[100 + 50*abs(i) for i in func.values()],
												 node_color=func.values(),
												 cmap=plt.cm.bwr,
												 alpha=0.4,
												 vmin=vmin,
											   vmax=vmax
												)
	plt.axis('off')
	plt.title('Visualizing wavelet %d' %rownum)
	plt.savefig(PLOT_DIR + '%s_row_%d.png' %(title,rownum))

def mmffact(fname):
  '''
  @param{string} fname - name of the matrix file to run mmffact on
  @output{None}

  Runs mmffact on the matrix specified by fname.
  '''
  call = '%s %s' %(MMFFACT, fname)
  os.system(call)


def mmf_fname(fname):
  '''
  @param{string} fname
  @output{string} q_fname - the name of the Q matrix that mmffact should spit out
  '''
  i = fname.index('.')
  q_fname = fname[:i] + '.Q.dat'
  return q_fname

def make_graph(graph_type, num_vertices):
  ''' 
  @param{string} graph_type: one of the keys given in the GRAPH_FUNCS dictionary
                             defines which graph generating function to use from
                             the networkx module
  @param{int} num_vertices
  @output{networkx graph object}
  '''
  assert graph_type in GRAPH_FUNCS, '%s is not a supported graph type' %graph_type

  if graph_type == 'barbell':
    return GRAPH_FUNCS[graph_type](num_vertices, 0)
  if graph_type == 'grid':
    return GRAPH_FUNCS[graph_type](num_vertices, num_vertices)
  else:
    return GRAPH_FUNCS[graph_type](num_vertices)

def make_layout(graph, layout_type):
  assert layout_type in ['spring', 'spectral', 'circular', 'random'], \
    'Layout %s is not a supported layout type' %layout_type
  layout_func = LAYOUT_FUNCS.get(layout_type)
  return layout_func(graph)

def make_name(graph_type, num_vertices, ext=None):
  #directory = 'data'
  name = '%s_%d' %(graph_type, num_vertices)
  if ext:
    name = name + '.' + ext
  return name 

def get_cmd_options(args):
  '''
  Parses the command line options.
  Currenltly the options expected/supported are:
    -type: type of graph to generate. The supported graph types are the keys of the GRAPH_FUNCS
          dict
    -n: number of vertices
    -k: number of wavelets to plot
    -layout: denotes which layout to use for plotting the nodes/edges of the graph
            the supported layouts are the keys of the LAYOUT_FUNCS dictionary
  '''
  options = {}
  for a in args:
    eq_index = a.index('=')
    options[a[:eq_index]] = a[eq_index+1:]

  assert 'type' in options, 'Need to specify a graph type' 
  assert options['type'] in GRAPH_FUNCS, \
    '%s is not a supported graph type' %options['type']
  assert 'n' in options, 'Need to specify number of vertices'
  options['n'] = int(options['n'])
  options['k'] = int(options.get('k', options['n']))
  options['layout'] = options.get('layout', 'spring')

  return options

if __name__ == '__main__':
  args = sys.argv[1:]
  options = get_cmd_options(args)

  g = make_graph(options['type'], options['n'])
  pos_dict = make_layout(g, options['layout']) # might not be the best thing to use
  dense_laplacian = nx.laplacian_matrix(g).todense() # TODO: Support sparse/other formats
  lap_fname = make_name(options['type'], options['n'], ext='txt')
  np.savetxt(DATA_DIR + lap_fname, dense_laplacian, fmt='%.2f',
             delimiter=' ', newline='\n')

  mmffact(lap_fname)
  q_fname = make_name(options['type'], options['n'], ext='Q.dat')
  q_matrix = np.loadtxt(DATA_DIR + q_fname)
  title = make_name(options['type'], options['n'])

  # Plot the rows of the Q matrix
  #for row in range(q_matrix.shape[0]):
  for row in range(options['k']):
    wavelet_row = {j: q_matrix[row, j] for j in range(q_matrix.shape[0])}
    draw_graph(g, pos_dict, wavelet_row, rownum=row, vmin=-1, vmax=1, title=title)
  print("Finished plotting")
