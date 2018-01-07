import json
import requests
from pprint import pprint as pp
from RxAPIWrapper import RxAPIWrapper
import pdb


class DrugHelpers(object):

    def __init__(self):
        self.api = RxAPIWrapper()
        self.drug_class_types = {
            'VA': 'Class',
            'MoA': 'Mechanism of Action',
            'PK': 'Pharmacokinetics',
            'PE': 'Physiological Effect',
            'Chem': 'Chemical Name',
            'MESHPA': 'MeSH Pharmacological Actions',
            'EPC': 'Established Pharmacological Classes',
            'ATC1-4': 'Anatomical Therapeutic Chemical',
            'DISEASE': 'Indications'
        }



    def get_class_description_of_drug(self, drug_name):
        ret = self.api.find_class_by_drug_name(drug_name)
        classes = {
            (source['rxclassMinConceptItem']['className'], source['rxclassMinConceptItem']['classType'])
            for source in ret['rxclassDrugInfoList']['rxclassDrugInfo']
        }

        return classes

    def basic_information_of_drug(self, drug_name):
        ret = self.api.find_class_by_drug_name(drug_name)
        info = ret['rxclassDrugInfoList']['rxclassDrugInfo']

        pdb.set_trace()

bot = DrugHelpers()
pp(bot.get_class_description_of_drug('fluoxetine'))
