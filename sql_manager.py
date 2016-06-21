# -*- coding: utf-8 -*-
"""
Created on Tue Jun 07 15:19:55 2016

@author: tzupan
"""
import os
import tableFunctions as tf
reload(tf)

def main(directoryPath = "C:/Users/tzupan/Documents/PythonScripts/SQL_manager"):
    '''
    '''
    tf.createTable()
    files = [directoryPath +'/'+ x for x in os.listdir(directoryPath) if x.endswith('.sql')]
        
    for i in files:
        tableName = i.split('/')[-1]
#       check if record already exists for current file
#       if it does not, add record to queryIndex
        if tf.doesRecordExist(tableName) == []:
            tf.addNewRecord(i)
            
#        if yes:
        else:
#            check if more recent updateddt (from DB) > most recent modified date
            realFileUpdateTime = os.path.getmtime(tableName)
            
            modDate = float(tf.getLastModifiedDate(tableName)[0][0])
            createDate = tf.getLastModifiedDate(tableName)[0][1]

#            if no:
            if realFileUpdateTime > modDate: 
#                save createdt of file (from DB)
#                delete current record
#                add new record
                tf.updateOldRecord(i, createDate)
            else: pass
    
    return 'Succesfully Updated Records'
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        