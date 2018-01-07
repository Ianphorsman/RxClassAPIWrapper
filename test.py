from RxAPIWrapper import RxAPIWrapper
from RxClassHelpers import DrugHelpers
from pprint import pprint as pp


class APITester(object):

    def __init__(self):
        self.api = RxAPIWrapper()

    def test_api_calls(self):
        pass

    def test_drug_helpers(self):
        with DrugHelpers() as helper:
            helper.drug_info('fluoxetine')

