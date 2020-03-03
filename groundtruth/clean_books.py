"""
This script cleans the OCR files, so that we have uniform documents with the same pre-processing applied to each of
them. For every book, a new document is created so that the original file is always available for cross-checking etc.
"""

import os
import re
from tqdm import tqdm


# directories
books_original_dir = '/home/jan/Projects/Travelogues/tl-classification/data/travelogues-groundtruth/16th_century/books/travelogue'
output_dir = './16th_century_clean/'

clean_page = []
clean_book = []
for fname in tqdm(sorted(os.listdir(books_original_dir))):
    # save the current id, need it later to store a new copy
    current_book_id = fname[:-4]

    # books are in .txt files, metadata in .meta
    if fname.endswith('.txt'):
        with open(os.path.join(books_original_dir, fname), 'r', encoding='utf-8') as f:
            for line in f.readlines():
                # if there is only a linebreak, we reached the end of a page
                if line == '\n':
                    # only keep pages that contain more than one line of text
                    if len(clean_page) > 1:
                        # join all lines into one string
                        final_page = ''.join(clean_page)

                        # the first line of a page often contains the page number, we want to remove it
                        final_page = re.sub(r'^\d*', '', final_page)

                        # in the special case that we have the OCR output of an empty page, we get 404 from SACHA
                        if final_page.startswith('statuscode'):
                           final_page = '<EMPTY_PAGE>'

                        # add this page to our book, with an added linebreak! in the new file, one page equals one line.
                        # also, everything is lowercase
                        clean_book.append(final_page.lower() + '\n')

                    # if len(clean_page) == 0:
                    #     # this is the case if a page only contains whitespace/special characters
                    #     final_page = '<EMPTY_PAGE>'
                    #
                    #     # add this page to our book, with an added linebreak! in the new file, one page equals one line.
                    #     clean_book.append(final_page + '\n')

                    # reset
                    final_page = []
                    clean_page = []
                # every other content of a line means that it is within a page and will be processed
                else:
                    # remove linebreaks
                    clean_line = line.replace('\n', '')

                    # remove hyphens and special characters, also whitespace (everything that is not a letter or digit)
                    clean_line = re.sub(r'\W', '', clean_line)

                    # substitue long s with normal s
                    clean_line = clean_line.replace('ſ', 's')

                    # append, unless the line is empty (which means it only contained linebreaks or whitespace)
                    # if clean_line is not '':
                    clean_page.append(clean_line)

    with open(os.path.join(output_dir, current_book_id + '_clean.txt'), 'w', encoding='utf-8') as out:
        for page in clean_book:
            out.write(page)
        clean_book = []
