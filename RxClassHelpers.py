import json
import requests
from collections import Counter
from functools import reduce
import os
import _pickle as picklerick
from pprint import pprint as pp
from RxAPIWrapper import RxAPIWrapper
import pdb


class RxClassHelpers(object):

    def __init__(self, save_memo=True, filename="rxclass_data"):
        self.save_memo = save_memo
        self.filename = filename
        self.api = RxAPIWrapper()
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
        ret = self.get_class_by_name(class_name)
        if 'classId' not in ret:
            return "{} not found in database.".format(class_name)
        class_type_id = ret['classId']
        opts = {
            'relaSource': 'NDFRT',
            'rela': "CI_{}".format(rela)
        }
        ret = self.api.get_class_members(class_type_id, opts)
        title = "{} contraindications".format(class_name)
        if 'drugMemberGroup' not in ret:
            return title, None
        drug_names = [member['minConcept']['name'] for member in ret['drugMemberGroup']['drugMember']]
        return title, drug_names

    def drug_induces(self, disease):
        ret = self.get_class_by_name(disease)
        if 'classId' not in ret:
            return "{} not found in database.".format(disease)
        disease_id = ret['classId']
        opts = {
            'relaSource': 'NDFRT',
            'rela': 'induces'
        }
        ret = self.api.get_class_members(disease_id, opts)
        title = "Drugs that induce {}".format(disease)
        if 'drugMemberGroup' not in ret:
            return title, None
        drug_names = [member['minConcept']['name'] for member in ret['drugMemberGroup']['drugMember']]
        return title, drug_names

    def drugs_that_may(self, action, disease):
        ret = self.get_class_by_name(disease)
        if 'classId' not in ret:
            return "{} not found in database.".format(disease)
        disease_id = ret['classId']
        opts = {
            'relaSource': 'NDFRT',
            'rela': "may_{}".format(action)# action items allowed: prevent, diagnose, treat
        }
        ret = self.api.get_class_members(disease_id, opts)
        title = "Drugs that may {} {}".format(action, disease)
        if 'drugMemberGroup' not in ret:
            return title, None
        drug_names = [member['minConcept']['name'] for member in ret['drugMemberGroup']['drugMember']]
        return title, drug_names

    def drugs_with_physiological_effect(self, effect):
        ret = self.get_class_by_name(effect)
        if 'classId' not in ret:
            return "{} not found in database.".format(effect)
        effect_id = ret['classId']
        opts = {
            'relaSource': 'NDFRT',
            'rela': 'has_PE'
        }
        ret = self.api.get_class_members(effect_id, opts)
        title = "Drugs that result in {}".format(effect)
        drug_names = [member['minConcept']['name'] for member in ret['drugMemberGroup']['drugMember']]
        return title, drug_names

    def drugs_with_similar_pharmacokinetics(self, drug_name):
        self.get_class_data_of_drug(drug_name)
        pk_id, pk_name = self.memo[drug_name]['PK'][0]
        opts = {
            'relaSource': 'NDFRT',
            'rela': 'has_PK'
        }
        ret = self.api.get_class_members(pk_id, opts)
        title = "Drugs processed via {}".format(pk_name)
        drug_names = [member['minConcept']['name'] for member in ret['drugMemberGroup']['drugMember']]
        return title, drug_names

    def get_class_by_name(self, class_name):
        ret = self.api.find_class_by_name(class_name)
        if 'rxclassMinConceptList' not in ret:
            return ret
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

    def drugs_sharing_properties(self, prop_1, prop_2):
        prop_1_id = self.get_class_by_name(prop_1)
        prop_2_id = self.get_class_by_name(prop_2)

        ret = self.api.compare_classes()

    def properties_shared_by_drugs(self, drug_name_1, drug_name_2):
        pass

    def subtypes(self, class_name):
        ret = self.get_class_by_name(class_name)
        if 'classId' not in ret:
            return "{} not found in database".format(class_name)
        class_id = ret['classId']
        pdb.set_trace()
        ret = self.api.get_class_tree(class_id)
        title = "Subtypes of {}".format(class_name)
        if 'rxClassTree' not in ret:
            return title, None
        subtypes = [sub['minConcept'] for sub in ret['rxClassTree']['rxClass']]
        return title, subtypes

    def class_name_suggestions(self, class_name, only_drugs=False, class_type='CLASS'):
        if only_drugs:
            class_type = 'DRUGS'
        ret = self.api.get_spelling_suggestions(class_name, class_type)
        if 'suggestionList' not in ret:
            return "Items similarly named to {} were not found.".format(class_name)
        return ret['suggestionList']['suggestion']


    def understand_class_types(self):
        return reduce(lambda acc, ct: acc + ["{} = {}".format(ct[0], ct[1])], self.drug_class_types.items(), [])

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

    def save(self):
        with open("{}.p".format(self.filename), 'wb') as f:
            picklerick.dump(self.memo, f)

    def wipe(self):
        open("{}.p".format(self.filename), 'wb').close()

    def load(self):
        if not os.path.exists("{}.p".format(self.filename)):
            with open("{}.p".format(self.filename), 'wb') as f:
                picklerick.dump({}, f)
        with open("{}.p".format(self.filename), 'rb') as f:
            try:
                data = picklerick.load(f)
            except EOFError:
                data = {}
        return data

    def __enter__(self):
        self.memo = self.load()
        return self

    def __exit__(self, type, value, traceback):
        if self.save_memo:
            self.save()

helper = RxClassHelpers()
with helper:
    #pp(bot.drug_info('fluoxetine'))
    #pp(bot.get_class_data_of_drug('fluoxetine'))
    #pp(bot.get_similarly_acting_drugs('fluoxetine'))
    #pp(bot.api.find_class_by_name('long qt syndrome'))
    #pp(bot.contraindications('with', 'seizure disorder'))
    #pp(bot.contraindications('with', 'hypoglycemia'))
    #pp(bot.drug_induces('vomiting'))
    #pp(bot.drugs_that_may('treat', 'pain'))
    #pp(bot.drugs_with_physiological_effect('Increased Serotonin Activity'))
    #pp(bot.drugs_with_similar_pharmacokinetics('fluoxetine'))

    #pp(bot.drugs_sharing_properties(''))
    #pp(bot.subtypes('Cytochrome P450 Inducers'))
    pp(helper.class_name_suggestions('oxetine', only_drugs=True))