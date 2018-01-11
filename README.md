<h1>RxClass API Wrapper with Helper Utility</h1>

<h2>Getting Started</h2>
<p>
    This project contains a python wrapper for the RxClass API as well as a set of helper functions to
    obtain useful information stripped of unimportant data.
</p>
<h3>Helper Functions</h3>
<p>
    `RxClassHelpers` contains several high level helper functions to acquaint yourself with
    what the RxClass API can (and can't) do. Just create an instance to get started.
    <strong>Warning:</strong> there are a lot of false negative results.
</p>

```python

helper = RxClassHelpers()

```

<p>Supplying a <strong>with</strong> statement will also automatically load and save gathered data given a filename.</p>

```python

helper = RxClassHelpers(filename='data')
with helper:
    ...

```

<h4>Obtaining Class's Id and Type</h4>
<p>Unique identifiers are represented as <strong>classId</strong>(s). Every class in RxClass has a <strong>classId</strong> and <strong>classType</strong>.</p>

```python

helper.get_class_by_name('fluoxetine')

#=>
{'classId': 'N0000007101',
  'className': 'Fluoxetine',
  'classType': 'CHEM'}

helper.get_class_by_name('SSRI')

#=>
{'classId': 'N0000175696',
 'className': 'Serotonin Reuptake Inhibitor',
 'classType': 'EPC'}

 helper.get_class_by_name('Drug Hypersensitivity')

#=>
{'classId': 'N0000000999',
 'className': 'Drug Hypersensitivity',
 'classType': 'DISEASE'}

```

<h4>Class Types</h4>
<p>List all the class types with descriptions.</p>

```python

helper.list_class_types()

#=>
['MESHPA = MeSH Pharmacological Actions',
 'VA = Class',
 'PK = Pharmacokinetics',
 'EPC = Established Pharmacological Classes',
 'DISEASE = Indication / Condition / Disease',
 'ATC1-4 = Anatomical Therapeutic Chemical',
 'CHEM = Chemical Name',
 'MOA = Mechanism of Action',
 'PE = Physiological Effect']

```

<h4>Drug Indications</h4>

```python

helper.indications('bupropion')

#=>
['Anorexia',
 'Attention Deficit Disorder with Hyperactivity',
 'Bulimia',
 'Depressive Disorder',
 'Drug Hypersensitivity',
 'Seizures',
 'Substance Withdrawal Syndrome',
 'Tobacco Use Disorder']

 helper.indications('azithromycin')

 #=>
 ['Chlamydia Infections',
 'Endocarditis, Bacterial',
 'Haemophilus Infections',
 'Hypersensitivity',
 'Liver Diseases',
 'Mycobacterium Infections, Nontuberculous',
 'Neisseriaceae Infections',
 'Otitis Media',
 'Pharyngitis',
 'Pneumonia, Bacterial',
 'Pneumonia, Mycoplasma',
 'Respiratory Tract Infections',
 'Sexually Transmitted Diseases, Bacterial',
 'Skin Diseases, Infectious',
 'Staphylococcal Infections',
 'Streptococcal Infections',
 'Tonsillitis',
 'Urethritis']


```

<h4>Drug's Mechanism of Action</h4>

```python

helper.mechanism_of_action('marijuana') # 'marijuana' will not be in database

#=>
[]

helper.mechanism_of_action('tetrahydrocannabinol') # chemical name will be found though

#=>
['Cannabinoid Receptor Agonists']

helper.similarly_acting_drugs('fluoxetine')

#=>
[('Serotonin Uptake Inhibitors',
  ['Citalopram',
   'Desvenlafaxine',
   'duloxetine',
   'Escitalopram',
   'Fluoxetine',
   'Fluvoxamine',
   'levomilnacipran',
   'milnacipran',
   'Paroxetine',
   'Sertraline',
   'venlafaxine']),
 ('Monoamine Oxidase Inhibitors',
  ['Isocarboxazid',
   'Phenelzine',
   'rasagiline',
   'safinamide',
   'Selegiline',
   'Tranylcypromine'])]

```

<h4>Drug's Physiological Effect</h4>

```python

helper.physiological_effect('aripiprazole')

#=>
['Decreased Dopamine Activity', 'Decreased Serotonin Activity']

helper.drugs_with_similar_physiological_response('ibuprofen')

#=>
[('Decreased Platelet Activating Factor Production', None),
 ('Decreased Prostaglandin Production', ['Aspirin', 'Diclofenac']),
 ('Decreased Thromboxane Production', None)]

helper.drugs_with_similar_physiological_response('aripiprazole') # will yield a false negative

#=>
[('Decreased Dopamine Activity', None),
 ('Decreased Serotonin Activity', None)]

helper.drugs_with_physiological_effect('Decreased Dopamine Activity') # but this works

#=>
('Decreased Dopamine Activity',
 ['acetophenazine',
  'aripiprazole',
  'Chlorpromazine',
  'Chlorprothixene',
  'Clozapine',
  'deutetrabenazine',
  'Fluphenazine',
  'Haloperidol',
  'Mesoridazine',
  ...])

```

<h4>Drug's Pharmacokinetics</h4>

```python

helper.pharmacokinetics('ibuprofen')

#=>
['Hepatic Metabolism', 'Renal Excretion']

helper.drugs_with_similar_pharmacokinetics('ibuprofen')

#=>
[('Drugs processed via Renal Excretion',
  ['Acetaminophen',
   'Albuterol',
   'Alprazolam',
   'Amoxicillin',
   'Aspirin',
   'Atenolol',
   ...]),
 ('Drugs processed via Hepatic Metabolism',
  ['Acetaminophen',
   'Albuterol',
   'Aspirin',
   'atorvastatin',
   ...])]

helper.drugs_with_pharmacokinetics('Hepatic Metabolism')

#=>
('Hepatic Metabolism',
 ['Acetaminophen',
  'Albuterol',
  'Aspirin',
  'atorvastatin',
  'celecoxib',
  'Codeine',
  ...])

```

<h4>Therapeutic Class</h4>

```python

helper.therapeutic_class('azithromycin')

#=>
['Antibiotics', 'Macrolides']

helper.therapeutic_class('budesonide')

#=>
['Adrenergics in combination with corticosteroids or other drugs, excl. '
 'anticholinergics',
 'Corticosteroids',
 'Corticosteroids acting locally',
 'Corticosteroids, potent (group III)',
 'Glucocorticoids']

```

<h4>Drug Type</h4>

```python

helper.drug_type('azithromycin')

#=>
['ANTIBACTERIALS,TOPICAL OPHTHALMIC', 'ERYTHROMYCINS/MACROLIDES']

helper.drug_type('budesonide')

#=>
['ANTI-INFLAMMATORIES,INHALATION',
 'ANTI-INFLAMMATORIES,NASAL',
 'ANTIASTHMA,OTHER',
 'GLUCOCORTICOIDS']

```

<h4>Class information of a given drug.</h4>

```python

helper.drug_info('ketamine')

#=>
{'Drug Type': ['GENERAL ANESTHETICS,OTHER'],
 'Indications': ['Aneurysm',
                 'Angina Pectoris',
                 'Burns',
                 'Drug Hypersensitivity',
                 'Heart Failure',
                 'Hypertension',
                 'Intracranial Hypertension',
                 'Pain',
                 'Psychotic Disorders',
                 'Thyrotoxicosis',
                 'Unconsciousness'],
 'Mechanism of Action': [],
 'Name': 'Ketamine Hydrochloride',
 'Pharmacokinetics': None,
 'Physiological Effects': ['Blood Pressure Alteration',
                           'Decreased Cerebral Cortex Organized Electrical '
                           'Activity',
                           'Decreased Midbrain Organized Electrical Activity',
                           'Decreased Sensory-Somatic Nervous System '
                           'Organized Electrical Activity',
                           'General Anesthesia',
                           'Increased Epinephrine Activity',
                           'Increased Norepinephrine Activity'],
 'Therapeutic Class': ['Other general anesthetics']}

```

<h4>Drugs that can induce a reaction or condition.</h4>

```python

helper.drug_induces(vomiting')

#=>
('Drugs that induce vomiting',
 ['Disulfiram', 'ethyl ether', 'Ipecac', 'Nitrous Oxide'])

helper.drug_induces(seizure disorder')

#=>
('Drugs that induce seizure disorder', ['Pentylenetetrazole'])

```

<h4>Drugs that may prevent a condition or acute reaction.</h4>

```python

helper.drugs_that_may('prevent', 'seizure disorder')

#=>
('Drugs that may prevent seizure disorder',
 ['fosphenytoin', 'Magnesium Sulfate', 'Phenytoin', 'Thiamylal'])

helper.drugs_that_may('prevent', 'dementia')

#=>
('Drugs that may prevent alzheimer disease', ['Vitamin E'])

```

<h4>Drugs that <strong>may</strong> treat a condition or acute response.</h4>

```python

helper.drugs_that_may('treat', 'seizures')

#=>
('Drugs that may treat seizure disorder',
 ['Acetazolamide',
  'Amobarbital',
  'Brivaracetam',
  'Carbamazepine',
  'clobazam',
  'Clonazepam',
  'clorazepate',
  'Corticotropin',
  'Diazepam',
  'Ethosuximide',
  'Ethotoin',
  'Etomidate',
  'ezogabine',
  'felbamate',
  'fosphenytoin',
  'gabapentin',
  ...])

helper.drugs_that_may('treat', 'depressive disorder')

#=>
('Drugs that may treat depressive disorder',
 ['Alprazolam',
  'Amitriptyline',
  'Amoxapine',
  'brexpiprazole',
  'Bupropion',
  'Buspirone',
  'Citalopram',
  'Clomipramine',
  'Desipramine',
  'Desvenlafaxine',
  'Doxepin',
  'duloxetine',
  'Escitalopram',
  'Fluoxetine',
  'Fluvoxamine',
  'Imipramine',
  'Isocarboxazid',
  'Isoflurane',
  'Kava preparation',
  'levomilnacipran',
  'Lithium',
  'Lorazepam',
  'lurasidone',
  'Maprotiline',
  'Melatonin',
  'Methylphenidate',
  'milnacipran',
  ...])

```

<h4>Drugs that can diagnose a condition.</h4>

```python

helper.drugs_that_may('diagnose', '<condition>')

#=> # yet to find a condition name that yields results from NDFRT database

```

<h4>Contraindications</h4>
<p>Not as straightforward. Supply 'with' instead of 'DISEASE'.</p>

```python

helper.contraindications('with', 'Drug Hypersensitivity')

#=>
('Drug Hypersensitivity contraindications',
 ['17-alpha-Hydroxyprogesterone',
  '4-Aminobenzoic Acid',
  'abacavir',
  'abciximab',
  'Acarbose',
  'Acebutolol',
  'acemannan',
  'Acetaminophen',
  'Acetazolamide',
  'Acetic Acid',
  ...])

helper.contraindications('with', 'bulimia')

#=>
('bulimia contraindications', ['Bupropion'])

helper.contraindications('with', 'schizophrenia')

#=>
('schizophrenia contraindications',
 ['Fenfluramine', 'Ginseng Preparation', 'Tetrahydrocannabinol'])

```

<h4>Class Subtypes</h4>
<p>Use of this function appears to be limited currently.</p>

```python

helper.subtypes('')

#=> # Let me know if you find a valid use case that works.

```

<h4>Spelling Suggestions</h4>

```python

helper.class_name_suggestions('amines')

#=>
['amines',
 'amides',
 'diamines',
 'azides',
 'amidines',
 'acids',
 'ascites',
 'apnea',
 'anions',
 'amnesia']

helper.class_name_suggestions('oxetine', only_drugs=True) # returns only drug names

#=>
['fluoxetine',
 'paroxetine',
 'reboxetine',
 'duloxetine',
 'oxypertine',
 'oxerutins',
 'oxetorone']

```


<h4><emp>Statement of Credit</emp></h4>

This product uses publicly available data from the U.S. National Library of Medicine (NLM), National Institutes of Health, Department of Health and Human Services; NLM is not responsible for the product and does not endorse or recommend this or any other product."
