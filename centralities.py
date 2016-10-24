import networkx as nx 
from sys import argv 

def read_graph(filename):
	G = nx.Graph()
	with open(filename, 'r') as f:
		for line in f.readlines():
			u, v, w = line.split('\t')
			G.add_edge(u, v, weight=float(w))
	return G

def main():
	if len(argv) < 2:
		print 'Enter the filename of the edgelist (and not the whole path) as a command line argument'
		return 

	G = read_graph(argv[1])
	
	deg_cent = nx.degree_centrality(G)
	bet_cent = nx.betweenness_centrality(G, weight='weight')
	
	try:
		eig_cent = nx.eigenvector_centrality(G, max_iter=1000, weight='weight')
	except nx.exception.NetworkXError:
		print 'Eigenvector centrality failed to converge'
		eig_cent = {node: 'x' for node in G.nodes_iter()}
	
	try:
		pgrnk_cent = nx.pagerank(G, weight='weight')
	except nx.exception.NetworkXError:
		print 'PageRank centrality failed to converge'
		pgrnk_cent = {node: 'x' for node in G.nodes_iter()}

	with open('centrality_info_%s' % argv[1], 'w') as f:
		f.write('Node label\tDegree_centr\tBetw_cent\tEig_cent\tPageRank_cent\n')
		for node in G.nodes_iter():
			f.write('%s\t%s\t%s\t%s\t%s\n' % (node, deg_cent[node], bet_cent[node], eig_cent[node], pgrnk_cent[node]))

	print 'centralities stored at centrality_info_%s' % argv[1]   



if __name__ == '__main__':
	main()