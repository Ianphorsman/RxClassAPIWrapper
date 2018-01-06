import requests
import json
import csv
import xml
from pprint import pprint as pp
import _pickle as picklerick

class RxDrugAPIWrapper(object):

    def __init__(self):
        self.base_uri_interactions = 'https://rxnav.nlm.nih.gov/REST/interaction'
        self.base_uri_class = 'https://rxnav.nlm.nih.gov/REST/rxclass'
        self.drug_class_soaps = []


    def get_interaction_uri(self):
        return self.base_uri_class + '/interaction.json?rxcui=' + str(341248)

    def find_class_by_rxcui(self, rxcui):
        return self.base_uri_class +

    def test(self):
        self.req = requests.get(self.get_interaction_uri())
        self.save()

    def scrape(self, drug_name):
        pass

    def sanitize(self):
        pass

    def return_json(self):
        pass

    def return_csv(self):
        pass

    def save(self):
        pp(json.dumps(self.req.json(), "/req_{}.json".format(self.rxcui)))


scraper = Scraper()
scraper.test()