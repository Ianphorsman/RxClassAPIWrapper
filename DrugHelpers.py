import json
import requests
from collections import Counter
from functools import reduce
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
            'CHEM': 'Chemical Name',
            'MESHPA': 'MeSH Pharmacological Actions',
            'EPC': 'Established Pharmacological Classes',
            'ATC1-4': 'Anatomical Therapeutic Chemical',
            'DISEASE': 'Indications'
        }

    def memo(func):
        def wrapper(self, drug_name):
            if drug_name not in self.memo:
                self.get_class_data_of_drug(drug_name)
            return func(self, drug_name)
        return wrapper

    def deep_memo(func):
        def wrapper(self, drug_name, drug_property):
            if drug_name not in self.memo:
                self.get_class_data_of_drug(drug_name)
            if drug_property not in self.memo[drug_name]:
                getattr(self, drug_property)(drug_name)
            return func(self, drug_name, drug_property)
        return wrapper


    def get_class_data_of_drug(self, drug_name):
        ret = self.api.find_class_by_drug_name(drug_name)
        classes = {
            (source['rxclassMinConceptItem']['className'],
             source['rxclassMinConceptItem']['classType'],
             source['rxclassMinConceptItem']['classId'])
            for source in ret['rxclassDrugInfoList']['rxclassDrugInfo']
        }
        arranged_classes = {}
        #pdb.set_trace()
        for tup in classes:
            if tup[1] not in arranged_classes:
                arranged_classes[tup[1]] = [(tup[2], tup[0])]
            else:
                arranged_classes[tup[1]].append((tup[2], tup[0]))
        self.memo[drug_name] = arranged_classes
        return arranged_classes

    def get_similarly_acting_drugs(self, drug_name):
        moa_id, moa = self.memo[drug_name]['MOA'][0]
        opts = {
            'relaSource': 'DAILYMED',
            'rela': "has_{}".format('MOA')
        }
        ret = self.api.get_class_members(moa_id, opts)
        if 'drugMemberGroup' not in ret:
            return
        return (moa, [member['minConcept']['name'] for member in ret['drugMemberGroup']['drugMember']])

    def contraindications(self, rela, class_name):
        class_type_id = self.get_class_by_name(class_name)['classId']
        #pdb.set_trace()
        opts = {
            'relaSource': 'NDFRT',
            'rela': "CI_{}".format(rela)
        }
        ret = self.api.get_class_members(class_type_id, opts)
        title = "{} contraindications".format(class_name)
        if 'drugMemberGroup' not in ret:
            return (title, None)
        drug_names = [member['minConcept']['name'] for member in ret['drugMemberGroup']['drugMember']]
        return title, drug_names

    def drug_induces(self, disease):
        disease_id = self.get_class_by_name(disease)['classId']
        opts = {
            'relaSource': 'NDFRT',
            'rela': 'induces'
        }
        ret = self.api.get_class_members(disease_id, opts)
        title = "Drugs that induce {}".format(disease)
        if 'drugMemberGroup' not in ret:
            return (title, None)
        drug_names = [member['minConcept']['name'] for member in ret['drugMemberGroup']['drugMember']]
        return title, drug_names

    def get_class_by_name(self, class_name):
        ret = self.api.find_class_by_name(class_name)
        if 'rxclassMinConceptList' not in ret:
            return
        return ret['rxclassMinConceptList']['rxclassMinConcept'][0]


    @memo
    def mechanism_of_action(self, drug_name):
        moa = set()
        meshpa = set()
        if 'MOA' in self.memo[drug_name]:
            moa = set([tup[1] for tup in self.memo[drug_name]['MOA']])
        if 'MESHPA' in self.memo[drug_name]:
            meshpa = set([tup[1] for tup in self.memo[drug_name]['MESHPA']])

        return sorted(moa & meshpa)

    @memo
    def drug_type(self, drug_name):
        if 'VA' not in self.memo[drug_name]:
            return
        return sorted(set([tup[1] for tup in self.memo[drug_name]['VA']]))

    @memo
    def indications(self, drug_name):
        if 'DISEASE' not in self.memo[drug_name]:
            return
        return sorted(set([tup[1] for tup in self.memo[drug_name]['DISEASE']]))

    @memo
    def physiological_effects(self, drug_name):
        if 'PE' not in self.memo[drug_name]:
            return
        return sorted(set([tup[1] for tup in self.memo[drug_name]['PE']]))

    @memo
    def pharmacokinetics(self, drug_name):
        if 'PK' not in self.memo[drug_name]:
            return
        return sorted(set([tup[1] for tup in self.memo[drug_name]['PK']]))

    @memo
    def therapeutic_class(self, drug_name):
        if 'ATC1-4' not in self.memo[drug_name]:
            return
        return sorted(set([tup[1] for tup in self.memo[drug_name]['ATC1-4']]))

    @memo
    def pharmacological_classes(self, drug_name):
        if 'EPC' not in self.memo[drug_name]:
            return
        return sorted(set([tup[1] for tup in self.memo[drug_name]['EPC']]))


    @memo
    def chemical_name_of_brand(self, brand_name):
        if 'CHEM' not in self.memo[brand_name]:
            return
        return Counter([tup[1] for tup in self.memo[brand_name]['CHEM']]).most_common(1)[0][0]

    def drug_names_in_class(self, class_name):
        pass

    def drug_info(self, drug_name):
        return {
            'Name': self.chemical_name_of_brand(drug_name),
            'Drug Type': self.drug_type(drug_name),
            'Therapeutic Class': self.therapeutic_class(drug_name),
            'Indications': self.indications(drug_name),
            'Mechanism of Action': self.mechanism_of_action(drug_name),
            'Physiological Effects': self.physiological_effects(drug_name),
            'Pharmacokinetics': self.pharmacokinetics(drug_name),
        }

    def save(self, filename='class_memo'):
        with open("{}.p".format(filename), 'wb') as f:
            picklerick.dump(self.memo, f)

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
        self.memo = self.load()
        return self

    def __exit__(self, type, value, traceback):
        self.save()


with DrugHelpers() as bot:
    #pp(bot.drug_info('fluoxetine'))
    #pp(bot.get_class_data_of_drug('fluoxetine'))
    #pp(bot.get_similarly_acting_drugs('fluoxetine'))
    #pp(bot.api.find_class_by_name('long qt syndrome'))
    #pp(bot.contraindications('with', 'seizure disorder'))
    #pp(bot.contraindications('with', 'hypoglycemia'))
    pp(bot.drug_induces('vomiting'))

