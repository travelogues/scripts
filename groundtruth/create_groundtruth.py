"""
This script helps with the creation of Travelogues ground truth. It goes through all documents, and compares the
keywords against the title. If any keyword is in the title, the file is moved and subsequently checked again.
"""

import os
import json
import shutil

dir_19th = '../../tl-classification/data/travelogues-groundtruth/19th_century'

# travelogue title keywords
keywords = ['faart', 'fahrt', 'fart', 'rais',  'raiß', 'raisz', 'rays', 'rayß', 'raysz',
            'reis', 'reiß', 'reisz', 'reys', 'reyß', 'reysz', 'rys', 'ryß']

travelogue_dir = '../../tl-classification/data/travelogues-groundtruth/19th_century/books/travelogue'

for subdir in ['candidates/part1', 'candidates/part2',
               'candidates/part3', 'candidates/part4', 'candidates/part5',
               'candidates/part6', 'candidates/part7', 'candidates/part8', 'candidates/part9', 'candidates/part10',
               'candidates/part11', 'candidates/part12', 'candidates/part13', 'candidates/part14', 'candidates/part15',
               'candidates/part16', 'candidates/part17', 'candidates/part18', 'candidates/part19']:
    print('Current dir: ' + subdir)
    for book in os.listdir(os.path.join(dir_19th, 'books', subdir)):
        metadata = os.path.join(dir_19th, ('metadata/' + book[:-4] + '.meta'))
        with open(metadata, 'r') as jsonfile:
            data = json.load(jsonfile)
            for entry in data:
                # find the title of this document
                if type(entry.get('label')[0]) is dict:
                    if entry.get('label')[0].get('@value') == 'Title':  # en value
                        title = entry.get('value')

                        # check if any keyword is in the title: if true, move to candidate folder
                        if any(k in title for k in keywords):
                            print('Moving: ' + title)
                            shutil.move(os.path.join(dir_19th, 'books', subdir, book), os.path.join(travelogue_dir, book))






