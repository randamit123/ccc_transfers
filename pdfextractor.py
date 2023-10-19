import re
import sys
import os
import pdfrw
from pdfminer.high_level import extract_text


class PDFExtractor:
    def __init__(self, file_name, num_pages=0):
        self.file_name = file_name
        self.num_pages = num_pages

    def dict_from_file(self):
        try:
            self.process_file()
            req_to_equiv = self.dict_from_text()
            print("Req_to_equiv:", req_to_equiv)
            return req_to_equiv
        except Exception as e:
            print(f"An error occurred in dict_from_file: {str(e)}")
            return None

    def process_file(self):
        try:
            writer = pdfrw.PdfWriter()
            for page in pdfrw.PdfReader(self.file_name).pages:
                self.num_pages += 1
                print(self.num_pages)
                for x in [0, 0.5]:
                    print("x in 0.05:", x)
                    new_page = pdfrw.PageMerge()
                    new_page.add(page, viewrect=(x, 0, 0.5, 1))
                    writer.addpages([new_page.render()])
            writer.write('output.pdf')
        except Exception as e:
            print(f"An error occurred in process_file: {str(e)}")

    def dict_from_text(self):
        req_to_equiv = {}
        if not os.path.exists('output.pdf'):
            print("Error: 'output.pdf' does not exist.")
            return req_to_equiv

        for page in range(self.num_pages):
            page_num = 2 * page
            try:
                text = extract_text('output.pdf')
                print(repr(text))
                text = extract_text('output.pdf', page_numbers=[page_num])
                print("Text:", repr(text))
                req_to_equiv = self.process_page(req_to_equiv, text)
                print("Req to equiv:", req_to_equiv)
            except Exception as e:
                print(
                    f"An error occurred in dict_from_text on page {page_num}: {str(e)}")
        return req_to_equiv

    def process_page(self, req_to_equivs_old, text):
        text = text.replace('\u200b', ' ')
        text = text.replace('Please refer to additional important General Informationsection above', '')
        outs = re.split('\(\d\.\d0\)', text)
        outs = map(str.strip, outs)
        outs = list(outs)
        outs = outs[:-1]
        req_to_equivs = req_to_equivs_old
        req = ''
        equiv = ''
        for item in outs:
            if 'Same-As' in item:
                item = item.replace('--- Or ---', ' *OR* ').replace('--- And ---', ' *AND* ') \
                    .replace('---Or---', ' *OR* ').replace('---And---', ' *AND* ') \
                    .replace('Same-As: ', ' / ')
                if equiv == '':
                    req += item
                else:
                    # This is a big deal: it means there's a "Same-As" in the equiv followed by a new req, all in the
                    # same item. My approach is to find the position of the last number before the new req and split
                    # there. It's not a problem if this happens in the left column, since the arrow will still indicate
                    # the split between req and equiv.
                    # This works so long as there's no letter in the name of the course, which is sometimes the case
                    # and needs to be manually adjusted after scraping
                    if ' - ' in item and '*OR*' not in item and '*AND*' not in item:  # it's the end of the equiv
                        num_pos = re.search(r'(\d)[^\d]*$', item[: item.index(' - ') - 5]).start() + 1
                        equiv += item[: num_pos]
                        req_to_equivs[req] = equiv
                        equiv = ''
                        req = item[num_pos:]
                        print('POTENTIAL ISSUE WITH', self.file_name, item)
                    else:
                        equiv += item
                continue

            if 'No Course Articulated' in item:
                while 'No Course Articulated' in item:
                    item = item[item.find('No Course Articulated') + 21:]
                req = item
                equiv = ''
                continue

            first_char = item[0]

            if first_char.isalpha():
                if req == '':
                    req = item
                elif equiv == '':
                    equiv = item
                else:
                    req_to_equivs[req] = equiv
                    equiv = ''
                    req = item

            elif first_char == '←':
                equiv = item[1:]

            elif '---And---' in item:
                if equiv == '':
                    req += ' *AND* ' + item[item.index('---And---') + 9:]
                else:
                    equiv += ' *AND* ' + item[item.index('---And---') + 9:]

            elif '--- And ---' in item:
                if equiv == '':
                    req += ' *AND* ' + item[item.index('--- And ---') + 11:]
                else:
                    equiv += ' *AND* ' + item[item.index('--- And ---') + 11:]

            elif '---Or---' in item:
                if equiv == '':
                    req += ' *OR* ' + item[item.index('---Or---') + 8:]
                else:
                    equiv += ' *OR* ' + item[item.index('---Or---') + 8:]

            elif '--- Or ---' in item:
                if equiv == '':
                    req += ' *OR* ' + item[item.index('--- Or ---') + 10:]
                else:
                    equiv += ' *OR* ' + item[item.index('--- Or ---') + 10:]

            else:
                print('ISSUE WITH', self.file_name, item)
                break

        if req != '' and equiv != '':
            req_to_equivs[req] = equiv

        return req_to_equivs
