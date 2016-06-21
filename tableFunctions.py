# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 08:12:57 2016

@author: tzupan
"""

import sqlite3
import os
import os.path
import time
import parsingFunctions as pf
reload(pf)

def createTable():
    '''
    Creates a base table called queryIndex, if this table does not already exist.
    If the table does exist, this query does nothing.
    
    INPUT:
        NONE
    OUTPUT:
        creates table (with no output)
        STRING: completed step 1
    '''
    
    conn = sqlite3.connect('IndexDB.sqlite')
    cur = conn.cursor()
    
    cur.execute('''
                CREATE TABLE IF NOT EXISTS queryIndex
                (ID             INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                Keywords        varchar(255),
                Summary         varchar(255),
                FileName        varchar(100),
                FileLocation    varchar(100),
                QueryCreateDate varchar(100),
                LastUpdateDate  varchar(100),
                LastUpdateID    varchar(100)
                )'''
                )
    conn.commit()
    return 'completed step 1'
    
def doesRecordExist(tableName):
    '''
    Checks if a given SQL file already has a record in the table queryIndex
    
    INPUT: 
        tableName(str): the name of the table to be checked
    RETURN:
        the result of the query for tableName, will return an empty list if the 
        record does not exist
    '''
    conn = sqlite3.connect('IndexDB.sqlite')
    cur = conn.cursor()
    
    cur.execute('''SELECT FileName
                    FROM queryIndex 
                    WHERE FileName = ?''',(tableName,))
    return cur.fetchall()
    

def getLastModifiedDate(tableName):
    '''
    Will return the most recent modified date for the table.
    Used to determine in index needs to be updated or not.
    
    INPUT: 
        tableName(str): the name of the table to be checked
    RETURN:  
        a list of two elements; the ID of when the record was last updated and
        the original create date of the query.
        Will be empty if the record does not exist.
    
    '''
    
    conn = sqlite3.connect('IndexDB.sqlite')
    cur = conn.cursor()
    
    cur.execute('''SELECT LastUpdateID, QueryCreateDate
                    FROM queryIndex 
                    WHERE FileName = ?''',(tableName,))
    return cur.fetchall()

#should split this into create function and update function
#create function will not need a create date parameter bc it will be the same as last modified
def addNewRecord(i, createDate = None):
    '''
    creates a new record and associated data for a SQL file
    INPUT: 
        i(str): the full filepath of the SQL file to be added to the table
    RETURN:
        NONE
        Adds new record and associated data to the table
    
    '''
    
    #open database connection
    conn = sqlite3.connect('IndexDB.sqlite')
    cur = conn.cursor()
    
    summary, keyword, lastModifiedDatetime, lastUpdateID = pf.parseQuery(i)
    fileName = str(i.split('/')[-1])
    filepath = str(i)
    fileCreateDate = time.ctime(os.path.getctime(i))
    
    cur.execute('''
                INSERT INTO queryIndex
                (Keywords, Summary, FileName, FileLocation,
                 QueryCreateDate, LastUpdateDate, LastUpdateID)
                VALUES(?,?,?,?,?,?,?);'''
                ,(keyword, summary, fileName, filepath, fileCreateDate, lastModifiedDatetime, lastUpdateID))
    conn.commit()
     
    return ''
    
def updateOldRecord(i, createDate):
    '''
    Deletes the current record for the SQL file passed in, and addes a new
    record with update information.  Maintains the original create date.
    INPUT:
        i(str): full file path for the record to be updated
    OUTPUT:
        NONE
    '''
    
    #open database connection
    conn = sqlite3.connect('IndexDB.sqlite')
    cur = conn.cursor()
    
    summary, keyword, lastModifiedDatetime, lastUpdateID = pf.parseQuery(i)
    fileName = str(i.split('/')[-1])
    filepath = str(i)
    
    fileCreateDate = createDate
    
    cur.execute('''
                DELETE FROM queryIndex
                WHERE fileName = ?''',(fileName,))
    conn.commit()
    
    cur.execute('''
                INSERT INTO queryIndex
                (Keywords, Summary, FileName, FileLocation,
                 QueryCreateDate, LastUpdateDate, LastUpdateID)
                VALUES(?,?,?,?,?,?,?);'''
                ,(keyword, summary, fileName, filepath, fileCreateDate,lastModifiedDatetime, lastUpdateID))
    conn.commit()
     
    return '' 