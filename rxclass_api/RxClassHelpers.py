import _pickle as picklerick
import os
from collections import Counter
from functools import reduce

from .RxAPIWrapper import RxAPIWrapper


class RxClassHelpers(object):

    def __init__(self, save_memo=True, filename="rxclass_data"):
        self.save_memo = save_memo
        self.memo = {}
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
            'DISEASE': 'Indication / Condition / Disease'
        }

    def memo(func):
        def wrapper(self, drug_name):
            if drug_name not in self.memo:
                self.get_class_data_of_drug(drug_name)
            return func(self, drug_name)
        return wrapper


    def get_class_data_of_drug(self, drug_name):
        ret = self.api.find_class_by_drug_name(drug_name)
        if 'rxclassDrugInfoList' not in ret:
            error = "{} not found in database".format(drug_name)
            self.memo[drug_name] = [error]
            return error
        classes = {
            (source['rxclassMinConceptItem']['className'],
             source['rxclassMinConceptItem']['classType'],
             source['rxclassMinConceptItem']['classId'])
            for source in ret['rxclassDrugInfoList']['rxclassDrugInfo']
        }
        arranged_classes = {}
        for tup in classes:
            if tup[1] not in arranged_classes:
                arranged_classes[tup[1]] = [(tup[2], tup[0])]
            else:
                arranged_classes[tup[1]].append((tup[2], tup[0]))
        self.memo[drug_name] = arranged_classes
        return arranged_classes


    @memo
    def similarly_acting_drugs(self, drug_name):
        if 'MOA' not in self.memo[drug_name]:
            return "{} has no recorded mechanism of action.".format(drug_name)
        pairs = self.memo[drug_name]['MOA']
        moa_data = []
        def get_similar(id, name):
            opts = {
                'relaSource': 'DAILYMED',
                'rela': "has_{}".format('MOA')
            }
            ret = self.api.get_class_members(id, opts)
            if 'drugMemberGroup' not in ret:
                return name, None
            return name, [member['minConcept']['name'] for member in ret['drugMemberGroup']['drugMember']]
        for moa_id, moa_name in pairs:
            moa_data.append(get_similar(moa_id, moa_name))
        return moa_data

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

    @memo
    def drugs_with_similar_physiological_response(self, drug_name):
        if not 'PE' in self.memo[drug_name]:
            return "{} does not have a recorded physiological response or was not found in database.".format(drug_name)
        pairs = self.memo[drug_name]['PE']
        pe_data = []
        def get_similar(id, name):
            opts = {
                'relaSource': 'DAILYMED',
                'rela': 'has_PE'
            }
            ret = self.api.get_class_members(id, opts)
            if 'drugMemberGroup' not in ret:
                return name, None
            return name, [member['minConcept']['name'] for member in ret['drugMemberGroup']['drugMember']]
        for pe_id, pe_name in pairs:
            pe_data.append(get_similar(pe_id, pe_name))
        return pe_data

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
        if 'drugMemberGroup' not in ret:
            return effect, None
        drug_names = [member['minConcept']['name'] for member in ret['drugMemberGroup']['drugMember']]
        return effect, drug_names

    @memo
    def drugs_with_similar_pharmacokinetics(self, drug_name):
        pairs = self.memo[drug_name]['PK']
        pe_data = []
        def get_similar(id, name):
            opts = {
                'relaSource': 'NDFRT',
                'rela': 'has_PK'
            }
            ret = self.api.get_class_members(id, opts)
            if 'drugMemberGroup' not in ret:
                return name, None
            drug_names = [member['minConcept']['name'] for member in ret['drugMemberGroup']['drugMember']]
            return name, drug_names
        for pk_id, pk_name in pairs:
            pe_data.append(get_similar(pk_id, pk_name))
        return pe_data


    def drugs_with_pharmacokinetics(self, pe_name):
        ret = self.get_class_by_name(pe_name)
        if 'classId' not in ret:
            return "{} not found in database.".format(pe_name)
        pk_id = ret['classId']
        opts = {
            'relaSource': 'NDFRT',
            'rela': 'has_PK'
        }
        ret = self.api.get_class_members(pk_id, opts)
        if 'drugMemberGroup' not in ret:
            return pe_name, None
        drug_names = [member['minConcept']['name'] for member in ret['drugMemberGroup']['drugMember']]
        return pe_name, drug_names


    def get_class_by_name(self, class_name):
        ret = self.api.find_class_by_name(class_name)
        if 'rxclassMinConceptList' not in ret:
            return ret
        return ret['rxclassMinConceptList']['rxclassMinConcept'][0]

    def get_class_by_id(self, class_id):
        ret = self.api.find_class_by_id(class_id)
        if 'rxclassMinConceptList' not in ret:
            return ret
        return ret['rxclassMinConceptList']['rxclassMinConcept'][0]

    def similar_classes(self, class_name, limit=10):
        ret = self.get_class_by_name(class_name)
        if 'classId' not in ret:
            return "{} not found in database.".format(class_name)
        opts = {
            'relaSource': 'ATC',
            #'rela': 'MOA',
            'scoreType': 2,
            'top': limit,
            'equivalenceThreshold': 0.3,
            'inclusionThreshold': 0.3
        }
        ret = self.api.find_similar_classes_by_class(ret['classId'], opts)



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


    def subtypes(self, class_name):
        ret = self.get_class_by_name(class_name)
        if 'classId' not in ret:
            return "{} not found in database".format(class_name)
        class_id = ret['classId']
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


    def list_class_types(self):
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
print(helper.indications('bupropion'))