import json
import requests
from pprint import pprint as pp
from RxAPIWrapper import RxAPIWrapper
import pdb


class DrugHelpers(object):

    def __init__(self):
        self.api = RxAPIWrapper()


    def get_class_description_of_drug(self, drug_name):
        ret = self.api.find_class_by_drug_name(drug_name)
        return set([source['rxclassMinConceptItem']['className'] for source in ret['rxclassDrugInfoList']['rxclassDrugInfo']])
        #pdb.set_trace()

    def basic_information_of_drug(self, drug_name):
        ret = self.api.find_class_by_drug_name(drug_name)
        info = ret['rxclassDrugInfoList']['rxclassDrugInfo']

        pdb.set_trace()

bot = DrugHelpers()
pp(bot.get_class_description_of_drug('fluoxetine'))
