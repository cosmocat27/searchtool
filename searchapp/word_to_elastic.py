#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions for uploading new documents to ElasticSearch
"""

from __future__ import print_function, division

# reference the docx_processing.py file functions
# this was the original build in the extracting_text exercise
import searchapp.docx_processing as docx_processing

# reference the yield_files function from word_to_json
# also from the extracting_text exercises
from searchapp.word_to_json import yield_files

# import the elastic loading function
# that you just created in this exercise
from searchapp.elastic_loader import ElasticLoader

# core libraries for processing the files
import json
import os
import sys
import glob

# useful for troubleshooting dictionary content
from pprint import pprint

def word_to_elastic(fn, docID, splitFields=['tags']):

    '''
    Given a Word document file name, fn, and specific
    fields that will be split, create the JSON file 
    to match the mapping definition and use the 
    ElasticLoader to register the mapping
    into the object, create an index, and load the document. 

    SIGNATURE:
        INPUT: fn = word document file name
            splitFields = array of fields that should be 
            split when gathered from the header
        OUPUT: Nothing returned, but loads the fn as a JSON
            into the created elasticsearch index
    '''

    indexName = doctype = 'transcript'

    transcript_mapping = {
        doctype: {
            'dynamic':'strict',
            'properties': {
                'date': {'type':'string'}
                , 'researcher': {'type':'string'}
                , 'filename': {'type':'string'}
                , 'project': {'type':'string'}
                , 'tags': {'type':'string', 'index_name':'tags'}
                , 'transcription': {'type':'string'}
            }
        }
    }

    
    # STEP 1: Create a new instance of an ElasticLoader object
    el = ElasticLoader()

    # STEP 2: Create an index with the mapping
    el.create_index_with_mapping(indexName, transcript_mapping)

    # STEP 3: Create a JSON document that is the header, transcription, and filename, from the Word document.
    #print(fn, file=sys.stderr)
    json_out = docx_processing.header_extract(fn, splitFields)
    json_out['transcription'] = docx_processing.paragraph_extract(fn)
    
    #print(json_out)

    # STEP 4: Insert the document into the index.
    el.try_insert(indexName, docID, doctype, json_out, False)


def delete_from_index(docID):
    el = ElasticLoader()
    indexName = doctype = 'transcript'

    el.try_delete(indexName, docID, doctype, False)


if __name__ == '__main__':

    '''
    This is the main function that uses yield_files to 
    pass Word documents to the Word-to-Elastic loader.
    No modification is required.
    '''

    searchPath='./transcriptions/*.docx'

    for fn in yield_files(searchPath):
        print("Adding file: %s" % fn)
        word_to_elastic(fn)

