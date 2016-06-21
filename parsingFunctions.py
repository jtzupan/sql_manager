# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 08:28:06 2016

@author: tzupan
"""

import re
import os
import os.path
import time

def parseQuery(filename):
    '''
    Given a SQL file, finds the keywords and summary, as well as create and 
    modify information for the query.
    
    INPUT:
        fileName(str): name of a .sql file
    OUPUT:
        summaryList(str): the summary from the SQL file
        keywordList(str): the keywords from the SQL file
        lastModifiedDatetime(date): when the file was last modified
        lastUpdateID(float): time, in seconds, of when the file was last modified
    '''
    
    fileIn = open(filename,'rb+').read()
    queryString = ''
    for letter in list(fileIn):
        if letter!= '\x00':
            queryString += letter.strip('\r\n')
    
    summaryPattern = re.compile(r'SUMMARY: (.*)<end>KEY', re.DOTALL)
    keywordPattern = re.compile(r'KEYWORDS: (.*)<end>', re.DOTALL) 

#   variables to be returned  (as lists)      
    summaryList = re.findall(summaryPattern, queryString)     
    keywordList = re.findall(keywordPattern, queryString)
    lastModifiedDatetime = time.ctime(os.path.getmtime(filename))
    lastUpdateID = os.path.getmtime(filename)
            
    
    return ''.join(summaryList), ''.join(keywordList), str(lastModifiedDatetime), str(lastUpdateID)