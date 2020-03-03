import math

"""
A super-simple script that splits a text document into a given number of parts.
Note that this script is fairly specific to the properties of the texts in the
Travelogues corpus: splits are placed only where there are two empty lines (i.e.
three consecutive newline characters), since we know these denote line breaks in
the corpus documents.
"""

# TODO commandline-arguments?
INPUT_FILE = './156843801.txt'
NUM_PARTS = 26

# Computes the desired end_offset for the clip,
# given the text (txt), the current cursor position,
# and the number of pages this part should include.
def get_end_offset(txt, cursor, n):
  text_after_cursor = txt[cursor:]
  pages_after_cursor = text_after_cursor.split('\n\n\n')

  # print(f'{len(pages_after_cursor)} pages after the cursor')

  offset = cursor
  pages = n if len(pages_after_cursor) > n else len(pages_after_cursor)

  # print(f'Counting length for {n} pages')
  
  for i in range(pages):
    # print(i)
    offset += len(pages_after_cursor[i])
    # print(offset)

  return offset

with open(INPUT_FILE, 'r') as infile:
  # Count 'pages'
  txt = infile.read()
  pages = txt.split('\n\n\n')

  total_chars = 0
  for page in pages:
    total_chars += len(page)

  print(f'Read {len(pages)} pages, {total_chars} characters total')
  
  pages_per_part = math.ceil(len(pages) / NUM_PARTS)
  print(f'Splitting into {NUM_PARTS} parts, {pages_per_part} pages per part')

  i = 1 # Running index, used only for filename
  page_cursor = 0
  while page_cursor < len(pages):
    # Construct outfile name
    without_ext = INPUT_FILE[:INPUT_FILE.rfind('.')]
    padded_idx = str(i) if i > 9 else f'0{i}'
    outfile = f'{without_ext}.part{padded_idx}.txt'

    to_page = (page_cursor + pages_per_part) if (page_cursor + pages_per_part) < len(pages) else len(pages)

    print(f'Writing to file {outfile}: page {page_cursor} to {to_page}')

    with open(outfile, 'w') as out:

      for p in range(page_cursor, to_page):
        out.write(f'{pages[p]}\n\n\n')

      out.close()

    page_cursor += pages_per_part
    i += 1
      