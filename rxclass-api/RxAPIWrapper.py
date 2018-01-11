import requests
import json
from pprint import pprint as pp
from functools import reduce

class RxAPIWrapper(object):

    def __init__(self):
        self.base_uri_interactions = 'https://rxnav.nlm.nih.gov/REST/interaction'
        self.base_uri_class = 'https://rxnav.nlm.nih.gov/REST/rxclass'
        self.base_uri_norm = 'https://rxnav.nlm.nih.gov/REST'
        self.drug_class_soaps = []

    def make_request(api_url_getter):
        def wrapper(self, *args):
            return requests.get(api_url_getter(self, *args)).json()
        return wrapper

    def sanitize(self, opts):
        if type(opts) is dict:
            return reduce(lambda acc, i: acc + "&{}={}".format(i[0], i[1]), opts.items(), "")
        return ''

    @make_request
    def get_interaction_uri(self):
        return self.base_uri_class + '/interaction.json?rxcui=' + str(341248)

    @make_request
    def find_class_by_id(self, drug_class_id):
        return self.base_uri_class + "/class/byId.json?classId={}".format(drug_class_id)

    @make_request
    def find_class_by_name(self, name):
        return self.base_uri_class + "/class/byName.json?className={}".format(name)

    @make_request
    def find_class_by_drug_name(self, drug_name, opts=None):
        return self.base_uri_class + "/class/byDrugName.json?drugName={}".format(drug_name) + self.sanitize(opts)

    @make_request
    def find_similar_classes_by_class(self, class_id, opts=None):
        return self.base_uri_class + "/class/similar.json?classId={}".format(class_id) + self.sanitize(opts)

    @make_request
    def find_similar_classes_by_drug_list(self, drug_ids, opts=None):
        return self.base_uri_class + "/class/similarByRxcuis?rxcuis={}".format(drug_ids) + self.sanitize(opts)

    @make_request
    def get_all_classes(self, class_types=None):
        return self.base_uri_class + "/allClasses.json" + self.sanitize(class_types)

    @make_request
    def get_class_contexts(self, class_id):
        return self.base_uri_class + "/classContext.json?classId={}".format(class_id)

    @make_request
    def get_class_graph(self, class_id):
        return self.base_uri_class + "/classGraph.json?classId={}".format(class_id)

    @make_request
    def get_class_members(self, class_id, opts=None):
        return self.base_uri_class + "/classMembers.json?classId={}".format(class_id) + self.sanitize(opts)

    @make_request
    def get_class_tree(self, class_id):
        return self.base_uri_class + "/classTree.json?classId={}".format(class_id)

    @make_request
    def get_class_types(self):
        return self.base_uri_class + "/classTypes.json"

    @make_request
    def get_relationships(self, rela_source):
        return self.base_uri_class + "/relas.json?relaSource={}".format(rela_source)

    @make_request
    def compare_classes(self, class_id_1, opts=None):
        return self.base_uri_class + "/similarInfo.json?" + self.sanitize(opts)[1:]

    @make_request
    def get_sources_of_drug_class_relations(self):
        return self.base_uri_class + "/relaSources.json"

    @make_request
    def get_spelling_suggestions(self, term, type_of_name):
        return self.base_uri_class + "/spellingsuggestions.json?term={}&type={}".format(term, type_of_name)

    def save(self):
        pp(json.dumps(self.req.json(), "/req_1.json"))

