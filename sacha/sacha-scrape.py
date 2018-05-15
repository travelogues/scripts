import requests
import json
import time
import logging

logging.basicConfig(handlers=[logging.FileHandler('sacha.log'),
                              logging.StreamHandler()],
                    # level=logging.DEBUG,
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p')

targetdir = 'neunzehn'

with open('barcodes.txt', 'r', encoding='utf-8') as barcodes:
    for barcode in barcodes.readlines():
        barcode = barcode.strip()  # remove linebreak from barcodes file
        logging.info('Now requesting %s' % barcode)
        r = requests.get('http://fue.onb.ac.at/sacha/services/presentation/+%s/manifest/' % barcode)
        logging.info('HTTP status: %s' % r.status_code)

        manifest = json.loads(r.text)

        # store the meta data
        with open('%s/%s.meta' % (targetdir, barcode), 'w', encoding='utf-8') as metadata:
            logging.info('Now storing the meta data...')
            json.dump(manifest['metadata'], fp=metadata, sort_keys=True, indent=4)

        # store content
        with open('%s/%s.txt' % (targetdir, barcode), 'w', encoding='utf-8') as fulltext:
            # iterate the manifest
            logging.info('Now requesting %d manifest pages...' % len(manifest['sequences'][0]['canvases']))
            for canvas in manifest['sequences'][0]['canvases']:
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
                    time.sleep(0.1)
