# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 22:09:39 2016

@author: johnzupan
"""

import sqlite3
#import operator

def createDictionary():
    '''
    '''
    conn = sqlite3.connect('IndexDB.sqlite')
    cur = conn.cursor()
    
    cur.execute('''SELECT id, keywords
                    FROM queryIndex''')
                    
    rlist = cur.fetchall()
    
    
    masterDict = {}
    #list of all the keywords
    for element in rlist:
        elementID = element[0]
        elementString = str(element[1]).split(',')
        for word in elementString:
            print elementID, word.replace(' ', '')
            word = word.replace(' ','')
            if masterDict.get(word.upper()) != None:
                masterDict[word.upper()].append(elementID)
            else:
                masterDict[word.upper()] = [elementID]
        
    return masterDict
    
    
def returnSearchResults(searchTerms, masterDict):
    '''
    '''
    searchTermsList = searchTerms.upper().split(' ')
    masterList = []
    for term in searchTermsList:
        try:
            indices = masterDict[term]
            masterList.extend(indices)
        except KeyError:
            pass
        
    returnDict = {}
    for index in masterList:
        returnDict[index] = returnDict.get(index, 0) + 1
    
    sortedReturnList = sorted(returnDict.items(), key = lambda x: x[1])[-5:]
        
        
    return sortedReturnList
    
def returnQueryResults(sortedList):
    '''
    '''
    conn = sqlite3.connect('IndexDB.sqlite')
    cur = conn.cursor()
       
    for i in sortedList:
        tableID = i[0]
        cur.execute('''SELECT Summary
                                 ,FileName
                                 ,FileLocation
                        FROM queryIndex
                        WHERE ID = ?''',(tableID,))
        queryResults = str(cur.fetchall()[0]).split(',')
        print 'Query name: ' + str(queryResults[1]).strip('u')
        print 'Query locations: ' + str(queryResults[2]).strip(')')
        print 'Query summary: ' + str(queryResults[0]).strip('(')
        print
        print
    return 'Printed top 5 results'
        
   