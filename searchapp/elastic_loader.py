#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions for interacting with ElasticSearch via Python
"""

from __future__ import print_function, division

# required for elastic search connection
from elasticsearch import Elasticsearch

import sys
import os
import time

class ElasticLoader():

    '''
    A loader class for elastic search. It wraps the Python Elastic
    Search API with methods to create an index, delete an index, 
    and load documents. 
    '''

    def __init__(self):
        '''
        Initialize an ElasticLoader object with the .es ElasticSearch property.
        No modification is required. 
        '''
        self.es = Elasticsearch()

    def create_index_with_mapping(self, idxName, mapping):
        ''' 
        Given an index name and a mapping, create the
        index with the mapping. By default set the ignore=400
        parameter on the create method.

        Signature:
            idxName = name of the index to create
            mapping = dictionary with the mapping for the index

        ref: https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.client.IndicesClient.create
        '''
        self.es.indices.create(index=idxName, body=mapping, ignore=400)
        
    def insert(self, idxName, docID, docType, body):
        '''
        Insert a document of specified type into the index.

        Signature: 
            idxName = name of existing index for document loading
            docID = id of the document to be inserted
            docType = the document type to be added associated to the post
            body = a dictionary document to be posted

        ref: https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.index
        '''
        self.es.index(index=idxName, id=docID, doc_type=docType, body=body)
        
    def try_insert(self, indexName, docID, doctype, body, silent=True):
        '''
        Wrap the self.insert method in a try/except
        statement with optional output on failure. 
        No modification is required.
        '''
        try:
            self.insert(indexName, docID, doctype, body)

        except:
            if (silent):
                pass
            else:
                print("ERROR {}".format(sys.exc_info()))

    def delete(self, idxName, docID, doctype):
        '''
        Delete a document from the index.

        Signature:
            idxName = name of existing index for document loading
            docID = id of the document to be deleted

        ref: https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.index
        '''
        self.es.delete(index=idxName, id=docID, doc_type=doctype)

    def try_delete(self, indexName, docID, doctype, silent=True):
        '''
        Wrap the self.delete method in a try/except
        statement with optional output on failure.
        No modification is required.
        '''
        try:
            self.delete(indexName, docID, doctype)

        except:
            if (silent):
                pass
            else:
                print("ERROR {}".format(sys.exc_info()))

    def delete_index(self, idxName):
        '''
        Delete a specified index, set the "ignore" parameter
        to be 400 and 404. 
        No modification is required here. 

        ref: https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.client.IndicesClient.delete
        '''
        self.es.indices.delete(index=idxName, ignore=[400, 404])

def unit_test():
    
    '''
    This main function executes when the script is run directly 
    to perform the unit test. This will create a temporary 
    index on localhost:9200 and post a single document to the index. 
    It will then attempt to run a curl request against the index
    and subsequently delete the index. 

    No modification is required here, this is meant to show you 
    how the class will operate.
    '''

    def list_indicies():
        ''' Utility function for listing indicies in localhost elasticsearch '''
        print('Index list')
        os.system("curl -XGET 'http://localhost:9200/_cat/indices?v'")

    # for unit testing, specify all values to be 'ut'
    docs = {
        1: {'indexName': 'ut', 'doctype': 'ut', 'post': {'Transcription':'unit test from class load'}},
        2: {'indexName': 'ut', 'doctype': 'ut', 'post': {'Transcription':'Additional test document'}}
    }

    indexName = doctype = 'ut'

    # create a simple document mapping schema
    ut_mapping = {
        doctype: {
            'dynamic':'strict',
            'properties':{
                'Transcription':{'type':'string'}
            }
        }
    }

    # initialize the loader class as a new object
    # create a new index with the mapping
    el = ElasticLoader()
    el.create_index_with_mapping(indexName, ut_mapping)

    # Perform the unit test
    # insert the document

    # ensure there are no errors since 'silent' is set to false
    print('Test insertion to Elastic Search')
    for docID in docs:
        el.try_insert(docs[docID]['indexName'], docID, docs[docID]['doctype'], docs[docID]['post'], False)

    # list all indicies
    time.sleep(1)
    list_indicies()

    print('Test deletion from Elastic Search')
    docID = 2
    el.try_delete(docs[docID]['indexName'], docID, docs[docID]['doctype'], False)

    # pause for 1 second to ensure all commits to the index complete
    # before performing the curl request
    print('Waiting 1 second before querying')
    time.sleep(1)

    # perform a test search against the unit test index
    print('Test retrieval of unit posting')
    os.system("curl -XGET 'http://localhost:9200/ut/_search?' | python3 -m json.tool")

    # remove the unit test index
    print('Deleting index')
    el.delete_index(indexName)

    # list all indicies again, the unit test one should disappear
    list_indicies()

if __name__ == '__main__':

    unit_test()


