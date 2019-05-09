import csv
from pymarc import parse_xml_to_array

# edit the path accordingly
marcxml_file = 'data/TravelogueD17_Probeset_MARCXML.xml'
export_file = 'marc_export.csv'

records = parse_xml_to_array(marcxml_file)

with open(export_file, 'w', newline='') as export:
    exportwriter = csv.writer(export, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for record in records:
        if record is not None:  # not sure if this is an error with the exported file at hand or a general issue
            # Normierung: Signatur
            norm_sig = ''
            if record['852'] is not None:
                norm_sig = record['852']['8']  # does not show up in sample!

            # Normierung: Permalink
            norm_perma = ''
            if record['856'] is not None:
                norm_perma = record['856']['u']

            # Normierung: Normnummer
            norm_nr = ''
            if record['024'] is not None:
                norm_nr = record['024']['a']
            if record['555'] is not None:  # problem: some records have both
                norm_nr = norm_nr + ' ' + record['555']['d']

            # Normierung: Volltitel
            norm_full = ''
            if record['245'] is not None:
                norm_full = record['245']['a']
                if record['245']['b'] is not None:
                    norm_full = norm_full + ' --- ' + record['245']['b']

            # AutorInnen
            author = ''
            if record['100'] is not None:
                author = record['100']['a']

            # Herausgeber/Übersetzer
            author_editor = ''
            author_translator = ''
            author_engraver = ''
            author_litographer = ''
            author_contributor = ''
            if record['700'] is not None:
                if record['700']['4'] is 'edt':
                    author_editor = record['700']['a']
                if record['700']['4'] is 'trl':
                    author_translator = record['700']['a']
                if record['700']['4'] is 'egr':
                    author_engraver = record['700']['a']
                if record['700']['4'] is 'lit':
                    author_litographer = record['700']['a']
                if record['700']['4'] is 'ctb':
                    author_contributor = record['700']['a']
                # etc.???

            publisher = ''
            publish_loc = ''
            publish_date = ''
            if record['264'] is not None:
                # Offizine/Verlage
                publisher = record['264']['b']
                # Druckorte
                publish_loc = record['264']['a']
                # Erscheinungsdatum
                publish_date = record['264']['c']

            pages_count = ''
            pages_size = ''
            pages_graphic = ''
            if record['300'] is not None:
                # Umfang
                pages_count = record['300']['a']
                # Größe
                pages_size = record['300']['c']
                # Graphiken/Titelgraphik
                pages_graphic = record['300']['b']

            # Ausgabenzahl
            edition = ''
            if record['250'] is not None:
                edition = record['250']['a']

            # Paratexte: Widmung
            # Paratexte: Privileg
            # Paratexte: Vorrede
            # Metatexte: Fuß- bzw Endnoten
            # Inhalt: Region
            # Inhalt: Zeitabstand Reise- und Erscheinungsdatum
            # Literatur
            # Anmerkungen
            # Gattung
            # Inhalt
            # Fingerprint
            # Kollationsformel
            # Reihentitel

            # Bandangabe
            volume = ''
            if record['245'] is not None:
                volume = record['245']['n']

            # Sprache/Übersetzung
            lang_original = ''
            if record['041'] is not None:
                lang_original = record['041']['h']  # original language

            exportwriter.writerow([norm_sig, norm_perma, norm_nr, norm_full,
                                  author, author_editor, author_translator, author_engraver, author_litographer, author_contributor,
                                  publisher, publish_loc, publish_date,
                                  pages_count, pages_size, pages_graphic,
                                  edition, volume,
                                  lang_original])

