#!/usr/bin/env python

from fileutil import readFloat
import numpy as np

def findMaxIndex(array):
    max_value=-1;
    index=0
    for value in array:
        if value > max_value:
            max_value=value
            max_index=index
        index += 1
    return max_index;

""""""""""""""""""""

docs=1552
slices=12
topics=15

theta_all=readFloat("/Users/wangjian/Workspace/hopic-end/News/guardian/snowden/lda/all/theta_1.dat")

fo=open("/Users/wangjian/Workspace/hopic-end/News/guardian/snowden/lda/all/dists.dat", 'w+')

topic=[]
for index in range(docs):
    k=findMaxIndex(theta_all[index*topics:(index+1)*topics])
    topic.append(k);
    fo.write(str(k+1)+"\n")
fo.close()

docs_per_slice=readFloat("/Users/wangjian/Workspace/hopic-end/News/guardian/snowden/lda/snowden-seq-even.dat")
docs_per_slice.pop(0)

docs_per_slice_topic=np.zeros((slices,topics), dtype=np.int)

doc_i=0
for index in range(slices):
    count=0
    while (count < int(docs_per_slice[index])):
        docs_per_slice_topic[index][topic[doc_i]] += 1
        count += 1
        doc_i += 1
        
print docs_per_slice_topic
        