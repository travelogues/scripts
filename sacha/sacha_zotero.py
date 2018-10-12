# This script is used to download books taken from Zotero .csv export files.

import csv
import json
import logging
import requests
import time
from tqdm import tqdm

logging.basicConfig(handlers=[logging.FileHandler('sacha.log'),
                              logging.StreamHandler()],
                    # level=logging.DEBUG,
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p')

csv_file = '../../tl-classification/data/travelogues-groundtruth/17th_complete_2018-08-26.csv'
target_dir = '../../tl-classification/data/travelogues-groundtruth/17th_century'

print('Now processing %s.' % csv_file)

with open(csv_file) as csvfile:
    csv_reader = csv.DictReader(csvfile, delimiter=',')
    for row in csv_reader:
        barcode = row['Url']
        barcode = barcode.split('/')[4]

        logging.info('Now requesting %s' % barcode)
        r = requests.get('http://iiif.onb.ac.at/presentation/ABO/%s/manifest/' % barcode)
        logging.info('HTTP status: %s' % r.status_code)

        if r.status_code != 200:
            logging.critical('Requesting %s produced a HTTP %s' % (barcode, r.status_code))
        elif r.status_code == 200:
            manifest = json.loads(r.text)

            # store the meta data
            with open('%s/metadata/%s.meta' % (target_dir, barcode[2:]), 'w', encoding='utf-8') as metadata:
                logging.info('Now storing the meta data...')
                json.dump(manifest['metadata'], fp=metadata, sort_keys=True, indent=4)

            # store content
            with open('%s/travelogue/%s.txt' % (target_dir, barcode[2:]), 'w', encoding='utf-8') as fulltext:
                # iterate the manifest
                logging.info('Now requesting %d manifest pages...' % len(manifest['sequences'][0]['canvases']))
                for canvas in tqdm(manifest['sequences'][0]['canvases']):
                    content = canvas['otherContent'][0]['resources'][0]['resource']['@id']
                    if content[-3:] == 'txt':
                        canvas_text = requests.get(content)
                        status = canvas_text.status_code
                        if status == 200:
                            pass
                        else:
                            logging.critical('Requesting %s produced a HTTP %s' % (content, status))
                        fulltext.write(canvas_text.text)
                        fulltext.write('\n')
                        time.sleep(0.01)
