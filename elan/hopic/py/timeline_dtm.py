#!/usr/bin/env python
# encoding: utf-8
'''
Created on 2014年3月1日

@author: wangjian
'''
import json
from timeline import timeline

class timeline_dtm(timeline):
    '''
    Timeline generated from DTM, inherit from timeline
    '''
    def __init__(self, ntopics, nslices, voc_size, basesep, basedir):
        timeline.__init__(self, ntopics, nslices, voc_size, basesep, basedir)
    
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
            omit_label = ''
            for topic in epoch["topics"]:
                if topic_i > 2 and topic_i < self.ntopics:
                    omit_label += '.'
                    if topic_i == self.ntopics-1:
                        node_name = "slice {0} topic 2-{1}".format(slice_i, self.ntopics-1)
                        self.G.add_node(node_name, label=omit_label, shape='plaintext')
                        nodes_per_slice.append(self.G.get_node(node_name));
                else:  
                    # set node name
                    node_name = "slice {0} topic {1}".format(slice_i, topic_i)
                    # set node label
                    node_label = ""
                    for topword in topic["topwords"]:
                        node_label += topword+"\n"
                    self.G.add_node(node_name, label=node_label, shape='box')
                    nodes_per_slice.append(self.G.get_node(node_name));
                # increase index
                topic_i += 1
                node_i += 1
            slice_i += 1
            self.nodes.append(nodes_per_slice)
            
            
    def draw(self, outputfile, hasEdge=False):
        self.G.graph_attr['rankdir'] = 'LR'
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
            self.G.add_subgraph(cluster_nodes, name='cluster %d'%slice_i, rank="same", style="dotted",
                                color="blue")
        
        # output graph
        self.G.layout('dot')
        self.G.draw(outputfile)


if __name__ == '__main__':
    base_dir="/Users/wangjian/Workspace/hopic-end/News/guardian/snowden/dtm/topics_15/even/"
    graph = timeline_dtm(15, 12, 7732, 1, base_dir)
    
    graph.readTimepoints()
    graph.addNodes()
    
    graph.draw('evolution_dtm.png', False)
        