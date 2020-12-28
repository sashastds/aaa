## Pizza CLI
### Avito Analytics Academy's python course final project

#### usage is pretty much explained in pdf-file and also in corresponding help-strings
just go for a test drive ;)

some examples:

```python pizza.py menu```

```python pizza.py order --help```

```python pizza.py order speciale*3 --delivery```

```python pizza.py order speciale -s XL pepperoni -s L```

```python pizza.py order speciale pepperoni margherita --size XL --delivery```


#### you can run tests like this:
pytest --cov --cov-branch -v test_pizza.py > test.results --cov-report html
