<h1>RxClass API Wrapper with Helper Utility</h1>

<h2>Getting Started</h2>
<p>
    This project contains a python wrapper for the RxClass API as well as a set of helper functions to
    obtain useful information stripped of unimportant data.
</p>
<h3>Helper Functions</h3>
<p>
    The DrugHelper class contains several high level helper functions to help acquaint yourself with
    what the RxClass API can do. Just create an instance to get started.
</p>

```python

helper = RxClassHelpers()

```

<p>Supplying a with statement will also automatically load and save gathered data given a `filename`.</p>

```python

helper = RxClassHelpers(filename='data')
with helper:
    `...`

```
<h3>API Wrapper Functions</h3>


*Statement of Credit*
This product uses publicly available data from the U.S. National Library of Medicine (NLM), National Institutes of Health, Department of Health and Human Services; NLM is not responsible for the product and does not endorse or recommend this or any other product."
