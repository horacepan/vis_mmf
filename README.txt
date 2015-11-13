Files:

vis_graph.py
  - This file can be run to generate and plot various simple graphs including
  - cycle, path, complete, barbell, grid, star and wheel graphs.
  - Running the file with a specified graph type and a specified number of
    vertices will generate a graph of this type and run mmffact on the 
    graph lacplacian of the generated graph. Then it will plot the nodes
    and edges of the graph with the wavelets as functions on the graph.
  - plots are then saved inside the plots/ directory.
Commandline Options/Arguments:
  - type: cycle, path, complete, barbell, grid, star or wheel
  - n: number of vertices to construct the graph with
  - k: number of wavelets to plot. If not supplied, k defaults to the number of nodes of
       the graph
  - layout: 'spectral', 'spring', 'circular' or 'random'
      - 'spectral' will position the nodes using the eigenvectors of the graph
        laplacian
      - 'circular' will position the nodes on a circle
      - 'spring' will position the nodes using Fruchterman-Reingold force-directed algorithm
        In practice using the spring layout will more often than not, plot something
        reasonable.

Sample usages:

python vis_graph type=cycle n=15 layout=spectral
  - this plots the cycle graph on 15 vertices and plots the nodes and edges
    positioned using the eigenvectors of the graph laplacian.


python vis_graph type=barbell n=15 layout=spring
  - this plots the barbell graph(two cliques of size 15) connected by a path of length 1
    and lays out the nodes using the 'spring' layout


Notes:
In practice, this probably won't be very helpful for visualizing anything more than 30 or so
vertices because the plot just gets too cluttered.
