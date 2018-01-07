import json
import requests
import os
import _pickle as picklerick
from pprint import pprint as pp
from RxAPIWrapper import RxAPIWrapper
import pdb


class DrugHelpers(object):

    def __init__(self):
        self.api = RxAPIWrapper(throttle=20)
        self.drug_class_types = {
            'VA': 'Class',
            'MOA': 'Mechanism of Action',
            'PK': 'Pharmacokinetics',
            'PE': 'Physiological Effect',
            'Chem': 'Chemical Name',
            'MESHPA': 'MeSH Pharmacological Actions',
            'EPC': 'Established Pharmacological Classes',
            'ATC1-4': 'Anatomical Therapeutic Chemical',
            'DISEASE': 'Indications'
        }

    def memo(func):
        def wrapper(self, drug_name):
            if drug_name not in self.class_memo:
                self.get_class_data_of_drug(drug_name)
            return func(self, drug_name)
        return wrapper


    def get_class_data_of_drug(self, drug_name):
        ret = self.api.find_class_by_drug_name(drug_name)
        classes = {
            (source['rxclassMinConceptItem']['className'], source['rxclassMinConceptItem']['classType'])
            for source in ret['rxclassDrugInfoList']['rxclassDrugInfo']
        }
        arranged_classes = {}
        for tup in classes:
            if tup[1] not in arranged_classes:
                arranged_classes[tup[1]] = [tup[0]]
            else:
                arranged_classes[tup[1]].append(tup[0])
        self.class_memo[drug_name] = arranged_classes
        return arranged_classes

    @memo
    def mechanism_of_action(self, drug_name):
        moa = set()
        meshpa = set()
        if 'MOA' in self.class_memo[drug_name]:
            moa = set(self.class_memo[drug_name]['MOA'])
        if 'MESHPA' in self.class_memo[drug_name]:
            meshpa = set(self.class_memo[drug_name['MESHPA']])

        return sorted(moa & meshpa)

    @memo
    def drug_type(self, drug_name):
        if 'VAD' not in self.class_memo[drug_name]:
            return
        return sorted(set(self.class_memo[drug_name]['VA']))

    @memo
    def indications(self, drug_name):
        if 'DISEASE' not in self.class_memo[drug_name]:
            return
        return sorted(set(self.class_memo[drug_name]['DISEASE']))

    @memo
    def physiological_effects(self, drug_name):
        if 'PE' not in self.class_memo[drug_name]:
            return
        return sorted(set(self.class_memo[drug_name]['PE']))

    @memo
    def pharmacokinetics(self, drug_name):
        if 'PK' not in self.class_memo[drug_name]:
            return
        return sorted(set(self.class_memo[drug_name]['PK']))

    @memo
    def pharmacological_class(self, drug_name):
        if 'EPC' not in self.class_memo[drug_name]:
            return
        return sorted(set(self.class_memo[drug_name]['EPC']))


    @memo
    def chemical_name_of_brand(self, brand_name):
        pass

    def drug_names_in_class(self, class_name):
        pass

    @memo
    def basic_information_of_drug(self, drug_name):
        pass

    def save(self, filename='class_memo'):
        with open("{}.p".format(filename), 'wb') as f:
            picklerick.dump(self.class_memo, f)

    def wipe(self, filename='class_memo'):
        open("{}.p".format(filename), 'wb').close()

    def load(self, filename='class_memo'):
        if not os.path.exists("{}.p".format(filename)):
            with open("{}.p".format(filename), 'wb') as f:
                picklerick.dump({}, f)
        with open("{}.p".format(filename), 'rb') as f:
            try:
                data = picklerick.load(f)
            except EOFError:
                data = {}
        return data

    def __enter__(self):
        self.class_memo = self.load()
        return self

    def __exit__(self, type, value, traceback):
        self.save()

with DrugHelpers() as bot:
    #pp(bot.indications('fluoxetine'))
    #pp(bot.physiological_effects('fluoxetine'))
    #pp(bot.pharmacokinetics('fluoxetine'))
    #pp(bot.mechanism_of_action('fluoxetine'))
    pp(bot.drug_type('fluoxetine'))
    #pp(bot.get_class_data_of_drug('fluoxetine'))
    #pp(bot.indications('fluoxetine'))
