#!/usr/bin/env python
# encoding: utf-8
'''
Created on 2014年2月26日

@author: wangjian
'''
import json
import entropy
import fileutil
import numpy as np
import pygraphviz as pgv

class timeline(object):
    '''
    display topics of each time slice
    '''

    def __init__(self, ntopics, nslices, voc_size, basesep, basedir):
        '''
        Constructor
        
        Arguments:
            - basedir (``str``) the basedir where the phi files are located
        '''
        self.ntopics = ntopics
        self.nslices = nslices
        self.voc_size = voc_size
        self.basesep = basesep
        self.basedir = basedir
        self.phi = []
        self.timepoints = []
        self.edges = []
        self.nodes = []
        self.G = pgv.AGraph(fontsize=12, fontname='ArialMT', ratio='auto')
        
        
    def readPhi(self):
        '''
        Read Topic-Word distribution data phi which is 3-dimensions array
        '''
        for slice_i in range(self.nslices):
            path = self.basedir + "phi_{0}.dat".format(slice_i+1)
            data = fileutil.readFloat(path)
            phi_per_slice = []
            for topic_i in range(self.ntopics):
                phi_per_slice.append(data[topic_i*self.voc_size:(topic_i+1)*self.voc_size])
            self.phi.append(phi_per_slice)
    
    def readTimepoints(self):
        '''
        Read Time Points from file 
        '''
        lines = fileutil.readLines(self.basedir + "timepoints.dat")
        for line in lines:
            self.timepoints.append(line);
    
    
    def addNodes(self):
        '''
        Read top-10 words of each topic in each slice 
        '''
        fo = open(self.basedir + "res.json")
        result = json.loads(fo.read(-1))
        fo.close()
        
        slice_i = 1
        node_i = 1
        
        for epoch in result["slices_topwords"]:
            nodes_per_slice = []
            topic_i = 1
            for topic in epoch["topics"]:
                # set node name
                node_name = "slice {0} topic {1}".format(slice_i, topic_i)
                # set node label
                node_label = ""
                w_i=0
                for topword in topic["topwords"]:
                    node_label += topword
                    w_i += 1
                    if w_i%3 == 0:
                        node_label += "\n"
                    else:
                        node_label += " "
                self.G.add_node(node_name, label=node_label, shape='box', width=3)
                nodes_per_slice.append(self.G.get_node(node_name));
                # increase index
                topic_i += 1
                node_i += 1
            slice_i += 1
            self.nodes.append(nodes_per_slice)


    def calcEdges(self):
        '''
        calculate the topic semantic similarity (JSD) of adjacent slices,
        and add an edge to the most similar topics
        '''
        weights=np.array([0.5, 0.5], dtype=np.float)
        # find the most similar topics between any two adjacent slices
        for slice_i in range(self.nslices-1):
            min_distance = 1
            link = [1, 1]
            # calculate the distances between any topic of the adjacent slices
            for topic_i in range(self.ntopics):
                for topic_j in range(self.ntopics):
                    freq = np.array([self.phi[slice_i][topic_i], self.phi[slice_i+1][topic_j]], dtype=np.float)
                    distance = entropy.jensen_shannon_divergence(freq, weights)
                    if distance <= min_distance:
                        min_distance = distance
                        link[0] = topic_i
                        link[1] = topic_j
            # add an edge to the most similar topics 
            self.edges.append(link)
        
    
    def draw(self, outputfile, hasEdge=False):
        self.G.graph_attr['rankdir'] = 'TB'
        self.G.graph_attr['ranksep'] = .3

        # add time points
        for slice_i in range(self.nslices):
            self.G.add_node(self.timepoints[slice_i], shape='plaintext', fontsize=14)
            if slice_i > 0:
                self.G.add_edge(self.timepoints[slice_i-1], self.timepoints[slice_i], dir='forward')
        
        # add subgraph and nodes
        for slice_i in range(self.nslices):
            cluster_nodes = self.nodes[slice_i][:]
            cluster_nodes.append(self.timepoints[slice_i])
            self.G.add_subgraph(cluster_nodes, name='cluster %d'%slice_i, style="dotted", color="black")
        
        # add edges between nodes
        if hasEdge == True:
            slice_i = 1
            for edge in self.edges:
                u="slice {0} topic {1}".format(slice_i, edge[0]+1)
                v="slice {0} topic {1}".format(slice_i+1, edge[1]+1)
                self.G.add_edge(u, v, dir="forward")
                slice_i += 1;
        
        # output graph
        self.G.layout('dot')
        self.G.draw(outputfile)


if __name__ == '__main__':
    base_dir="/Users/wangjian/Workspace/hopic-end/News/guardian/snowden/lda/topics_3/kmeans/"
    timeline = timeline(3, 12, 7732, 1, base_dir)
    
    timeline.readPhi()
    timeline.readTimepoints()
    timeline.addNodes()
    timeline.calcEdges()
    
    timeline.draw('evolution_lda_kmeans2.jpg', True)
        