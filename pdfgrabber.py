import time
import urllib.request
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed


class PDFGrabber():
    def __init__(self, school_id=120, major='Game Design & Interactive Media, B.S.', major_code='GDIM', delay=0.5):
        self.school_id = school_id
        self.major = major
        self.major_code = major_code
        self.delay = delay

    def get_agreements(self):
        with urllib.request.urlopen(f'https://assist.org/api/institutions/{self.school_id}/agreements') as url:
            data = json.loads(url.read().decode())
        agreement_list = []
        i = 0
        for agreement in list(data):
            i += 1
            if agreement['isCommunityCollege']:
                school_id = agreement['institutionParentId']
                year = agreement['sendingYearIds'][-1]
                curr = {'id': school_id, 'year': year}
                agreement_list.append(curr)
        return agreement_list

    def get_keys(self):
        agreement_list = self.get_agreements()
        keys = []
        i = 0

        def fetch_keys(agreement):
            nonlocal i
            school_id, year = agreement['id'], agreement['year']
            with urllib.request.urlopen(f'https://assist.org/api/agreements?receivingInstitutionId={self.school_id}&sendingInstitutionId={school_id}&academicYearId={year}&categoryCode=major') as url:
                data = json.loads(url.read().decode())
            data = data['reports']
            for report in list(data):
                if report['label'] == self.major:
                    keys.append({'key': report['key'], 'school_id': school_id})
                    print("Key:", report['key'], i)
            i += 1

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(fetch_keys, agreement)
                       for agreement in agreement_list]

        for future in as_completed(futures):
            future.result()

        return keys

    def get_pdfs(self):
        keys = self.get_keys()
        id_to_key = {}
        i = 0

        save_directory = 'agreements'

        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        for key in keys:
            i += 1
            school_id = key['school_id']
            key_val = key['key']
            print(key_val)
            if key_val is not None:
                pdf_url = f'https://assist.org/api/artifacts/{key_val}'
                file_name = f'{save_directory}/report_{self.school_id}_{school_id}_{self.major_code}.pdf'
                try:
                    with open(file_name, 'wb') as f:
                        print("PDF:", i)
                        f.write(urllib.request.urlopen(pdf_url).read())
                        print("test 2")
                    id_to_key[school_id] = key_val
                except Exception as e:
                    print(
                        f"Error while saving PDF for school ID {school_id}: {str(e)}")
            else:
                print("test 4")

        return id_to_key
