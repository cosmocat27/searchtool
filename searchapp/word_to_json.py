#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions for converting Word documents to JSON format
"""

from __future__ import print_function, division

# core libraries for processing the files
import glob
import json
import os
from pprint import pprint  # useful for troubleshooting dictionary content
import re

# reference the docx_processing.py file functions
import searchapp.docx_processing as docx_processing


def yield_files(searchPath):
    """This function is designed to yield all of the file names within a given
    directory and search path. We've discussed regex, and it is recommended
    that you use glob for this function though is not necessary:
    https://docs.python.org/2/library/glob.html

    Yield is used to define the function as a generator.
    https://wiki.python.org/moin/Generators

    Args:
        searchPath (str): a search path that may include regex

    Returns:
        the file path/name yielded for iteration
    """
    
    for filename in glob.glob(searchPath):
        yield filename


def word_to_json(targetDir='./json_output/',
                 searchPath='./transcriptions/*.docx',
                 splitFields=['tags']):
    """This function is designed to extract the header and transcription from a
    Word document using the docx_processing functions and write the values as
    JSON to the specified targetDir using the same file name with a .json
    extension e.g. "transcript01.docx" will be stored as "transcript01.json".

    You can either make the targetDirectory ahead of time, or add the
    appropriate code to check if the directory exists and create it if it is
    missing.

    The header keys can stay as the values specified in the document. The
    transcription key should be "Transcription" and the "Tags" field from the
    header tables should be split.

    Args:
        targetDir (str): the landing folder for the JSON files
        searchPath (str): the regex search path for source documents

    Returns:
        None from the function, but a file is written to the targetDir for each
            file in searchPath
    """

    if not os.path.isdir(targetDir):
        os.mkdir(targetDir)
    
    for filename in yield_files(searchPath):
        print(filename)
        json_out = docx_processing.header_extract(filename, splitFields)
        json_out['transcription'] = docx_processing.paragraph_extract(filename)
        
        outfilename = targetDir + re.split('[/.\\\\]', filename)[-2] + '.json'
        print(outfilename)
        with open(outfilename, 'w') as outfile:
            json.dump(json_out, outfile)


if __name__ == '__main__':
    word_to_json()
    
    
    
