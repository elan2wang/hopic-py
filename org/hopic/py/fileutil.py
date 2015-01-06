#!/usr/bin/env python
# encoding: utf-8
"""
:mod:`org.hopic.py.fileutil`
===========================

File Operation.
"""
import os

def readFloat(filepath=None):
    fo=open(filepath, "rb")
    lines=fo.readlines()
    fo.close()
    
    data=[]
    for line in lines:
        value=float(line.strip('\n'))
        data.append(value)

    return data

def readLines(filepath=None):
    fo = open(filepath, 'rd')
    lines = fo.readlines()
    fo.close()
    
    data=[]
    for line in lines:
        value=line.strip('\n')
        data.append(value)

    return data

def rename(basedir=None):
    for file in os.listdir(basedir):
        if file == 'parse' or file == 'old': continue
        
        newname = file
        num = file.split('_')[0]
        filename = file.split('_')[1]
        if len(num) < 4 :
            zeros = 4 - len(num)
            while zeros > 0:
                num = '0'+num
                zeros -= 1
            newname = num+"_"+filename
        
        print newname
        os.rename(basedir+file, basedir+newname)
        
    