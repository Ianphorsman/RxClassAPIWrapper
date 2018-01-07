<h1>RxClass API Wrapper with Helper Utility</h1>

<h2>Getting Started</h2>
<p>
    This project contains a python wrapper for the RxClass API as well as a set of helper functions to
    obtain useful information stripped of unimportant data.
</p>
<h3>Helper Functions</h3>
<p>
    `RxClassHelpers` contains several high level helper functions to help acquaint yourself with
    what the RxClass API can do. Just create an instance to get started.
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

```

<h4>Class Types</h4>
<p>List all the class types with descriptions.</p>

```python

helper.list_class_types()

#=>

```

<h4>Drug Indications</h4>

```python

helper.indications('bupropion')

#=>

helper.drugs_indicated_for('fibromyalgia')

```

<h4>Drug's Mechanism of Action</h4>

```python

helper.mechanism_of_action('fluoxetine')

#=>

helper.similarly_acting_drugs('methylphenidate')

#=>

```

<h4>Drug's Physiological Effect</h4>

```python

helper.physiological_effect('aripiprazole')

#=>

helper.drugs_with_similar_physiological_response('aripiprazole')

#=>

helper.drugs_with_physiological_effect('Increased Dopamine Activity')

#=>

```

<h4>Drug's Pharmacokinetics</h4>

```python

helper.pharmacokinetics('fluoxetine')

#=>

helper.drugs_with_similar_pharmacokinetics('fluoxetine')

#=>

helper.drugs_with_pharmacokinetics('Hepatic Metabolism')

#=>

```

<h4>Therapeutic Class</h4>

```python

helper.therapeutic_class('azithromycin')

#=>

helper.therapeutic_class('venlafaxine')

#=>

```

<h4>Drug Type</h4>

```python

helper.drug_type('azithromycin')

#=>

helper.drug_type('venlafaxine')

#=>

```

<h4>Class information of a given drug.</h4>

```python

helper.drug_info('ketamine')

#=>

```

<h4>Drugs that can induce a reaction or condition.</h4>

```python

helper.drug_induces(vomiting')

#=>

helper.drug_induces(seizures')

#=>

```

<h4>Drugs that may prevent a condition or acute reaction.</h4>

```python

helper.drugs_that_may('prevent', 'seizures')

#=>

helper.drugs_that_may('prevent', '')

#=>

```

<h4>Drugs that <strong>may</strong> treat a condition or acute response.</h4>

```python

helper.drugs_that_may('treat', 'seizures')

#=>

helper.drugs_that_may('treat', 'major depression')

#=>

```

<h4>Drugs that can diagnose a condition.</h4>

```python

helper.drugs_that_may('diagnose', '')

#=>

helper.drugs_that_may('diagnose', '')

#=>

```

<h4>Contraindications</h4>
<p>Not as straightforward. Supply 'with' instead of 'DISEASE'.</p>

```python

helper.contraindications('with', 'bulimia')

#=>

helper.contraindications('', '')

#=>

helper.contraindications('', '')

#=>

helper.contraindications('', '')

#=>

```

<h4>Class Subtypes</h4>
<p>Use of this function appears to be limited currently.</p>
```python

helper.subtypes('')

#=>

```

<h4>Spelling Suggestions</h4>

```python

helper.class_name_suggestions('')

#=>

helper.class_name_suggestions('oxetine', only_drugs=True) # returns only drug names

#=>

```

<h4></h4>

<h3>API Wrapper Functions</h3>


###*Statement of Credit*

This product uses publicly available data from the U.S. National Library of Medicine (NLM), National Institutes of Health, Department of Health and Human Services; NLM is not responsible for the product and does not endorse or recommend this or any other product."
